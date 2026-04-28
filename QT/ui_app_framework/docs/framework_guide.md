# UI Task Framework Guide

This document explains the framework at the architectural level rather than walking line by line through the code.

It focuses on:

- the problems the framework is trying to solve
- the reasoning behind the current module split
- the design patterns in use
- the runtime workflow
- best practices for Qt/PySide task orchestration
- common pitfalls when the system grows

Use this file together with [detailed_design.md](./detailed_design.md):

- `framework_guide.md` explains the “why”
- `detailed_design.md` explains the “how”

## 1. What problem does this framework solve?

In a desktop PySide application, task execution is usually a subsystem, not just a helper function.

You typically need all of the following at the same time:

1. Long-running work that does not freeze the UI.
2. Safe progress reporting from worker threads.
3. Cooperative cancellation.
4. UI state that stays consistent with task state.
5. An easy way to add new task types.
6. A runtime model that can power dashboards, logs, snapshots, and future analytics.

Without a framework, task code often degenerates into:

- views creating workers directly
- workers emitting into widgets with too much coupling
- cancellation logic copied in multiple places
- every task type using a slightly different execution pattern
- no central operational visibility

This framework is an attempt to put those concerns on top of a reusable skeleton.

## 2. Is this already a real framework?

In the practical sense: yes, it is becoming one.

It already has several framework-like characteristics:

- core abstractions
- extension points
- runtime state infrastructure
- a coordinator/facade
- a separation between reusable framework code and demo application code

In the stricter “production-complete framework” sense: not yet.

It still lacks features such as:

- retry policy
- timeout policy
- task priority and scheduling strategies
- task dependency graphs
- persistence for history
- structured telemetry
- test coverage
- a clearly versioned public API

The correct assessment is:

`This is a strong framework skeleton, not a finished framework product.`

## 3. Current project structure

The project is now split into three major areas:

- `framework/`
- `demo_app/`
- `docs/`

This is an important improvement over a flat directory because it separates reusable code from showcase code.

### `framework/`

This is the reusable subsystem:

- `domain.py`
- `registry.py`
- `runtime_store.py`
- `qt_adapter.py`
- `views.py`
- `presenter.py`
- `manager.py`

If this project were packaged later, `framework/` would be the first candidate for extraction into a standalone package.

### `demo_app/`

This is the showcase application that consumes the framework.

It is intentionally richer than a toy example so the framework gets exercised under more realistic conditions.

### `docs/`

This is where architecture notes, diagrams, and learning materials live.

### `main.py`

This is only an entrypoint.

That is good architecture hygiene. The entrypoint should be small.

## 4. Module responsibilities

### `framework/domain.py`

Contains:

- `ProgressReporter`
- `DomainTask`
- task implementations
- `TaskType`
- `TaskStatus`
- factory abstractions
- `TaskDefinition`

This is the semantic core of the framework.

### `framework/registry.py`

Contains `TaskRegistry`.

This is the framework’s extension point for mapping task types to definitions and factories.

### `framework/runtime_store.py`

Contains:

- `TaskRuntimeEntry`
- `TaskRuntimeStore`

This is the central in-memory operational state model.

### `framework/qt_adapter.py`

Contains:

- `TaskSignals`
- `QtProgressReporter`
- `QtTaskRunner`

This is the thread and signal adapter layer.

### `framework/views.py`

Contains:

- `TaskViewPort`
- `TaskView`
- `RuntimeStoreView`
- `EventLogView`

These are framework-level widgets and widget contracts.

### `framework/presenter.py`

Contains:

- `TaskPresenter`
- `RuntimeStorePresenter`

These presenters orchestrate task execution and runtime monitoring.

### `framework/manager.py`

Contains `TaskManager`.

This is the facade and coordination layer exposed to the application.

## 5. Problem-to-solution mapping

### Problem: “The UI freezes during long work”

Solution:

- `QtTaskRunner`
- `QThreadPool`
- worker-thread domain execution

### Problem: “Domain code is tied to Qt”

Solution:

- `ProgressReporter`
- `QtProgressReporter`

This is a small but useful application of Dependency Inversion.

### Problem: “Every new task type needs more manager branching”

Solution:

- `TaskRegistry`
- `TaskDefinition`

This is a registry-based extension mechanism.

### Problem: “I have no central place to inspect what tasks are doing”

Solution:

- `TaskRuntimeStore`

That store is what makes monitoring, export, and dashboards viable.

### Problem: “My widgets are overloaded with orchestration logic”

Solution:

- `TaskPresenter`
- `RuntimeStorePresenter`
- `TaskViewPort`

That keeps widgets focused on rendering and interaction surfaces.

## 6. Design patterns currently in use

### Adapter

- `QtProgressReporter`
- `QtTaskRunner`

