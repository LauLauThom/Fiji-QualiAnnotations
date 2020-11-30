from ij				  import IJ, WindowManager, Prefs
from ij.plugin.filter import Analyzer
from ij.plugin.frame  import RoiManager
from ij.measure		  import ResultsTable, Measurements
import os
from collections	import OrderedDict
from java.awt.event import ActionListener
from java.awt 		import Label, Component
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
	All plugin share the same backbone but have a custom central panel that is passed via the constructor
	
	Backbone
	--------
	- Message
	- Custom Panel
	- Add category button
	- Comments
	- Default options including
		-- add to Manager, nextSlice, runMeasurement
		-- citation message
		-- help button
	
	Daughter class should implement the following methods:
	- __init__ , if the plugin should have a different structure than the backbone above
	- makeCategoryComponent(category) which should return a new category component to add to the main dialog
	- addAction(), function when the button Add is pressed (add to table)
	- fillTable(table), function stating how to add to the table
	'''
	
	def __init__(self, title, message, panel):
		"""This can be overwritten to readjust the order or if some component are not needed"""
		GenericDialogPlus.__init__(self, title)
		self.setModalityType(None) # like non-blocking generic dialog
		self.addMessage(message)
		self.addPanel(panel)
		self.addButton("Add new category", self) # the GUI also catches the event for this button too
		self.addStringField("Comments", "")
		self.addButton("Add", self)
		self.addDefaultOptions()
	
	def getPanel(self):
		"""Return the panel contained in the GenericDialog"""
		return self.getComponent(1) # Might need to adapt it, if we add more items before the panel
	
	def actionPerformed(self, event):
		'''
		Handle buttons clicks, delegates to custom methods
		OK: save parameters in memory
		Add new category: delegate to addCategoryComponent() (should be overwritten in daughter)
		Add: delegate to addAction()
		NB: NEVER use getNext methods here, since we call them several time 
		'''
		sourceLabel = event.getSource().getLabel()
		if sourceLabel == "  OK  ":
			# Check options and save them in persistence
			checkboxes	= self.getCheckboxes()
			doMeasure	= checkboxes[-2].getState()
			doNext		= checkboxes[-1].getState()
			
			# Save them in preference
			Prefs.set("annot.doMeasure", doMeasure)
			Prefs.set("annot.doNext", doNext)
		
		
		elif sourceLabel == "Add new category":
			self.addCategoryComponent()
		
		elif sourceLabel == "Add":
			self.addAction()
		
		else:
			pass
			
		# Do the mother class usual action handling()
		GenericDialogPlus.actionPerformed(self, event)
	
	
	def addAction(self):
		"""
		Action following the action clicking the button "Add" 
		This method can be overwritten in descendant class, if more than the classical defaultActionSequence
		"""
		self.defaultActionSequence()
		
	def makeCategoryComponent(self, category):
		"""
		This method should return a new component (checkbox, button...) to add to the GUI when the button add new category is cliked
		This method should be overwritten in the daughter classes, it is illustrated here with a label
		"""
		return Label(category)
	
	def addCategoryComponent(self):
		"""
		Request a new category name, create the associated category component via the makeCategory method and update the dialog 
		"""
		newCategory = IJ.getString("Enter new category name", "new category")
		if not newCategory: return # if Cancelled (ie newCat=="") or empty field just dont go further 
		
		# Add new component to the gui for this category and repaint GUI
		newComponent = self.makeCategoryComponent(newCategory)
		if newComponent is None: return
		if not isinstance(newComponent, Component): raise TypeError("Expect a component to be added to the dialog")
		self.getPanel().add(newComponent) # component 1 is the panel
		self.validate() # recompute the layout and update the display
	
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
	
	
	def fillTable(self, table):
		'''
		Function defining custom command to check GUI and add to table
		It should be overwritten in the descendant classes
		'''
		pass
	
	def keyPressed(self, event):
		'''
		Handle keyboard shortcuts (either + or F1-F12)
		the method should be implemented in descendant classes
		but it should usually call self.defaultActionSequence()
		'''
		pass
	
	def getChosenDimension(self):
		"""Return 'time', 'channel' or 'Z-slice'"""
		listChoices = self.getChoices()
		return listChoices[0].getSelectedItem()
	
	def defaultActionSequence(self):
		"""
		Central function (DO NOT OVERWRITE) called if a button is clicked or shortcut called
		It trigger the following actions:
		- getting the current table
		- checking the GUI state (checkboxes, dropdown...)
		- running measurements if measure is selected
		- setting ROI attribute (if roi)
		- incrementing table counter
		- adding image directory and name to table
		- filling columns from GUI state using custom fillTable()
		- switching to next slice
		- displaying the annotation GUI to the front, important to catch next keyboard shortcuts
		"""
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