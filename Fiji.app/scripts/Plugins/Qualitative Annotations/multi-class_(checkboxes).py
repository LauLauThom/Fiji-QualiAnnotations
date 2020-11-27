#@ Integer (Label = "Number of categories", value=2, min=1, stepSize=1) N_category_   
#@ PrefService pref   
#@ ImageJ ij   
'''
This script can be used to manually classify full images from a stack into N user-defined categories.   
A first window pops up to request the number of categories.   
A second window follows asking for the name to use for those categories.   
Finally a third window will show up with one button per category.   
Clicking on the button will generate a new entry in a table with the image name and the category.   
It will also skip to the next slice for stacks.   
'''
from ij.gui		    import GenericDialog   
from java.awt 		import GridLayout, Button, Panel, Checkbox
from java.awt.event import ActionListener
from collections 	import OrderedDict 
from QualiAnnotations import CustomDialog, ButtonAction
import os 
 
class MainDialog(CustomDialog):
	"""
	Main annotation dialog for this plugin
	In this case the panel contains checkboxes
	"""
	
	def __init__(self, title, message, panel):
		CustomDialog.__init__(self, title, message, panel)
		self.panel = panel # Expose the panel to the other functions
	
	def fillTable(self, table):
		'''Read checkbox state and update table'''  
		for checkbox in self.panel.getComponents():
			table.addValue( checkbox.getLabel(), checkbox.getState() )
	
	def keyPressed(self, keyEvent):
		'''Pressing any of the + key also adds to the table like the Add button''' 
		code = keyEvent.getKeyCode()
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS: 
			self.doAction()
 
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############
listCat = pref.getList(ij.class, "listCat_")  # try to retrieve the list of categories from the persistence, if not return [] - ij.class workaround see https://forum.image.sc/t/store-a-list-using-the-persistence-prefservice/26449   

# Add N string fields to the dialog for class names   
catDialog = GenericDialog("Categories names")   

for i in range(N_category_):
	
	if listCat and i<=len(listCat)-1:  # read previous categories
		catName = listCat[i]  
	
	else:  
		catName = "Category_" + str(i+1)   
	  
	catDialog.addStringField("Category: ", catName)   
	catDialog.addMessage("") # skip one line   
	   
catDialog.showDialog()   
 
 
################# After OK clicking ###########   
class NewCategoryAction(ActionListener): # extends action listener	
	
	def __init__(self):
		ActionListener.__init__(self)
	
	def actionPerformed(self, event):  
		'''
		Called when button "Add new category" is clicked
		'''
		# Prompt a string input
		# Recover the new category name
		# close the winButton and redisplay it
		pass
		
# Recover fields from the formular   
if catDialog.wasOKed():    
	
	# Loop over categories, adding a tickbox to the panel for each  
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns  
	listCat = [] # for perstistence
	for i in range(N_category_):   
		   
		# Recover the category name   
		category = catDialog.getNextString()   
		listCat.append(category)

		# Make a checkbox with the category name
		box = Checkbox(category, False)
		box.setFocusable(False) # important to have the keybard shortcut working

		# Add checkbox to the gui for this category   
		catPanel.add(box)   
	   
	# Save categories in memory   
	pref.put(ij.class, "listCat_", listCat )
	
	## Initialize dialog
	title = "Qualitative Annotations - multi-classes (checkboxes)"
	message = """Tick the categories corresponding to the current image, then click 'Add' or press the '+' key.
	To annotate ROI, draw a new ROI or select some ROI(s) in the RoiManager before clicking 'Add'/pressing '+'."""
	
	
	winButton = MainDialog(title, message, catPanel)
	winButton.addButton("Add", ButtonAction(winButton))   
	 
	# Add defaults 
	winButton.addDefaultOptions() 
	winButton.showDialog()

