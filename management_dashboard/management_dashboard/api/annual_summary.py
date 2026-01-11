from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

import frappe


@dataclass(frozen=True)
class Period:
	start_date: date
	end_date: date
	label: str


def _require_management_role():
	if frappe.session.user == "Guest":
		frappe.throw("Login required", frappe.PermissionError)
	if not frappe.has_role("Management"):
		frappe.throw("You are not permitted to access this dashboard.", frappe.PermissionError)


def _get_default_company() -> Optional[str]:
	try:
		return frappe.defaults.get_user_default("Company") or frappe.db.get_value("Company", {}, "name")
	except Exception:
		return None


def _get_period(year: Optional[int] = None, fiscal_year: Optional[str] = None) -> Period:
	# Prefer ERPNext Fiscal Year if provided.
	if fiscal_year:
		try:
			row = frappe.db.get_value(
				"Fiscal Year",
				fiscal_year,
				["year_start_date", "year_end_date"],
				as_dict=True,
			)
			if row and row.year_start_date and row.year_end_date:
				return Period(
					start_date=row.year_start_date,
					end_date=row.year_end_date,
					label=str(fiscal_year),
				)
		except Exception:
			# If ERPNext isn't installed, fall back to calendar year below.
			pass

	today = date.today()
	y = int(year) if year else today.year
	return Period(start_date=date(y, 1, 1), end_date=date(y, 12, 31), label=str(y))


def _sum_doctype_field(
	doctype: str,
	field: str,
	filters: Dict[str, Any],
) -> float:
	# Use SQL aggregate for speed and to avoid loading docs.
	condition_sql = []
	values: Dict[str, Any] = {}
	for k, v in filters.items():
		if isinstance(v, (list, tuple)) and len(v) == 2:
			op, val = v
			condition_sql.append(f"`{k}` {op} %({k})s")
			values[k] = val
		else:
			condition_sql.append(f"`{k}` = %({k})s")
			values[k] = v

	where = " AND ".join(condition_sql) if condition_sql else "1=1"
	res = frappe.db.sql(
		f"""
		SELECT COALESCE(SUM(`{field}`), 0)
		FROM `tab{doctype}`
		WHERE {where}
		""",
		values=values,
	)
	return float(res[0][0] or 0)


def _monthly_sums(
	doctype: str,
	value_field: str,
	date_field: str,
	base_filters: Dict[str, Any],
) -> List[Dict[str, Any]]:
	condition_sql = []
	values: Dict[str, Any] = {}
	for k, v in base_filters.items():
		if isinstance(v, (list, tuple)) and len(v) == 2:
			op, val = v
			condition_sql.append(f"`{k}` {op} %({k})s")
			values[k] = val
		else:
			condition_sql.append(f"`{k}` = %({k})s")
			values[k] = v

	where = " AND ".join(condition_sql) if condition_sql else "1=1"
	rows = frappe.db.sql(
		f"""
		SELECT
			DATE_FORMAT(`{date_field}`, '%%Y-%%m-01') AS month,
			COALESCE(SUM(`{value_field}`), 0) AS total
		FROM `tab{doctype}`
		WHERE {where}
		GROUP BY DATE_FORMAT(`{date_field}`, '%%Y-%%m')
		ORDER BY month ASC
		""",
		values=values,
		as_dict=True,
	)
	return [{"month": r["month"], "total": float(r["total"] or 0)} for r in rows]


