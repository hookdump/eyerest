import sys
import json
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QAction,
                             QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

settings_file = 'settings.json'

# Load settings from JSON file
def load_settings():
    try:
        with open(settings_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'frequency': 15}

# Save settings to JSON file
def save_settings(settings):
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

# Function to display the notification
def show_notification():
    tray_icon.showMessage("Rest Your Eyes", "It's time to rest your eyes.", QSystemTrayIcon.Warning, 10000)

# Function to show the settings window
def show_settings():
    settings = load_settings()
    dialog = QDialog()
    dialog.setWindowTitle("Settings")
    layout = QVBoxLayout()

    label = QLabel("Notification Frequency (minutes):")
    layout.addWidget(label)

    spinbox = QSpinBox()
    spinbox.setRange(1, 60)
    spinbox.setValue(settings.get('frequency', 15))
    layout.addWidget(spinbox)

    save_button = QPushButton("Save")
    def on_save():
        settings['frequency'] = spinbox.value()
        save_settings(settings)
        timer.start(settings['frequency'] * 60 * 1000)
        tray_icon.showMessage("Settings Saved", "Notification frequency updated.", QSystemTrayIcon.Information, 5000)
        # Update the current frequency action text
        current_freq_action.setText(f"Current Frequency: {settings['frequency']} minutes")
        dialog.close()
    save_button.clicked.connect(on_save)
    layout.addWidget(save_button)

    dialog.setLayout(layout)
    dialog.exec_()

# Create the Qt application
app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)

# Create the context menu for the system tray icon
menu = QMenu()

# Global variable for the current frequency action
current_freq_action = QAction(menu)

# Add the current frequency action to the menu
menu.addAction(current_freq_action)

settings_action = QAction("Settings", menu)
settings_action.triggered.connect(show_settings)
menu.addAction(settings_action)

exit_action = QAction("Exit", menu)
exit_action.triggered.connect(app.quit)
menu.addAction(exit_action)

# Set the context menu for the system tray icon
tray_icon.setContextMenu(menu)

# Set a timer to display the notification
timer = QTimer()
timer.timeout.connect(show_notification)
settings = load_settings()

# Set the initial text for current frequency action
current_freq_action.setText(f"Current Frequency: {settings.get('frequency', 15)} minutes")
timer.start(settings.get('frequency', 15) * 60 * 1000)

# Show the system tray icon
tray_icon.show()

# Show notification immediately on application start (for testing purposes)
show_notification()

# Start the Qt event loop
sys.exit(app.exec_())

