#!/usr/bin/env python3

#
# Copyright (C) 2002-2007
# ASTRON (Netherlands Foundation for Research in Astronomy)
# and The MeqTree Foundation
# P.O.Box 2, 7990 AA Dwingeloo, The Netherlands, seg@astron.nl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#  (c) 2013.				 (c) 2011.
#  National Research Council		 Conseil national de recherches
#  Ottawa, Canada, K1A 0R6 		 Ottawa, Canada, K1A 0R6
#
#  This software is free software;	 Ce logiciel est libre, vous
#  you can redistribute it and/or	 pouvez le redistribuer et/ou le
#  modify it under the terms of	         modifier selon les termes de la
#  the GNU General Public License	 Licence Publique Generale GNU
#  as published by the Free		 publiee par la Free Software
#  Software Foundation; either	 	 Foundation (version 3 ou bien
#  version 2 of the License, or	 	 toute autre version ulterieure
#  (at your option) any later	 	 choisie par vous).
#  version.
#
#  This software is distributed in	 Ce logiciel est distribue car
#  the hope that it will be		 potentiellement utile, mais
#  useful, but WITHOUT ANY		 SANS AUCUNE GARANTIE, ni
#  WARRANTY; without even the	 	 explicite ni implicite, y
#  implied warranty of			 compris les garanties de
#  MERCHANTABILITY or FITNESS FOR	 commercialisation ou
#  A PARTICULAR PURPOSE.  See the	 d'adaptation dans un but
#  GNU General Public License for	 specifique. Reportez-vous a la
#  more details.			 Licence Publique Generale GNU
#  					 pour plus de details.
#
#  You should have received a copy	 Vous devez avoir recu une copie
#  of the GNU General Public		 de la Licence Publique Generale
#  License along with this		 GNU en meme temps que ce
#  software; if not, contact the	 logiciel ; si ce n'est pas le
#  Free Software Foundation, Inc.	 cas, communiquez avec la Free
#  at http://www.fsf.org.		 Software Foundation, Inc. au
#						 http://www.fsf.org.
#
#  email:				 courriel:
#  business@hia-iha.nrc-cnrc.gc.ca	 business@hia-iha.nrc-cnrc.gc.ca
#
#  National Research Council		 Conseil national de recherches
#      Canada				    Canada
#  Herzberg Institute of Astrophysics	 Institut Herzberg d'astrophysique
#  5071 West Saanich Rd.		 5071 West Saanich Rd.
#  Victoria BC V9E 2E7			 Victoria BC V9E 2E7
#  CANADA					 CANADA
#
#

# A plugin to plot matplotlib / pylab scripts generated by JEN pynodes.
# Gratefully adapted from the matplotlib examples: embedding_in_qt.py
# and embedding_in_qt4.py

# modules that are imported




from Timba.dmi import *
from Timba import utils
from Timba.Meq import meqds
from Timba.Meq.meqds import mqs
from MeqGUI.GUI.pixmaps import pixmaps
from MeqGUI.GUI import widgets
from MeqGUI.GUI.browsers import *
from MeqGUI import Grid

from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QApplication, QMenu, QMainWindow, QVBoxLayout, QSizePolicy

from ResultsRange_qt5 import *
from BufferSizeDialog_qt5 import *

from numpy import arange, sin, cos, pi
import os, sys

# test if matplotlib / pylab is installed
global has_pylab
has_pylab = False
try:
  import matplotlib
  from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
  from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
  from matplotlib.figure import Figure
  import pylab
  has_pylab = True
except:
  print(' ')
  print('*** matplotlib/pylab not imported! ***')
  print('The system will assume that matplotlib is not present.')

from Timba.utils import verbosity
_dbg = verbosity(0,name='pylab_plotter');
_dprint = _dbg.dprint;
_dprintf = _dbg.dprintf;

if has_pylab:
 class MyPylabPlotter(FigureCanvas):
   
   def __init__(self, parent=None, dpi=100):
     self.fig = Figure(dpi=dpi)
     FigureCanvas.__init__(self, self.fig)
