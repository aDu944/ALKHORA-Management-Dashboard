# Migration Plan: Management Dashboard → ALKHORA App

This document outlines the migration from a single-purpose Management Dashboard app to a general ALKHORA company app.

## Strategy

Since Frappe app names must match directory names, we have two options:

### Option 1: Keep Current Structure, Rebrand (Recommended for now)
- Update app metadata to ALKHORA branding
- Structure code for multiple workspaces/modules
- Management Dashboard becomes the first workspace
- Easier migration, no directory renaming needed

### Option 2: Full Rename (Requires directory movement)
- Rename `management_dashboard/` → `alkhora/`
- Rename `management_dashboard/management_dashboard/` → `alkhora/alkhora/`
- Update all imports and references
- More complex but cleaner long-term

## Current Implementation

We're implementing Option 1 with clear workspace structure, making Option 2 easier later if needed.
