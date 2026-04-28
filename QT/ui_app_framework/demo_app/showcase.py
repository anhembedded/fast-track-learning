from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from PySide6.QtCore import QDate, QObject, Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QLineEdit,
)

from framework.domain import TaskStatus, TaskType
from framework.manager import TaskManager
from framework.presenter import RuntimeStorePresenter
from framework.views import EventLogView, RuntimeStoreView

from .models import ScenarioDefinition, TaskBlueprint
from .widgets import JsonSnapshotView, MetricCard, StatusDistributionWidget


class ShowcasePresenter(QObject):
    def __init__(self, runtime_store, metric_cards: dict[str, MetricCard], chart: StatusDistributionWidget, recent_list: QListWidget, json_view: JsonSnapshotView):
        super().__init__(chart)
        self.runtime_store = runtime_store
        self.metric_cards = metric_cards
        self.chart = chart
        self.recent_list = recent_list
        self.json_view = json_view

        self.runtime_store.entry_added.connect(self.refresh)
        self.runtime_store.entry_updated.connect(self.refresh)
        self.runtime_store.entry_removed.connect(self.refresh)
        self.refresh()

    @Slot()
    @Slot(str)
    def refresh(self, _task_id: str | None = None):
        entries = self.runtime_store.list_entries()
        summary = self.runtime_store.summary_by_status()

        self.metric_cards["total"].set_value(str(len(entries)), "Tracked tasks")
        self.metric_cards["running"].set_value(str(summary[TaskStatus.RUNNING]), "Running now")
        self.metric_cards["failed"].set_value(str(summary[TaskStatus.FAILED]), "Need attention")
        completed = summary[TaskStatus.COMPLETED] + summary[TaskStatus.CANCELLED]
        self.metric_cards["closed"].set_value(str(completed), "Closed tasks")

        self.chart.set_items(
            [
                ("Pending", summary[TaskStatus.PENDING], "#94a3b8"),
                ("Running", summary[TaskStatus.RUNNING], "#0ea5e9"),
                ("Completed", summary[TaskStatus.COMPLETED], "#16a34a"),
                ("Cancelled", summary[TaskStatus.CANCELLED], "#f59e0b"),
                ("Failed", summary[TaskStatus.FAILED], "#dc2626"),
            ]
        )

        self.recent_list.clear()
        sorted_entries = sorted(entries, key=lambda item: item.created_at, reverse=True)[:8]
        for entry in sorted_entries:
            item = QListWidgetItem(f"{entry.task_name} | {entry.status.value} | {entry.progress}%")
            self.recent_list.addItem(item)

        self.json_view.set_snapshot(self.runtime_store.export_snapshot())


class ShowcaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Track UI Task Framework Studio")
        self.resize(1540, 980)
        self.manager = TaskManager()
        self._scenario_map = self._build_scenarios()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        header = QHBoxLayout()
        title = QLabel("Framework Studio")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        subtitle = QLabel("Dashboard, task lab, runtime center, scenario browser, and JSON export in one showcase.")
        subtitle.setStyleSheet("color: #475569;")
        title_box = QVBoxLayout()
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        root.addLayout(header)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self._build_dashboard_tab()
        self._build_task_lab_tab()
        self._build_runtime_center_tab()
        self._build_scenarios_tab()

        self.runtime_table_presenter = RuntimeStorePresenter(
            self.manager.runtime_store,
            self.runtime_view,
            self.event_log_view,
        )
        self.showcase_presenter = ShowcasePresenter(
            self.manager.runtime_store,
            self.metric_cards,
            self.status_chart,
            self.recent_tasks_list,
            self.json_snapshot_view,
        )

        self._seed_showcase_cards()

    def _build_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        metrics = QHBoxLayout()
        self.metric_cards = {
            "total": MetricCard("Tracked Tasks", "#2563eb"),
            "running": MetricCard("Running", "#0891b2"),
            "failed": MetricCard("Failed", "#dc2626"),
            "closed": MetricCard("Closed", "#16a34a"),
        }
        for card in self.metric_cards.values():
            metrics.addWidget(card)
        layout.addLayout(metrics)

        body = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(body)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Prebuilt Task Board"))
        task_grid = QGridLayout()
        self.dashboard_cards_layout = task_grid
        left_layout.addLayout(task_grid)

        quick_group = QGroupBox("Quick Scenarios")
        quick_layout = QHBoxLayout(quick_group)
        morning_btn = QPushButton("Run Morning Ops")
        chaos_btn = QPushButton("Run Chaos Drill")
        reporting_btn = QPushButton("Run Reporting Burst")
        quick_layout.addWidget(morning_btn)
        quick_layout.addWidget(chaos_btn)
        quick_layout.addWidget(reporting_btn)
        left_layout.addWidget(quick_group)
        left_layout.addStretch()

        morning_btn.clicked.connect(lambda: self.run_scenario("Morning Ops"))
        chaos_btn.clicked.connect(lambda: self.run_scenario("Chaos Drill"))
        reporting_btn.clicked.connect(lambda: self.run_scenario("Reporting Burst"))

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.status_chart = StatusDistributionWidget()
        self.recent_tasks_list = QListWidget()
        right_layout.addWidget(QLabel("Runtime Distribution"))
        right_layout.addWidget(self.status_chart)
        right_layout.addWidget(QLabel("Recent Tasks"))
        right_layout.addWidget(self.recent_tasks_list)

        body.addWidget(left_panel)
        body.addWidget(right_panel)
        body.setSizes([900, 460])

        self.tabs.addTab(tab, "Operations Dashboard")

    def _build_task_lab_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        left = QGroupBox("Task Composer")
        form = QFormLayout(left)
        self.task_type_combo = QComboBox()
        for task_type in TaskType:
            self.task_type_combo.addItem(task_type.value, task_type)
        self.primary_input = QLineEdit("custom_dataset")
        self.secondary_input = QSpinBox()
        self.secondary_input.setRange(1, 100)
        self.secondary_input.setValue(8)
        self.schedule_date = QDateEdit()
        self.schedule_date.setDate(QDate.currentDate())
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Operator notes, assumptions, handoff context...")
        self.create_card_button = QPushButton("Create Task Card")
        form.addRow("Task Type", self.task_type_combo)
        form.addRow("Primary Value", self.primary_input)
        form.addRow("Intensity / Count", self.secondary_input)
        form.addRow("Target Date", self.schedule_date)
        form.addRow("Notes", self.notes_input)
        form.addRow("", self.create_card_button)

        sheet_group = QGroupBox("Batch Launcher Sheet")
        sheet_layout = QVBoxLayout(sheet_group)
        self.sheet_table = QTableWidget(4, 4)
        self.sheet_table.setHorizontalHeaderLabels(["Task Type", "Primary", "Secondary", "Comment"])
        sheet_rows = [
            ("download", "https://example.com/assets/roadmap.pdf", "1", "onboarding asset"),
            ("process_data", "crm_stage_snapshot", "14", "weekly crunch"),
            ("generate_report", "executive_rollup", "9", "Friday board pack"),
            ("failing_job", "quality_gate", "40", "resilience drill"),
        ]
        for row, values in enumerate(sheet_rows):
            for col, value in enumerate(values):
                self.sheet_table.setItem(row, col, QTableWidgetItem(value))
        launch_row_btn = QPushButton("Launch Selected Row")
        launch_all_btn = QPushButton("Launch All Rows")
        sheet_layout.addWidget(self.sheet_table)
        sheet_actions = QHBoxLayout()
        sheet_actions.addWidget(launch_row_btn)
        sheet_actions.addWidget(launch_all_btn)
        sheet_layout.addLayout(sheet_actions)

        left_stack = QVBoxLayout()
        left_stack.addWidget(left)
        left_stack.addWidget(sheet_group)

        right = QGroupBox("Dynamic Task Board")
        right_layout = QVBoxLayout(right)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        board_container = QWidget()
        self.dynamic_cards_layout = QVBoxLayout(board_container)
        self.dynamic_cards_layout.addStretch()
        scroll.setWidget(board_container)
        right_layout.addWidget(scroll)

        layout.addLayout(left_stack, 1)
        layout.addWidget(right, 2)

        self.create_card_button.clicked.connect(self.create_task_from_form)
        launch_row_btn.clicked.connect(self.launch_selected_sheet_row)
        launch_all_btn.clicked.connect(self.launch_all_sheet_rows)

        self.tabs.addTab(tab, "Task Lab")

    def _build_runtime_center_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        top = QSplitter(Qt.Orientation.Horizontal)
        self.runtime_view = RuntimeStoreView()
        self.event_log_view = EventLogView()
        top.addWidget(self.runtime_view)
        top.addWidget(self.event_log_view)
        top.setSizes([760, 620])

        self.json_snapshot_view = JsonSnapshotView()
        self.json_snapshot_view.refresh_button.clicked.connect(self.refresh_json_snapshot)
        self.json_snapshot_view.export_button.clicked.connect(self.export_json_snapshot)

        layout.addWidget(top)
        layout.addWidget(self.json_snapshot_view)
        self.tabs.addTab(tab, "Runtime Center")

    def _build_scenarios_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        self.scenario_tree = QTreeWidget()
        self.scenario_tree.setHeaderLabels(["Scenario", "Description"])
        for name, scenario in self._scenario_map.items():
            item = QTreeWidgetItem([name, scenario.description])
            self.scenario_tree.addTopLevelItem(item)
        self.scenario_tree.expandAll()

        panel = QGroupBox("Scenario Runner")
        panel_layout = QVBoxLayout(panel)
        self.scenario_description = QTextEdit()
        self.scenario_description.setReadOnly(True)
        self.scenario_run_button = QPushButton("Run Selected Scenario")
        self.scenario_preview_list = QListWidget()
        panel_layout.addWidget(QLabel("Description"))
        panel_layout.addWidget(self.scenario_description)
        panel_layout.addWidget(QLabel("Task Blueprint Preview"))
        panel_layout.addWidget(self.scenario_preview_list)
        panel_layout.addWidget(self.scenario_run_button)

        layout.addWidget(self.scenario_tree, 1)
        layout.addWidget(panel, 1)

        self.scenario_tree.currentItemChanged.connect(self.on_scenario_selected)
        self.scenario_run_button.clicked.connect(self.run_selected_scenario)
        if self.scenario_tree.topLevelItemCount():
            self.scenario_tree.setCurrentItem(self.scenario_tree.topLevelItem(0))

        self.tabs.addTab(tab, "Scenario Browser")

    def _seed_showcase_cards(self):
        cards = [
            self.manager.create_task(TaskType.DOWNLOAD, "https://example.com/assets/course_bundle.zip", "/tmp/course_bundle.zip"),
            self.manager.create_task(TaskType.PROCESS_DATA, "student_sessions_2026", 10),
            self.manager.create_task(TaskType.GENERATE_REPORT, "weekly_kpi_digest", 7),
            self.manager.create_task(TaskType.FAILING_JOB, "nightly_validation", 60),
        ]
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for card, (row, column) in zip(cards, positions):
            self.dashboard_cards_layout.addWidget(card, row, column)

    def _create_task_card(self, task_type: TaskType, primary: str, secondary: int):
        if task_type == TaskType.DOWNLOAD:
            return self.manager.create_task(task_type, primary, "/tmp/generated_output.bin")
        return self.manager.create_task(task_type, primary, secondary)

    def _append_dynamic_card(self, task_type: TaskType, primary: str, secondary: int):
        card = self._create_task_card(task_type, primary, secondary)
        self.dynamic_cards_layout.insertWidget(self.dynamic_cards_layout.count() - 1, card)
        return card

    def _build_scenarios(self) -> dict[str, ScenarioDefinition]:
        return {
            "Morning Ops": ScenarioDefinition(
                name="Morning Ops",
                description="A mixed startup workload: refresh source files, crunch overnight data, and prepare a briefing pack.",
                tasks=(
                    TaskBlueprint(TaskType.DOWNLOAD, "Asset bundle", "https://example.com/assets/morning_bundle.zip", 1),
                    TaskBlueprint(TaskType.PROCESS_DATA, "Overnight sessions", "overnight_sessions", 12),
                    TaskBlueprint(TaskType.GENERATE_REPORT, "Ops brief", "ops_brief", 6),
                ),
            ),
            "Chaos Drill": ScenarioDefinition(
                name="Chaos Drill",
                description="Stress the framework with long-running work, cancellation opportunities, and one deliberate failure.",
                tasks=(
                    TaskBlueprint(TaskType.PROCESS_DATA, "Warehouse backfill", "warehouse_backfill", 18),
                    TaskBlueprint(TaskType.FAILING_JOB, "Quality gate", "quality_gate", 45),
                    TaskBlueprint(TaskType.GENERATE_REPORT, "Incident digest", "incident_digest", 10),
                ),
            ),
            "Reporting Burst": ScenarioDefinition(
                name="Reporting Burst",
                description="Generate multiple report-style tasks side by side to inspect concurrency and runtime visibility.",
                tasks=(
                    TaskBlueprint(TaskType.GENERATE_REPORT, "Board summary", "board_summary", 8),
                    TaskBlueprint(TaskType.GENERATE_REPORT, "Customer digest", "customer_digest", 9),
                    TaskBlueprint(TaskType.DOWNLOAD, "Reference archive", "https://example.com/reference/archive.zip", 1),
                ),
            ),
        }

    @Slot()
    def create_task_from_form(self):
        task_type = self.task_type_combo.currentData()
        primary = self.primary_input.text().strip() or f"task_{time.time_ns()}"
        secondary = self.secondary_input.value()
        self._append_dynamic_card(task_type, primary, secondary)

    @Slot()
    def launch_selected_sheet_row(self):
        row = self.sheet_table.currentRow()
        if row < 0:
            return
        self._launch_sheet_row(row)

    @Slot()
    def launch_all_sheet_rows(self):
        for row in range(self.sheet_table.rowCount()):
            self._launch_sheet_row(row)

    def _launch_sheet_row(self, row: int):
        type_item = self.sheet_table.item(row, 0)
        primary_item = self.sheet_table.item(row, 1)
        secondary_item = self.sheet_table.item(row, 2)
        if not type_item or not primary_item or not secondary_item:
            return
        task_type = TaskType(type_item.text())
        primary = primary_item.text()
        secondary = int(secondary_item.text())
        self._append_dynamic_card(task_type, primary, secondary)

    @Slot()
    def refresh_json_snapshot(self):
        self.json_snapshot_view.set_snapshot(self.manager.runtime_store.export_snapshot())

    @Slot()
    def export_json_snapshot(self):
        exports_dir = Path(__file__).resolve().parents[1] / "exports"
        exports_dir.mkdir(exist_ok=True)
        default_path = exports_dir / f"runtime_snapshot_{int(time.time())}.json"
        path, _ = QFileDialog.getSaveFileName(self, "Export Runtime Snapshot", str(default_path), "JSON Files (*.json)")
        if not path:
            return
        payload = self.manager.runtime_store.export_snapshot()
        Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        self.json_snapshot_view.set_export_path(path)

    @Slot()
    def run_selected_scenario(self):
        item = self.scenario_tree.currentItem()
        if item is None:
            return
        self.run_scenario(item.text(0))

    def run_scenario(self, name: str):
        scenario = self._scenario_map.get(name)
        if scenario is None:
            return
        for blueprint in scenario.tasks:
            self._append_dynamic_card(blueprint.task_type, blueprint.primary_value, blueprint.secondary_value)

    @Slot()
    def on_scenario_selected(self):
        item = self.scenario_tree.currentItem()
        if item is None:
            return
        scenario = self._scenario_map[item.text(0)]
        self.scenario_description.setPlainText(scenario.description)
        self.scenario_preview_list.clear()
        for blueprint in scenario.tasks:
            self.scenario_preview_list.addItem(
                f"{blueprint.task_type.value} | {blueprint.primary_value} | intensity={blueprint.secondary_value}"
            )


def run():
    app = QApplication(sys.argv)
    window = ShowcaseMainWindow()
    window.show()
    return app.exec()
