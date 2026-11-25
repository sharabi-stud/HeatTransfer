from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QDoubleSpinBox, QSlider
)
from PySide6.QtCore import QTimer
from Body import Body
from GraphWindow import GraphWindow
from AboutWindow import AboutWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_window = GraphWindow(self)
        self.about_window = AboutWindow()

        self.body1 = None
        self.body2 = None
        self.dt = 0.1
        self.current_time = 0.0

        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setGeometry(100, 100, 600, 400)

        self.left_temp_slider = QSlider(self)
        self.left_temp_slider.setGeometry(40, 40, 30, 160)
        self.left_temp_slider.setRange(0, 200)
        self.left_temp_slider.setValue(200)
        self.left_temp_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_box = QLabel("", self)
        self.left_body_box.setGeometry(90, 40, 110, 160)
        self.left_body_box.setStyleSheet("background-color: rgb(255, 0, 0);")

        self.conductivity_label = QLabel("Conductivity", self)
        self.conductivity_label.setGeometry(260, 40, 100, 25)

        self.conductivity_spinbox = QDoubleSpinBox(self)
        self.conductivity_spinbox.setGeometry(240, 70, 120, 30)
        self.conductivity_spinbox.setRange(0.01, 100.0)
        self.conductivity_spinbox.setValue(1.00)
        self.conductivity_spinbox.setSuffix(" J/s°C")

        self.bridge_bar = QLabel("", self)
        self.bridge_bar.setGeometry(200, 115, 200, 30)
        self.bridge_bar.setStyleSheet("background-color: darkgray;")

        self.right_body_box = QLabel("", self)
        self.right_body_box.setGeometry(400, 40, 110, 160)
        self.right_body_box.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.right_temp_slider = QSlider(self)
        self.right_temp_slider.setGeometry(530, 40, 30, 160)
        self.right_temp_slider.setRange(0, 200)
        self.right_temp_slider.setValue(0)
        self.right_temp_slider.valueChanged.connect(self.right_temperature_changed)

        self.left_temp_text = QLabel("Temp.", self)
        self.left_temp_text.setGeometry(30, 230, 55, 30)

        self.left_temp_display = QLabel("200.0 °C", self)
        self.left_temp_display.setGeometry(90, 230, 110, 30)
        self.left_temp_display.setStyleSheet("background-color: lightgray; border: 1px solid gray;")

        self.left_mass_text = QLabel("Mass", self)
        self.left_mass_text.setGeometry(30, 275, 55, 30)

        self.left_mass_spinbox = QDoubleSpinBox(self)
        self.left_mass_spinbox.setGeometry(90, 275, 110, 30)
        self.left_mass_spinbox.setRange(0.01, 1000.0)
        self.left_mass_spinbox.setValue(10.00)
        self.left_mass_spinbox.setSuffix(" kg")

        self.left_hcap_text = QLabel("H. Cap.", self)
        self.left_hcap_text.setGeometry(30, 320, 55, 30)

        self.left_hcap_spinbox = QDoubleSpinBox(self)
        self.left_hcap_spinbox.setGeometry(90, 320, 110, 30)
        self.left_hcap_spinbox.setRange(0.01, 100.0)
        self.left_hcap_spinbox.setValue(0.40)
        self.left_hcap_spinbox.setSuffix(" J/kg°C")

        self.start_stop_button = QPushButton("Start", self)
        self.start_stop_button.setGeometry(245, 230, 110, 45)
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
        self.start_stop_button.clicked.connect(self.start_stop_button_method)

        self.graphs_button = QPushButton("Graphs", self)
        self.graphs_button.setGeometry(245, 285, 110, 40)
        self.graphs_button.clicked.connect(self.open_graph_window)

        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(245, 335, 110, 35)
        self.about_button.clicked.connect(self.open_about_window)

        self.right_temp_display = QLabel("0.0 °C", self)
        self.right_temp_display.setGeometry(400, 230, 110, 30)
        self.right_temp_display.setStyleSheet("background-color: lightgray; border: 1px solid gray;")

        self.right_temp_text = QLabel("Temp.", self)
        self.right_temp_text.setGeometry(520, 230, 55, 30)

        self.right_mass_spinbox = QDoubleSpinBox(self)
        self.right_mass_spinbox.setGeometry(400, 275, 110, 30)
        self.right_mass_spinbox.setRange(0.01, 1000.0)
        self.right_mass_spinbox.setValue(10.00)
        self.right_mass_spinbox.setSuffix(" kg")

        self.right_mass_text = QLabel("Mass", self)
        self.right_mass_text.setGeometry(520, 275, 55, 30)

        self.right_hcap_spinbox = QDoubleSpinBox(self)
        self.right_hcap_spinbox.setGeometry(400, 320, 110, 30)
        self.right_hcap_spinbox.setRange(0.01, 100.0)
        self.right_hcap_spinbox.setValue(0.40)
        self.right_hcap_spinbox.setSuffix(" J/kg°C")

        self.right_hcap_text = QLabel("H. Cap.", self)
        self.right_hcap_text.setGeometry(520, 320, 55, 30)

    def get_red_color(self, temp):
        red = int((temp / 200.0) * 255)
        if red > 255:
            red = 255
        if red < 0:
            red = 0
        return f"background-color: rgb({red}, 0, 0);"

    def left_temperature_changed(self):
        temp = self.left_temp_slider.value()
        self.left_temp_display.setText(f"{temp:.1f} °C")
        self.left_body_box.setStyleSheet(self.get_red_color(temp))

    def right_temperature_changed(self):
        temp = self.right_temp_slider.value()
        self.right_temp_display.setText(f"{temp:.1f} °C")
        self.right_body_box.setStyleSheet(self.get_red_color(temp))

    def start_stop_button_method(self):
        if self.start_stop_button.isChecked():
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")

            t1 = float(self.left_temp_slider.value())
            t2 = float(self.right_temp_slider.value())
            m1 = self.left_mass_spinbox.value()
            m2 = self.right_mass_spinbox.value()
            c1 = self.left_hcap_spinbox.value()
            c2 = self.right_hcap_spinbox.value()

            self.body1 = Body(m1, c1, t1)
            self.body2 = Body(m2, c2, t2)

            self.current_time = 0.0
            self.time_history = [0.0]
            self.body1_temp_history = [t1]
            self.body2_temp_history = [t2]

            self.timer.start()
        else:
            self.timer.stop()
            self.start_stop_button.setText("Start")
            self.start_stop_button.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")

    def timer_method(self):
        sigma = self.conductivity_spinbox.value()
        t1 = self.body1.temperature
        t2 = self.body2.temperature

        i1 = sigma * (t2 - t1)
        i2 = sigma * (t1 - t2)

        dq1 = i1 * self.dt
        dq2 = i2 * self.dt

        new_t1 = self.body1.add_heat(dq1)
        new_t2 = self.body2.add_heat(dq2)

        self.current_time = self.current_time + self.dt
        self.time_history.append(self.current_time)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        self.left_temp_slider.setValue(int(round(new_t1)))
        self.left_temp_display.setText(f"{new_t1:.1f} °C")
        self.left_body_box.setStyleSheet(self.get_red_color(new_t1))

        self.right_temp_slider.setValue(int(round(new_t2)))
        self.right_temp_display.setText(f"{new_t2:.1f} °C")
        self.right_body_box.setStyleSheet(self.get_red_color(new_t2))

    def open_graph_window(self):
        self.graph_window.show()

    def open_about_window(self):
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()