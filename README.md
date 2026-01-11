# ALKHORA Company App

Custom ERPNext/Frappe application for ALKHORA, providing specialized workspaces, dashboards, and business intelligence tools.

## Overview

This repository contains the ALKHORA company app - a general-purpose Frappe/ERPNext application designed to be extensible with multiple workspaces and features.

**Current Version**: 1.0.0  
**App Title**: ALKHORA  
**Technical App Name**: `management_dashboard` (for Frappe framework compatibility)

## Current Features

### Management Dashboard Workspace
A comprehensive annual management dashboard featuring:
- **Financial KPIs**: Sales (Net/Gross), Sales Orders, Delivery Notes, Purchases, Net Profit
- **Accounts**: AR/AP outstanding with aging buckets, Cash & Bank balances
- **Customer Health**: New customers, top overdue customers
- **Purchasing**: Top suppliers analysis
- **HR Metrics**: Headcount, payroll cost, open positions
- **Analytics**: Monthly/Quarterly/Weekly period analysis
- **Filters**: Multi-select filters for Cost Center, Branch, Project, Customer/Supplier/Item Groups
- **Export**: CSV, Excel, PDF export capabilities
- **Internationalization**: RTL/Arabic support
- **Access Control**: Management and System Manager roles
- **Audit Trail**: Dashboard view logging

## Installation

```bash
# From your bench directory
bench get-app management_dashboard /absolute/path/to/ALKHORA-Management-Dashboard/management_dashboard

# Install on your site
bench --site <your-site-name> install-app management_dashboard

# Migrate
bench --site <your-site-name> migrate

# Restart
bench restart
```

## Access

After installation:
- Go to Desk → search "Management Dashboard"
- Or navigate to `/app/management_dashboard`

## Adding New Workspaces

This app is designed to be extended with new workspaces. See:
- **[WORKSPACE_GUIDE.md](management_dashboard/WORKSPACE_GUIDE.md)** - Detailed guide for adding new workspaces
- **[ALKHORA_APP_STRUCTURE.md](ALKHORA_APP_STRUCTURE.md)** - Architecture and structure documentation

### Quick Example

To add a new workspace (e.g., "Inventory Tracker"):

1. Create directories:
   ```bash
   mkdir -p management_dashboard/page/inventory_tracker
   mkdir -p management_dashboard/api/inventory_tracker
   ```

2. Create pages, APIs, and configuration files
3. Update `modules.txt` and `config/desktop.py`
4. Follow patterns from Management Dashboard workspace

See `WORKSPACE_GUIDE.md` for complete instructions.

## App Structure

```
management_dashboard/              # App root
├── management_dashboard/          # Python package
│   ├── api/                      # API endpoints (organized by workspace)
│   ├── config/                   # Configuration files
│   ├── doctype/                  # Custom doctypes
│   ├── page/                     # Custom pages (organized by workspace)
│   ├── hooks.py                  # App metadata and hooks
│   └── modules.txt               # Module definitions
├── setup.py
├── pyproject.toml
└── README.md
```

## Documentation

- **[App README](management_dashboard/README.md)** - Detailed app documentation
- **[Workspace Guide](management_dashboard/WORKSPACE_GUIDE.md)** - Adding new workspaces
- **[App Structure](ALKHORA_APP_STRUCTURE.md)** - Architecture documentation
- **[Installation Guide](INSTALL.md)** - Installation instructions

## Development

### Requirements
- Frappe Framework (v15+)
- ERPNext (v15+)
- Python 3.10+

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd ALKHORA-Management-Dashboard

# Install in your bench
bench get-app management_dashboard ./management_dashboard

# Install on site
bench --site <site-name> install-app management_dashboard

# Development mode
bench --site <site-name> set-config developer_mode 1
bench restart
```

## Version History

### Version 1.0.0 (Current)
- Initial release as ALKHORA Company App
- Management Dashboard workspace
- Comprehensive KPI analytics
- Multi-currency support
- RTL/Arabic support
- Export capabilities
- Extensible workspace architecture

## License

MIT License - See `management_dashboard/license.txt` for details

## Support

For support, feature requests, or questions:
- Email: support@alkhora.co
- Refer to documentation in this repository

## Contributing

When adding new workspaces or features:
1. Follow the workspace structure guidelines
2. Maintain code consistency
3. Update documentation
4. Test thoroughly
5. Follow Frappe Framework conventions

## Future Roadmap

Potential future workspaces:
- Inventory Management
- Project Management Tools
- Enhanced Reporting
- Customer Portal Features
- HR Analytics
- Custom Business Processes

See `WORKSPACE_GUIDE.md` for instructions on adding these.