These bridge domain-style contracts to Qt-native execution and signaling.

### Registry

- `TaskRegistry`

This is the right pattern when the system must stay open to new task types.

### Factory

- `TaskFactory`
- concrete factory implementations

This keeps presenters from depending on raw constructor details.

### Presenter / Supervising Controller

- `TaskPresenter`
- `RuntimeStorePresenter`

These coordinate behavior between model-like state and widgets without putting too much logic into the widgets themselves.

### State Store

- `TaskRuntimeStore`

This is not a frontend state-management library clone. It is simply the right central place for runtime task state.

### Composition Root

- `demo_app/showcase.py`
- `main.py`

Application wiring is separated from the framework modules.

## 7. Showcase application coverage

The showcase application is deliberately broader now.

It covers several kinds of runtime behavior:

### Common scenarios

1. Download-style progress
2. Batch-like processing progress
3. Report generation workflow progress
4. Task cancellation
5. Parallel task execution
6. Dynamic task card creation

### Less typical but important scenarios

1. Deliberate failure tasks
2. Runtime dashboard monitoring
3. Event log inspection
4. JSON snapshot export
5. Closing the window while tasks are still running
6. Scenario-driven task launches

That makes the demo much better at pressure-testing the framework than a single static card screen.

## 8. Runtime workflow

The full runtime path looks like this:

1. The app requests a task card or binds a view.
2. `TaskManager` resolves the task definition through the registry.
3. A presenter is attached to the view.
4. The user starts the task.
5. The presenter creates a domain task and a task runner.
6. The runtime store registers the task.
7. The runner executes in the thread pool.
8. Progress and messages are emitted back safely.
9. The presenter updates both the view and the runtime store.
10. Monitoring views react to runtime store signals.
11. On completion, cancellation, or failure, the presenter finalizes both runtime and UI state.

That is a healthy workflow because it keeps one consistent path for all task outcomes.

## 9. Best practices reflected in the framework

1. Worker threads never touch widgets directly.
2. Completion is emitted from `finally`.
3. Cancellation is cooperative.
4. Runtime state is centralized.
5. Presenters talk to view contracts rather than reaching deeply into child widgets.
6. Task registration goes through a registry instead of branching logic.
7. Shutdown-time signal emission is guarded so teardown is less fragile.
8. Showcase code lives outside the reusable framework package.

## 10. Pitfalls to watch for

### Pitfall 1: turning `TaskManager` into a god object

It already coordinates a lot. Resist the temptation to dump every new feature there.

When the framework grows, split concerns such as:

- retry policy
- scheduling policy
- history persistence
- telemetry

### Pitfall 2: bypassing `TaskRuntimeStore`

If monitoring logic starts reading random presenter internals instead of the runtime store, the framework loses coherence.

### Pitfall 3: letting presenters manipulate widget internals again

The `TaskViewPort` boundary exists for a reason. Keep using it.

### Pitfall 4: mixing framework code with showcase-only code

The `demo_app/` layer should remain a consumer of the framework, not an extension dumping ground.

### Pitfall 5: assuming the demo proves production readiness

The showcase is much stronger now, but it is still a showcase. It does not replace tests, packaging discipline, or operational hardening.

## 11. Clean Architecture assessment

This project is moving toward pragmatic Clean Architecture, not textbook-pure Clean Architecture.

What is good:

- domain tasks do not depend on Qt widgets
- runtime state is separated from presentation
- app composition is separated from framework code
- presenters work through a view-facing contract

What is still Qt-bound:

- presenters are `QObject`s
- the manager is a `QObject`
- runtime signaling is still Qt-native

That is a reasonable compromise for a PySide desktop framework.

Trying to force purity too early would likely add ceremony without enough payoff.

## 12. Where to go next

If you want to push the framework further, the next valuable steps are:

1. Add tests for presenters, registry, and runtime store.
2. Add retry and timeout policies.
3. Add task history persistence.
4. Split framework widgets into a dedicated subpackage when they grow further.
5. Define a stable public API surface and hide more internals.

## 13. Recommended study order

If the goal is to learn the framework deeply, study it in this order:

1. [project_layout.md](./project_layout.md)
2. [module.puml](./module.puml)
3. [framework/domain.py](../framework/domain.py)
4. [framework/registry.py](../framework/registry.py)
5. [framework/runtime_store.py](../framework/runtime_store.py)
6. [framework/qt_adapter.py](../framework/qt_adapter.py)
7. [framework/views.py](../framework/views.py)
8. [framework/presenter.py](../framework/presenter.py)
9. [framework/manager.py](../framework/manager.py)
10. [demo_app/showcase.py](../demo_app/showcase.py)

That sequence moves from core abstractions outward to orchestration and application behavior.
