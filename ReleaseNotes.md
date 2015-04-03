### 1.1.15-beta ###
13-Jun-2014
  * WebP support
  * Added user-configurable API key for Comic Vine access
  * Experimental option to wait and retry after exceeding Comic Vine rate limit

### 1.1.14-beta ###
18-Apr-2014
  * Make sure app gets raised when enforcing single instance
  * Added warning dialog for when opening rar files, and no (un)rar tool
  * remove pil from python package requirements

### 1.1.13-beta ###
9-Apr-2014
  * Handle non-ascii usernames properly
  * better parsing of html table in summary text, and optional removal
  * Python package should auto-install requirements
  * Specify default GUI tag style on command-line
  * enforce single GUI instance
  * new CBL transform to copy story arcs to generic tags
  * Persist some auto-tag settings

### 1.1.12-beta ###
23-Mar-2014
  * Fixed noisy version update error

### 1.1.11-beta ###
23-Mar-2014
  * Updated unrar library to hand Rar tools 5.0 and greater
  * Other misc bug fixes

### 1.1.10-beta ###
30-Jan-2014
  * Updated series query to match changes on Comic Vine side
  * Added a message when not able to open a file or folder
  * Fixed an issue where series names with periods would fail on search
  * Other misc bug fixes

### 1.1.9-beta ###
8-May-2013
  * Filename parser and identification enhancements
  * Misc bug fixes

### 1.1.8-beta ###
21-Apr-2013
  * Handle occasional error 500 from Comic Vine by retrying a few times
  * Nicer handling of colon (":") in file rename
  * Fixed command-line option parsing issue for add-on scripts
  * Misc bug fixes


### 1.1.7-beta ###
12-Apr-2013
  * Added description and cover date to issue selection dialogs
  * Added notification of new version
  * Added setting to attempt to parse scan info from file name
  * Last sorted column in the file list is now remembered
  * Added CLI option ('-1') to assume [issue #1](https://code.google.com/p/comictagger/issues/detail?id=#1) if not found/parsed
  * Misc bug fixes

### 1.1.6-beta ###
03-Apr-2013
  * More ComicVine API-related fixes
  * More efficient automated search using new CV API issue filters
  * Minor bug fixes

### 1.1.5-beta ###
30-Mar-2013
  * More updates for handling changes to ComicVine API and result sets
  * Even better handling of non-numeric issue "numbers" ("½", "X")

### 1.1.4-beta ###
27-Mar-2013
  * Updated to match the changes to the ComicVine API and result sets
  * Better handling of weird issue numbers ("0.1", "6au")

### 1.1.3-beta ###
25-Feb-2013
#### Bug Fixes ####
  * Fixed a bug when renaming on non-English systems
  * Fixed issue when saving settings on non-English systems
  * Fixed a rare crash when comic image is not-RGB format
  * Fixed sequence order of ComicInfo.xml items

Note:
> New requirement for users of the python package:  "configparser"


### 1.1.2-beta ###
14-Feb-2013
#### Changes ####
  * Source is now packaged using Python distutils
  * Recursive mode for CLI
  * Run custom add-on scripts from CLI
  * Minor UI tweaks
  * Misc bug fixes

### 1.1.0-beta ###
06-Feb-2013
#### Changes ####
  * Enhanced identification process now uses alternative covers from ComicVine
  * Post auto-tag manual matching now includes single low-confidence matches (CLI & GUI)
  * Page and cover view mini-browser available throughout app.  Most images can be double-clicked for embiggened view
  * Export-to-zip in CLI (very handy in scripts!)
  * More rename template variables
  * Misc GUI & CLI Tweaks

### 1.0.3-beta ###
31-Jan-2013

#### Changes ####
> Misc bug fixes and enhancements

### 1.0.2-beta ###
25-Jan-2013

#### Changes ####
  * More verbose logging during auto-tag
  * Added %month% and %month\_name% for renaming
  * Better parsing of volume numbers in file name
#### Bug Fixes ####
  * Better exception handling with corrupted image data
  * Fixed issues with RAR reading on OS X
  * Other minor bug fixes

### 1.0.1-beta ###
23-Jan-2013

Bug Fix:
**Fixed an issue where unicode strings can't be printed to OS X Console**

### 1.0.0-beta ###
23-Jan-2013

Version 1!  New multi-file processing in GUI!

#### GUI Changes ####
  * Open multiple files and/or folders via drag/drop or file dialog
  * File management list for easy viewing and selection
  * Batch tag remove
  * Batch export as zip
  * Batch rename
  * Batch tag copy
  * Batch auto-tag (automatic identification and save!)

### 0.9.5-beta ###
16-Jan-2013

#### Changes ####
  * Added CLI option to search by comicvine issue ID
  * Some image loading optimizations
  * Bug Fix:  Some CBL fields that should have been ints were written as strings

### 0.9.4-beta ###
7-Jan-2013

#### Changes ####
  * Better handling of non-ascii characters in filenames and data
  * Add CBL Transform to copy Web Link and Notes to comments
  * Minor bug fixes

### 0.9.3-beta ###
19-Dec-2012

#### Changes ####
  * File rename in GUI
  * Setting for file rename
  * Option to use series start year as volume
  * Added "CBL Transform" to handle primary credits copying data into the generic tags field
  * Bug Fix:  unicode characters in credits caused crash
  * Bug Fix:  bad or non-image data in file caused crash

#### Note ####
The user should clear the cache and delete the existing settings when first running this version.

### 0.9.2-beta ###
12-Dec-2012
  * Page List/Type editing in GUI
  * File globbing for windows CLI (i.e. use of wildcards like '`*`.cbz')
  * Fixed RAR writing bug on windows
  * Minor bug and crash fixes

### 0.9.1-beta ###
07-Dec-2012

  * Export as ZIP Archive
  * Added help menu option for websites
  * Added Primary Credit Flag editing
  * Menu enhancements
  * CLI Enhancements:
    * Interactive selection of matches
    * Tag copy
    * Better output
    * CoMet support
  * Minor bug and crash fixes


### 0.9.0-beta ###
30-Nov-2012

Initial beta release