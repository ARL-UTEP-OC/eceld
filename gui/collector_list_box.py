import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from utils.css_provider import CssProvider
from utils.collector_action import Action
import engine.collector
import definitions
import os

class CollectorListBox(Gtk.ListBox):

    def __init__(self, engine, main_gui):
        super(CollectorListBox,self).__init__()

        self.engine = engine
        self.numCollectors = self.engine.get_collector_length()
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.attached_gui = main_gui
        self.css = CssProvider("widget_styles.css")

        self.collectorStatus = {}

        self.connect("row-selected",self.update_row_colors)
        self.connect("row-activated",self.row_activated_handler)
        # Enable multiple collector selection when CTRL + left click occurs (selection mode == MULTIPLE)
        self.connect("key-press-event",self.enable_multiple)
        # List box updates collector rows on up/down arrow/tab key presses.
        self.connect("key-release-event",self.key_release_handler)

        for i, collector in enumerate(self.engine.collectors):
            self.add(self.create_collector_row(collector))
            self.collectorStatus[collector.name] = False

    # Collector List Box enables mutliple selection on CTRL + left click
    def enable_multiple(self, lBox, event):
        # modifiers = Gtk.accelerator_get_default_mod_mask()
        # print "Entering Enable multiple"

        #print "Event state and modifiers", event.state & modifiers
        ###Was not working for control###
        '''if(event.button == Gdk.BUTTON_PRIMARY and  ((event.state & modifiers) == Gdk.ModifierType.CONTROL_MASK)):
            print "CTRL was pressed"
            self.set_selection_mode(Gtk.SelectionMode.MULTIPLE)'''

        if(Gdk.keyval_name(event.keyval) == 'Shift_L' or Gdk.keyval_name(event.keyval) == 'Shift_R'):
				print("Shift was pressed.")
				
				if(self.get_selection_mode() == Gtk.SelectionMode.MULTIPLE):
					self.disconnect_by_func(self.re_enable_single)
				else:
					lBox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
				# print self.get_selection_mode()
				# lBox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
				print("MULTIPLE selection is activated")
				current_selected_collector = self.get_selected_row().get_name()
				self.collectorStatus[current_selected_collector] = True


    # Left pane responds to up/down arrow and tab key presses
    def key_release_handler(self, listBox, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        reactivate_single = (event.state & modifiers) != Gdk.ModifierType.SHIFT_MASK if os.name == "nt" else (event.state & modifiers) == Gdk.ModifierType.SHIFT_MASK
       	print "event state:", event.state
       	print "modifiers:", modifiers

        print "Reactivate single:", reactivate_single

        if (Gdk.keyval_name(event.keyval) == 'Up' or Gdk.keyval_name(event.keyval) == 'Down' or Gdk.keyval_name(event.keyval) == 'Tab'):
            collector = self.engine.get_collector(self.get_selected_row().get_name())
            if(self.get_selection_mode() == Gtk.SelectionMode.SINGLE):
                self.attached_gui.create_config_window(event,collector)

        if(reactivate_single):
            # The next click will renable single selection
            print "activating single!!!!"
            self.connect("button-press-event",self.re_enable_single)

		# if(Gdk.keyval_name(event.keyval) == 'Shift_L' or Gdk.keyval_name(event.keyval) == 'Shift_R'):
		# 	print("Shift was released.")

        if(self.get_selection_mode() == Gtk.SelectionMode.SINGLE):
            collector = self.engine.get_collector(self.get_selected_row().get_name())
            self.attached_gui.create_config_window(event,collector)


    # When CTRL is released, the next left click resets the list box to single selection mode.
    def re_enable_single(self, lBox, event):
        if(event.button == Gdk.BUTTON_PRIMARY):
            rows = self.get_selected_rows()
            for lBoxRow in rows:
                self.collectorStatus[lBoxRow.get_name()] = False
            
        	self.disconnect_by_func(self.re_enable_single)
        	self.unselect_all()
        	self.set_selection_mode(Gtk.SelectionMode.SINGLE)

    # Create Gtk.ListBoxRow() with collector information
    def create_collector_row(self,collector):

        label = Gtk.Label()
        label.set_label(collector.name)

        row = Gtk.ListBoxRow()
        row_height = (definitions.MAIN_WINDOW_HEIGHT / self.numCollectors) / 3
        row.set_size_request(definitions.COLLECTOR_WIDGET_WIDTH,row_height)
        row.set_name(collector.name)

        box = Gtk.EventBox()
        box.add(label)
        box.connect("button-press-event",self.collector_listbox_handler,collector.name)

        row.add(box)
        row.get_style_context().add_class("listBoxRow")
        row.get_style_context().add_class("inactive-color")

        return row

    # Show options over collector row on right click, select collector and create config window on left click
    def collector_listbox_handler(self, eventBox, event, collectorName):
    	if(self.get_selection_mode() == Gtk.SelectionMode.MULTIPLE):
    		if(event.type == Gdk.EventType._2BUTTON_PRESS or event.type == Gdk.EventType._3BUTTON_PRESS):
	    		rows = self.get_selected_rows()
	        	for lBoxRow in rows:
	        		self.collectorStatus[lBoxRow.get_name()] = False
	        	self.unselect_all()
	        	self.toggle_clicked_row(self.last_selected_row)
	        	double_clicked_collector = self.engine.get_collector(self.last_selected_row.get_name())
	        	self.attached_gui.create_config_window(Gdk.Event(), double_clicked_collector)        	

        collector = self.engine.get_collector(collectorName)
        if(event.button == Gdk.BUTTON_SECONDARY): # right click
            self.show_collector_popup_menu(event,collector)

    # Toggle the clicked row if the selection mode is multiple
    def toggle_clicked_row(self, row):
        activate = not self.collectorStatus[row.get_name()]

        if(activate == True):
        	self.last_selected_row = row
        	self.select_row(row)
        if(activate == False):
            self.unselect_row(row)

        self.collectorStatus[row.get_name()] = activate
        self.update_row_colors(Gdk.Event(), row)

    # Return the Gtk.ListBoxRow() based on the its name (string)
    def get_row(self, name):
        row = filter(lambda r: r.get_name() == name, self.get_children())
        return row.pop()

    # Show the popup menu on right click
    def show_collector_popup_menu(self, event, collector):
        menu = Gtk.Menu()

        runItem = Gtk.MenuItem("Run " + collector.name)
        runItem.connect("activate", self.attached_gui.startIndividualCollector, collector)

        stopItem = Gtk.MenuItem("Stop " + collector.name)
        stopItem.connect("activate", self.attached_gui.stopIndividualCollector, collector)

        parseItem = Gtk.MenuItem("Parse " + collector.name + " data")
        parseItem.connect("activate", self.attached_gui.parser, collector)

        # manual collector should only be run by icon
        if (isinstance(collector, engine.collector.AutomaticCollector)):
            menu.append(runItem)
            menu.append(stopItem)

        menu.append(parseItem)

        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

        return True

    # Update background colors of collector rows based on isSelected()
    def update_row_colors(self, event, lBoxRow):
        self.foreach(self.update_row_color)

    # Helper for update_row_colors
    def update_row_color(self, row):
        if (row.is_selected()):
            row.get_style_context().add_class("active-color")
            row.get_style_context().remove_class("inactive-color")
        else:
            row.get_style_context().remove_class("active-color")
            row.get_style_context().add_class("inactive-color")

    # Runs when a Gtk.ListBoxRow() is activated
    def row_activated_handler(self,lBox,lBoxRow):
        collector = self.engine.get_collector(lBoxRow.get_name())
        if(self.get_selection_mode() == Gtk.SelectionMode.SINGLE):
            self.select_row(lBoxRow)
            self.attached_gui.create_config_window(Gdk.Event(),collector)
        if(self.get_selection_mode() == Gtk.SelectionMode.MULTIPLE):
			if(lBoxRow.get_name() != self.attached_gui.get_current_config_window_name()):
				
				no_collectors_active = True
				for i in self.collectorStatus:
					if(self.collectorStatus[i] == True):
						no_collectors_active = False

				self.toggle_clicked_row(lBoxRow)
				if(no_collectors_active):
					self.attached_gui.create_config_window(Gdk.Event(), collector)

			elif(lBoxRow.get_name() == self.attached_gui.get_current_config_window_name()):
				self.toggle_clicked_row(lBoxRow)
				for c in self.collectorStatus:
					if(self.collectorStatus[c] == True):
						collector = self.engine.get_collector(c)
						self.attached_gui.create_config_window(Gdk.Event(), collector)
						break
			if(not self.attached_gui.is_config_window_active()):
				self.attached_gui.create_config_window(Gdk.Event(), collector)
        self.update_row_colors(Gdk.Event(),lBoxRow)

    # Called by the start/stop all collector menu option in the staus icon menu. Updates the status of the collector rows when they are pressed.
    def update_collector_status(self, action, collectorName):
        row = filter(lambda r: r.get_name() == collectorName, self.get_children())
        if (row.__len__() > 0):
            collectorRow = row.pop()
            if (action == Action.RUN):
                self.select_row(collectorRow)
            if (action == Action.STOP):
                self.unselect_row(collectorRow)
            self.update_row_color(collectorRow)
