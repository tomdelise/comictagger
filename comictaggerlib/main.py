"""
A python app to (automatically) tag comic archives
"""

"""
Copyright 2012  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import signal
import os
import traceback
import platform

import utils
import cli
from settings import ComicTaggerSettings
from options import Options

try:
	qt_available = True
	from PyQt4 import QtCore, QtGui
	from taggerwindow import TaggerWindow
except ImportError as e:
	qt_available = False
#---------------------------------------

def ctmain():
	utils.fix_output_encoding()

	opts = Options()
	opts.parseCmdLineArgs()

	settings = ComicTaggerSettings()
	
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	if not qt_available and not opts.no_gui:
		opts.no_gui = True
		print >> sys.stderr, "PyQt4 is not available.  ComicTagger is limited to command-line mode."
	
	if opts.no_gui:
		cli.cli_mode( opts, settings )
	else:
		app = QtGui.QApplication(sys.argv)
		
		if platform.system() != "Linux":
			img =  QtGui.QPixmap(ComicTaggerSettings.getGraphic('tags.png'))
			
			splash = QtGui.QSplashScreen(img)
			splash.show()
			splash.raise_()
			app.processEvents()
	
		try:			
			tagger_window = TaggerWindow( opts.file_list, settings )
			tagger_window.show()

			if platform.system() != "Linux":
				splash.finish( tagger_window )

			sys.exit(app.exec_())
		except Exception, e:
			QtGui.QMessageBox.critical(QtGui.QMainWindow(), "Error", "Unhandled exception in app:\n" + traceback.format_exc() )

    
    
    
