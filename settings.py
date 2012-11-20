"""
Settings class for comictagger app
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

#import sys
import os
import sys
import ConfigParser
import platform

import utils

class ComicTaggerSettings:

	settings_file = ""
	folder = ""
	
	rar_exe_path = ""
	unrar_exe_path = ""
	cv_api_key = ""
	
	# automatic settings
	last_selected_data_style = 0
	last_opened_folder = None
	last_main_window_width = 0
	last_main_window_height = 0
	last_main_window_x = 0
	last_main_window_y = 0
	
	# identifier settings
	id_length_delta_thresh = 5
	id_publisher_blacklist = "panini comics, abril, scholastic book services"
	
	@staticmethod
	def getSettingsFolder():
		if platform.system() == "Windows":
			return os.path.join( os.environ['APPDATA'], 'ComicTagger' )
		else:
			return os.path.join( os.path.expanduser('~') , '.ComicTagger')

	@staticmethod
	def baseDir():
		if platform.system() == "Darwin" and getattr(sys, 'frozen', None):
			return sys._MEIPASS
		elif platform.system() == "Windows":
			return "."
		else:
			return os.path.dirname(__file__)

		
	def __init__(self):
		
		self.config = ConfigParser.RawConfigParser()
		self.folder = ComicTaggerSettings.getSettingsFolder()
		
		if not os.path.exists( self.folder ):
			os.makedirs( self.folder )
		
		self.settings_file = os.path.join( self.folder, "settings")
		
		# if config file doesn't exist, write one out
		if not os.path.exists( self.settings_file ):
			self.save()
		else:
			self.load()
		
		# take a crack at finding rar exes, if not set already
		if self.rar_exe_path == "":
			if platform.system() == "Windows":
				# look in some likely places for windows machine
				if os.path.exists( "C:\Program Files\WinRAR\Rar.exe" ):
					self.rar_exe_path = "C:\Program Files\WinRAR\Rar.exe"
				elif os.path.exists( "C:\Program Files (x86)\WinRAR\Rar.exe" ):
					self.rar_exe_path = "C:\Program Files (x86)\WinRAR\Rar.exe"
			else:
				# see if it's in the path of unix user
				if utils.which("rar") is not None:
					self.rar_exe_path = utils.which("rar")
			if self.rar_exe_path != "":
				self.save()
					
		if self.unrar_exe_path == "":
			if platform.system() != "Windows":
				# see if it's in the path of unix user
				if utils.which("unrar") is not None:
					self.unrar_exe_path = utils.which("unrar")
			if self.unrar_exe_path != "":
				self.save()

	def load(self):
		
		self.config.read( self.settings_file )
		
		self.rar_exe_path =    self.config.get( 'settings', 'rar_exe_path' )
		self.unrar_exe_path =  self.config.get( 'settings', 'unrar_exe_path' )
		#self.cv_api_key =      self.config.get( 'settings', 'cv_api_key' )
    
		self.last_selected_data_style =  self.config.getint( 'auto', 'last_selected_data_style' )
		self.last_opened_folder =        self.config.get( 'auto', 'last_opened_folder' )
		if self.config.has_option('auto', 'last_main_window_width'):
			self.last_main_window_width =    self.config.getint( 'auto', 'last_main_window_width' )
		if self.config.has_option('auto', 'last_main_window_height'):
			self.last_main_window_height =   self.config.getint( 'auto', 'last_main_window_height' )
		if self.config.has_option('auto', 'last_main_window_x'):
			self.last_main_window_x =   self.config.getint( 'auto', 'last_main_window_x' )
		if self.config.has_option('auto', 'last_main_window_y'):
			self.last_main_window_y =   self.config.getint( 'auto', 'last_main_window_y' )

		if self.config.has_option('identifier', 'id_length_delta_thresh'):
			self.id_length_delta_thresh =   self.config.getint( 'identifier', 'id_length_delta_thresh' )
		if self.config.has_option('identifier', 'id_publisher_blacklist'):
			self.id_publisher_blacklist =        self.config.get( 'identifier', 'id_publisher_blacklist' )
    
	def save( self ):

		if not self.config.has_section( 'settings' ):
			self.config.add_section( 'settings' )
			
		#self.config.set( 'settings', 'cv_api_key',     self.cv_api_key )
		self.config.set( 'settings', 'rar_exe_path',   self.rar_exe_path )
		self.config.set( 'settings', 'unrar_exe_path', self.unrar_exe_path )

		if not self.config.has_section( 'auto' ):
			self.config.add_section( 'auto' )

		self.config.set( 'auto', 'last_selected_data_style', self.last_selected_data_style )
		self.config.set( 'auto', 'last_opened_folder', self.last_opened_folder )
		self.config.set( 'auto', 'last_main_window_width', self.last_main_window_width )
		self.config.set( 'auto', 'last_main_window_height', self.last_main_window_height )
		self.config.set( 'auto', 'last_main_window_x', self.last_main_window_x )
		self.config.set( 'auto', 'last_main_window_y', self.last_main_window_y )

		if not self.config.has_section( 'identifier' ):
			self.config.add_section( 'identifier' )

		self.config.set( 'identifier', 'id_length_delta_thresh', self.id_length_delta_thresh )
		self.config.set( 'identifier', 'id_publisher_blacklist', self.id_publisher_blacklist )
			
		with open( self.settings_file, 'wb') as configfile:
			self.config.write(configfile)    
    
    
    
