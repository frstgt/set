import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, cairo

class EditCodeDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, name, code):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(400, 300)

        vbox = self.get_content_area()

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        scrolledwindow.add(self.textview)
        vbox.pack_start(scrolledwindow, True, True, 0)

        self.set_code(name, code)

        self.show_all()

    def set_code(self, name, code):
        self.entry.set_text(name)
        self.textview.get_buffer().set_text(code)
    def get_code(self):
        name = self.entry.get_text()
        buffer = self.textview.get_buffer()
        code = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter(), False)
        return [name, code]


class StateButton(Gtk.ToggleButton):

    id = 1

    @classmethod
    def new_name(self):
                name = "State" + str(StateButton.id)
                StateButton.id += 1
                return name

    def __init__(self, name):
        Gtk.ToggleButton.__init__(self, name)

        self.code = ""

    def set_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_code(self):
        return [self.get_label(), self.code]

    def edit_code(self, win_title, parent):
        
        name, code = self.get_code()
        dialog = EditCodeDialog(win_title, parent, name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
                name, code = dialog.get_code()
                self.set_code(name, code)

        dialog.destroy()


class EventButton(Gtk.ToggleButton):

    id = 1

    @classmethod
    def new_name(self):
                name = "Event" + str(EventButton.id)
                EventButton.id += 1
                return name

    def __init__(self, name):
        Gtk.ToggleButton.__init__(self, name)

        self.code = ""

    def set_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_code(self):
        return [self.get_label(), self.code]

    def edit_code(self, win_title, parent):
        
        name, code = self.get_code()
        dialog = EditCodeDialog(win_title, parent, name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
                name, code = dialog.get_code()
                self.set_code(name, code)

        dialog.destroy()


class StateEventTable(Gtk.Grid):

    id = 1
    @classmethod
    def new_name(self):
                name = "Table" + str(StateEventTable.id)
                StateEventTable.id += 1
                return name

    def __init__(self):
        Gtk.Grid.__init__(self)

        self.states = [] # button
        self.events = []
        self.current_state = None # button
        self.current_event = None

    def get_current_state_pos(self):
        name = self.current_state.get_label()
        return self.states.index(name)
    def get_current_event_pos(self):
        name = self.current_event.get_label()
        return self.events.index(name)

        #

    def edit_state(self, parent):
        button = self.current_state
        name, _ = button.get_code()
        button.edit_code("Edit State: " + name, parent)

    def append_state(self, name):
        if name == None:
                name = StateButton.new_name()
        pos = len(self.states)

        button = StateButton(name)
        button.connect("clicked", self.on_clicked_for_state)
        button.clicked()

        self.states.insert(pos, button)

        self.insert_row(pos+1)
        self.attach(button, 0, pos+1, 1, 1)
        for si, st1 in enumerate(self.states):
                if si != pos:
                        for ei, ev in enumerate(self.events):
                                combo = self.get_child_at(ei+1, si+1)
                                combo.insert_text(pos+1, name)
                else:
                        for ei, ev in enumerate(self.events):
                                combo = Gtk.ComboBoxText()
                                combo.append_text("")
                                for st2 in self.states:
                                        if st2 != button:
                                                nm2, _ = st2.get_code()
                                                combo.append_text(nm2)
                                self.attach(combo, ei+1, pos+1, 1, 1)

    def remove_state(self):

        pos = self.get_current_state_pos()
        if self.states[pos] != "Start" or self.states[pos] != "End":

                del self.states[pos]

                self.remove_row(pos+1)
                for si, st in enumerate(self.states):
                        for ei, ev in enumerate(self.events):
                                combo = self.get_child_at(ei+1, si+1)
                                combo.remove(pos+1)
                if pos >= len(self.states):
                        pos = len(self.states)-1
                self.current_state = self.get_child_at(0, pos+1)

        #

    def edit_event(self, parent):
        button = self.current_event
        name, _ = button.get_code()
        button.edit_code("Edit Event: " + name, parent)

    def append_event(self, name):
        if name == None:
                name = EventButton.new_name()
        pos = len(self.events)

        button = EventButton(name)
        button.connect("clicked", self.on_clicked_for_event)
        button.clicked()

        self.events.insert(pos, button)

        self.insert_column(pos+1)
        self.attach(button, pos+1, 0, 1, 1)
        for si, st1 in enumerate(self.states):
                combo = Gtk.ComboBoxText()
                combo.append_text("")
                for st2 in self.states:
                        if st2 != st1:
                                nm2, _ = st2.get_code()
                                combo.append_text(nm2)
                self.attach(combo, pos+1, si+1, 1, 1)

    def remove_event(self):

        if len(self.events) > 1:
                pos = self.get_current_event_pos()

                del self.events[pos]

                self.remove_column(pos+1)
                if pos >= len(self.events):
                        pos = len(self.events)-1
                self.current_evnet = self.get_child_at(pos+1, 0)

        #

    def on_clicked_for_state(self, button):
        if button.get_active():
                self.current_state = button
                for st in self.states:
                        if st != button:
                                st.set_active(False)
                self.show_all()
        else:
                if self.current_state == button:
                        button.set_active(True)

    def on_clicked_for_event(self, button):
        if button.get_active():
                self.current_event = button
                for ev in self.events:
                        if ev != button:
                                ev.set_active(False)
                self.show_all()
        else:
                if self.current_event == button:
                        button.set_active(True)


class StateEventTables(Gtk.Notebook):

    def __init__(self):
        Gtk.Notebook.__init__(self)

    def get_current_table(self):
        page = self.get_current_page()
        table = self.get_nth_page(page)
        return table

    def get_nth_table_name(self, page):
        table = self.get_nth_page(page)
        label = self.get_tab_label(table)
        return label.get_text()

    def append_table(self, name):
        if name == None:
                        name = StateEventTable.new_name()

        table = StateEventTable()

        table.append_state("Start")
        table.append_state("End")
        table.append_event(None)

        self.append_page(table, Gtk.Label(name))
        self.set_tab_reorderable(table, True)

    def remove_table(self):
        page = self.get_current_page()
        name = self.get_nth_table_name(page)
        if name != "main":
                self.remove_page(page)

