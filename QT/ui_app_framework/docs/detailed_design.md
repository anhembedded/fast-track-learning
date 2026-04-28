# Task Framework Detailed Design

This document explains the current design of the task framework in detail, with a focus on how the code works today and why the responsibilities are split the way they are.

If [framework_guide.md](./framework_guide.md) is the architectural overview, this file is the implementation-oriented walkthrough.

## 1. Design goals

The framework is built to solve a familiar set of problems in PySide applications:

1. Run long tasks without blocking the UI thread.
2. Send progress and messages back from worker threads safely.
3. Support cooperative cancellation.
4. Keep UI state aligned with task state.
5. Add new task types without rewriting orchestration code.
6. Provide a foundation for dashboards, logs, snapshots, and future operational tooling.

The current implementation is split into a few clear layers:

1. Domain layer
2. Registry layer
3. Runtime state layer
4. Qt adapter layer
5. View and presenter layer
6. Coordination layer

That is also the best order in which to study the code.

## 2. PlantUML files

The `docs/` folder contains:

- `class.puml`: class relationships and ownership
- `component.puml`: component boundaries and thread roles
- `sequence.puml`: runtime interaction flow
- `state.puml`: task view lifecycle
- `module.puml`: package/module dependency layout

Suggested reading order:

1. `module.puml`
2. `component.puml`
3. `sequence.puml`
4. `class.puml`
5. `state.puml`

## 3. Domain layer

The domain layer lives in [framework/domain.py](../framework/domain.py).

### `ProgressReporter`

This is the smallest abstraction a domain task needs:

- `report_progress(percent)`
- `report_message(message)`
- `is_cancelled()`

Why it matters:

- Domain tasks do not know about `QObject`, `Signal`, or `QWidget`.
- Domain tasks only know they can report progress and ask whether cancellation has been requested.
- That keeps the domain logic independent from Qt.

This is a lightweight use of Dependency Inversion: domain code depends on an abstraction instead of a UI framework API.

### `DomainTask`

`DomainTask` is the abstract base class for units of work.

It only defines:

- `name`
- `execute(reporter)`

Important rule:

`execute()` contains business work, not thread management and not UI manipulation.

### Concrete tasks

The framework currently includes several example tasks:

- `DownloadTask`
- `ProcessDataTask`
- `GenerateReportTask`
- `FailingTask`

They deliberately cover different runtime behaviors:

- normal progress reporting
- staged or batched work
- longer multi-step workflows
- exception paths

That makes them useful for testing the framework, not just demonstrating a happy path.

## 4. Registry layer

The registry layer lives in [framework/registry.py](../framework/registry.py).

### `TaskDefinition`

`TaskDefinition` describes how a task type should be exposed:

- which factory class creates the task
- which start button label should be used
- which cancel button label should be used

This lets the framework carry UI-facing metadata next to the construction rule for a task type.

### `TaskRegistry`

`TaskRegistry` maps `TaskType` to `TaskDefinition`.

Its job is simple:

- register task definitions
- resolve task definitions
- create task factories

This replaces a growing `if/elif` dispatch chain with a registry-based extension point.

That is a meaningful step toward framework-like structure because new task types can be added without reopening multiple orchestration methods.

## 5. Runtime state layer

The runtime state layer lives in [framework/runtime_store.py](../framework/runtime_store.py).

### `TaskRuntimeEntry`

This dataclass is the in-memory runtime record for one task.

It tracks:

- `task_id`
- `task_type`
- `task_name`
- `view_id`
- `status`
- `progress`
- `last_message`
- `error_message`
- `cancellation_requested`
- timestamps such as `created_at`, `started_at`, `finished_at`

This is not business persistence. It is operational runtime state.

### `TaskRuntimeStore`

`TaskRuntimeStore` is the central place that stores runtime entries and emits change notifications.

It supports:

- registering a task
- updating progress
- updating messages
- marking cancellation
- storing error text
- marking completion
- exporting a snapshot
- building summaries by status and type

Why this matters:

- dashboards can subscribe to one source
- logs can subscribe to one source
- JSON export has one source
- future history or analytics features can start from one source

Without this store, runtime knowledge would be spread across presenters and widgets.

## 6. Qt adapter layer

The adapter layer lives in [framework/qt_adapter.py](../framework/qt_adapter.py).

This is where domain abstractions are converted into Qt-native threading and signal mechanics.

### `TaskSignals`

`QRunnable` does not provide signals directly, so the framework uses a dedicated `QObject` helper:

- `progress`
- `message`
- `error`
- `finished`

This is a standard and practical PySide pattern.

### `QtProgressReporter`

This class implements `ProgressReporter` by translating domain callbacks into Qt signals.

It also holds the cancellation flag protected by `QMutex`.

Key point:

The domain layer talks to `ProgressReporter`.
The Qt layer talks in signals.
`QtProgressReporter` bridges those two worlds.

### `QtTaskRunner`

`QtTaskRunner` adapts a domain task into a `QRunnable`.

Responsibilities:

- hold the domain task
- create the progress reporter
- track `TaskStatus`
- emit `error`
- always emit `finished`

### Safe signal emission during shutdown

One subtle production issue appears when the main window is closed while worker tasks are still running.

At that point, some Qt-side signal sources may already have been destroyed while the worker thread is still executing. If the worker blindly emits a signal, PySide may raise:

`RuntimeError: Signal source has been deleted`

The framework now guards signal emission with a safe helper and `isValid(...)`.

That makes shutdown behavior much more robust.

## 7. View layer

Reusable framework-side widgets live in [framework/views.py](../framework/views.py).

### `TaskViewPort`

`TaskViewPort` is a small view contract used by the presenter.

It defines methods such as:

