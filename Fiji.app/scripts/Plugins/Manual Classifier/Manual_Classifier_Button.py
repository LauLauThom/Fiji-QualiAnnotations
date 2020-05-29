#@ int (Label = "Number of categories", min=1) N_category  
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
from java.awt 		import GridLayout, Button, Panel 
from java.awt.event import ActionListener
from QualiAnnotations import CustomDialog, getTable, ButtonAction
import os  

class ButtonAction(ActionListener): 
	'''Define what happens when a button is clicked'''
	
	def actionPerformed(self, event): 
		'''Update the selected category and doAction to fill the table'''
		winButton.selectedCategory = event.getSource().getLabel() 
		winButton.doAction() 
		 
 
class ButtonDialog(CustomDialog): 
	'''Annotation dialog, also define keyboard shortcut and function to fill the table'''
		
	def __init__(self, title, message, panel, choiceIndex): 
		CustomDialog.__init__(self, title, message, panel) 
		self.choiceIndex = choiceIndex 
		self.selectedCategory = "" 
	 
	def fillTable(self, table): 
		if self.choiceIndex==0: # single category column 
			table.addValue("Category", self.selectedCategory) 
		 
		else: # 1 column/category with 0/1 
			for cat in listCat:  
				if cat == self.selectedCategory:  
					table.addValue(cat, 1)  
				else:  
					table.addValue(cat, 0) 
	
	def keyPressed(self, keyEvent): 
		'''
		Map button to keyboard shortcuts (use F1..F12)
		ie one can press F1 to assign to the first category instead of clicking the button
		'''		 
		code = keyEvent.getKeyCode()
		
		if code in listShortcut: 
			index = listShortcut.index(code)
			self.selectedCategory = listCat[index] 
			self.doAction() 	 
		
  
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############  
  
Win = GenericDialog("Categories names") 
 
choice = ["a single category column", "1 column per category"] 
indexDefault = pref.getInt("table_style", 0) 
Win.addChoice("Classification table shoud have",  
				choice,  
				choice[indexDefault] ) 
  
# Add N string field to get class names 
for i in range(N_category): 
	listCat = pref.getList(ij.class, "listCat")            # try to retrieve the list of categories from the persistence, if not return [] - ij.class workaround see https://forum.image.sc/t/store-a-list-using-the-persistence-prefservice/26449 
	 
	if listCat and i<=len(listCat)-1: 
		catName = listCat[i] 
	else: 
		catName = "Category_" + str(i+1) 
	 
	Win.addStringField("Category: ", catName) 
	 
	Win.addMessage("") # skip one line  
	  
Win.showDialog() 
  
  
################# After OK clicking ###########  
  
# Recover fields from the formular  
if (Win.wasOKed()):   
 
	# get Choice single/multi column 
	choiceIndex = Win.getNextChoiceIndex() 
	pref.put("table_style", choiceIndex) 
	 
	tableTitle, Table = getTable()
	
	# Loop over categories and add a button to the panel for each  
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns 
	
	# Define actionListener for buttons: they share the same one, associated to the dialog
	action = ButtonAction()	
	listCat = []
	listShortcut = range(112, 112+N_category)
	
	for i in range(N_category):  
		  
		# Recover the category name  
		Cat = Win.getNextString()  
		listCat.append(Cat)  
		
		# Create a Button  
		button = Button(Cat) # button label 
		
		# Bind action to button  
		button.addActionListener(action)  
		
		# Add a button to the gui for this category  
		button.setFocusable(False) # prevent the button to take the focus, only the window should be able to take the keyboard shortcut
		catPanel.add(button)
		
		
	# Save categories in memory 
	pref.put(ij.class, "listCat", listCat) 
	
	## Initialize classification gui
	title = "Manual classifier - Single class per image"
	message = "Click the category of the current image or ROI, or use the F1-F12 keyboard shortcuts.\nTo annotate ROI, draw a ROI or activate one before clicking the category button." 
	winButton = ButtonDialog(title, message, catPanel, choiceIndex)
		
	# Add default fields 
	winButton.addDefaultOptions() 
	winButton.showDialog()