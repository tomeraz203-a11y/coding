from pathlib import Path 
import sys
import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CSV Plot Viewer")
        self.resize(1080, 760)

        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(36, 30, 36, 30)
        page_layout.setSpacing(22)

        heading = QLabel("CSV Plot Viewer")
        heading.setObjectName("heading")
        subtitle = QLabel("Choose a CSV file to get started.")
        subtitle.setObjectName("subtitle")
        page_layout.addWidget(heading)
        page_layout.addWidget(subtitle)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(12)
        self.choose_file_button = QPushButton("Choose CSV file")
        self.choose_file_button.setObjectName("primaryButton")
        self.choose_file_button.clicked.connect(self.open_file)
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("secondaryButton")
        self.about_button.clicked.connect(self.show_about)
        toolbar.addWidget(self.choose_file_button)
        toolbar.addWidget(self.about_button)
        toolbar.addStretch()
        page_layout.addLayout(toolbar)

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")
        page_layout.addWidget(self.file_label)

        chart_panel = QWidget()
        chart_panel.setObjectName("chartPanel")
        chart_layout = QVBoxLayout(chart_panel)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        chart_layout.setSpacing(12)
        chart_heading = QLabel("Chart preview")
        chart_heading.setObjectName("panelHeading")
        chart_layout.addWidget(chart_heading)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_axis_off()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setObjectName("plotCanvas")
        chart_layout.addWidget(self.canvas, stretch=1)
        page_layout.addWidget(chart_panel, stretch=1)

        self.setCentralWidget(page)

    def open_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a CSV file",
            "",
            "CSV files (*.csv)",
        )
        if not file_path:
            return

        self.file_label.setText(Path(file_path).name)
        self.plot_data(file_path)

    def plot_data(self, file_path: str) -> None:
        temperatures = []
        revenues = []

        with open(file_path, "r") as f:
            next(f)
            for line in f:
                temp, rev = line.strip().split(",")
                temperatures.append(float(temp))
                revenues.append(float(rev))

        coefficients = np.polyfit(temperatures, revenues, 1)
        line_function = np.poly1d(coefficients)
        line_x = np.linspace(min(temperatures), max(temperatures), 100)
        line_y = line_function(line_x)

        self.ax.clear()
        self.ax.set_axis_on()
        self.ax.scatter(temperatures, revenues, label="Data", s=10, color="blue", marker="x")
        self.ax.plot(line_x, line_y, color="red", label="Trend Line")
        self.ax.text(
            min(temperatures),
            max(revenues) * 0.9,
            f"y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}",
            color="red",
        )
        self.ax.set_xlabel("Temperature")
        self.ax.set_ylabel("Revenue")
        self.ax.set_title("Ice Cream Sales vs Temperature")
        self.ax.legend()
        self.canvas.draw()

    def show_about(self) -> None:
        from homework4_2.About1 import Aboutwindow

        self.about_window = Aboutwindow()
        self.about_window.show()


def main() -> None:
    app = QApplication(sys.argv)
    stylesheet = Path(__file__).with_name("style.qss").read_text(encoding="utf-8")
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
