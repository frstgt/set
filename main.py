import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

import AppDef, AppView, AppFile

# This would typically be its own file
MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <submenu>
      <attribute name="label" translatable="yes">File</attribute>
      <section>
        <item>
          <attribute name="action">win.new</attribute>
          <attribute name="label" translatable="yes">_New</attribute>
          <attribute name="accel">&lt;Primary&gt;n</attribute>
        </item>
        <item>
          <attribute name="action">win.open</attribute>
          <attribute name="label" translatable="yes">_Open</attribute>
          <attribute name="accel">&lt;Primary&gt;o</attribute>
        </item>
        <item>
          <attribute name="action">win.save</attribute>
          <attribute name="label" translatable="yes">_Save</attribute>
          <attribute name="accel">&lt;Primary&gt;s</attribute>
        </item>
        <item>
          <attribute name="action">win.save_as</attribute>
          <attribute name="label" translatable="yes">Save As</attribute>
        </item>
        <item>
          <attribute name="action">win.close</attribute>
          <attribute name="label" translatable="yes">Close</attribute>
        </item>
      </section>
      <section>
        <item>
          <attribute name="action">app.about</attribute>
          <attribute name="label" translatable="yes">About</attribute>
        </item>
        <item>
          <attribute name="action">app.quit</attribute>
          <attribute name="label" translatable="yes">_Quit</attribute>
          <attribute name="accel">&lt;Primary&gt;q</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">Control</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Init</attribute>
          <attribute name="action">win.init_table</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Step</attribute>
          <attribute name="action">win.step_table</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Run</attribute>
          <attribute name="action">win.run_table</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Stop</attribute>
          <attribute name="action">win.stop_table</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">Table</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Append</attribute>
          <attribute name="action">win.append_table</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Remove</attribute>
          <attribute name="action">win.remove_table</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Edit Name</attribute>
          <attribute name="action">win.edit_table_name</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">State</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Append</attribute>
          <attribute name="action">win.append_state</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Remove</attribute>
          <attribute name="action">win.remove_state</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Edit Name</attribute>
          <attribute name="action">win.edit_state_name</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Edit Code</attribute>
          <attribute name="action">win.edit_state_code</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">Event</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Append</attribute>
          <attribute name="action">win.append_event</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Remove</attribute>
          <attribute name="action">win.remove_event</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Edit Name</attribute>
          <attribute name="action">win.edit_event_name</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Edit Code</attribute>
          <attribute name="action">win.edit_event_code</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.set_default_size(640, 480)

        ###

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        #

        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hbox, False, True, 0)

        self.init_btn = Gtk.Button("||<<")
        hbox.pack_start(self.init_btn, False, True, 0)
        self.step_btn = Gtk.Button(">|")
        hbox.pack_start(self.step_btn, False, True, 0)
        self.run_btn = Gtk.Button(">")
        hbox.pack_start(self.run_btn, False, True, 0)
        self.stop_btn = Gtk.Button("||")
        hbox.pack_start(self.stop_btn, False, True, 0)

        #

        self.tables = AppView.StateEventTables()
        self.file = AppFile.AppFile(self, self.tables)
        vbox.pack_start(self.tables, True, True, 0)

        self.file.new_file()

        self.show_all()

        ###

        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_new)
        self.add_action(action)
        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)
        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.on_save)
        self.add_action(action)
        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.on_save_as)
        self.add_action(action)
        action = Gio.SimpleAction.new("close", None)
        action.connect("activate", self.on_close)
        self.add_action(action)

        #

        action = Gio.SimpleAction.new("append_table", None)
        action.connect("activate", self.on_append_table)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_table", None)
        action.connect("activate", self.on_remove_table)
        self.add_action(action)
        action = Gio.SimpleAction.new("edit_table_name", None)
        action.connect("activate", self.on_edit_table_name)
        self.add_action(action)

        action = Gio.SimpleAction.new("append_state", None)
        action.connect("activate", self.on_append_state)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_state", None)
        action.connect("activate", self.on_remove_state)
        self.add_action(action)
        action = Gio.SimpleAction.new("edit_state_name", None)
        action.connect("activate", self.on_edit_state_name)
        self.add_action(action)
        action = Gio.SimpleAction.new("edit_state_code", None)
        action.connect("activate", self.on_edit_state_code)
        self.add_action(action)

        action = Gio.SimpleAction.new("append_event", None)
        action.connect("activate", self.on_append_event)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_event", None)
        action.connect("activate", self.on_remove_event)
        self.add_action(action)
        action = Gio.SimpleAction.new("edit_event_name", None)
        action.connect("activate", self.on_edit_event_name)
        self.add_action(action)
        action = Gio.SimpleAction.new("edit_event_code", None)
        action.connect("activate", self.on_edit_event_code)
        self.add_action(action)

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
            lambda obj, pspec: max_action.set_state(
                GLib.Variant.new_boolean(obj.props.is_maximized)))

        #

    def save_changes(self):
        self.file.save_changes()
    def on_new(self, action, param):
        self.file.new_file()
    def on_open(self, action, param):
        self.file.open_file()
    def on_save(self, action, param):
        self.file.save_file()
    def on_save_as(self, action, param):
        self.file.save_as_file()
    def on_close(self, action, param):
        self.file.close_file()

        #

    def on_append_table(self, action, value):
        self.tables.append_table(None)
        self.show_all()
    def on_remove_table(self, action, value):
        self.tables.remove_table()
        self.show_all()
    def on_edit_table_name(self, action, value):
        self.tables.edit_table_name(parent=self)
        self.show_all()

    def on_append_state(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.append_state(None)
        self.show_all()
    def on_remove_state(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.remove_state()
        self.show_all()
    def on_edit_state_name(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.edit_state_name(parent=self)
        self.show_all()
    def on_edit_state_code(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.edit_state_code(parent=self)
        self.show_all()

    def on_append_event(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.append_event(None)
        self.show_all()
    def on_remove_event(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.remove_event()
        self.show_all()
    def on_edit_event_name(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.edit_event_name(parent=self)
        self.show_all()
    def on_edit_event_code(self, action, value):
        table = self.tables.get_current_table()
        if table == None:
            return
        table.edit_event_code(parent=self)
        self.show_all()

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args,
                         application_id="org.frstgt.set",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title=AppDef.APP_NAME)
            self.window.connect("delete-event", self.on_delete_event)

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        res = self.window.file.save_changes()
        if res == Gtk.ResponseType.YES:
            return
        self.quit()

    def on_delete_event(self, widget, event):
        res = self.window.file.save_changes()
        if res == Gtk.ResponseType.YES:
            return True
        return False

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)