#    self.reparent(parent, QPoint(0, 0))
#    self.setParent(Qt.QWidget())
     FigureCanvas.setSizePolicy(self,
                                QSizePolicy.Expanding,
                                QSizePolicy.Expanding)
     FigureCanvas.updateGeometry(self)

   def sizeHint(self):
     w, h = self.get_width_height()
     return QSize(w, h)

   def minimumSizeHint(self):
     return QSize(10, 10)

   # The following method is adapted from 
   # matplotlib/examples/pythonic_matplotlib.py
   # It shows how you can approximate pylab calls
   # in a 'pythonic' manner which allows the plot
   # to be embedded in the MyPylabPlotter figure.
   def demo_pythonic_matplotlib(self):
     """Simple demo canvas with some sine plots."""
     t = arange(0.0, 1.0, 0.01)
     ax1 = self.fig.add_subplot(211)
     ax1.plot(t, sin(2*pi*t))
     ax1.grid(True)
     ax1.set_ylim( (-2,2) )
     ax1.set_ylabel('1 Hz')
     ax1.set_title('A sine wave or two')

     for label in ax1.get_xticklabels():
         label.set_color('r')

     ax2 = self.fig.add_subplot(212)
     ax2.plot(t, sin(2*2*pi*t))
     ax2.grid(True)
     ax2.set_ylim( (-2,2) )
     ax2.set_ylabel('2 Hz')
     l = ax2.set_xlabel('Hi mom')
     l.set_color('g')
     l.set_fontsize('large')

   # The following method causes a separate pylab figure to  
   # appear. 
   def demo_pylab_figure(self):
     """Simple demo canvas with a sine plot."""
     # create a separate pylab figure
     pylab.figure(1)   
     pylab.subplot(111)
     t = arange(0.0, 3.0, 0.01)
     s = sin(2*pi*t)
     pylab.plot(t, s)
     pylab.grid()
     pylab.title('Demonstration of Matplotlib pylab-style Plugin')
     pylab.xlabel('time')
     pylab.ylabel('sine')
     pylab.show()

   #-------------------------------------------------------------------------

   def make_plot(self, plot_defs):
     """Make a pylab plot from all items in plot_defs.
     """
     from Timba.Contrib.JEN.pylab import PyNodePlot
     PyNodePlot.make_pylab_figure(plot_defs, figob=self.fig)
     return None

#========================================================================

class PylabPlotter(GriddedPlugin):
  """ a class to visualize data from external pylab graphics files """

  _icon = pixmaps.bars3d
  viewer_name = "Pylab Plotter";
  def is_viewable (data):
    return len(data) > 0;
  is_viewable = staticmethod(is_viewable);

  def __init__(self,gw,dataitem,cellspec={},**opts):
    GriddedPlugin.__init__(self,gw,dataitem,cellspec=cellspec);
    """ a plugin for showing pylab plots """

    self._rec = None;
    self._wtop = None;
    self.dataitem = dataitem
    self.png_number = 0
    self.data_list = []
    self.data_list_labels = []
    self.data_list_length = 0
    self.max_list_length = 50
    self.layout_created = False
    self.counter = -1

    self.reset_plot_stuff()

