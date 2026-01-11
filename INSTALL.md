# Installation Instructions

## Correct Installation Method

The app structure is correct. The setup files (`setup.py` and `pyproject.toml`) are located in the `management_dashboard/` directory.

### Option 1: Install from Local Directory

If you have the repository locally, point `bench get-app` to the `management_dashboard` directory:

```bash
# From your bench directory
bench get-app management_dashboard /absolute/path/to/ALKHORA-Management-Dashboard/management_dashboard
```

For example:
```bash
bench get-app management_dashboard /Users/adu94/ALKHORA-Management-Dashboard/management_dashboard
```

### Option 2: Install from Git Repository

If this is a git repository, you can install directly:

```bash
# From your bench directory
bench get-app management_dashboard https://github.com/your-username/ALKHORA-Management-Dashboard.git --branch main
```

Then install the app:
```bash
bench --site <your-site-name> install-app management_dashboard
```

### Option 3: Copy to apps directory

Alternatively, you can copy the `management_dashboard` directory directly to your bench's `apps` directory:

```bash
# From your bench directory
cp -r /path/to/ALKHORA-Management-Dashboard/management_dashboard apps/
bench --site <your-site-name> install-app management_dashboard
```

## Verify Installation

After installation, verify the app structure:

```bash
cd apps/management_dashboard
ls -la
# You should see: setup.py, pyproject.toml, MANIFEST.in, management_dashboard/
```

## Important Notes

- The `management_dashboard/` directory (the one containing `setup.py`) is the app root
- The `management_dashboard/management_dashboard/` directory contains the actual app code
- This structure is correct for Frappe apps

## Troubleshooting

If you still get the error "Not a valid Frappe App!", check:

1. **Make sure you're pointing to the correct directory**: The directory containing `setup.py` should be the one you pass to `bench get-app`

2. **Check file permissions**: Ensure all files are readable
   ```bash
   ls -la management_dashboard/setup.py
   ```

3. **Verify the structure**: Run this from the app directory:
   ```bash
   cd management_dashboard
   ls -1
   # Should show: setup.py, pyproject.toml, MANIFEST.in, management_dashboard/, etc.
   ```
