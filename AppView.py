import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, cairo

class EditNameDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, name):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 50)

        vbox = self.get_content_area()

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_changed_for_entry)
        vbox.pack_start(self.entry, False, True, 0)

        self.set_name(name)
        self.entry_changed = False

        self.show_all()

    def get_changed(self):
        return self.entry_changed
    def set_name(self, name):
        self.entry.set_text(name)
    def get_name(self):
        return self.entry.get_text()

    def on_changed_for_entry(self, entry):
        self.entry_changed = True

class EditNameCodeDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, name, code):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(400, 300)

        vbox = self.get_content_area()

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_changed_for_entry)
        vbox.pack_start(self.entry, False, True, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.buffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)
        vbox.pack_start(scrolledwindow, True, True, 0)

        self.set_name_code(name, code)
        self.entry_changed = False
        self.buffer.set_modified(False)

        self.show_all()

    def get_changed(self):
        return self.entry_changed or self.buffer.get_modified()
    def set_name_code(self, name, code):
        self.entry.set_text(name)
        self.textview.get_buffer().set_text(code)
    def get_name_code(self):
        name = self.entry.get_text()
        buffer = self.textview.get_buffer()
        code = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False)
        return [name, code]

    def on_changed_for_entry(self, entry):
        self.entry_changed = True


class StateButton(Gtk.ToggleButton):

    def __init__(self, name=None, code=""):
        Gtk.ToggleButton.__init__(self, name)

        self.code = code

    def set_code(self, code):
        self.code = code
    def get_code(self):
        return self.code

    def set_name(self, name):
        self.set_label(name)
    def get_name(self):
        return self.get_label()

    def set_name_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_name_code(self):
        return [self.get_label(), self.code]


class EventButton(Gtk.ToggleButton):

    def __init__(self, name=None, code=""):
        Gtk.ToggleButton.__init__(self, name)

        self.code = code

    def set_code(self, code):
        self.code = code
    def get_code(self):
        return self.code

    def set_name(self, name):
        self.set_label(name)
    def get_name(self):
        return self.get_label()

    def set_name_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_name_code(self):
        return [self.get_label(), self.code]


