# Project Layout

This document explains the current directory structure of `ui_app_framework` and why the project is split this way.

The main goal is to make it obvious which code is:

- reusable framework code
- showcase/demo code
- documentation

## Directory structure

```text
ui_app_framework/
├─ main.py
├─ framework/
│  ├─ __init__.py
│  ├─ domain.py
│  ├─ registry.py
│  ├─ runtime_store.py
│  ├─ qt_adapter.py
│  ├─ views.py
│  ├─ presenter.py
│  └─ manager.py
├─ demo_app/
│  ├─ __init__.py
│  ├─ models.py
│  ├─ widgets.py
│  └─ showcase.py
├─ docs/
│  ├─ framework_guide.md
│  ├─ detailed_design.md
│  ├─ project_layout.md
│  └─ *.puml
└─ exports/
```

## What each area is for

### `main.py`

This is only the application entrypoint.

It should stay small.
It should not contain framework logic.
It should not become a second orchestration layer.

The current implementation follows that rule.

### `framework/`

This is the reusable core.

It currently contains:

- domain abstractions
- task registry
- runtime state store
- Qt adapter code
- reusable views
- presenters
- the task manager/facade

If the project is ever packaged as a reusable library, this directory is the natural starting point.

### `demo_app/`

This directory contains the showcase application that consumes the framework.

That separation matters because:

- the demo can evolve without polluting framework internals
- the framework can stay reusable
- architectural boundaries are easier to maintain

### `docs/`

This is the documentation area:

- guides
- design notes
- PlantUML diagrams
- project layout notes

Keeping documentation here avoids mixing study notes with executable framework code.

### `exports/`

This is the intended place for exported JSON snapshots and similar generated artifacts.

In a production app, this might later become:

- a user-selected export path
- a temp directory
- an application data directory

## Why this structure is better than a flat folder

Before the refactor, the project had the usual signs of a growing prototype:

- framework logic and demo logic were mixed
- documentation reflected older layouts
- the entrypoint still carried too much showcase responsibility

The new structure is better because:

1. framework code is isolated
2. demo code is explicitly a consumer
3. the docs folder has a clear purpose
4. future packaging is easier

## Maintenance rules

Here are the rules worth following if you want this structure to stay healthy.

### When adding a new task type

Update:

- `framework/domain.py`
- registration logic through the framework boundary

Do not bury new task-type rules inside the demo app if they belong to the framework.

### When adding a new monitoring or analytics feature

Start with:

- `framework/runtime_store.py`

Only then move to widgets or demo screens.

### When adding a new showcase screen

Put it in:

- `demo_app/`

That keeps the framework package from becoming application-specific.

### When adding reusable widgets

Put them in:

- `framework/views.py`

or split them into a future `framework/widgets/` subpackage if the widget set becomes large enough.

### When adding documentation

Put it in:

- `docs/`

Keep executable code focused on execution, not on long-form explanation.

## Warning signs that the structure is degrading

Watch for these symptoms:

- `demo_app/` importing framework internals in ad hoc ways
- `framework/manager.py` growing into a god object
- presenters starting to carry business rules
- runtime monitoring bypassing `TaskRuntimeStore`
- docs drifting away from the real code structure

When those signs appear, it is time for another round of extraction and cleanup.

## Likely future refinements

If the framework keeps growing, the next structure improvements may include:

- `framework/tasks/`
- `framework/widgets/`
- `framework/presenters/`
- `framework/policies/`
- `framework/history/`

The current structure is not the final form, but it is already much more professional than a single mixed folder.
