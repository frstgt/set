import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

import SetTable

# This would typically be its own file
MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <submenu>
      <attribute name="label" translatable="yes">File</attribute>
      <section>
        <item>
          <attribute name="action">win.new_table</attribute>
          <attribute name="label" translatable="yes">_New</attribute>
        </item>
        <item>
          <attribute name="action">win.open_table</attribute>
          <attribute name="label" translatable="yes">_Open</attribute>
        </item>
        <item>
          <attribute name="action">win.close_table</attribute>
          <attribute name="label" translatable="yes">Close</attribute>
        </item>
        <item>
          <attribute name="action">win.save_table</attribute>
          <attribute name="label" translatable="yes">_Save</attribute>
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
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">State</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Edit</attribute>
          <attribute name="action">win.edit_state</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Append</attribute>
          <attribute name="action">win.append_state</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Remove</attribute>
          <attribute name="action">win.remove_state</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">Event</attribute>
      <section>
        <item>
          <attribute name="label" translatable="yes">Edit</attribute>
          <attribute name="action">win.edit_event</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Append</attribute>
          <attribute name="action">win.append_event</attribute>
        </item>
        <item>
          <attribute name="label" translatable="yes">Remove</attribute>
          <attribute name="action">win.remove_event</attribute>
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

        self.tables = SetTable.StateEventTables()
        vbox.pack_start(self.tables, True, True, 0)

        self.tables.append_table("main")

        self.show_all()

        ###

        action = Gio.SimpleAction.new("append_table", None)
        action.connect("activate", self.on_append_table)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_table", None)
        action.connect("activate", self.on_remove_table)
        self.add_action(action)

        action = Gio.SimpleAction.new("edit_state", None)
        action.connect("activate", self.on_edit_state)
        self.add_action(action)
        action = Gio.SimpleAction.new("append_state", None)
        action.connect("activate", self.on_append_state)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_state", None)
        action.connect("activate", self.on_remove_state)
        self.add_action(action)

        action = Gio.SimpleAction.new("edit_event", None)
        action.connect("activate", self.on_edit_event)
        self.add_action(action)
        action = Gio.SimpleAction.new("append_event", None)
        action.connect("activate", self.on_append_event)
        self.add_action(action)
        action = Gio.SimpleAction.new("remove_event", None)
        action.connect("activate", self.on_remove_event)
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

    def on_append_table(self, action, value):
        self.tables.append_table(None)
        self.show_all()
    def on_remove_table(self, action, value):
        self.tables.remove_table()
        self.show_all()

    def on_edit_state(self, action, value):
        table = self.tables.get_current_table()
        table.edit_state(self)
        self.show_all()
    def on_append_state(self, action, value):
        table = self.tables.get_current_table()
        table.append_state(None)
        self.show_all()
    def on_remove_state(self, action, value):
        table = self.tables.get_current_table()
        table.remove_state()
        self.show_all()

    def on_edit_event(self, action, value):
        table = self.tables.get_current_table()
        table.edit_event(self)
        self.show_all()
    def on_append_event(self, action, value):
        table = self.tables.get_current_table()
        table.append_event(None)
        self.show_all()
    def on_remove_event(self, action, value):
        table = self.tables.get_current_table()
        table.remove_event()
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
                         application_id="org.example.stt",
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
            self.window = AppWindow(application=self, title="Main Window")

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
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)


