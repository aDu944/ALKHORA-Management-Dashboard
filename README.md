# ALKHORA-Management-Dashboard

This repository contains a Frappe/ERPNext app scaffold under `management_dashboard/`.

## What you get

- A Desk Page (restricted to role **Management**) that shows an annual KPI overview
- A backend API that calculates annual totals and trends from ERPNext doctypes

## Install (bench)

```bash
bench get-app /path/to/this/repo/management_dashboard
bench --site <site-name> install-app management_dashboard
```

## Open

- Desk → search **Management Dashboard**
- Or go to `/app/management_dashboard`
