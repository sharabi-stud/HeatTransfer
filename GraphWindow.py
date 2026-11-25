import os
import sys
import subprocess
from PySide6.QtWidgets import QWidget, QComboBox, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.setGeometry(150, 150, 620, 420)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(15, 15, 420, 390)

        self.ax = self.figure.add_subplot(111)
        self.format_axes()

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(455, 30, 140, 35)
        self.body_combo.addItem("Body 1")
        self.body_combo.addItem("Body 2")

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(455, 80, 140, 40)
        self.draw_button.clicked.connect(self.draw_graph)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(455, 135, 140, 40)
        self.clear_button.clicked.connect(self.clear_graph)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(455, 190, 140, 40)
        self.export_button.clicked.connect(self.export_csv)

    def format_axes(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_graph(self):
        if len(self.main_window.time_history) == 0:
            return

        selected = self.body_combo.currentText()
        if selected == "Body 1":
            self.ax.plot(
                self.main_window.time_history,
                self.main_window.body1_temp_history,
                color="red",
                label="Body 1"
            )
        else:
            self.ax.plot(
                self.main_window.time_history,
                self.main_window.body2_temp_history,
                color="blue",
                label="Body 2"
            )

        self.ax.legend()
        self.format_axes()

    def clear_graph(self):
        self.ax.clear()
        self.format_axes()

    def export_csv(self):
        if len(self.main_window.time_history) == 0:
            return

        file_name = "heat_transfer_data.csv"
        f = open(file_name, "w")
        f.write("Time (s),Temperature 1 (C),Temperature 2 (C)\n")
        for i in range(len(self.main_window.time_history)):
            t = self.main_window.time_history[i]
            t1 = self.main_window.body1_temp_history[i]
            t2 = self.main_window.body2_temp_history[i]
            f.write(f"{t:.2f},{t1:.2f},{t2:.2f}\n")
        f.close()

        if sys.platform.startswith("win"):
            os.startfile(file_name)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", file_name])
        else:
            subprocess.call(["xdg-open", file_name])