# -*- coding: utf-8 -*-

import sys, io, re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import AppDef

class EditCtrl(Gtk.Box):

  def __init__(self, parent_window, appview):
      Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
      
      self.parent_window = parent_window
      self.appview = appview

      #

      table_label = Gtk.Label("Table: ")
      self.pack_start(table_label, False, True, 0)
      self.append_table_btn = Gtk.Button("+")
      self.append_table_btn.connect("clicked", self.on_clicked_for_append_table)
      self.pack_start(self.append_table_btn, False, True, 0)
      self.remove_table_btn = Gtk.Button("-")
      self.remove_table_btn.connect("clicked", self.on_clicked_for_remove_table)
      self.pack_start(self.remove_table_btn, False, True, 0)
      self.edit_table_btn = Gtk.Button("E")
      self.edit_table_btn.connect("clicked",
                                   self.on_clicked_for_edit_table)
      self.pack_start(self.edit_table_btn, False, True, 0)

      state_label = Gtk.Label("     State: ")
      self.pack_start(state_label, False, True, 0)
      self.append_state_btn = Gtk.Button("+")
      self.append_state_btn.connect("clicked", self.on_clicked_for_append_state)
      self.pack_start(self.append_state_btn, False, True, 0)
      self.remove_state_btn = Gtk.Button("-")
      self.remove_state_btn.connect("clicked", self.on_clicked_for_remove_state)
      self.pack_start(self.remove_state_btn, False, True, 0)
      self.edit_state_btn = Gtk.Button("E")
      self.edit_state_btn.connect("clicked",
                                  self.on_clicked_for_edit_state)
      self.pack_start(self.edit_state_btn, False, True, 0)

      event_label = Gtk.Label("     Event: ")
      self.pack_start(event_label, False, True, 0)
      self.append_event_btn = Gtk.Button("+")
      self.append_event_btn.connect("clicked", self.on_clicked_for_append_event)
      self.pack_start(self.append_event_btn, False, True, 0)
      self.remove_event_btn = Gtk.Button("-")
      self.remove_event_btn.connect("clicked", self.on_clicked_for_remove_event)
      self.pack_start(self.remove_event_btn, False, True, 0)
      self.edit_event_btn = Gtk.Button("E")
      self.edit_event_btn.connect("clicked",
                                  self.on_clicked_for_edit_event)
      self.pack_start(self.edit_event_btn, False, True, 0)

  def on_clicked_for_append_table(self, button):
      self.appview.append_table(None)
      self.show_all()
  def on_clicked_for_remove_table(self, button):
      self.appview.remove_table()
      self.show_all()
  def on_clicked_for_edit_table(self, button):
      self.appview.edit_table(self.parent_window)
      self.show_all()

  def on_clicked_for_append_state(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.append_state(None)
      self.show_all()
  def on_clicked_for_remove_state(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.remove_state()
      self.show_all()
  def on_clicked_for_edit_state(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.edit_state(self.parent_window)
      self.show_all()

  def on_clicked_for_append_event(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.append_event(None)
      self.show_all()
  def on_clicked_for_remove_event(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.remove_event()
      self.show_all()
  def on_clicked_for_edit_event(self, button):
      table = self.appview.get_current_table()
      if table == None:
          return
      table.edit_event(self.parent_window)
      self.show_all()


class ProgCtrl(Gtk.Box):

  def __init__(self, parent_window, appview):
      Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

      self.parent_window = parent_window
      self.appview = appview

      self.rundata = None
      self.globals = {}
      self.locals = {}
      self.current_table = None
      self.current_state = None
      self.stack = []
      self.stop_flag = True
      self.return_flag = True

      #

      self.init_btn = Gtk.Button("Init")
      self.init_btn.connect("clicked", self.on_clicked_for_init)
      self.pack_start(self.init_btn, False, True, 0)
      self.step_btn = Gtk.Button("Step")
      self.step_btn.connect("clicked", self.on_clicked_for_step)
      self.pack_start(self.step_btn, False, True, 0)
      self.go_btn = Gtk.Button("Go")
      self.go_btn.connect("clicked", self.on_clicked_for_go)
      self.pack_start(self.go_btn, False, True, 0)
      self.go_entry = Gtk.Entry()
      self.pack_start(self.go_entry, False, True, 0)
      self.run_btn = Gtk.Button("Run")
      self.run_btn.connect("clicked", self.on_clicked_for_run)
      self.pack_start(self.run_btn, False, True, 0)
      self.stop_btn = Gtk.Button("Stop")
      self.stop_btn.connect("clicked", self.on_clicked_for_stop)
      self.pack_start(self.stop_btn, False, True, 0)

  def check(self):
      pass

  def init(self):
      self.rundata = self.appview.get_rundata()
      self.globals = {}
      self.locals = {}
      self.current_table = "main"
      self.current_state = "start"
      self.stack = []
      self.stop_flag = False
      self.return_flag = False

      print("initialized")

  def step(self):
      if self.stop_flag:
          return

      # entry
      print(">>> table/state: " +
            self.current_table + "/" + self.current_state)
      sdata, edata = self.rundata[self.current_table]
      scode, ev_st_list = sdata[self.current_state]

      # do
      if self.return_flag != True:
          match = re.match("# call ", scode)
          if match:
              self.stack.append([self.current_table, self.current_state])
              self.current_table = scode[7:]
              self.current_state = "start"
              return
          else:
              exec(scode, self.globals, self.locals)
      else:
          print(">>> skip")
      self.return_flag = False

      if self.current_table != "main" and self.current_state == "end":
          stack_data = self.stack.pop()
          self.current_table, self.current_state = stack_data
          self.return_flag = True
          return
      if self.current_table == "main" and self.current_state == "end":
          self.stop_flag = True
          return

      # exit
      for ev_st in ev_st_list:
          ename, sname = ev_st
          ret = eval(edata[ename], self.globals, self.locals)
          print(">>> event: " + ename + " -> " + str(ret))
          if ret:
              self.current_state = sname
              return

  def go(self):
      if self.stop_flag:
          return
      trg_state = self.go_entry.get_text()
      print(trg_state)
      while self.stop_flag != True and self.current_state != trg_state:
          self.step()

  def run(self):
      while self.stop_flag != True:
          self.step()

  def stop(self):
      self.stop_flag = True

      #

  def on_clicked_for_init(self, button):
      self.init()
  def on_clicked_for_step(self, button):
      self.step()
  def on_clicked_for_go(self, button):
      self.go()
  def on_clicked_for_run(self, button):
      self.run()
  def on_clicked_for_stop(self, button):
      self.stop()

# end of file
