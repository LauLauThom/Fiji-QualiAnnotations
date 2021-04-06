'''
MULTI-CLASS CHECKBOX
This script can be used to manually classify full images or ROIs into user-defined categories.  
Mutliple categories can be assigned to an image using the checkboxes.
  
A first window pops up asking where to get the categories:
- Memory       : read persisted values from memory
- Active table : parse a prevous annotation table
- Text fiele   : read a text file with one category per row
     
A second window follows with text fields to edit the category names
Leaving a field empty results in removing this category.
    
Once OK the annotation window shows up with one checkbox per category.    
Clicking on the button will generate a new entry in a table with the image name and the category.    
It will also skip to the next slice for stacks.    
'''
#@ String  (Label="Read categories from", choices={"Text file", "Active table", "Memory"}, value="Memory" ) categorySource 
#@ File    (label="Text file (if selected above)", style="file", required=false) textFile
#@ String  (label="Browsing mode", choices={"stack", "directory"}) browse_mode
#@ Boolean (label="Run measure", value=false) run_measure 

from fiji.util.gui    import GenericDialogPlus
from ij 			  import Prefs 
from java.awt 		  import GridLayout, Button, Panel, Checkbox 
from QualiAnnotations.utils          import getCategoriesFrom, CustomDialog
from QualiAnnotations.CategoryDialog import CategoryDialog
import os  
  
class MainDialog(CustomDialog): 
	"""
	Main annotation dialog for this plugin 
	In this case the panel contains checkboxes 
	"""
	 
	def __init__(self,
				 panel,
				 browseMode="stack",
				 runMeasure=False):
		
		title = "Qualitative Annotations - multi-classes (checkboxes)"
		message = """Tick the categories corresponding to the current image, then click 'Add' or press the '+' key.
		To annotate ROI, draw a new ROI or select some ROI(s) in the RoiManager before clicking 'Add'/pressing '+'."""
		CustomDialog.__init__(self, title, message, panel) 
		
		self.addButton("Add new category", self) # the GUI also catches the event for this button too 
		self.addStringField("Comments", "") 
		self.addButton(CustomDialog.LABEL_ADD, self) 
		 
		self.browseMode = browseMode # important to define it before addDefaultOptions and nextSlice... 
		self.runMeasure = runMeasure 
		self.addDefaultOptions() 
 
	def fillTable(self, table): 
		'''Read checkbox state and update table'''   
		for checkbox in self.getPanel().getComponents(): 
			table.addValue( checkbox.getLabel(), checkbox.getState() ) 
	 
	def keyPressed(self, keyEvent): 
		"""Define shortcut: pressing any of the + key also adds to the table like the Add button"""  
		code = keyEvent.getKeyCode() 
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS:  
			self.defaultActionSequence() 
	 
	def makeCategoryComponent(self, category): 
		"""
		Generates a checkbox with the new category name, to add to the GUI 
		Overwrite the original method 
		"""
		stringCat = Prefs.get("annot.listCat", "") 
		newStringCat = stringCat + "," + category if stringCat else category 
		Prefs.set("annot.listCat", newStringCat) 
		 
		# Make a new checkbox with the category name 
		checkbox = Checkbox(category, False) 
		checkbox.setFocusable(False) # important to have the keybard shortcut working 
		return checkbox 
  
############### GUI - CATEGORY DIALOG  ############# 
textFilePath   = textFile.getPath() if textFile else "" 
listCategories = getCategoriesFrom(categorySource, textFilePath)
 
# Initialize a category dialog with list of categories 
catDialog = CategoryDialog(listCategories)    
catDialog.showDialog() 
 
# Recover fields from the formular    
if catDialog.wasOKed():     
	 
	# Loop over categories, adding a tickbox to the panel for each   
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns   
	 
	for category in catDialog.getListCategories():    
		 
		# Make a checkbox with the category name 
		box = Checkbox(category, False) 
		box.setFocusable(False) # important to have the keyboard shortcut working 
 
		# Add checkbox to the gui for this category    
		catPanel.add(box)    
	 
	## Initialize dialog 
	winButton = MainDialog(catPanel, browse_mode, run_measure)  
	winButton.showDialog()