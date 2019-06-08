from mouse_handler import Mouse_Handler
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, qApp, QMenu
from PyQt5.QtGui import QIcon


class UI_Input:
    def __init__(self, config):
        # Construct UI input object to be pass to mouse_handler
        self.delay = config["mouse_movement"]["delay"]
        self.offset = config["mouse_movement"]["offset"]
        self.random_movement_enabled = False
        self.random_delay_enabled = False
        self.random_movement = [
            config["mouse_movement"]["min_random_movement"],
            config["mouse_movement"]["max_random_movement"]
        ]
        self.random_delay = [
            config["mouse_movement"]["min_random_delay"],
            config["mouse_movement"]["max_random_delay"]
        ]
        self.timer_enabled = False
        self.timer_Hour = 0
        self.timer_Minute = 0
        self.timer_Second = 0


class UI_Handler:
    def __init__(self, ui, MainWindow, config):
        # Initialize input value
        self.ui = ui
        self.timer_enabled = False
        self.random_movement_enabled = False
        self.random_delay_enabled = False
        self.tray_minimize_enabled = False
        self.mouse_handler = Mouse_Handler()
        self.ui_input = UI_Input(config)

        # Iinitialize minimize to tray handler
        self.MainWindow = MainWindow
        self.MainWindow.closeEvent = self.closeEvent
        self.tray_icon = QSystemTrayIcon(self.MainWindow)
        self.tray_icon.setIcon(QIcon('resource/256x256.png'))
        show_action = QAction("Restore", self.MainWindow)
        quit_action = QAction("Exit", self.MainWindow)
        show_action.triggered.connect(self.MainWindow.show)
        quit_action.triggered.connect(qApp.quit)
        quit_action.triggered.connect(self.tray_icon.hide)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.MainWindow.show)

    def enable_timer(self, element):
        # Enable timer
        if element.isChecked():
            self.timer_enabled = True
            self.ui.timerHour.setEnabled(True)
            self.ui.timerMinute.setEnabled(True)
            self.ui.timerSecond.setEnabled(True)
        else:
            self.timer_enabled = False
            self.ui.timerHour.setEnabled(False)
            self.ui.timerMinute.setEnabled(False)
            self.ui.timerSecond.setEnabled(False)

        self.ui_input.timer_enabled = self.timer_enabled

    def enable_random_movement(self, element):
        # Enable random movement
        if element.isChecked():
            self.random_movement_enabled = True
        else:
            self.random_movement_enabled = False

        self.ui_input.random_movement_enabled = self.random_movement_enabled

    def enable_random_delay(self, element):
        # Enable random delay interval between each movement
        if element.isChecked():
            self.random_delay_enabled = True
        else:
            self.random_delay_enabled = False
        
        self.ui_input.random_delay_enabled = self.random_delay_enabled

    def enable_tray_minimize(self, element):
        # Enable the program to be minimize to system tray
        if element.isChecked():
            self.tray_minimize_enabled = True
        else:
            self.tray_minimize_enabled = False
        
    def start_mouse_movement(self, element):
        # Start mouse movement
        element.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.enable_settings_input(False)

        self.mouse_handler.start_mouse_movement(self.ui_input)

        if self.timer_enabled:
            self.get_timer_values()
            self.start_timer()
    
    def stop_mouse_movement(self):
        # Stop mouse movement
        self.ui.stopButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)
        self.enable_settings_input(True)

        self.mouse_handler.stop_mouse_movement()
        self.ui.currentTimerValue.setText("00:00:00")
    
    def start_timer(self):
        # Convert the timer inputs to seconds
        total_time = (self.ui_input.timer_Hour * 60 * 60) + \
            (self.ui_input.timer_Minute * 60) + (self.ui_input.timer_Second)
        self.mouse_handler.start_timer(total_time, self)
    
    def enable_settings_input(self, state):
        """
        Enable or disable all the settings input
        This will be call when the user press "Start" or "Stop" button
        """
        self.ui.timerEnabled.setEnabled(state)
        if state is True:
            if self.ui.timerEnabled.isChecked():
                self.ui.timerHour.setEnabled(True)
                self.ui.timerMinute.setEnabled(True)
                self.ui.timerSecond.setEnabled(True)
            else:
                self.ui.timerHour.setEnabled(False)
                self.ui.timerMinute.setEnabled(False)
                self.ui.timerSecond.setEnabled(False)
        else:
            self.ui.timerHour.setEnabled(state)
            self.ui.timerMinute.setEnabled(state)
            self.ui.timerSecond.setEnabled(state)
        self.ui.randomMovementEnabled.setEnabled(state)
        self.ui.randomDelayEnabled.setEnabled(state)
    
    def get_timer_values(self):
        # Get the input value from the timer field
        if(self.ui.timerHour.text() != ''):
            self.ui_input.timer_Hour = int(self.ui.timerHour.text())
        else:
            self.ui_input.timer_Hour = 0
        
        if(self.ui.timerMinute.text() != ''):
            self.ui_input.timer_Minute = int(self.ui.timerMinute.text())
        else:
            self.ui_input.timer_Minute = 0
        
        if(self.ui.timerSecond.text() != ''):
            self.ui_input.timer_Second = int(self.ui.timerSecond.text())
        else:
            self.ui_input.timer_Second = 0
    
    def closeEvent(self, event):
        # Will trigger when user pressed close button on the UI window
        if self.tray_minimize_enabled:
            event.ignore()
            self.MainWindow.hide()
            # self.tray_icon.showMessage(
            #     "Mouse Mover",
            #     "Minimized to tray",
            #     QSystemTrayIcon.Information,
            #     2000
            # )
        else:
            self.stop_mouse_movement()
            self.tray_icon.hide()