# back to 'real' work
    if dataitem and dataitem.data is not None:
      self.set_data(dataitem);

  def reset_plot_stuff(self):
    """ resets widgets to None. Needed if we have been putting
        out a message about Cache not containing results, etc
    """
    self._pylab_plotter = None
    self._toolbar = None
    self.results_selector = None
    self.status_label = None
    self.layout_parent = None
    self.layout = None

  def wtop (self):
    """ function needed by Oleg for reasons known only to him! """
    return self._wtop;

  def create_layout_stuff(self):
    """ create grid layouts into which plotter widgets are inserted """
    if self.layout_parent is None or not self.layout_created:
      self.layout_parent = Qt.QWidget(self.wparent())
      self.layout = Qt.QGridLayout(self.layout_parent)
      self.set_widgets(self.layout_parent,self.dataitem.caption,icon=self.icon())
      self.layout_created = True
    self._wtop = self.layout_parent;       

  def set_data (self,dataitem,default_open=None,**opts):
    """ this callback receives data from the meqbrowser, when the
        user has requested a plot. It decides whether the data is
        from a VellSet or visu data record, and  after any
        necessary preprocssing forwards the data to one of
        the functions which does the actual plotting """

    _dprint(3, '** in pylab_plotter:set_data callback')

    if not has_pylab:
      Message = "Matplotlib does not appear to be installed so no plot can be made."
      cache_message = Qt.QLabel(Message,self.wparent())
#     cache_message.setTextFormat(Qt.RichText)
      self._wtop = cache_message
      self.set_widgets(cache_message)
      self.reset_plot_stuff()
      return

    self._rec = dataitem.data;
    _dprint(3, 'set_data: initial self._rec ', self._rec)
# if we are single stepping through requests, Oleg may reset the
# cache, so check for a non-data record situation
    if self._rec is None:
      return
    if isinstance(self._rec, bool):
      return

    self.label = '';  # extra label, filled in if possible
# there's a problem here somewhere ...
    if dmi_typename(self._rec) != 'MeqResult': # data is not already a result?
      # try to put request ID in label
      rq_id_found = False
      data_failure = False
      try:
        if "request_id" in self._rec.cache:
          self.label = "rq " + str(self._rec.cache.request_id);
          rq_id_found = True
        if "result" in self._rec.cache:
          self._rec = self._rec.cache.result; # look for cache.result record
          if not rq_id_found and "request_id" in self._rec:
            self.label = "rq " + str(self._rec.request_id);
        else:
          data_failure = True
        _dprint(3, 'we have req id ', self.label)
      except:
        data_failure = True
      if data_failure:
        _dprint(3, ' we have a data failure')
# cached_result not found, display an empty viewer with a "no result
# in this node record" message (the user can then use the Display with
# menu to switch to a different viewer)
        Message = "No cache result record was found for this node, so no plot can be made."
        cache_message = Qt.QLabel(Message,self.wparent())
#       cache_message.setTextFormat(Qt.RichText)
        self._wtop = cache_message
        self.set_widgets(cache_message)
        self.reset_plot_stuff()

        return
    
# update display with current data
    process_result = self.process_data()

# add this data set to internal list for later replay
    if process_result:
      if self.max_list_length > 0:
        self.data_list.append(self._rec)
        self.data_list_labels.append(self.label)
        if len(self.data_list_labels) > self.max_list_length:
          del self.data_list_labels[0]
          del self.data_list[0]
        if len(self.data_list) != self.data_list_length:
          self.data_list_length = len(self.data_list)
        if self.data_list_length > 1:
          _dprint(3, 'calling adjust_selector')
          self.adjust_selector()

  def process_data (self):
    """ process the actual record structure associated with a Cache result """
    process_result = False
# are we dealing with an pylab result?
    if "plotdefs" in self._rec:
      self.create_layout_stuff()
      self.show_pylab_plot()
      process_result = True

# enable & highlight the cell
    self.enable();
    self.flash_refresh();
    _dprint(3, 'exiting process_data')
    return process_result

  def replay_data (self, data_index):
    """ call to redisplay contents of a result record stored in 
        a results history buffer
    """
    if data_index < len(self.data_list):
      self._rec = self.data_list[data_index]
      self.label = self.data_list_labels[data_index]
      self.results_selector.setLabel(self.label)
      process_result = self.process_data()

  def show_pylab_plot(self, store_rec=True):
    """ process incoming data and attributes into the
        appropriate type of plot """

    # if we are single stepping through requests, Oleg may reset the
    # cache, so check for a non-data record situation
    if store_rec and isinstance(self._rec, bool):
      return

    pylab_record = self._rec.plotdefs
    if not self._pylab_plotter is None:
