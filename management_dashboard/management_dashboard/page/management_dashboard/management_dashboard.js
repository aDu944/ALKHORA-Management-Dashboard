/* global frappe */

frappe.pages["management_dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Management Dashboard"),
		single_column: true,
	});

	wrapper.classList.add("management-dashboard");
	page.set_primary_action(__("Refresh"), () => load_data());

	const $root = $(wrapper).find(".layout-main-section");

	// Filters
	const $filters = $(`
		<div class="md-filters">
			<div class="md-filter"></div>
			<div class="md-filter"></div>
			<div class="md-filter md-filter-actions"></div>
		</div>
	`);
	$root.append($filters);

	const year = new Date().getFullYear();
	const year_control = frappe.ui.form.make_control({
		parent: $filters.find(".md-filter").eq(0),
		df: {
			fieldtype: "Int",
			label: __("Year"),
			fieldname: "year",
			reqd: 1,
			default: year,
		},
		render_input: true,
	});
	year_control.set_value(year);

	const company_control = frappe.ui.form.make_control({
		parent: $filters.find(".md-filter").eq(1),
		df: {
			fieldtype: "Link",
			options: "Company",
			label: __("Company"),
			fieldname: "company",
		},
		render_input: true,
	});

	// Content containers
	const $kpis = $(`<div class="md-kpis"></div>`);
	const $charts = $(`
		<div class="md-grid-2">
			<div class="md-card">
				<div class="md-card-title">${__("Monthly Sales vs Purchases")}</div>
				<div class="md-chart" data-chart="monthly"></div>
			</div>
			<div class="md-card">
				<div class="md-card-title">${__("Net Profit (proxy) & Working Capital")}</div>
				<div class="md-kpi-rows" data-panel="secondary"></div>
			</div>
		</div>
	`);
	const $breakdowns = $(`
		<div class="md-grid-2">
			<div class="md-card">
				<div class="md-card-title">${__("Top Customers")}</div>
				<div class="md-list" data-list="customers"></div>
			</div>
			<div class="md-card">
				<div class="md-card-title">${__("Cash & Bank (as of period end)")}</div>
				<div class="md-list" data-list="cash"></div>
			</div>
		</div>
	`);

	$root.append($kpis, $charts, $breakdowns);

	function money(v) {
		try {
			return frappe.format(v || 0, { fieldtype: "Currency" });
		} catch (e) {
			return (v || 0).toLocaleString();
		}
	}

	function set_loading(is_loading) {
		$root.toggleClass("md-loading", !!is_loading);
	}

	function render_kpis(data) {
		const k = (data && data.kpis) || {};
		const period = (data && data.period) || {};
		const title = `${__("Annual Summary")} — ${frappe.utils.escape_html(period.label || "")}`;

		$kpis.empty().append(`
			<div class="md-kpis-header">
				<div class="md-kpis-title">${title}</div>
				<div class="md-kpis-subtitle">
					${__("Period")}: ${frappe.utils.escape_html(period.start_date || "")} → ${frappe.utils.escape_html(
			period.end_date || ""
		)}
				</div>
			</div>
			<div class="md-kpis-grid">
				<div class="md-kpi">
					<div class="md-kpi-label">${__("Sales")}</div>
					<div class="md-kpi-value">${money(k.sales_total)}</div>
				</div>
				<div class="md-kpi">
					<div class="md-kpi-label">${__("Purchases")}</div>
					<div class="md-kpi-value">${money(k.purchases_total)}</div>
				</div>
				<div class="md-kpi">
					<div class="md-kpi-label">${__("Net Profit (proxy)")}</div>
					<div class="md-kpi-value">${money(k.net_profit)}</div>
				</div>
				<div class="md-kpi">
					<div class="md-kpi-label">${__("Receivables (Outstanding)")}</div>
					<div class="md-kpi-value">${money(k.ar_outstanding)}</div>
				</div>
				<div class="md-kpi">
					<div class="md-kpi-label">${__("Payables (Outstanding)")}</div>
					<div class="md-kpi-value">${money(k.ap_outstanding)}</div>
				</div>
			</div>
		`);

		const $secondary = $charts.find('[data-panel="secondary"]').empty();
		$secondary.append(`
			<div class="md-kpi-row">
				<div class="md-kpi-row-label">${__("Income")}</div>
				<div class="md-kpi-row-value">${money(k.income_total)}</div>
			</div>
			<div class="md-kpi-row">
				<div class="md-kpi-row-label">${__("Expense")}</div>
				<div class="md-kpi-row-value">${money(k.expense_total)}</div>
			</div>
			<div class="md-kpi-row">
				<div class="md-kpi-row-label">${__("Working Capital (AR - AP)")}</div>
				<div class="md-kpi-row-value">${money((k.ar_outstanding || 0) - (k.ap_outstanding || 0))}</div>
			</div>
		`);
	}

	function render_monthly_chart(data) {
		const monthly_sales = ((data && data.trends && data.trends.monthly_sales) || []).map((r) => ({
			month: r.month,
			total: r.total || 0,
		}));
		const monthly_purchases = ((data && data.trends && data.trends.monthly_purchases) || []).map((r) => ({
			month: r.month,
			total: r.total || 0,
		}));

		const months = Array.from(
			new Set([].concat(monthly_sales.map((r) => r.month), monthly_purchases.map((r) => r.month)))
		).sort();

		const sales_by_month = Object.fromEntries(monthly_sales.map((r) => [r.month, r.total]));
		const purchases_by_month = Object.fromEntries(monthly_purchases.map((r) => [r.month, r.total]));

		const labels = months.map((m) => frappe.datetime.str_to_user(m));
		const sales_values = months.map((m) => sales_by_month[m] || 0);
		const purchases_values = months.map((m) => purchases_by_month[m] || 0);

		const $target = $charts.find('[data-chart="monthly"]').empty();
		if (!labels.length) {
			$target.html(`<div class="md-empty">${__("No data for the selected period.")}</div>`);
			return;
		}

		if (typeof frappe.Chart !== "function") {
			$target.html(
				`<div class="md-empty">${__(
					"Chart library not available. Data was loaded, but chart rendering is unavailable."
				)}</div>`
			);
			return;
		}

		// eslint-disable-next-line no-new
		new frappe.Chart($target[0], {
			data: {
				labels,
				datasets: [
					{ name: __("Sales"), chartType: "line", values: sales_values },
					{ name: __("Purchases"), chartType: "line", values: purchases_values },
				],
			},
			type: "axis-mixed",
			height: 240,
			colors: ["#4F46E5", "#F59E0B"],
			lineOptions: { hideDots: 0, regionFill: 1 },
			axisOptions: { xIsSeries: 1 },
		});
	}

	function render_breakdowns(data) {
		const customers = (data && data.breakdowns && data.breakdowns.top_customers) || [];
		const cash = (data && data.breakdowns && data.breakdowns.cash_bank) || [];

		const $cust = $breakdowns.find('[data-list="customers"]').empty();
		if (!customers.length) {
			$cust.html(`<div class="md-empty">${__("No customers found for the selected period.")}</div>`);
		} else {
			$cust.append(
				customers
					.map(
						(r) => `
						<div class="md-list-row">
							<div class="md-list-main">
								<a class="md-link" href="/app/customer/${encodeURIComponent(r.customer)}">
									${frappe.utils.escape_html(r.customer)}
								</a>
							</div>
							<div class="md-list-value">${money(r.total)}</div>
						</div>
					`
					)
					.join("")
			);
		}

		const $cash = $breakdowns.find('[data-list="cash"]').empty();
		if (!cash.length) {
			$cash.html(`<div class="md-empty">${__("No Cash/Bank accounts found.")}</div>`);
		} else {
			$cash.append(
				cash
					.map(
						(r) => `
						<div class="md-list-row">
							<div class="md-list-main">
								${frappe.utils.escape_html(r.account_name || r.account)}
								<span class="md-badge">${frappe.utils.escape_html(r.account_type || "")}</span>
							</div>
							<div class="md-list-value">${money(r.balance)}</div>
						</div>
					`
					)
					.join("")
			);
		}
	}

	async function load_data() {
		set_loading(true);
		try {
			const args = {
				year: year_control.get_value(),
				company: company_control.get_value(),
			};
			const r = await frappe.call({
				method: "management_dashboard.management_dashboard.api.annual_summary.get_annual_summary",
				args,
				freeze: true,
				freeze_message: __("Loading annual summary…"),
			});
			const data = r && r.message;
			render_kpis(data);
			render_monthly_chart(data);
			render_breakdowns(data);
		} catch (e) {
			console.error(e);
			frappe.msgprint({
				title: __("Management Dashboard"),
				message: __("Could not load dashboard data. Please contact your system administrator."),
				indicator: "red",
			});
		} finally {
			set_loading(false);
		}
	}

	// Initial load
	load_data();

	// Reload on filter changes
	year_control.$input && year_control.$input.on("change", () => load_data());
	company_control.$input && company_control.$input.on("change", () => load_data());
};

