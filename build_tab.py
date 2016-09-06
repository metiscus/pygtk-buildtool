import pygtk
pygtk.require('2.0')
import gtk

class BuildButton(gtk.Button):
	def __init__(self, label_txt):
		gtk.Button.__init__(self, label=label_txt)
		self.label = label_txt
		self.cmd = ""


class BuildTab(gtk.VButtonBox):
	def __init__(self, appwindow):
		gtk.VButtonBox.__init__(self)

		self.appwindow = appwindow
		self.set_layout(gtk.BUTTONBOX_START)

		# Clean
		self.clean_button = BuildButton("Clean")
		self.clean_button.connect("clicked", self.on_event)
		self.clean_button.cmd = ["make clean"]
		self.add(self.clean_button)
		self.appwindow.add_task("Clean")

		# Build
		self.build_button = BuildButton("Build")
		self.build_button.connect("clicked", self.on_event)
		self.build_button.cmd = ["make"]
		self.add(self.build_button)
		self.appwindow.add_task("Build")

		# Rebuild
		self.rebuild_button = BuildButton("Rebuild")
		self.rebuild_button.connect("clicked", self.on_event)
		self.rebuild_button.cmd = ["make clean && make"]
		self.add(self.rebuild_button)
		self.appwindow.add_task("Rebuild")

		self.add(gtk.HSeparator())

	def on_event(self, widget):
		string = "Event: " + widget.label + "\n";
		self.appwindow.log(string)
		if(widget.cmd != None):
			self.appwindow.activate_task_exec(widget.label, widget.cmd)
		else:
			self.appwindow.activate_task(widget.label)