def _pnl_from_gl(company: str, start_date: date, end_date: date) -> Dict[str, float]:
	# Net income = Income - Expense (based on account root_type).
	# This is a lightweight proxy; for exact figures, you may want to reuse ERPNext reports.
	income = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(gle.credit - gle.debit), 0) AS total
		FROM `tabGL Entry` gle
		INNER JOIN `tabAccount` acc ON acc.name = gle.account
		WHERE gle.is_cancelled = 0
			AND gle.company = %(company)s
			AND gle.posting_date BETWEEN %(start_date)s AND %(end_date)s
			AND acc.root_type = 'Income'
		""",
		{"company": company, "start_date": start_date, "end_date": end_date},
		as_dict=True,
	)
	expense = frappe.db.sql(
		"""
		SELECT COALESCE(SUM(gle.debit - gle.credit), 0) AS total
		FROM `tabGL Entry` gle
		INNER JOIN `tabAccount` acc ON acc.name = gle.account
		WHERE gle.is_cancelled = 0
			AND gle.company = %(company)s
			AND gle.posting_date BETWEEN %(start_date)s AND %(end_date)s
			AND acc.root_type = 'Expense'
		""",
		{"company": company, "start_date": start_date, "end_date": end_date},
		as_dict=True,
	)
	income_total = float((income or [{}])[0].get("total") or 0)
	expense_total = float((expense or [{}])[0].get("total") or 0)
	return {
		"income": income_total,
		"expense": expense_total,
		"net_profit": income_total - expense_total,
	}


def _cash_bank_balances(company: str, end_date: date) -> List[Dict[str, Any]]:
	accounts = frappe.get_all(
		"Account",
		filters={
			"company": company,
			"is_group": 0,
			"account_type": ["in", ["Cash", "Bank"]],
			"disabled": 0,
		},
		fields=["name", "account_name", "account_type"],
		order_by="account_name asc",
	)
	if not accounts:
		return []

	names = [a["name"] for a in accounts]
	placeholders = ", ".join(["%s"] * len(names))
	rows = frappe.db.sql(
		f"""
		SELECT gle.account, COALESCE(SUM(gle.debit - gle.credit), 0) AS balance
		FROM `tabGL Entry` gle
		WHERE gle.is_cancelled = 0
			AND gle.company = %s
			AND gle.posting_date <= %s
			AND gle.account IN ({placeholders})
		GROUP BY gle.account
		""",
		tuple([company, end_date] + names),
		as_dict=True,
	)
	by_account = {r["account"]: float(r["balance"] or 0) for r in rows}
	return [
		{
			"account": a["name"],
			"account_name": a["account_name"],
			"account_type": a["account_type"],
			"balance": float(by_account.get(a["name"], 0)),
		}
		for a in accounts
	]


@frappe.whitelist()
def get_annual_summary(
	year: Optional[int] = None,
	fiscal_year: Optional[str] = None,
	company: Optional[str] = None,
) -> Dict[str, Any]:
	"""
	Return annual KPI summary for the management dashboard.

	- Restricted to role: Management
	- Designed for ERPNext; requires doctypes like Sales Invoice, Purchase Invoice, GL Entry, Account
	"""
	_require_management_role()

	company = company or _get_default_company()
	if not company:
		frappe.throw("No Company found/configured.")

	period = _get_period(year=year, fiscal_year=fiscal_year)

	common_date_filters = {"posting_date": ["between", [period.start_date, period.end_date]]}

	# Sales / Purchases (in company currency base fields)
	sales_total = _sum_doctype_field(
		"Sales Invoice",
		"base_grand_total",
		{
			"docstatus": 1,
			"company": company,
			**common_date_filters,
		},
	)
	purchases_total = _sum_doctype_field(
		"Purchase Invoice",
		"base_grand_total",
		{
			"docstatus": 1,
			"company": company,
			**common_date_filters,
		},
	)

	# Receivables / Payables from invoice outstanding
	ar_outstanding = _sum_doctype_field(
		"Sales Invoice",
		"outstanding_amount",
		{
			"docstatus": 1,
			"company": company,
			**common_date_filters,
		},
	)
	ap_outstanding = _sum_doctype_field(
		"Purchase Invoice",
		"outstanding_amount",
		{
			"docstatus": 1,
			"company": company,
			**common_date_filters,
		},
	)

	# P&L proxy from GL
	pnl = _pnl_from_gl(company=company, start_date=period.start_date, end_date=period.end_date)

	# Trends
	monthly_sales = _monthly_sums(
		"Sales Invoice",
		"base_grand_total",
		"posting_date",
		{"docstatus": 1, "company": company, **common_date_filters},
	)
	monthly_purchases = _monthly_sums(
		"Purchase Invoice",
		"base_grand_total",
		"posting_date",
		{"docstatus": 1, "company": company, **common_date_filters},
	)

	# Top customers (Sales Invoice)
	top_customers = frappe.db.sql(
		"""
		SELECT si.customer, COALESCE(SUM(si.base_grand_total), 0) AS total
		FROM `tabSales Invoice` si
		WHERE si.docstatus = 1
			AND si.company = %(company)s
			AND si.posting_date BETWEEN %(start_date)s AND %(end_date)s
			AND IFNULL(si.customer, '') != ''
		GROUP BY si.customer
		ORDER BY total DESC
		LIMIT 5
		""",
		{"company": company, "start_date": period.start_date, "end_date": period.end_date},
		as_dict=True,
	)

	# Cash & Bank balances as-of end date
	cash_bank = _cash_bank_balances(company=company, end_date=period.end_date)

	return {
		"company": company,
		"period": {
			"label": period.label,
			"start_date": str(period.start_date),
			"end_date": str(period.end_date),
		},
		"kpis": {
			"sales_total": sales_total,
			"purchases_total": purchases_total,
			"ar_outstanding": ar_outstanding,
			"ap_outstanding": ap_outstanding,
			"income_total": pnl["income"],
			"expense_total": pnl["expense"],
			"net_profit": pnl["net_profit"],
		},
		"trends": {
			"monthly_sales": monthly_sales,
			"monthly_purchases": monthly_purchases,
		},
		"breakdowns": {
			"top_customers": [{"customer": r["customer"], "total": float(r["total"] or 0)} for r in top_customers],
			"cash_bank": cash_bank,
		},
	}

