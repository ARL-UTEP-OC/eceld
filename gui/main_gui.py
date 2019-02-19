import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
from utils.collector_action import Action
import os
import subprocess
import status_icon
import definitions
import engine.collector
import ecel_service
from collector_list_box import CollectorListBox
from gui.dss_gui import DssGUI
from gui.export_gui import ExportGUI
from gui.progress_bar import ProgressBar
from gui.plugin_config_gui import PluginConfigGUI
from _version import __version__
from psutil import NoSuchProcess

class MainGUI(Gtk.Window):

    def __init__(self, app_engine):
        super(MainGUI, self).__init__()

        self.set_title("Evaluator-Centric and Extensible Logger v%s" % (__version__))
        self.set_size_request(definitions.MAIN_WINDOW_WIDTH, definitions.MAIN_WINDOW_HEIGHT)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.hide_on_delete)

        self.engine = app_engine
        self.numCollectors = self.engine.get_collector_length()

        # Main container grid
        self.grid = Gtk.Grid()

        self.startall_button = Gtk.ToolButton()
        self.startall_button.set_icon_widget(self.get_image("start.png"))
        self.startall_button.connect("clicked", self.process_active_collectors,Action.RUN)
        self.startall_button.set_sensitive(False)

        self.stopall_button = Gtk.ToolButton()
        self.stopall_button.set_icon_widget(self.get_image("stop.png"))
        self.stopall_button.connect("clicked", self.process_active_collectors,Action.STOP)
        self.stopall_button.set_sensitive(False)

        self.parseall_button = Gtk.ToolButton()
        self.parseall_button.set_icon_widget(self.get_image("json.png"))
        self.parseall_button.connect("clicked", self.process_active_collectors, Action.PARSE)

        self.export_button = Gtk.ToolButton()
        self.export_button.set_icon_widget(self.get_image("export.png"))
        self.export_button.connect("clicked", self.export_all)

        self.remove_data_button = Gtk.ToolButton()
        self.remove_data_button.set_icon_widget(self.get_image("delete.png"))
        self.remove_data_button.connect("clicked", self.delete_all)

        self.dss_button = Gtk.ToolButton()
        self.dss_button.set_icon_widget(self.get_image("model.png"))
        self.dss_button.connect("clicked", self.call_dss_module, app_engine.collectors)

        self.toolbarWidget = Gtk.Box()
        self.toolbarWidget.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.toolbarWidget.set_size_request(definitions.MAIN_WINDOW_WIDTH,definitions.TOOL_BAR_HEIGHT)
        self.toolbarWidget.add(self.create_toolbar())

        # List of Gtk.ListBoxRows representing collector plugins
        self.collectorList = CollectorListBox(self.engine, self)

        # Container for the list of collector plugins (the 'left pane')
        self.collectorWidget = Gtk.ScrolledWindow()
        self.collectorWidget.set_size_request(definitions.COLLECTOR_WIDGET_WIDTH,definitions.MAIN_WINDOW_HEIGHT - definitions.TOOL_BAR_HEIGHT)
        self.collectorWidget.add(self.collectorList)

        self.currentConfigWindow = PluginConfigGUI(self,None)

        # Area of grid where configuration window appears.
        # Scrolled window allows the pane to be scrolled through should its width be exceeded by a child.
        self.configWidget = Gtk.ScrolledWindow()
        self.configWidget.set_size_request(definitions.CONFIG_WINDOW_WIDTH,definitions.CONFIG_WINDOW_HEIGHT)

        # contains collector widget AND config Widget
        self.main_body = Gtk.Box()
        self.main_body.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.main_body.add(self.collectorWidget)
        self.main_body.add(self.configWidget)

        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.grid.add(self.toolbarWidget)
        self.grid.add(self.main_body)

        self.add(self.grid)

        self.connect("destroy", self.close_all)

        self.show_all()
        self.status_context_menu = status_icon.CustomSystemTrayIcon(app_engine, self)

    def set_play_stop_btns(self, startSensitive, stopSensitive):
        self.startall_button.set_sensitive(startSensitive)
        self.stopall_button.set_sensitive(stopSensitive)

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        toolbar.set_size_request(definitions.MAIN_WINDOW_WIDTH,definitions.TOOL_BAR_HEIGHT)

        separator1 = Gtk.SeparatorToolItem()
        separator2 = Gtk.SeparatorToolItem()
        separator3 = Gtk.SeparatorToolItem()

        self.startall_button.set_tooltip_text("Start All Selected Collectors")
        toolbar.insert(self.startall_button, 0)
        self.stopall_button.set_tooltip_text("Stop All Selected collectors")
        toolbar.insert(self.stopall_button, 1)
        toolbar.insert(separator1, 2)
        self.parseall_button.set_tooltip_text("Execute Selected Parsers")
        toolbar.insert(self.parseall_button, 3)
        toolbar.insert(separator2, 4)
        self.export_button.set_tooltip_text("Export All Collector Data")
        toolbar.insert(self.export_button, 5)
        self.remove_data_button.set_tooltip_text("Delete All Collector Data")
        toolbar.insert(self.remove_data_button, 6)
        toolbar.insert(separator3, 7)
        self.dss_button.set_tooltip_text("DSS")
        toolbar.insert(self.dss_button, 8)

        return toolbar

    # Return image based on image name
    def get_image(self,name):
        image = Gtk.Image()
        image.set_from_file(os.path.join(definitions.ICONS_DIR, name))
        image.show()
        return image

    # Destroy anything in the current config window before placing new config window
    def clear_config_window(self):
        self.configWidget.foreach(self.delete_widget)

    # Helper for clear_config_window()
    def delete_widget(self,widget):
        widget.destroy()

    # Pull the collectors configuration from plugin_configure_gui.py and place in config window.
    def create_config_window(self,event,collector):
        self.currentConfigWindow = PluginConfigGUI(self, collector)
        self.currentConfigWindow.set_name(collector.name)
        self.currentConfigWindow.unparent()
        self.currentConfigWindow.show_all()
        self.currentConfigWindow.set_size_request(definitions.CONFIG_WINDOW_WIDTH,definitions.CONFIG_WINDOW_HEIGHT)
        ### So far following five lines work
        service_name = "ecel_service_"+collector.name
        service = ecel_service.ecel_Service(service_name, pid_dir='/tmp')
        self.configWidget.set_sensitive(service.is_running() == False)
        setStartSensitive = service.is_running() == False and not isinstance(collector,engine.collector.ManualCollector)
        self.set_play_stop_btns(setStartSensitive, service.is_running())
        ### Old code which seems to mess up GUI when using Stop/Play btns
        # self.configWidget.set_sensitive(collector.is_running() == False)
        # setStartSensitive = collector.is_running() == False and not isinstance(collector,engine.collector.ManualCollector)
        # self.set_play_stop_btns(setStartSensitive, collector.is_running())
        #
        self.clear_config_window()
        self.configWidget.add(self.currentConfigWindow)

    def show_gui(self):
        self.present()
        self.show_all()

    def export_all(self, event):
        ExportGUI(self)

    def call_dss_module(self, event, collectors):
        DssGUI(self, collectors)

    def delete_all(self, event):
        delete_script = "cleanCollectorData.bat" if os.name == "nt" else "cleanCollectorData.sh"
        if self.show_confirmation_dialog("Are you sure you want to delete all collector data (this cannot be undone)?"):
            remove_cmd = os.path.join(os.path.join(os.getcwd(), "scripts"), delete_script)
            subprocess.call(remove_cmd)  # TODO: Change this to not call external script

    # Perform the designated action (run,stop,parse) for all selected collectors
    def process_active_collectors(self,event,action):
        selected_collectors = self.collectorList.get_selected_rows()
        if(selected_collectors.__len__() == 0):
            print("No collectors selected...")
        for i, c in enumerate(selected_collectors):
            collector = self.engine.get_collector(c.get_name())
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                #TODO:Adjust the RUN to start a daemon
                if(action == Action.RUN):
                    '''New Code for service'''
                    service_name = "ecel_service_"+collector.name
                    print service_name
                    service = ecel_service.ecel_Service(service_name, pid_dir='/tmp')
                    service.start()
                    '''Old Code'''
                    #collector.run()
                    self.set_config_widget_sensitivity()
                #TODO:Adjust the STOP to start a daemon
                if(action == Action.STOP):
                    try:
                        '''New Code for service'''
                        service_name = "ecel_service_"+collector.name
                        service = ecel_service.ecel_Service(service_name, pid_dir='/tmp')
                        service.stop()
                        '''Old Code'''
                        #collector.terminate()
                        self.set_config_widget_sensitivity()
                    except NoSuchProcess:
                        # On windows, when a process finishes running a command, it terminates. This is needed to ensure
                        # ...ECEL doesnt crash on Windows if the stop button is pressed for a collector whose process...
                        # has already finished executing its command.
                        print(collector.name + " process has already terminated.")
                        collector.clean()
                        self.configWidget.set_sensitive(True)
                    except StopIteration:
                        # Catch this exception to smoothly handle this action sequence:
                        # ... ** 1. Select 'Start all' from status icon 2. hit' stop' button from main application window instead of 'stop all' from status icon
                        # ... For this action sequence, this exception is needed because if not,
                        self.collectorList.set_selection_mode(Gtk.SelectionMode.SINGLE)
                        self.set_play_stop_btns(False,False)
                        self.status_context_menu.stopall_menu_item.set_sensitive(False)

            if(action == Action.PARSE):
                collector.parser.parse()
        self.status_context_menu.startall_menu_item.set_sensitive(self.engine.has_collectors_running() == False)

    #Here is where the buttons for Play and Stop get Updated
    #TODO: Adjust this method to check if the daemon exists as opposed to if collector is running
    def set_config_widget_sensitivity(self):
        collector = self.engine.get_collector(self.currentConfigWindow.get_name()) #NOTE: in orignal
        service_name = "ecel_service_"+collector.name
        service = ecel_service.ecel_Service(service_name, pid_dir='/tmp')
        
        self.configWidget.set_sensitive(service.is_running() == True) #NOTE: changed False to True
        
        #self.set_play_stop_btns(service.is_running() == False, service.is_running()) #NOTE: replaced this line wih the condition below
        # If the configuration widget is sensitive, the start button is sensitive;
        # otherwise, the stop button is sensitive
        if(self.configWidget.is_sensitive()):
            self.set_play_stop_btns(True, False)
        else:
            self.set_play_stop_btns(False, True)

    def get_current_config_window_name(self):
        return self.currentConfigWindow.get_name()

    def is_config_window_active(self):
        return self.currentConfigWindow.active

    def create_collector_bbox(self, collector):
        frame = Gtk.Frame()

        if collector.is_enabled():
            layout = Gtk.ButtonBoxStyle.SPREAD
            spacing = 10

            bbox = Gtk.HButtonBox()
            bbox.set_border_width(1)
            bbox.set_layout(layout)
            bbox.set_spacing(spacing)
            frame.add(bbox)

            startCollectorButton = Gtk.Button('Start Collector')
            startCollectorButton.connect("clicked", self.startIndividualCollector, collector)
            startCollectorButton.set_sensitive(not isinstance(collector, engine.collector.ManualCollector))
            bbox.add(startCollectorButton)

            stopCollectorButton = Gtk.Button('Stop Collector')
            stopCollectorButton.connect("clicked", self.stopIndividualCollector, collector)
            stopCollectorButton.set_sensitive(not isinstance(collector, engine.collector.ManualCollector))
            bbox.add(stopCollectorButton)

            parseButton = Gtk.Button('Parse Data')
            parseButton.connect("clicked", self.parser, collector)
            bbox.add(parseButton)
        else:
            label = Gtk.Label(label="Collector Disabled")
            frame.add(label)

        return frame

    def startall_collectors(self, button):
        self.collectorList.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.set_play_stop_btns(False,True)
        self.status_context_menu.tray_ind.set_icon(Gtk.STOCK_MEDIA_RECORD)
        self.status_context_menu.stopall_menu_item.set_sensitive(True)
        self.status_context_menu.startall_menu_item.set_sensitive(False)
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                collector.run()
                self.collectorList.update_collector_status(Action.RUN,collector.name)
                if(self.currentConfigWindow != None):
                    self.currentConfigWindow.set_sensitive(False)
            pb.setValue(i / len(self.engine.collectors))
            pb.pbar.set_text("Stopping " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
                pb.setValue(i)
            i += 1
            if(i == len(self.engine.collectors)):
                pb.setValue(100)
            pb.destroy()
        #if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            #pb.destroy()

    def stopall_collectors(self, button):
        self.collectorList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.set_play_stop_btns(False,False)
        self.status_context_menu.tray_ind.set_icon(Gtk.STOCK_NO)
        self.status_context_menu.stopall_menu_item.set_sensitive(False)
        self.status_context_menu.startall_menu_item.set_sensitive(True)
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            if collector.is_enabled() and isinstance(collector, engine.collector.AutomaticCollector):
                collector.terminate()
                self.collectorList.update_collector_status(Action.STOP,collector.name)
                if(self.currentConfigWindow != None):
                    self.currentConfigWindow.set_sensitive(True)
            pb.setValue(i / len(self.engine.collectors))
            pb.pbar.set_text("Stopping " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
            i += 1
            if (i == len(self.engine.collectors)):
                pb.setValue(100)
            pb.destroy()
            # if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            # pb.destroy()

    def parse_all(self, event):
        i = 0.0
        pb = ProgressBar()
        while Gtk.events_pending():
            Gtk.main_iteration()

        for collector in self.engine.collectors:
            collector.parser.parse()
            pb.setValue(i/len(self.engine.collectors))
            pb.pbar.set_text("Parsing " + collector.name)
            while Gtk.events_pending():
                Gtk.main_iteration()
            i += 1
        if not pb.emit("delete-event", Gdk.Event(Gdk.DELETE)):
            pb.destroy()

        alert = Gtk.MessageDialog(self, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                                      Gtk.ButtonsType.CLOSE, "Parsing complete")
        alert.run()
        alert.destroy()

    def close_all(self, event):
        for collector in self.engine.collectors:
            if collector.is_enabled:
               collector.terminate()


    def parser(self, event, collector):
        collector.parser.parse()

    def stopIndividualCollector(self, event, collector):
        collector.terminate()
        self.set_play_stop_btns(True,False)
        self.set_config_widget_sensitivity()
        self.status_context_menu.startall_menu_item.set_sensitive(self.engine.has_collectors_running() == False)

    def startIndividualCollector(self, event, collector):
        print "Collector running", event
        collector.run()
        self.collectorList.update_collector_status(Action.RUN,collector.name)
        self.set_play_stop_btns(False,True)
        self.create_config_window(event, collector)
        self.set_config_widget_sensitivity()
        self.status_context_menu.startall_menu_item.set_sensitive(False)

    def show_confirmation_dialog(self, msg):
        dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                                      Gtk.ButtonsType.YES_NO, msg)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            return True

        return False

    # Manual override on widget.hide_on_delete()
    # Without this, app window terminates when gui is closed.
    def hide_on_delete(self, this, event):
        this.hide()
        return True
