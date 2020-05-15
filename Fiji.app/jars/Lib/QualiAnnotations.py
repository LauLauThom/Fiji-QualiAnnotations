from ij 			  import IJ, WindowManager 
from ij.plugin.filter import Analyzer
from ij.plugin.frame  import RoiManager
from ij.measure 	  import ResultsTable, Measurements
import os
from java.awt.event import ActionListener

def addDefaultOptions(dialog):
	'''Add stack mode choice, message and help button''' 
	
	# Add mode for stacks
	choice = ["slice", "stack"]
	dialog.addChoice("Stack mode : 1 table entry per", choice, choice[0])
	
	# Checkbox next slice and run Measure 
	dialog.addCheckbox("Add ROI to Manager", True)
	dialog.addCheckbox("run 'Measure'", False)
	dialog.addCheckbox("Auto next slice", True)
	
	# Add message about citation and doc
	dialog.addMessage("If you use this plugin, please cite : ***")
	dialog.addMessage("Documentation and generic analysis workflows available on the GitHub repo (click Help)")
	
	# Add Help button pointing to the github
	dialog.addHelp(r"https://github.com/LauLauThom/ImageJ-ManualClassifier")

	dialog.hideCancelButton() 
	

def getTable():
	'''Check if a table is open and get its name'''
	# Check if a table called Classification or Classification.csv exists otherwise open a new one
	win  = WindowManager.getWindow("Classification")
	win2 = WindowManager.getWindow("Classification.csv")
	
	if win: # different of None
		Table = win.getResultsTable()
		tableTitle = "Classification"
		
	elif win2 : # different of None
		Table = win2.getResultsTable()
		tableTitle = "Classification.csv"
		
	else:
		Table = ResultsTable()
		tableTitle = "Classification"
	
	return tableTitle, Table

def getRoiManager():
	rm = RoiManager.getInstance()
	if not rm: rm = RoiManager() # create a new instance
	return rm

def getImageDirAndName(imp, stackMode):
	
	fileInfo = imp.getOriginalFileInfo()
	if not fileInfo: return "", ""
	
	# Recover image directory
	directory = fileInfo.directory.rstrip(os.path.sep) 
	
	# Recover image name 
	if imp.getStackSize()==1 or stackMode == "stack":  # single image or 1 entry/stack
		filename = fileInfo.fileName
	
	else: 
		Stack = imp.getStack() 
		filename = Stack.getSliceLabel(imp.currentSlice) 
		 
		if filename is None: # the slice label can be empty sometimes 
			filename = 'Slice' + str(imp.currentSlice)	 
				 
		else :  
			filename = filename.split('\n',1)[0] # can be useful when ImagesToStack/Import Sequence was used
	
	return directory, filename
	

class ButtonAction(ActionListener): # extends action listener   
	'''
	Generic class used to defined button actions
	In particular it contains 2 key functions
	- actionPerformed : Call when the button is clicked, this method does the default action + a custom action define in fillFunction
	- fillFunction(Table) : Allows to perform custom action on the table, it is called by actionPErformed and thus executed on button-clicks
	'''  
	
	def __init__(self, dialog):
		ActionListener.__init__(self)
		self.dialog = dialog
	
	def fillFunction(self, Table):
		'''
		Function to overwrite in descendant classes, used to add custom item to table.
		It is called by action performed and thus executed when button is clicked
		'''
		pass
	
	def actionPerformed(self, event):  
		'''
		Called when button is clicked, no need to overwrite
		It adds default column contents (image path + measures)
		It also calls FillFunction
		'''  
  
		imp = IJ.getImage() # get current image  				
		
		# Get stack mode
		stackChoice = self.dialog.getChoices()[-1] # last dropdown
		stackMode   = stackChoice.getSelectedItem()
		
		# Check options
		checkboxes  = self.dialog.getCheckboxes()
		addRoi      = checkboxes[-3].getState()
		doMeasure   = checkboxes[-2].getState()
		doNext      = checkboxes[-1].getState()
		
		# Get current table
		tableTitle, Table = getTable()
		Table.showRowNumbers(True)
		
		if doMeasure: # Automatically increment counter
			analyzer = Analyzer(imp, Table)
			analyzer.setMeasurement(Measurements.LABELS, False) # dont add label to table
			analyzer.measure() # as selected in Set Measurements

		else:
			Table.incrementCounter() # Automatically done if doMeasure 
		
		# Recover image name  
		directory, filename = getImageDirAndName(imp, stackMode)
		#Table.addValue("Index", Table.getCounter() )  
		Table.addValue("Folder", directory) 
		Table.addValue("Image", filename)

		# Add selected items (implementation-specific)
		self.fillFunction(Table)
 
		# Read comment 
		stringField = self.dialog.getStringFields()[0] 
		Table.addValue("Comment", stringField.text) 
		
		# Add Roi to RoiManager + set its properties
		if addRoi:
			roi = imp.getRoi()
			if roi: 
				
				# Set properties of roi with new row
				for heading in Table.getHeadings():
					value = Table.getStringValue(heading, Table.size()-1)
					roi.setProperty(heading, value)
				
				# Add to Manager
				rm = getRoiManager()
				rm.addRoi(roi)
				
				# Add roi name to table
				roiName = rm.getRoi(rm.getCount()-1).getName()
				Table.addValue("Roi", roiName)
		 
		Table.show(tableTitle) # Update table	    
		#Table.updateResults() # only for result table but then addValue does not work !  
		  
		# Go to next slice  
		if doNext: imp.setSlice(imp.currentSlice+1)
		  
		# Bring back the focus to the button window (otherwise the table is in the front)  
		WindowManager.setWindow(self.dialog)  


class AddButtonAction(ButtonAction):
	'''Class for Add button used by checkbox and dropdown plugin'''
	
	def __init__(self, dialog, function):
		ButtonAction.__init__(self, dialog)
		self.function = function
	
	def fillFunction(self, Table):
		self.function(Table)