import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


STUDENT_NAME = "Tomer Raz"
STUDENT_EMAIL = "Tomeraz203@gmail.com"
REPOSITORY_URL = "https://github.com/tomeraz203-a11y/coding.git"


class GradeCorrectionWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.student_ids: list[str | int] = []
        self.original_grades: list[str | int | float] = []
        self.corrected_grades: list[str | int | float] = []
        self.selected_file: str = ""

        self.setWindowTitle("Grade Correction Tool")
        self.resize(1000, 760)
        self.setMinimumSize(760, 560)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(32, 28, 32, 28)
        main_layout.setSpacing(20)

        title = QLabel("Grade Correction")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Load a CSV file, review grades, and apply a bonus.")
        subtitle.setObjectName("pageSubtitle")
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        controls = QFrame()
        controls.setObjectName("controlsCard")
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(20, 18, 20, 18)
        controls_layout.setSpacing(14)

        file_row = QHBoxLayout()
        file_row.setSpacing(12)
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setMinimumWidth(0)
        self.file_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.choose_file_button = QPushButton("Choose CSV File")
        self.choose_file_button.setObjectName("primaryButton")
        self.choose_file_button.clicked.connect(self.choose_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(self.choose_file_button)
        controls_layout.addLayout(file_row)

        bonus_row = QHBoxLayout()
        bonus_row.setSpacing(12)
        bonus_label = QLabel("Bonus points")
        bonus_label.setObjectName("fieldLabel")
        self.bonus_input = QSpinBox()
        self.bonus_input.setObjectName("bonusInput")
        self.bonus_input.setRange(0, 10000)
        self.bonus_input.setFixedWidth(150)
        self.bonus_input.lineEdit().returnPressed.connect(self.apply_bonus)
        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("secondaryButton")
        self.update_button.clicked.connect(self.update_file)
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("textButton")
        self.about_button.clicked.connect(self.show_about)
        bonus_row.addWidget(bonus_label)
        bonus_row.addWidget(self.bonus_input)
        bonus_row.addStretch()
        bonus_row.addWidget(self.update_button)
        bonus_row.addWidget(self.about_button)
        controls_layout.addLayout(bonus_row)
        main_layout.addWidget(controls)

        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(12, 12, 12, 12)

        self.table = QTableWidget(50, 3)
        self.table.setObjectName("gradesTable")
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        table_layout.addWidget(self.table)
        main_layout.addWidget(table_card, 1)

    def choose_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select grades CSV",
            "",
            "CSV files (*.csv);;All files (*)",
        )
        if not file_path:
            return

        self.selected_file = file_path
        self.file_label.setText(file_path)
        self.load_grades(file_path)

    def load_grades(self, file_path: str) -> None:
        self.selected_file = file_path
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, "r") as f:
            next(f)
            for line in f:
                student_id, grade = line.strip().split(",")
                self.student_ids.append(student_id)
                self.original_grades.append(int(grade))
                self.corrected_grades.append(int(grade))

        self.update_table()

    def apply_bonus(self) -> None:
        bonus = self.bonus_input.value()
        self.corrected_grades = []

        for grade in self.original_grades:
            new_grade = min(100, grade + bonus)
            self.corrected_grades.append(new_grade)

        self.update_table()

    def update_file(self) -> None:
        pass

    def update_table(self) -> None:
        self.table.clearContents()
        columns = (
            self.student_ids,
            self.original_grades,
            self.corrected_grades,
        )
        row_count = min(self.table.rowCount(), max(map(len, columns), default=0))

        for row in range(row_count):
            for column, values in enumerate(columns):
                value = str(values[row]) if row < len(values) else ""
                self.table.setItem(row, column, QTableWidgetItem(value))

    def show_about(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.setMinimumWidth(380)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(16)

        details = QLabel(
            f"<h3>Grade Correction Tool</h3>"
            f"<p><b>{STUDENT_NAME}</b><br>{STUDENT_EMAIL}</p>"
            f'<p><a href="{REPOSITORY_URL}">GitHub repository</a></p>'
        )
        details.setObjectName("aboutDetails")
        details.setOpenExternalLinks(False)
        details.linkActivated.connect(
            lambda link: QDesktopServices.openUrl(QUrl(link))
        )
        layout.addWidget(details)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()


def main() -> None:
    app = QApplication(sys.argv)
    stylesheet_path = Path(__file__).with_name("style.qss")
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

    window = GradeCorrectionWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
