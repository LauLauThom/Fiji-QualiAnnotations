from ij				  import IJ, WindowManager, Prefs
from ij.plugin.filter import Analyzer
from ij.plugin.frame  import RoiManager
from ij.measure		  import ResultsTable, Measurements
import os
from collections	import OrderedDict
from java.awt.event import ActionListener
from fiji.util.gui	import GenericDialogPlus

hyperstackDim = ["time", "channel", "Z-slice"]


def getTable():
	''' Check if a table called Annotations or Annotations.csv exists otherwise open a new one'''
	win	 = WindowManager.getWindow("Annotations")
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
	"""
	Return existing RoiManager or create a new instance if no existing one.
	Always display the RoiManager
	"""
	rm = RoiManager.getInstance()
	if not rm: rm = RoiManager() # create a new instance
	return rm

def getImageDirAndName(imp):
	
	out = OrderedDict([("Folder",""), 
					   ("Image", "")])
	
	fileInfo = imp.getOriginalFileInfo()
	
	# Recover image directory
	if fileInfo and fileInfo.directory:
		directory = fileInfo.directory.rstrip(os.path.sep) # remove the last slash of the directory path
		out["Folder"] = directory

	# Get image name 
	imageName = ""
	if fileInfo: 
		imageName = fileInfo.fileName
	
	if imageName=="Untitled" or not imageName: 
		imageName = imp.getWindow().getTitle()
		
	# Populate Image field
	out["Image"]  = imageName
	
	# Get slice name 
	if imp.isStack():
		Stack = imp.getStack() 

		# Slice name
		sliceName = Stack.getSliceLabel(imp.currentSlice) 
		 
		if sliceName is None: # the slice label can be empty sometimes 
			if imp.isHyperStack(): 
				sliceName = "C:{},Z:{},T:{}".format(imp.getC(), imp.getZ(), imp.getT() )
			else: # 1D stack
				sliceName = 'Slice ' + str(imp.currentSlice)	 
			 
		else :
			sliceName = sliceName.split('\n',1)[0] # can be useful when ImagesToStack/Import Sequence was used
	
		out["Slice"] = sliceName 
	
	return out

def nextSlice(imp, dimension):
	"""Display next slice, dimension should be 'time', 'channel' or 'Z-slice' """
	if imp.isHyperStack(): 
		
		if dimension == hyperstackDim[0]:
			imp.setT( imp.getT()+1 )		 # increment the time slider
		
		elif dimension == hyperstackDim[1]:
			imp.setC( imp.getC()+1 )
		
		elif dimension == hyperstackDim[2]:
			imp.setZ( imp.getZ()+1 )
		
		else:
			pass
			
	elif imp.isStack(): imp.setSlice(imp.currentSlice+1) # increment unique slider
	
	else:pass

