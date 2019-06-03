import ctypes
import sys
import time
import yaml

from ui_mainwindow import *
from ui_handler import UI_Handler
    
def main():
    # Display the UI
    MainWindow.show()

    # Exit the program
    sys.exit(app.exec_())

if __name__ == "__main__":
    # This is added to fix the App Icon not appearing in Taskbar
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Load config
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Initialized UI
    app_icon = config["icon_path"]
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(app_icon))

    MainWindow = QtWidgets.QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Initialize UI event handlers
    ui_handler = UI_Handler(ui, MainWindow, config)

    # Attach UI elements to event handlers
    ui.timerEnabled.stateChanged.connect(lambda: ui_handler.enable_timer(ui.timerEnabled))
    ui.randomMovementEnabled.stateChanged.connect(lambda: ui_handler.enable_random_movement(ui.randomMovementEnabled))
    ui.randomDelayEnabled.stateChanged.connect(lambda: ui_handler.enable_random_delay(ui.randomDelayEnabled))
    ui.minimizeToTrayEnabled.stateChanged.connect(lambda: ui_handler.enable_tray_minimize(ui.minimizeToTrayEnabled))
    ui.startButton.clicked.connect(lambda: ui_handler.start_mouse_movement(ui.startButton))
    # ui.stopButton.clicked.connect(lambda: ui_handler.stop_mouse_movement(ui.stopButton))
    ui.stopButton.clicked.connect(ui_handler.stop_mouse_movement)

    # Start the app
    main()