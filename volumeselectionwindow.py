"""
A PyQT4 dialog to select specific series/volume from list
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
import time
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QUrl,pyqtSignal
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from comicvinetalker import ComicVineTalker
from issueselectionwindow import IssueSelectionWindow
from issueidentifier import IssueIdentifier
from genericmetadata import GenericMetadata
from imagefetcher import  ImageFetcher
from progresswindow import IDProgressWindow
from settings import ComicTaggerSettings


class SearchThread( QtCore.QThread):

	searchComplete = pyqtSignal()
	progressUpdate = pyqtSignal(int, int)

	def __init__(self, series_name, cv_api_key, refresh):
		QtCore.QThread.__init__(self)
		self.series_name = series_name
		self.cv_api_key = cv_api_key
		self.refresh = refresh
		
	def run(self):
		comicVine = ComicVineTalker( self.cv_api_key )
		matches = self.cv_search_results = comicVine.searchForSeries( self.series_name, callback=self.prog_callback, refresh_cache=self.refresh )
	
		self.searchComplete.emit()
		
	def prog_callback(self, current, total):
		self.progressUpdate.emit(current, total)


class IdentifyThread( QtCore.QThread):

	identifyComplete = pyqtSignal( )
	identifyLogMsg = pyqtSignal( str )
	identifyProgress = pyqtSignal( int, int )

	def __init__(self, identifier):
		QtCore.QThread.__init__(self)
		self.identifier = identifier
		self.identifier.setOutputFunction( self.logOutput )
		self.identifier.setProgressCallback( self.progressCallback )

	def logOutput(self, text):
		self.identifyLogMsg.emit( text )

	def progressCallback(self, cur, total):
		self.identifyProgress.emit( cur, total )
				
	def run(self):
		matches =self.identifier.search()
		self.identifyComplete.emit( )
		


class VolumeSelectionWindow(QtGui.QDialog):

	def __init__(self, parent, cv_api_key, series_name, issue_number, comic_archive, settings):
		super(VolumeSelectionWindow, self).__init__(parent)
		
		uic.loadUi(os.path.join(ComicTaggerSettings.baseDir(), 'volumeselectionwindow.ui' ), self)
		
		self.settings = settings
		self.series_name = series_name
		self.issue_number = issue_number
		self.cv_api_key = cv_api_key
		self.volume_id = 0
		self.comic_archive = comic_archive

		self.twList.resizeColumnsToContents()	
		self.twList.currentItemChanged.connect(self.currentItemChanged)
		self.twList.cellDoubleClicked.connect(self.cellDoubleClicked)
		self.btnRequery.clicked.connect(self.requery)			
		self.btnIssues.clicked.connect(self.showIssues)	
		self.btnAutoSelect.clicked.connect(self.autoSelect)	
		
		self.show()
		QtCore.QCoreApplication.processEvents()

		self.performQuery()		
		self.twList.selectRow(0)


	def requery( self,  ):
		self.performQuery( refresh=True )
		self.twList.selectRow(0)

	def autoSelect( self ):

		self.iddialog = IDProgressWindow( self)
		self.iddialog.setModal(True)
		self.iddialog.rejected.connect( self.identifyCancel )
		self.iddialog.show()
		
		self.ii = IssueIdentifier( self.comic_archive, self.cv_api_key )
		
		md = GenericMetadata()
		md.series = self.series_name
		md.issueNumber = self.issue_number
		self.ii.setAdditionalMetadata( md )
		
		self.id_thread = IdentifyThread( self.ii )
		self.id_thread.identifyComplete.connect( self.identifyComplete )	
		self.id_thread.identifyLogMsg.connect( self.logIDOutput )	
		self.id_thread.identifyProgress.connect( self.identifyProgress )	
		
		self.id_thread.start()
		
		self.iddialog.exec_()

	def logIDOutput( self, text ):
		print text,
		self.iddialog.textEdit.ensureCursorVisible()
		self.iddialog.textEdit.insertPlainText(text)

	def identifyProgress( self, cur, total ):
		self.iddialog.progressBar.setMaximum( total )
		self.iddialog.progressBar.setValue( cur )

	def identifyCancel( self ):
		self.ii.cancel = True
		
	def identifyComplete( self ):

		matches = self.ii.match_list
		if len(matches) == 1:
			self.iddialog.accept()

			print "VolumeSelectionWindow found a match!!", matches[0]['volume_id'], matches[0]['issue_number']
			self.volume_id = matches[0]['volume_id']
			self.issue_number = matches[0]['issue_number']
			self.selectByID()
			self.showIssues()

	def showIssues( self ):
		selector = IssueSelectionWindow( self, self.settings, self.volume_id, self.issue_number )
		selector.setModal(True)
		selector.exec_()
		if selector.result():
			#we should now have a volume ID
			self.issue_number = selector.issue_number
			self.accept()
		return

	def selectByID( self ):
		for r in range(0, self.twList.rowCount()):
			volume_id, b = self.twList.item( r, 0 ).data( QtCore.Qt.UserRole ).toInt()
			if (volume_id == self.volume_id):
				self.twList.selectRow( r )
				break
		
	def performQuery( self, refresh=False ):
		
		self.progdialog = QtGui.QProgressDialog("Searching Online", "Cancel", 0, 100, self)
		self.progdialog.setWindowTitle( "Online Search" )
		self.progdialog.canceled.connect( self.searchCanceled )
		self.progdialog.setModal(True)

		self.search_thread = SearchThread( self.series_name, self.cv_api_key, refresh )
		self.search_thread.searchComplete.connect( self.searchComplete )	
		self.search_thread.progressUpdate.connect( self.searchProgressUpdate )	
		self.search_thread.start()

		QtCore.QCoreApplication.processEvents()
		self.progdialog.exec_()

	def searchCanceled( self ):
		print "query cancelled"
		self.search_thread.searchComplete.disconnect( self.searchComplete )	
		self.search_thread.progressUpdate.disconnect( self.searchProgressUpdate )	
		self.progdialog.canceled.disconnect( self.searchCanceled )
		self.progdialog.reject()
		QtCore.QTimer.singleShot(200, self.closeMe)

	def closeMe( self ):
		print "closeme"
		self.reject()


	def searchProgressUpdate( self , current, total ):
		self.progdialog.setMaximum(total)
		self.progdialog.setValue(current)

	def searchComplete( self ):
		self.progdialog.accept()

		self.cv_search_results = self.search_thread.cv_search_results
				
		self.twList.setSortingEnabled(False)

		while self.twList.rowCount() > 0:
			self.twList.removeRow(0)
	
		row = 0
		for record in self.cv_search_results: 
			self.twList.insertRow(row)

			item_text = record['name']  
			item = QtGui.QTableWidgetItem(item_text)			
			item.setData( QtCore.Qt.UserRole ,record['id'])
			item.setFlags(QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsEnabled)
			self.twList.setItem(row, 0, item)
			
			item_text = str(record['start_year'])  
			item = QtGui.QTableWidgetItem(item_text)			
			item.setFlags(QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsEnabled)
			self.twList.setItem(row, 1, item)

			item_text = record['count_of_issues']  
			item = QtGui.QTableWidgetItem(item_text)			
			item.setData(QtCore.Qt.DisplayRole, record['count_of_issues'])
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.twList.setItem(row, 2, item)
			
			if record['publisher'] is not None:
				item_text = record['publisher']['name']
				item = QtGui.QTableWidgetItem(item_text)			
				item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
				self.twList.setItem(row, 3, item)
				
			row += 1

		self.twList.resizeColumnsToContents()
		self.twList.setSortingEnabled(True)
		self.twList.sortItems( 2 , QtCore.Qt.DescendingOrder )
		self.twList.selectRow(0)
		self.twList.resizeColumnsToContents()

	
	def cellDoubleClicked( self, r, c ):
		self.showIssues()
		
	def currentItemChanged( self, curr, prev ):

		if curr is None:
			return
		if prev is not None and prev.row() == curr.row():
				return

		self.volume_id, b = self.twList.item( curr.row(), 0 ).data( QtCore.Qt.UserRole ).toInt()

		# list selection was changed, update the info on the volume
		for record in self.cv_search_results: 
			if record['id'] == self.volume_id:

				self.teDetails.setText ( record['description'] )

				self.labelThumbnail.setPixmap(QtGui.QPixmap(os.path.join(ComicTaggerSettings.baseDir(), 'nocover.png' )))
				
				url = record['image']['super_url']
				self.fetcher = ImageFetcher( )
				self.fetcher.fetchComplete.connect(self.finishRequest)
				self.fetcher.fetch( url, user_data=record['id'] )


	def finishRequest(self, image_data, user_data):
		# called when the image is done loading
		img = QtGui.QImage()
		img.loadFromData( image_data )	
		self.setCover( img )	


	def setCover( self, img ):
		self.labelThumbnail.setPixmap(QtGui.QPixmap(img))
