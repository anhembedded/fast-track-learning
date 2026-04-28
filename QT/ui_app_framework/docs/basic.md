# Basic Overview

This file is intentionally short.

The project has grown beyond the original single-file learning note, so the recommended documentation entry points are now:

1. [framework_guide.md](./framework_guide.md)
2. [detailed_design.md](./detailed_design.md)
3. [project_layout.md](./project_layout.md)
4. the PlantUML files in `docs/`

## What this project is now

It is no longer just a small Qt threading example.

It is now split into:

- a reusable task framework in `framework/`
- a richer showcase application in `demo_app/`
- a documentation set in `docs/`

## Suggested reading order

If you are learning the project from scratch:

1. Read [project_layout.md](./project_layout.md)
2. Read [framework_guide.md](./framework_guide.md)
3. Read [detailed_design.md](./detailed_design.md)
4. Open the PlantUML diagrams
5. Read the code starting from `framework/domain.py`

## Why this file still exists

This file is kept as a lightweight landing page so the documentation folder still has a simple, low-friction starting point.
