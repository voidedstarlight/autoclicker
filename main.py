# -*- coding: utf-8 -*-
from pynput.mouse import Controller, Listener, Button
from pynput import keyboard

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import random

double_click = False
scroll_click = False
scroll_button = Button.right
multiplier_chance = 4


def toggleScrollButton():
	global scroll_button
	scroll_button = (Button.right if scroll_button == Button.left else Button.left)


def changeMultiplierChance():
	global multiplier_chance
	if multiplier_chance == 4:
		multiplier_chance = 1
	else:
		multiplier_chance += 1


class ToggleButton(QPushButton):
	def __init__(self, text, parent):
		super(ToggleButton, self).__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet("ToggleButton { border: none; background-color: #EEE; padding: 5px; } ToggleButton:hover { background-color: #DDD }")
		self.adjustSize()
		

class TextWidgetHorizontalCombo(QGroupBox):
	def __init__(self, parent, widget, text="", label_width_percent=0.3, widget_width_percent=0.7):
		super(TextWidgetHorizontalCombo, self).__init__(parent=parent)
		self.setLayout(QHBoxLayout())
		self.label = QLabel(text, self)
		self.widget = widget
		self.label_width_percent = label_width_percent
		self.widget_width_percent = widget_width_percent
		self.layout().addWidget(self.label)
		self.layout().addWidget(widget)
	
	def resizeEvent(self, event) -> None:
		self.label.resize(QSize(int(event.size().width() * self.label_width_percent // 1), event.size().height()))
		self.widget.resize(QSize(int(event.size().width() * self.widget_width_percent // 1), event.size().height()))
		super(TextWidgetHorizontalCombo, self).resizeEvent(event)


class KeyEdit(QLineEdit):
	def __init__(self, parent):
		super(KeyEdit, self).__init__(parent=parent)
	
	def keyPressEvent(self, event: QKeyEvent):
		key_int = event.key()
		key = Qt.Key(key_int)
		
		if key == Qt.Key_Escape or key == Qt.Key_Backspace:
			self.setText("")
			return
		
		modifiers: Qt.KeyboardModifiers = event.modifiers()
		
		print(modifiers & Qt.MetaModifier)
		
		# if modifiers.testFlag(Qt.NoModifier):
		# 	return
		# if modifiers.testFlag(Qt.ShiftModifier):
		# 	key_int += Qt.SHIF
		# if modifiers.testFlag(Qt.ControlModifier):
		# 	key_int += Qt.CTRL
		# if modifiers.testFlag(Qt.AltModifier):
		# 	key_int += Qt.AL
		#
		# self.setText(QKeySequence(key_int).toString(QKeySequence.NativeText))


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.setStyleSheet("background-color: white; border: none;")
		self.setMinimumSize(QSize(768, 768))
		self.mouse_listener = Listener(on_scroll=on_scroll, on_click=on_click)
		self.mouse_listener.start()
		self.keyboard_listener = keyboard.Listener(on_press=on_press)
		self.keyboard_listener.start()
		
		def toggleScroll():
			global scroll_click
			scroll_click = not scroll_click
			self.scroll_click_toggle.setText("Scroll: " + ("Off", "On")[scroll_click])
		
		def toggleDouble():
			global double_click
			double_click = not double_click
			self.double_click_toggle.setText("Multiplier: " + ("Off", "On")[double_click])
		
		self.scroll_click_column = QGroupBox(self)
		self.scroll_click_column.setLayout(QVBoxLayout())
		
		self.double_click_column = QGroupBox(self)
		self.double_click_column.setLayout(QVBoxLayout())
		
		self.fixed_click_column = QGroupBox(self)
		self.fixed_click_column.setLayout(QVBoxLayout())

		self.scroll_click_toggle = ToggleButton("Scroll: Off", self.scroll_click_column)
		self.scroll_click_toggle.pressed.connect(toggleScroll)
		self.scroll_button = ToggleButton("Right Button", self.scroll_click_column)
		self.scroll_button.pressed.connect(lambda self=self: [toggleScrollButton(), self.scroll_button.setText(("Right" if scroll_button == Button.right else "Left") + " Button")])
		self.scroll_click_column.layout().addWidget(self.scroll_click_toggle)
		self.scroll_click_column.layout().addWidget(self.scroll_button)
		
		self.double_click_toggle = ToggleButton("Multiplier: Off", self.double_click_column)
		self.double_click_toggle.pressed.connect(toggleDouble)
		self.double_click_chance = ToggleButton("Chance: 100%", self.double_click_column)
		self.double_click_chance.pressed.connect(lambda self=self: [changeMultiplierChance(), self.double_click_chance.setText(f"Chance: {multiplier_chance * 25}%")])
		self.double_click_column.layout().addWidget(self.double_click_toggle)
		self.double_click_column.layout().addWidget(self.double_click_chance)
		
		self.fixed_click_keystroke = TextWidgetHorizontalCombo(self.fixed_click_column, KeyEdit(self.fixed_click_column), "Keystroke")
		self.fixed_click_amount = TextWidgetHorizontalCombo(self.fixed_click_column, QLineEdit(self.fixed_click_column), "Amount")
		self.fixed_click_variation = TextWidgetHorizontalCombo(self.fixed_click_column, QLineEdit(self.fixed_click_column), "Variation")
		self.fixed_click_column.layout().addWidget(self.fixed_click_keystroke)
		self.fixed_click_column.layout().addWidget(self.fixed_click_amount)
		self.fixed_click_column.layout().addWidget(self.fixed_click_variation)
		
		self.scroll_click_column.layout().addStretch()
		self.double_click_column.layout().addStretch()
		self.fixed_click_column.layout().addStretch()
		self.show()
	
	def resizeEvent(self, event: QResizeEvent):
		self.scroll_click_column.resize(QSize(event.size().width() // 2, event.size().height() // 2))
		self.double_click_column.resize(QSize(event.size().width() // 2, event.size().height() // 2))
		self.double_click_column.move(QPoint(event.size().width() // 2, 0))
		self.fixed_click_column.resize(QSize(event.size().width(), event.size().height() // 2))
		self.fixed_click_column.move(QPoint(0, event.size().height() // 2))
		super(Window, self).resizeEvent(event)


controller = Controller()

doubling = False


def on_press(key):
	if key == keyboard.Key.shift_r:
		toggleScrollButton()


def on_click(_, __, button, pressed):
	if not pressed and double_click and random.choices([True, False], [multiplier_chance * 25, 100 - (multiplier_chance * 25)])[0]:
		global doubling
		if doubling:
			doubling = False
		else:
			doubling = True
			controller.press(button)
			controller.release(button)


def on_scroll(*_):
	if scroll_click:
		controller.press(scroll_button)
		controller.release(scroll_button)


application, window = QApplication([]), Window()
application.exec_()
