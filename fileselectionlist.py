# coding=utf-8
"""
A PyQt4 widget for managing list of files
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

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4.QtCore import pyqtSignal

from settings import ComicTaggerSettings
from comicarchive import ComicArchive
from genericmetadata import GenericMetadata, PageType
from options import MetaDataStyle

class FileTableWidget( QTableWidget ):

	def __init__(self, parent ):
		super(FileTableWidget, self).__init__(parent)
		
		
		self.setColumnCount(5)
		self.setHorizontalHeaderLabels (["File", "Folder", "CR", "CBL", ""])
		self.horizontalHeader().setStretchLastSection( True )


class FileTableWidgetItem(QTableWidgetItem):
   def __lt__(self, other):
        return (self.data(Qt.UserRole).toBool() <
                other.data(Qt.UserRole).toBool())


class FileInfo(  ):
	def __init__(self, ca ):
		self.ca = ca

class FileSelectionList(QWidget):

	selectionChanged = pyqtSignal(QVariant)
	listCleared = pyqtSignal()

	def __init__(self, parent , settings ):
		super(FileSelectionList, self).__init__(parent)

		uic.loadUi(os.path.join(ComicTaggerSettings.baseDir(), 'fileselectionlist.ui' ), self)
		
		self.settings = settings
		#self.twList = FileTableWidget( self )
		#gridlayout = QGridLayout( self )
		#gridlayout.addWidget( self.twList )
		
		#self.twList.itemSelectionChanged.connect( self.itemSelectionChangedCB )
		self.twList.currentItemChanged.connect( self.currentItemChangedCB )
		
		self.currentItem = None
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.modifiedFlag = False
		
		selectAllAction = QAction("Select All", self)
		removeAction = QAction("Remove Selected Items", self)
		self.separator = QAction("",self)
		self.separator.setSeparator(True)
		
		selectAllAction.setShortcut( 'Ctrl+A' )
		removeAction.setShortcut( 'Ctrl+X' )
		
		selectAllAction.triggered.connect(self.selectAll)
		removeAction.triggered.connect(self.removeSelection)

		self.addAction(self.separator)
		self.addAction(selectAllAction)			
		self.addAction(removeAction)

	def addAppAction( self, action ):
		self.insertAction( self.separator , action )
	
	def setModifiedFlag( self, modified ):
		self.modifiedFlag = modified
		
	def selectAll( self ):
		self.twList.setRangeSelected( QTableWidgetSelectionRange ( 0, 0, self.twList.rowCount()-1, 3 ), True )

	def deselectAll( self ):
		self.twList.setRangeSelected( QTableWidgetSelectionRange ( 0, 0, self.twList.rowCount()-1, 3 ), False )
	
	def removeSelection( self ):
		row_list = []
		for item in self.twList.selectedItems():
			if item.column() == 0:
			    row_list.append(item.row())

		if len(row_list) == 0:
			return
		
		if self.twList.currentRow() in row_list:
			if not self.modifiedFlagVerification( "Remove Archive",
					"If you close this archive, data in the form will be lost.  Are you sure?"):
				return
		
		row_list.sort()
		row_list.reverse()

		self.twList.currentItemChanged.disconnect( self.currentItemChangedCB )

		for i in row_list:
			self.twList.removeRow(i)
			
		self.twList.currentItemChanged.connect( self.currentItemChangedCB )
		
		if self.twList.rowCount() > 0:
			self.twList.selectRow(0)
		else:
			self.listCleared.emit()
	
	def addPathList( self, pathlist ):
		filelist = []
		for p in pathlist:
			# if path is a folder, walk it recursivly, and all files underneath
			if os.path.isdir( unicode(p)):
				for root,dirs,files in os.walk( unicode(p) ):
					for f in files:
						filelist.append(os.path.join(root,unicode(f)))
			else:
				filelist.append(unicode(p))
			
		# we now have a list of files to add

		progdialog = QProgressDialog("", "Cancel", 0, len(filelist), self)
		progdialog.setWindowTitle( "Adding Files" )
		progdialog.setWindowModality(Qt.WindowModal)
		
		firstAdded = None
		self.twList.setSortingEnabled(False)
		for idx,f in enumerate(filelist):
			QCoreApplication.processEvents()
			if progdialog.wasCanceled():
				break
			progdialog.setValue(idx)
			row = self.addPathItem( f )
			if firstAdded is None and row is not None:
				firstAdded = row
			
		progdialog.close()
		if firstAdded is not None:
			self.twList.selectRow(firstAdded)
			
		self.twList.setSortingEnabled(True)
		
		#Maybe set a max size??
		self.twList.resizeColumnsToContents()

		
	def isListDupe( self, path ):
		r = 0
		while r < self.twList.rowCount():
			fi = self.twList.item(r, 0).data( Qt.UserRole ).toPyObject()
			if fi.ca.path == path:
				return True
			r = r + 1
			
		return False		
		
	def addPathItem( self, path):
		path = unicode( path )
		#print "processing", path
		
		if self.isListDupe(path):
			return None
		
		ca = ComicArchive( path )
		if self.settings.rar_exe_path != "":
			ca.setExternalRarProgram( self.settings.rar_exe_path )
			
		if ca.seemsToBeAComicArchive() :
			
			row = self.twList.rowCount()
			self.twList.insertRow( row )
			
			fi = FileInfo( ca )
			
			filename_item = QTableWidgetItem()
			folder_item =   QTableWidgetItem()
			cix_item =      FileTableWidgetItem()
			cbi_item =      FileTableWidgetItem()
				
			filename_item.setFlags(Qt.ItemIsSelectable| Qt.ItemIsEnabled)
			filename_item.setData( Qt.UserRole , fi )
			self.twList.setItem(row, 0, filename_item)
					
			folder_item.setFlags(Qt.ItemIsSelectable| Qt.ItemIsEnabled)
			self.twList.setItem(row, 1, folder_item)

			cix_item.setFlags(Qt.ItemIsSelectable| Qt.ItemIsEnabled)
			cix_item.setTextAlignment(Qt.AlignHCenter)
			self.twList.setItem(row, 2, cix_item)

			cbi_item.setFlags(Qt.ItemIsSelectable| Qt.ItemIsEnabled)
			cbi_item.setTextAlignment(Qt.AlignHCenter)
			self.twList.setItem(row, 3, cbi_item)
			
			self.updateRow( row )
			
			return row

	def updateRow( self, row ):
		fi = self.twList.item( row, 0 ).data( Qt.UserRole ).toPyObject()

		filename_item = self.twList.item( row, 0 )
		folder_item =   self.twList.item( row, 1 )
		cix_item =      self.twList.item( row, 2 )
		cbi_item =      self.twList.item( row, 3 )

		item_text = os.path.split(fi.ca.path)[0]
		folder_item.setText( item_text )
		folder_item.setData( Qt.ToolTipRole, item_text )

		item_text = os.path.split(fi.ca.path)[1]
		filename_item.setText( item_text )
		filename_item.setData( Qt.ToolTipRole, item_text )

		if fi.ca.hasCIX():
			cix_item.setCheckState(Qt.Checked)       
			cix_item.setData(Qt.UserRole, True)
		else:
			cix_item.setData(Qt.UserRole, False)
			cix_item.setCheckState(Qt.Unchecked)       

		if fi.ca.hasCBI():
			cbi_item.setCheckState(Qt.Checked)       
			cbi_item.setData(Qt.UserRole, True)
		else:
			cbi_item.setData(Qt.UserRole, False)
			cbi_item.setCheckState(Qt.Unchecked)
			
		# Reading these will force them into the ComicArchive's cache
		fi.ca.readCIX()
		fi.ca.hasCBI()

	def getSelectedArchiveList( self ):
		ca_list = []
		for r in range( self.twList.rowCount() ):
			item = self.twList.item(r, 0)
			if self.twList.isItemSelected(item):
				fi = item.data( Qt.UserRole ).toPyObject()
				ca_list.append(fi.ca)

		return ca_list
	
	def updateCurrentRow( self ):
		self.updateRow( self.twList.currentRow() )

	def updateSelectedRows( self ):
		self.twList.setSortingEnabled(False)
		for r in range( self.twList.rowCount() ):
			item = self.twList.item(r, 0)
			if self.twList.isItemSelected(item):
				self.updateRow( r )
		self.twList.setSortingEnabled(True)
			
	def currentItemChangedCB( self, curr, prev ):

		new_idx = curr.row()
		old_idx = -1
		if prev is not None:
			old_idx = prev.row()
		#print "old {0} new {1}".format(old_idx, new_idx)
		
		if old_idx == new_idx:
			return
			
		# don't allow change if modified
		if prev is not None and new_idx != old_idx:
			if not self.modifiedFlagVerification( "Change Archive",
						"If you change archives now, data in the form will be lost.  Are you sure?"):
				self.twList.currentItemChanged.disconnect( self.currentItemChangedCB )
				self.twList.setCurrentItem( prev )
				self.twList.currentItemChanged.connect( self.currentItemChangedCB )
				# Need to defer this revert selection, for some reason
				QTimer.singleShot(1, self.revertSelection)
				return

		fi = self.twList.item( new_idx, 0 ).data( Qt.UserRole ).toPyObject()		
		self.selectionChanged.emit( QVariant(fi))
		
	def revertSelection( self ):
		self.twList.selectRow( self.twList.currentRow() )
		
	
	def modifiedFlagVerification( self, title, desc):
		if self.modifiedFlag:
			reply = QMessageBox.question(self, 
			     self.tr(title), 
			     self.tr(desc),
			     QMessageBox.Yes, QMessageBox.No )
			     
			if reply != QMessageBox.Yes:
				return False
		return True
		
		
# Attempt to use a special checkbox widget in the cell.
# Couldn't figure out how to disable it with "enabled" colors
#w = QWidget()
#cb = QCheckBox(w)
#cb.setCheckState(Qt.Checked)
#layout = QHBoxLayout()
#layout.addWidget( cb )
#layout.setAlignment(Qt.AlignHCenter)
#layout.setMargin(2)
#w.setLayout(layout)
#self.twList.setCellWidget( row, 2, w )