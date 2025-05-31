from pynput import keyboard
import threading
import time
import pyttsx3
import fitz 
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt , QTimer
from PyQt5.QtGui import QIcon


#an real time typing speed calculator which always in the top layer

app = QApplication(sys.argv)
app.setStyle('Fusion')

typed_char = 0
pre = 0
typed_word = 0
backspace = 0

class TypingSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_time = None or 0
        self.text = ""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

        self.listener_thread = threading.Thread(target=self.start_listener, daemon=True) 
        self.listener_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle('Typing Tracker')
        self.setGeometry(100, 100, 120, 60)
        self.setWindowIcon(QIcon(r"C:\Users\ASUS\Documents\Python project\Typing_Tracker\computer-keyboard.png"))
        self.setFixedSize(120,60)
        self.setStyleSheet("background-color: #f0f0f0; color: #1c1e33; font-size: 12px;")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint )
        self.setWindowOpacity(0.7)

        layout = QVBoxLayout()

        self.speed_label = QLabel("Speed: 0 WPM")
        layout.addWidget(self.speed_label)

        self.accuracy_label = QLabel("Accuracy: 0% ")
        layout.addWidget(self.accuracy_label)

        self.setLayout(layout)

    def on_text_changed(self,key):
        
        global typed_char,pre,typed_word,backspace

        try:
            if not self.start_time:
                self.start_time = time.time()
            if key == keyboard.Key.space:
                typed_word += 1
                pre = 1
            if key == keyboard.Key.backspace:
                if pre == 1:
                    typed_word -= 1
                    typed_char -= 1
                    backspace += 1
                    pre = 0
            if key.char.isalpha() or key.char.isdigit(): 
                typed_char += 1
        except AttributeError:
            pass

    def update_speed(self):
        elapsed_time = time.time() - self.start_time
        words = typed_word
        char = typed_char
        back = backspace
        speed = (words / elapsed_time) * 60 if elapsed_time > 0 else 0
        accuracy = (int(char) - int(back)) / int(char) * 100 if typed_char > 0 else 0

        self.accuracy_label.setText(f"Accuracy: {accuracy:.2f}%")
        self.speed_label.setText(f"Speed: {int(speed)} WPM")
        

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_text_changed) as listener:
            listener.join()

    def closeEvent(self, event):
        self.engine.stop() # Stop the text-to-speech engine
        event.accept() # Accept the close event
    
def main():
    global app
    typing_speed_calculator = TypingSpeedCalculator()
    typing_speed_calculator.show()
    sys.exit(app.exec_()) 
if __name__ == '__main__':
    main()
# This code creates a real-time typing speed calculator using PyQt5 and pynput.
