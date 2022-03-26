from pynput.mouse import Controller, Listener, Button
from pynput import keyboard

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


double_click = False
scroll_click = False


class ToggleButton(QPushButton):
	def __init__(self, text, parent):
		super(ToggleButton, self).__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet("ToggleButton { border: none; background-color: #EEE; padding: 5px; } ToggleButton:hover { background-color: #DDD }")
		self.adjustSize()


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.setStyleSheet("background-color: white;")
		self.setMinimumSize(QSize(768, 768))
		self.mouse_listener = Listener(on_scroll=on_scroll, on_click=on_click)
		self.mouse_listener.start()
		self.keyboard_listener = keyboard.Listener(on_press=on_press)
		self.keyboard_listener.start()
		
		def toggleScroll():
			global scroll_click
			scroll_click = not scroll_click
			self.scroll_click_toggle.setText("Scroll Click: " + ("Off", "On")[scroll_click])
		
		def toggleDouble():
			global double_click
			double_click = not double_click
			self.double_click_toggle.setText("Double Click: " + ("Off", "On")[double_click])

		self.scroll_click_column = QGroupBox(self)
		self.scroll_click_column.setLayout(QVBoxLayout())
		
		self.double_click_column = QGroupBox(self)
		self.double_click_column.setLayout(QVBoxLayout())

		self.scroll_click_toggle = ToggleButton("Scroll Click: Off", self.scroll_click_column)
		self.scroll_click_toggle.pressed.connect(toggleScroll)
		self.scroll_click_column.layout().addWidget(self.scroll_click_toggle)
		
		self.double_click_toggle = ToggleButton("Double Click: Off", self.double_click_column)
		self.double_click_toggle.pressed.connect(toggleDouble)
		self.double_click_column.layout().addWidget(self.double_click_toggle)
		
		self.scroll_click_column.layout().addStretch()
		self.double_click_column.layout().addStretch()
		self.show()
	
	def resizeEvent(self, event):
		self.scroll_click_column.resize(QSize(event.size().width() // 2, event.size().height()))
		self.double_click_column.resize(QSize(event.size().width() // 2, event.size().height()))
		self.double_click_column.move(QPoint(event.size().width() // 2, 0))
		super(Window, self).resizeEvent(event)


controller = Controller()

shift_pressed = False
doubling = False


def on_press(key):
	if key == keyboard.Key.shift_r:
		global shift_pressed
		shift_pressed = not shift_pressed


def on_click(_, __, button, pressed):
	if not pressed and double_click:
		global doubling
		if doubling:
			doubling = False
		else:
			doubling = True
			controller.press(button)
			controller.release(button)


def on_scroll(*_):
	if scroll_click:
		if not shift_pressed:
			controller.press(Button.right)
			controller.release(Button.right)
		else:
			controller.press(Button.left)
			controller.release(Button.left)


application, window = QApplication([]), Window()
application.exec_()