#     self._pylab_plotter.reparent(Qt.QWidget(), 0, Qt.QPoint())
      self._pylab_plotter.setParent(Qt.QWidget())
      self._pylab_plotter  = None
    if not self._toolbar is None:
#     self._toolbar.reparent(Qt.QWidget(), 0, Qt.QPoint())
      self._toolbar.setParent(Qt.QWidget())
      self._toolbar = None
    if self._pylab_plotter is None:
      self._pylab_plotter = MyPylabPlotter(parent=self.layout_parent)
      self.layout.addWidget(self._pylab_plotter,1,0)
      self._pylab_plotter.show()
    if self._toolbar is None:
      self._toolbar = NavigationToolbar(self._pylab_plotter, self.layout_parent)
      self._toolbar.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
      self.layout.addWidget(self._toolbar,0,0)
      self._toolbar.show()
    self._pylab_plotter.make_plot(pylab_record)
    
  # end show_pylab_plot()


  def set_results_buffer (self, result_value):
    """ callback to set the number of results records that can be
        stored in a results history buffer 
    """ 
    if result_value < 0:
      return
    self.max_list_length = result_value
    if len(self.data_list_labels) > self.max_list_length:
      differ = len(self.data_list_labels) - self.max_list_length
      for i in range(differ):
        del self.data_list_labels[0]
        del self.data_list[0]

    if len(self.data_list) != self.data_list_length:
      self.data_list_length = len(self.data_list)

    self.show_pylab_plot(store_rec=False)

  def adjust_selector (self):
    """ instantiate and/or adjust contents of ResultsRange object """
    if self.results_selector is None:
      self.results_selector = ResultsRange(self.layout_parent)
      self.results_selector.setMaxValue(self.max_list_length)
      self.results_selector.set_offset_index(0)
      self.results_selector.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
      self.layout.addWidget(self.results_selector,2,0)
      self.results_selector.show()
      QObject.connect(self.results_selector, PYSIGNAL('result_index'), self.replay_data)
      QObject.connect(self.results_selector, PYSIGNAL('adjust_results_buffer_size'), self.set_results_buffer)
    self.results_selector.set_emit(False)
    self.results_selector.setRange(self.data_list_length-1)
    self.results_selector.setLabel(self.label)
    self.results_selector.set_emit(True)

#Grid.Services.registerViewer(dmi_type('MeqResult',record),PylabPlotter,priority=10)
Grid.Services.registerViewer(meqds.NodeClass(),PylabPlotter,priority=50)

########################################
# stuff for testing
########################################
if has_pylab:
  class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
#                            "application main window",
#                            Qt.WType_TopLevel | Qt.WDestructiveClose)

        self.file_menu = QMenu('&File',self)
        self.file_menu.addAction('&Quit', self.fileQuit, Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        sc = MyPylabPlotter(self.main_widget, dpi=100)
        toolbar = NavigationToolbar(sc, self.main_widget)
        toolbar.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        l.addWidget(sc)
        l.addWidget(toolbar)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

# Produce a plot that is contained in MyPylabPlotter
        sc.demo_pythonic_matplotlib()
# Produce a plot that is separate from MyPylabPlotter
        sc.demo_pylab_figure()

    def fileQuit(self):
        exit(0)
#       sys.exit(app.exec_())

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        progname = os.path.basename(sys.argv[0])
        progversion = "0.1"
        QMessageBox.about(self, "About %s" % progname,
"""%(prog)s version %(version)s
Copyright \N{COPYRIGHT SIGN} 2005 Florent Rougon

This program is a simple example of a Qt application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
                          % {"prog": progname, "version": progversion})


def main( argv ):
  if has_pylab:
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
#   app.setMainWidget(aw)
    aw.show()
    sys.exit(app.exec_())
  else:
    print(' ')
    print('**** Sorry! It looks like matplotlib/pylab is not available! ****')


# Admire
if __name__ == '__main__':
  main(sys.argv)


