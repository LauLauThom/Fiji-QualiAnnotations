from ij 			  import IJ, WindowManager 
from ij.plugin.filter import Analyzer
from ij.plugin.frame  import RoiManager
from ij.measure 	  import ResultsTable, Measurements
import os
from java.awt.event import ActionListener
from fiji.util.gui  import GenericDialogPlus


def getTable():
	''' Check if a table called Annotations or Annotations.csv exists otherwise open a new one'''
	win  = WindowManager.getWindow("Annotations")
	win2 = WindowManager.getWindow("Annotations.csv")
	
	if win: # different of None
		Table = win.getResultsTable()
		tableTitle = "Annotations"
		
	elif win2 : # different of None
		Table = win2.getResultsTable()
		tableTitle = "Annotations.csv"
		
	else:
		Table = ResultsTable()
		tableTitle = "Annotations"
	
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
	'''
	Model class for the plugin dialog for the manual classifier
	All plugin share the same backbone, but have a custom central panel that is passed via the constructor
	'''
	
	def __init__(self, title, message, panel):
		GenericDialogPlus.__init__(self, title)
		self.setModalityType(None) # like non-blocking generic dialog
		self.addMessage(message)
		self.addPanel(panel)
		self.addStringField("Comments", "")
	
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
		but it should call self.doAction()
		'''
		pass
	
	def doAction(self):
		'''
		Main function called if a button is clicked or shortcut called
		It does the default stuff (adding imageName...)
		+ it also calls the function fillTable which is implemented in descendant classes
		DO NOT OVERWRITE
		'''
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
		roi = imp.getRoi()
		if roi: 
			
			# Set properties of roi with new row
			for heading in Table.getHeadings():
				value = Table.getStringValue(heading, Table.size()-1)
				roi.setProperty(heading, value)
			
			if addRoi:
				# Add to Manager
				rm = getRoiManager()
				rm.addRoi(roi)
				roiName = rm.getRoi(rm.getCount()-1).getName()
			
			else: # the ROI might belong to the ROI Manager
				roiName = roi.getName()
			
			# Add roi name to table
			Table.addValue("Roi", roiName)
		 
		Table.show(tableTitle) # Update table	    
		#Table.updateResults() # only for result table but then addValue does not work !  
		  
		# Go to next slice  
		if doNext: nextSlice(imp)
		  
		# Bring back the focus to the button window (otherwise the table is in the front)  
		WindowManager.toFront(self)  


class AddDialog(CustomDialog):
	'''
	Descendant class for dialog of Checkbox and Dropdown plugins with a Add button
	The particularity is that the fillFunction is passed via the constructor
	'''
	
	def __init__(self, title, message, panel, fillFunction):
		CustomDialog.__init__(self, title, message, panel)
		self.function = fillFunction
	
	def fillTable(self, Table):
		self.function(Table)
	
	def keyPressed(self, keyEvent):
		'''Pressing any of the + key also adds to the table like the Add button''' 
		code = keyEvent.getKeyCode()
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS: 
			self.doAction()
		
		
class ButtonAction(ActionListener): # extends action listener   
	'''
	Generic class used to defined button actions
	The action is initialized with the dialog to be able to do stuff with it
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