class StateEventTable(Gtk.Grid):

    state_id = 1
    event_id = 1
    def __init__(self, name=None):
        Gtk.Grid.__init__(self)

        self.states = [] # button
        self.events = []
        self.current_state = None # button
        self.current_event = None

        self.changed = False

    def get_changed(self):
        return self.changed
    def clear_changed(self):
        self.changed = False

    def clear_data(self):
        sn = len(self.states)
        for si in range(sn):
            self.remove_row(si+1)
        self.remove_row(0)

        self.states = []
        self.events = []
        self.current_state = None
        self.current_event = None
        self.changed = False

        StateEventTable.state_id = 1
        StateEventTable.event_id = 1

    def get_data(self):
        sd = []
        sn = len(self.states)
        for si in range(sn):
            sname, scode = self.states[si].get_name_code()
            sd.append([sname, scode])

        ed = []
        en = len(self.events)
        for ei in range(en):
            ename, ecode = self.events[ei].get_name_code()
            ed.append([ename, ecode])

        trd = []
        for si in range(sn):
            for ei in range(en):
                entry = self.get_child_at(ei+1, si+1)
                ts = entry.get_text()
                trd.append([si, ei, ts])

        return [sd, ed, trd]

    def set_data(self, data):
        sd, ed, trd = data

        for sname, scode in sd:
            self.append_state(sname, scode)

        for ename, ecode in ed:
            self.append_event(ename, ecode)

        for si, ei, ts in trd:
            entry = self.get_child_at(ei+1, si+1)
            entry.set_text(ts)

        #

    def get_rundata(self):

        sdata = {}
        for st in self.states:
            ev_st_list = []
            sp = self.states.index(st)
            for ei, ev in enumerate(self.events):
                entry = self.get_child_at(ei+1, sp+1)
                tsname = entry.get_text()
                if tsname != "":
                    ename = self.events[ei].get_name()
                    ev_st_list.append([ename, tsname])
            sname, scode = st.get_name_code()
            sdata[sname] = [scode, ev_st_list]

        edata = {}
        for ev in self.events:
            ename, ecode = ev.get_name_code()
            edata[ename] = ecode

        return [sdata, edata]

        #

    def append_state(self, name=None, code=""):

        if name == None:
            name = "State" + str(StateEventTable.state_id)
        StateEventTable.state_id += 1

        sn = len(self.states)

        button = StateButton(name, code)
        name = button.get_name()
        button.connect("clicked", self.on_clicked_for_state)
        button.clicked()

        self.states.insert(sn, button)

        self.insert_row(sn+1)
        self.attach(button, 0, sn+1, 1, 1)
        for ei, ev in enumerate(self.events):
            entry = Gtk.Entry()
            entry.connect("changed", self.on_changed)
            self.attach(entry, ei+1, sn+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_state(self):
        button = self.current_state
        if button == None:
            return

        sp = self.states.index(self.current_state)

        del self.states[sp]

        self.remove_row(sp+1)
        if sp >= len(self.states):
            sp = len(self.states)-1
        self.current_state = self.get_child_at(0, sp+1)

        self.changed = True
        self.show_all()

    def edit_state(self, parent):
        button = self.current_state
        if button == None:
            return

        name, code = button.get_name_code()
        dialog = EditNameCodeDialog("Edit State: " + name, parent,
                                name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if dialog.get_changed():
                name, code = dialog.get_name_code()
                button.set_name_code(name, code)
                self.changed = True

        dialog.destroy()

        #

    def append_event(self, name=None, code=""):
        if name == None:
            name = "Event" + str(StateEventTable.event_id)
        StateEventTable.event_id += 1

        en = len(self.events)

        button = EventButton(name, code)
        name = button.get_name()
        button.connect("clicked", self.on_clicked_for_event)
        button.clicked()

        self.events.insert(en, button)

        self.insert_column(en+1)
        self.attach(button, en+1, 0, 1, 1)
        for si, st1 in enumerate(self.states):
            entry = Gtk.Entry()
            entry.connect("changed", self.on_changed)
            self.attach(entry, en+1, si+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_event(self):
        button = self.current_event
        if button == None:
            return

        ep = self.events.index(self.current_event)

        del self.events[ep]

        self.remove_column(ep+1)
        if ep >= len(self.events):
            ep = len(self.events)-1
        self.current_evnet = self.get_child_at(ep+1, 0)

        self.changed = True
        self.show_all()

    def edit_event(self, parent):
        button = self.current_event
        if button == None:
            return

        name, code = button.get_name_code()
        dialog = EditNameCodeDialog("Edit Event: " + name, parent,
                                name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if dialog.get_changed():
                name, code = dialog.get_name_code()
                button.set_name_code(name, code)
                self.changed = True

        dialog.destroy()

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

    def on_changed(self, entry):
        self.changed = True

class StateEventTables(Gtk.Notebook):

    def __init__(self):
        Gtk.Notebook.__init__(self)

        self.id = 1
        self.changed = False
        self.connect("page_reordered", self.on_page_reordered)

    def get_changed(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            if table.get_changed():
                return True
        return self.changed
    def clear_changed(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            table.clear_changed()
        self.changed = False

    def clear_data(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            table.clear_data()
            self.remove_page(ti)

        self.id = 1

    def set_data(self, data):
        for ti, name_data in enumerate(data):
            tname, tdata = name_data
            self.append_table(tname)
            table = self.get_nth_page(ti)
            table.set_data(tdata)

    def get_data(self):
        data = []
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            tname = self.get_tab_label_text(table)
            tdata = table.get_data()
            data.append([tname, tdata])
        return data

        #

    def get_rundata(self):
        data = {}
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            tname = self.get_tab_label_text(table)
            tdata = table.get_rundata()
            data[tname] = tdata
        return data

        #

    def get_current_table(self):
        page = self.get_current_page()
        if page == -1:
            return None

        table = self.get_nth_page(page)
        return table

        #

    def append_table(self, name):

        if name == None:
            name = "Table" + str(self.id)
        self.id += 1

        table = StateEventTable()

        self.append_page(table, Gtk.Label(name))
        self.set_tab_reorderable(table, True)

        self.changed = True
        self.show_all()

    def remove_table(self):
        page = self.get_current_page()
        if page == -1:
            return

        self.remove_page(page)

        self.changed = True
        self.show_all()

    def edit_table(self, parent):
        page = self.get_current_page()
        if page == -1:
            return

        table = self.get_nth_page(page)
        name = self.get_tab_label_text(table)
        
        dialog = EditNameDialog("Edit Table Name: " + name, parent, name)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            if dialog.get_changed():
                name = dialog.get_name()
                self.set_tab_label_text(table, name)
                self.changed = True

        dialog.destroy()

        #

    def on_page_reordered(self, notebook, child, page_num):
        self.changed = True

# end of file