- `connect_start`
- `connect_cancel`
- `set_title`
- `reset_to_pending`
- `set_progress`
- `set_running`
- `set_final_state`
- `set_message`
- `set_cancelling`

Why it helps:

- the presenter no longer reaches into child widgets directly
- the concrete view can change internally without breaking presenter code
- the presenter becomes easier to reason about and easier to test

This is not “pure Clean Architecture” in the academic sense, but it is a very useful boundary.

### `TaskView`

`TaskView` is the reusable task card widget.

It knows how to display:

- title
- status
- progress
- message
- task id
- start/cancel actions

It does not know:

- how tasks are created
- how threads are managed
- how runtime state is stored

That separation is exactly what you want in a reusable task widget.

### `RuntimeStoreView`

This widget shows the task runtime store as a table.

It is useful for:

- operational visibility
- debugging
- framework demos
- future admin tooling

### `EventLogView`

This widget displays a plain-text event feed.

It is intentionally simple, but it proves that the runtime layer can drive global monitoring surfaces beyond task cards.

## 8. Presenter layer

Presenter logic lives in [framework/presenter.py](../framework/presenter.py).

### `TaskPresenter`

`TaskPresenter` is the main orchestration point between:

- the task view
- the task factory
- the task runner
- the runtime store
- the task manager

It runs on the UI thread and owns the interaction flow.

### `on_start()`

When the user presses Start:

1. Create a domain task from the factory.
2. Create a `QtTaskRunner`.
3. Connect runner signals.
4. Register the task in the runtime store.
5. Mark it as running.
6. Put the view into running mode.
7. Ask the manager to submit the runner.

### `on_cancel()`

The presenter does not kill the thread.

Instead it:

- requests cancellation on the runner
- marks the runtime entry as cancelling
- updates the view

That is cooperative cancellation, which is the correct model here.

### `on_runner_progress()` and `on_runner_message()`

These methods update both:

- the runtime store
- the visible task view

That is a deliberate design choice:

The presenter is the place where runtime state and UI state stay in sync.

### `on_runner_error()`

This captures the detailed error message, stores it in runtime state, and shows it in the view.

The framework intentionally preserves that detailed message rather than overwriting it later with a generic “Task failed”.

### `on_runner_finished()`

This method:

- converts the status payload back into `TaskStatus`
- computes the final user-facing message
- updates runtime state
- finalizes the view
- clears the current runner reference

### `RuntimeStorePresenter`

This presenter is separate from per-task presentation.

Its job is to observe `TaskRuntimeStore` and drive:

- `RuntimeStoreView`
- `EventLogView`

This is important because it proves the framework can drive cross-cutting operational views, not just one card at a time.

## 9. Coordination layer

Coordination lives in [framework/manager.py](../framework/manager.py).

### `TaskManager`

`TaskManager` acts as the framework-facing coordinator.

It owns:

- `QThreadPool`
- `TaskRegistry`
- `TaskRuntimeStore`
- presenter binding for views

It does not contain domain business logic.

### Default task registration

The manager registers a default set of task types on startup:

- download
- process data
- generate report
- failing job

That is good for the showcase app.

In a larger application, you might move some or all of that registration to a composition root or app bootstrap module.

### View cleanup

When a view is destroyed:

- the presenter mapping is removed
- any active task is asked to cancel
- runtime entries linked to that view are removed if the runtime store is still valid

This is a practical lifecycle cleanup path that matters in real UI shutdown behavior.

## 10. Demo app layer

The showcase application lives in [demo_app/showcase.py](../demo_app/showcase.py).

It is intentionally richer than a minimal demo.

The app now includes:

- an operations dashboard
- a task lab with form-driven creation
- a batch launch sheet
- a runtime center
- a scenario browser
- JSON snapshot export

That is useful because it exercises the framework from several directions:

- single-task interaction
- multi-task concurrency
- monitoring
- failure handling
- dynamic card creation
- shutdown behavior

## 11. Design patterns in practice

The framework currently uses a useful set of patterns:

- Adapter: `QtProgressReporter`, `QtTaskRunner`
- Registry: `TaskRegistry`
- Factory: `TaskFactory` and concrete factories
- Presenter / Supervising Controller: `TaskPresenter`, `RuntimeStorePresenter`
- State Store: `TaskRuntimeStore`
- Composition Root: the demo app entrypoint

These patterns are not present for decoration. Each one solves a specific pressure point in a task-driven desktop UI.

## 12. Best practices reflected in the code

1. Worker threads never touch widgets directly.
2. `finished` is emitted from `finally`.
3. Cancellation is cooperative, not forceful.
4. Runtime state is centralized.
5. Presenters talk to views through a contract, not by poking every child widget.
6. New task types are added through the registry rather than manager-side branching.
7. Shutdown behavior is guarded against dangling signal emission.

## 13. Known limitations

The current design is strong as a framework skeleton, but it is not a finished enterprise framework.

Still missing:

- retry policies
- timeouts
- task priorities
- task dependency graphs
- persistence for task history
- structured logging
- automated tests
- a stable public API surface for packaging

That is normal for the current stage.

## 14. Recommended reading order in code

If you want to learn the framework from the codebase itself, read in this order:

1. [framework/domain.py](../framework/domain.py)
2. [framework/registry.py](../framework/registry.py)
3. [framework/runtime_store.py](../framework/runtime_store.py)
4. [framework/qt_adapter.py](../framework/qt_adapter.py)
5. [framework/views.py](../framework/views.py)
6. [framework/presenter.py](../framework/presenter.py)
7. [framework/manager.py](../framework/manager.py)
8. [demo_app/showcase.py](../demo_app/showcase.py)
9. [main.py](../main.py)

That order mirrors the architecture from inner abstractions outward to orchestration and app composition.
