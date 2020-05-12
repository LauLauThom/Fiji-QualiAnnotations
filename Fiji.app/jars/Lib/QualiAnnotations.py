from ij 			  import IJ, WindowManager 
from ij.plugin.filter import Analyzer
from ij.measure 	  import ResultsTable, Measurements
import os
from java.awt.event import ActionListener

def addDefaultOptions(dialog):
	'''Add stack mode choice, message and help button''' 
	
	# Add mode for stacks
	choice = ["slice", "stack"]
	dialog.addChoice("Stack mode : 1 table entry per", choice, choice[0])
	
	# Checkbox next slice and run Measure 
	dialog.addCheckbox("Auto next slice", True)
	dialog.addCheckbox("run 'Measure'", False)
	
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
		
def nextSlice(imp, stackMode, doNext=True):
	'''Go to next slice if stackMode=slice''' 
	if stackMode=="slice" and doNext: # if We have a stack and the current slice is not the last slice
		imp.setSlice(imp.currentSlice+1) 
	

def getImageDirAndName(imp, stackMode):
	
	fileInfo = imp.getOriginalFileInfo()
	
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
	'''Class defining what happened when the Add button is clicked'''  
	
	def __init__(self, dialog, fillFunction):
		super(ButtonAction, self).__init__()
		self.dialog = dialog
		self.fillFunction = fillFunction
	
	def actionPerformed(self, event):  
		'''Called when button Add is clicked'''  
  
		imp = IJ.getImage() # get current image  				
		
		# Get stack mode
		stackChoice = self.dialog.getChoices()[-1] # last dropdown
		stackMode   = stackChoice.getSelectedItem()
		
		# Check options
		checkboxes  = self.dialog.getCheckboxes()
		doNext      = checkboxes[-2].getState() # 1 before last
		doMeasure   = checkboxes[-1].getState() # last				
		
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
		 
		Table.show(tableTitle) # Update table	    
		#Table.updateResults() # only for result table but then addValue does not work !  
		  
		# Go to next slice  
		nextSlice(imp, stackMode, doNext)
		  
		# Bring back the focus to the button window (otherwise the table is in the front)  
		WindowManager.setWindow(self.dialog)  