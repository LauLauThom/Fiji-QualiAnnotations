'''
This script can be used to manually classify full images from a stack into N user-defined categories.   
A first window pops up to request the number of categories.   
A second window follows asking for the name to use for those categories.   
Finally a third window will show up with one button per category.   
Clicking on the button will generate a new entry in a table with the image name and the category.   
It will also skip to the next slice for stacks.   
'''
#@ Integer (Label = "Number of categories", value=2, min=1, stepSize=1) N_category_
#@ Boolean (Label="Read categories from active table", value=False ) parse_table
#@ String  (label = "Browsing mode", choices={"stack", "directory"}) browse_mode

from ij.gui		    import GenericDialog
from ij 			import IJ, Prefs
from java.awt 		import GridLayout, Button, Panel, Checkbox
from QualiAnnotations import CustomDialog, CategoryDialog
import os 
 
class MainDialog(CustomDialog):
	"""
	Main annotation dialog for this plugin
	In this case the panel contains checkboxes
	"""
	
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
 
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############

# Initialize a category dialog with N categories
catDialog = CategoryDialog(N_category_, parse_table)   
catDialog.showDialog()
 
 
################# After OK clicking ###########   

# Recover fields from the formular   
if catDialog.wasOKed():    
	
	# Loop over categories, adding a tickbox to the panel for each  
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns  
	
	for category in catDialog.getCategoryNames():   
		
		# Make a checkbox with the category name
		box = Checkbox(category, False)
		box.setFocusable(False) # important to have the keybard shortcut working

		# Add checkbox to the gui for this category   
		catPanel.add(box)   
	
	## Initialize dialog
	title = "Qualitative Annotations - multi-classes (checkboxes)"
	message = """Tick the categories corresponding to the current image, then click 'Add' or press the '+' key.
	To annotate ROI, draw a new ROI or select some ROI(s) in the RoiManager before clicking 'Add'/pressing '+'."""
	
	winButton = MainDialog(title, message, catPanel, browse_mode) 
	winButton.showDialog()