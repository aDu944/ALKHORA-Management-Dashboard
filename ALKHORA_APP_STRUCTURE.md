# ALKHORA App - Structure and Architecture

## Overview

The ALKHORA app (technical name: `management_dashboard`) is a general-purpose Frappe/ERPNext application designed to be extensible with multiple workspaces and features.

## Current Structure

```
management_dashboard/                    # App root directory
├── management_dashboard/                # Python package
│   ├── api/                            # API endpoints
│   │   └── management_dashboard/       # Management Dashboard APIs
│   │       └── annual_summary.py
│   ├── config/                         # App configuration
│   │   ├── desktop.py                  # Desktop icons configuration
│   │   └── management_dashboard.py     # Management Dashboard module config
│   ├── doctype/                        # Custom doctypes
│   │   ├── dashboard_view_log/         # Audit trail doctype
│   │   └── kpi_definition/             # KPI configuration doctype
│   ├── page/                           # Custom pages
│   │   └── management_dashboard/       # Management Dashboard pages
│   │       ├── management_dashboard.json
│   │       ├── management_dashboard.js
│   │       ├── management_dashboard.css
│   │       └── management_dashboard.py
│   ├── hooks.py                        # App hooks (metadata, configuration)
│   └── modules.txt                     # Module definitions
├── setup.py                            # Package setup
├── pyproject.toml                      # Project configuration
├── MANIFEST.in                         # Package data manifest
├── README.md                           # App documentation
└── WORKSPACE_GUIDE.md                  # Guide for adding workspaces
```

## Workspaces Concept

A "workspace" in this app is a logical grouping of related functionality. Currently:

### 1. Management Dashboard (Current)
- Location: `page/management_dashboard/`, `api/management_dashboard/`
- Purpose: Annual management KPIs and analytics
- Features: Financial metrics, customer health, HR metrics, exports

### Future Workspaces (To be added)
Examples of workspaces you might add:
- **Inventory Tracker**: Real-time inventory monitoring
- **Project Manager**: Custom project management tools
- **Customer Portal**: Enhanced customer-facing features
- **Financial Reports**: Custom financial reporting
- **HR Analytics**: Advanced HR metrics and dashboards

## Adding New Workspaces

See `WORKSPACE_GUIDE.md` for detailed instructions on adding new workspaces.

### Quick Steps:
1. Create directories: `page/workspace_name/`, `api/workspace_name/`
2. Create pages, APIs, doctypes as needed
3. Update `modules.txt` if creating new modules
4. Update `config/desktop.py` for desktop shortcuts
5. Follow the structure patterns used in Management Dashboard

## Code Organization Principles

1. **Modularity**: Each workspace should be self-contained
2. **Consistency**: Follow existing patterns and naming conventions
3. **Scalability**: Structure code to handle growth
4. **Documentation**: Document new workspaces and features

## Naming Conventions

- **Directories/Files**: `snake_case` (e.g., `management_dashboard`, `inventory_tracker`)
- **Labels/Display Names**: `Title Case` (e.g., "Management Dashboard", "Inventory Tracker")
- **Python Modules**: `snake_case`
- **JavaScript Variables**: `camelCase`
- **CSS Classes**: `kebab-case` or prefixed (e.g., `md-kpi-card`)

## API Structure

APIs are organized by workspace:
```
api/
└── workspace_name/
    ├── __init__.py
    └── api_endpoint.py
```

API endpoints should:
- Be whitelisted with `@frappe.whitelist()`
- Include proper error handling
- Follow RESTful naming conventions
- Include docstrings

## Page Structure

Pages are organized by workspace:
```
page/
└── workspace_name/
    ├── workspace_name.json      # Page metadata
    ├── workspace_name.js        # JavaScript logic
    ├── workspace_name.css       # Styles (if needed)
    └── workspace_name.py        # Python context (if needed)
```

## Configuration Files

- **hooks.py**: App metadata, installed apps, fixtures
- **config/desktop.py**: Desktop icon configuration
- **config/workspace_name.py**: Workspace-specific configuration
- **modules.txt**: Module definitions for Frappe

## Best Practices

1. **Version Control**: Commit related changes together
2. **Testing**: Test new features before deploying
3. **Permissions**: Always define appropriate roles
4. **Performance**: Optimize queries, use caching where appropriate
5. **Documentation**: Update README and guides when adding features

## Migration Path

If you want to rename the app from `management_dashboard` to `alkhora` in the future:

1. Rename directory: `management_dashboard/` → `alkhora/`
2. Rename package: `management_dashboard/management_dashboard/` → `alkhora/alkhora/`
3. Update all imports: `management_dashboard.*` → `alkhora.*`
4. Update hooks.py: `app_name = "alkhora"`
5. Update setup.py and pyproject.toml
6. Run migrations and update references

**Note**: The current structure works perfectly fine as-is. Renaming is optional and only needed if you want the technical name to match the brand name.

## Support and Development

- Follow Frappe Framework conventions: https://frappeframework.com/docs
- Refer to ERPNext documentation: https://docs.erpnext.com
- Use `WORKSPACE_GUIDE.md` when adding new workspaces
- Contact: support@alkhora.co
