import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

# Function to display the notification
def show_notification():
    notification = QMessageBox()
    notification.setIcon(QMessageBox.Information)
    notification.setWindowTitle("Rest Your Eyes")
    notification.setText("It's time to rest your eyes.")
    notification.setStandardButtons(QMessageBox.Ok)
    notification.setWindowFlags(Qt.WindowStaysOnTopHint)  # This will keep the window on top
    notification.exec_()

# Create the Qt application
app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)

# Create the context menu for the system tray icon
menu = QMenu()
exit_action = QAction("Exit", menu)
exit_action.triggered.connect(app.quit)
menu.addAction(exit_action)

# Set the context menu for the system tray icon
tray_icon.setContextMenu(menu)

# Set a timer to display the notification every 15 minutes
timer = QTimer()
timer.timeout.connect(show_notification)
timer.start(5 * 1000)  # 15 minutes in milliseconds
# timer.start(15 * 60 * 1000)  # 15 minutes in milliseconds

# Show the system tray icon
tray_icon.show()

# Start the Qt event loop
sys.exit(app.exec_())

