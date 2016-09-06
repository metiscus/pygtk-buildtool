import pygtk
pygtk.require('2.0')
import gtk

from build_tab import BuildTab
from log_panel import LogPanel

class AppWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title("Build Studio")
		
		self.panes = gtk.HPaned()
		self.tabs = {}
		self.tab_objs = {}

		# Right pane contains sets of logs
		self.right_pane = gtk.Notebook();
		self.system_log_panel = LogPanel()
		self.right_pane.append_page(self.system_log_panel, gtk.Label("System Log"))

		self.panes.add2(self.right_pane)

		# Left pane contains sets of buttons
		self.left_pane  = gtk.Notebook()
		self.left_pane.append_page(BuildTab(self), gtk.Label("Build"))
		self.panes.add1(self.left_pane)

		self.add(self.panes)

	def log(self, text):
		self.system_log_panel.log(text)

	def add_task(self, task):
		if self.tabs.has_key(task) == False:
			self.tab_objs[task] = LogPanel()
			self.tabs[task] = self.right_pane.insert_page(self.tab_objs[task], gtk.Label(task), -1)

	def activate_task(self, task):
		if self.tabs.has_key(task):
			self.right_pane.set_current_page(self.tabs[task])
			self.tab_objs[task].begin_tail('/tmp/the_log')

	def activate_task_exec(self, task, cmd):
		if self.tabs.has_key(task):
			self.right_pane.set_current_page(self.tabs[task])
			self.tab_objs[task].begin_execute(cmd)