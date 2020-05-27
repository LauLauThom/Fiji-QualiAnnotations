from ij 			  import IJ, WindowManager 
from ij.plugin.filter import Analyzer
from ij.plugin.frame  import RoiManager
from ij.measure 	  import ResultsTable, Measurements
import os
from java.awt.event import ActionListener
from fiji.util.gui  import GenericDialogPlus


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
	if fileInfo.directory:
		directory = fileInfo.directory.rstrip(os.path.sep) 
	else:
		directory = ""
	
	# Recover image name 
	if not imp.isStack() or stackMode == "stack":  # single image or 1 entry/stack
		filename = fileInfo.fileName
		
		if filename=="Untitled" or not filename: filename = imp.getWindow().getTitle()
	
	else: # Stack + mode Slice
		Stack = imp.getStack() 
		filename = Stack.getSliceLabel(imp.currentSlice) 
		 
		if filename is None: # the slice label can be empty sometimes 
			if imp.isHyperStack(): filename = "C:{},Z:{},T:{}".format(imp.getC(), imp.getZ(), imp.getT() )
			else: # 1D stack
				filename = 'Slice ' + str(imp.currentSlice)	 
				 
		else :  
			filename = filename.split('\n',1)[0] # can be useful when ImagesToStack/Import Sequence was used
	
	return directory, filename

def nextSlice(imp):
	if imp.isHyperStack(): imp.setT(imp.getT()+1)        # increment the time slider
	elif imp.isStack(): imp.setSlice(imp.currentSlice+1) # increment unique slider
	else:pass


class CustomDialog(GenericDialogPlus):
	'''Model class for the plugin dialog for the manual classifier'''
	
	def __init__(self, title):
		GenericDialogPlus.__init__(self, title)
		self.setModalityType(None) # like non-blocking generic dialog 
	
	def addDefaultOptions(self):
		# Add mode for stacks
		choice = ["slice", "stack"]
		self.addChoice("Stack mode : 1 table entry per", choice, choice[0])
		
		# Checkbox next slice and run Measure 
		self.addCheckbox("Add ROI to Manager", True)
		self.addCheckbox("run 'Measure'", False)
		self.addCheckbox("Auto next slice", True)
		
		# Add message about citation and doc
		self.addMessage("If you use this plugin, please cite : ***")
		self.addMessage("Documentation and generic analysis workflows available on the GitHub repo (click Help)")
		
		# Add Help button pointing to the github
		self.addHelp(r"https://github.com/LauLauThom/ImageJ-ManualClassifier")

		self.hideCancelButton()
	
	
	def fillTable(self, Table):
		'''
		Function defining custom command to check GUI and add to table
		It should be overwritten in the descendant classes
		'''
		pass
	
	def keyPressed(self, event):
		'''
		This function should be overwritten in descendant classes
		code = keyEvent.getKeyCode()
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS: 
			self.doAction()
		'''
		pass
	
	def doAction(self):
		'''called if button clicked or shortcut called'''
		imp = IJ.getImage() # get current image  				
		
		# Get stack mode
		stackChoice = self.getChoices()[-1] # last dropdown
		stackMode   = stackChoice.getSelectedItem()
		
		# Check options
		checkboxes  = self.getCheckboxes()
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
		self.fillTable(Table)
 
		# Read comment 
		stringField = self.getStringFields()[0] 
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
		if doNext: nextSlice(imp)
		  
		# Bring back the focus to the button window (otherwise the table is in the front)  
		WindowManager.toFront(self)  


class AddDialog(CustomDialog):
	'''Descendant class for dialog of Checkbox and Dropdown plugins with a Add button'''
	
	def __init__(self, title, fillFunction):
		CustomDialog.__init__(self, title)
		self.function = fillFunction
	
	def fillTable(self, Table):
		self.function(Table)
	
	def keyPressed(self, keyEvent):
		code = keyEvent.getKeyCode()
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS: 
			self.doAction()
		
		
class ButtonAction(ActionListener): # extends action listener   
	'''
	Generic class used to defined button actions
	- actionPerformed : Call when the button is clicked, here it calls the Action.main() passed to the constructor 
	'''  
	
	def __init__(self, dialog):
		ActionListener.__init__(self)
		self.dialog = dialog
	
	def actionPerformed(self, event):  
		'''
		Called when button is clicked
		'''
		self.dialog.doAction()