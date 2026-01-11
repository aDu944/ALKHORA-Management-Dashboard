# Management Dashboard (ERPNext / Frappe App)

Annual management dashboard for users with the **Management** role.

## What this adds

- A Desk Page: **Management Dashboard**
- An API endpoint to fetch annual KPIs (sales, purchases, profit proxy, AR/AP, cash/bank balances, top customers/items)
- Role gating so only users with role **Management** can access

## Install (bench)

```bash
bench get-app /path/to/this/repo/management_dashboard
bench --site <site-name> install-app management_dashboard
```

## Use

- Open Desk → search for **Management Dashboard** (or open `/app/management_dashboard`)

## Notes

- This is a scaffold meant to be tailored to your KPI definitions, fiscal year rules, and chart preferences.

