import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os

import fcntl
import subprocess

OFLAGS = None

def set_nonblocking(file_handle):
    """Make a file_handle non-blocking."""
    global OFLAGS
    OFLAGS = fcntl.fcntl(file_handle, fcntl.F_GETFL)
    nflags = OFLAGS | os.O_NONBLOCK
    fcntl.fcntl(file_handle, fcntl.F_SETFL, nflags)

class LogPanel(gtk.ScrolledWindow):
	def __init__(self):
		gtk.ScrolledWindow.__init__(self)
		self.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
		self.text_view = gtk.TextView()
		self.text_view.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.add(self.text_view)
		self.buffer = gtk.TextBuffer()
		self.text_view.set_buffer(self.buffer)
		self.fd = None

	def log(self, text):
		self.buffer.insert(self.buffer.get_end_iter(), text)
		self.text_view.scroll_to_iter(self.buffer.get_end_iter(), 0, False, 0, 0)

	def begin_execute(self, command):
		print(command)
		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		self.fd = process.stdout
		gobject.io_add_watch(self.fd.fileno(), gobject.IO_IN, self.on_tail)

	def begin_tail(self, file):
		self.fd = open(file, 'rt');
		set_nonblocking(self.fd.fileno())
		gobject.io_add_watch(self.fd.fileno(), gobject.IO_IN, self.on_tail)

	def on_tail(self, source, condition):
		str = os.read(source,1024*5)
		self.log(str)
		if len(str) == 0:
			return False
		else:
			return True
