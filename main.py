#!/usr/bin/python2.7
import pygtk
pygtk.require('2.0')
import gtk

from appwindow import AppWindow

win = AppWindow()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()