def setRoiProperties(roi, table):
	"""
	Set the roi property as the value of the last table row 
	"""
	for heading in table.getHeadings():
		value = table.getStringValue(heading, table.size()-1)
		roi.setProperty(heading, value)


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
	
	def actionPerformed(self, event):
		'''Overwrite default: to save parameters in memory when ok is clicked'''
		
		if event.getSource().getLabel() == "  OK  ":
			
			# Check options
			checkboxes	= self.getCheckboxes()
			doMeasure	= checkboxes[-2].getState()
			doNext		= checkboxes[-1].getState()
			
			# Save them in preference
			Prefs.set("annot.doMeasure", doMeasure)
			Prefs.set("annot.doNext", doNext)
			
		# Do the mother class usual action handling()
		GenericDialogPlus.actionPerformed(self, event)
	
	
	def addDefaultOptions(self):
		'''
		Add default GUI items
		- add to Manager, nextSlice, runMeasurement
		- citation message
		- help button
		'''
		# Checkbox next slice and run Measure 
		self.addCheckbox("run 'Measure'", bool(Prefs.get("annot.doMeasure", False)) )
		self.addCheckbox("Auto next slice", bool(Prefs.get("annot.doNext", True)) )
		self.addToSameRow()
		self.addChoice("dimension (for hyperstack)", hyperstackDim, hyperstackDim[0])
		
		# Add message about citation and doc
		self.addMessage("""If you use this plugin, please cite : 
		
		Thomas LSV, Schaefer F and Gehrig J.
		Fiji plugins for qualitative image annotations: routine analysis and application to image classification
		[version 1; peer review: awaiting peer review]
		F1000Research 2020, 9:1248
		https://doi.org/10.12688/f1000research.26872.1""")
		
		self.addMessage("Documentation and generic analysis workflows available on the GitHub repo (click Help)")
		
		# Add Help button pointing to the github
		self.addHelp(r"https://github.com/LauLauThom/Fiji-QualiAnnotations")

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
	
	def getChosenDimension(self):
		"""Return 'time', 'channel' or 'Z-slice'"""
		listChoices = self.getChoices()
		return listChoices[0].getSelectedItem()
	
	def doAction(self):
		'''
		Main function called if a button is clicked or shortcut called
		It does the default stuff (adding imageName...)
		+ it also calls the function fillTable which is implemented in descendant classes
		DO NOT OVERWRITE
		'''
		imp = IJ.getImage() # get current image
		
		# Get current table
		tableTitle, Table = getTable()
		Table.showRowNumbers(True)
		
		# Check options, use getCheckboxes(), because the checkbox plugin have other checkboxes
		checkboxes	= self.getCheckboxes()
		
		# Initialize Analyzer
		doMeasure = checkboxes[-2].getState()
		if doMeasure:
			analyzer = Analyzer(imp, Table)
			analyzer.setMeasurement(Measurements.LABELS, False) # dont add label to table
		
		# Check if existing roi manager
		rm = RoiManager.getInstance()
		indexes = rm.getSelectedIndexes() if rm else [] # Check if roi selected
		
		if indexes:
			
			# Loop over selected ROI
			for index in indexes: # set selected features as property of rois
				
				roi = rm.getRoi(index)
				imp.setRoi(roi)
				
				# Run measure for the ROI
				if doMeasure: # Automatically increment counter
					analyzer.measure() # as selected in Set Measurements
					
				else:
					Table.incrementCounter() # Automatically done if doMeasure 
				
				#Table.addValue("Index", Table.getCounter() )  
				for key, value in getImageDirAndName(imp).iteritems():
					Table.addValue(key, value) 
				
				# Add selected items (implementation-specific)
				self.fillTable(Table)
		 
				# Read comment 
				stringField = self.getStringFields()[0] 
				Table.addValue("Comment", stringField.text)

				# Add roi name to the table + set its property
				Table.addValue("Roi", roi.getName()) # Add roi name to table
				setRoiProperties(roi, Table)
					
		# No roi selected in the Manager
		else:
		
			if doMeasure: # also automatically increment counter
				analyzer.measure() # as selected in Set Measurements
				
			else:
				Table.incrementCounter() # Automatically done if doMeasure 
			
			#Table.addValue("Index", Table.getCounter() )  
			for key, value in getImageDirAndName(imp).iteritems():
				Table.addValue(key, value) 

			# Add selected items (implementation-specific)
			self.fillTable(Table)
	 
			# Read comment 
			stringField = self.getStringFields()[0] 
			Table.addValue("Comment", stringField.text) 
			
			# Check if an active Roi, not yet present in Manager
			roi = imp.getRoi()
			
			if roi is not None:
				roi.setPosition(imp) 
				rm = getRoiManager()
				rm.addRoi(roi)
				
				# get back the roi from the manager to set properties
				roiBis	= rm.getRoi(rm.getCount()-1) 
				roiName = roiBis.getName()
				Table.addValue("Roi", roiName) # Add roi name to table
				setRoiProperties(roiBis, Table)
		
		Table.show(tableTitle) # Update table		
		#Table.updateResults() # only for result table but then addValue does not work !  
		  
		# Go to next slice
		doNext    = checkboxes[-1].getState()
		if doNext: nextSlice(imp, self.getChosenDimension() )
		  
		# Bring back the focus to the button window (otherwise the table is in the front)  
		if not IJ.getFullVersion().startswith("1.52p"): WindowManager.toFront(self)	 # prevent some ImageJ bug with 1.52p


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