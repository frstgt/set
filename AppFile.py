# -*- coding: utf-8 -*-

import sys, io

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import json
import AppDef

class AppFile:

  def __init__(self, parent_window, appdata):
      self.parent_window = parent_window
      self.filename = None
      self.appdata = appdata

  def set_title(self, filename):
      title = AppDef.APP_NAME
      if filename != None:
          title += ": " + filename
      self.parent_window.set_title(title)

  def load_data(self, filename):
      f = io.open(filename, 'r', encoding='utf-8')
      first_line = f.readline().rstrip()
      if first_line != AppDef.FILE_HEADER:
          return
      data = json.load(f)
      f.close

      self.appdata.set_data(data)

  def save_data(self, filename):
      data = self.appdata.get_data();

      f = io.open(filename, 'w', encoding='utf-8')
      f.write(AppDef.FILE_HEADER + "\n")

      # json.dumps return utf-8 as str. it is a bug.
      dump_utf8 = unicode(json.dumps(data, encoding='utf-8'))
      f.write(dump_utf8)

      f.close

      # 

  def save_changes(self):
      res = Gtk.ResponseType.NO
      if self.appdata.get_changed():
          res = self.save_changes_dialog()
      return res

  def new_file(self):
      if self.appdata.get_changed():
          res = self.save_changes_dialog()
          if res == Gtk.ResponseType.YES:
              return

      self.filename = None
      self.appdata.clear_data()
      self.appdata.clear_changed()
      self.set_title(None)

  def open_file(self):
      if self.appdata.get_changed():
          res = self.save_changes_dialog()
          if res == Gtk.ResponseType.YES:
              return

      res, filename = self.open_file_dialog()
      if res == Gtk.ResponseType.OK:
          self.filename = filename
          self.appdata.clear_data()
          self.load_data(self.filename)
          self.appdata.clear_changed()
          self.set_title(self.filename)

  def save_file(self):
      if self.filename != None:
          self.save_data(self.filename)
          self.appdata.clear_changed()
      else:
          res, filename = self.save_file_dialog()
          if res == Gtk.ResponseType.OK:
              self.filename = filename
              self.save_data(self.filename)
              self.appdata.clear_changed()
              self.set_title(self.filename)

  def save_as_file(self):
      res, filename = self.save_file_dialog()
      if res == Gtk.ResponseType.OK:
          self.filename = filename
          self.save_data(self.filename)
          self.appdata.clear_changed()
          self.set_title(self.filename)

  def close_file(self):
      self.new_file()

      #

  def save_changes_dialog(self): # return YES/NO

      message = "Would you like to save your changes?"
      dialog = Gtk.MessageDialog(self.parent_window, 0,
        Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.YES_NO, message)
      response = dialog.run()
      dialog.destroy()

      return response

  def get_filter(self):
      filter = Gtk.FileFilter()
      filter.set_name(AppDef.FILE_FORMAT)
      filter.add_pattern(AppDef.FILE_PATTERN)
      return filter

  def open_file_dialog(self): # return OK/CANCEL
      dialog = Gtk.FileChooserDialog('Open File', self.parent_window,
                                     Gtk.FileChooserAction.OPEN,
                                     (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                      Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

      dialog.add_filter(self.get_filter())

      filename = None
      response = dialog.run()
      if response == Gtk.ResponseType.OK:
          filename = dialog.get_filename()
      dialog.destroy()

      return [response, filename]

  def save_file_dialog(self): # return OK/CANCEL
      dialog = Gtk.FileChooserDialog('Save File', self.parent_window,
                                     Gtk.FileChooserAction.SAVE,
                                     (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                      Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

      dialog.add_filter(self.get_filter())
      dialog.set_do_overwrite_confirmation(True)

      filename = None
      response = dialog.run()
      if response == Gtk.ResponseType.OK:
          filename = dialog.get_filename()
      dialog.destroy()

      return [response, filename]

# end of file
