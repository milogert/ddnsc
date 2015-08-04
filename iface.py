#!/usr/bin/python2

from kivy.app import App
from kivy.uix.widget import Widget

class MainWindow(Widget):
  pass

class MyApp(App):
  def build(self):
    return MainWindow()

if __name__ == '__main__':
  MyApp().run()