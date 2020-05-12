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
 
TO DO : Add measurement possibility ? The addValue was not working so well in this case. Duplicate to another code to try with the result table 
'''
from ij	            import IJ, WindowManager
from ij.measure 	import ResultsTable, Measurements
from ij.plugin.filter import Analyzer
from ij.gui		    import GenericDialog, NonBlockingGenericDialog 
from java.awt.event import ActionListener 
from java.awt 		import GridLayout, Button, Panel
from QualiAnnotations import addDefaultOptions, getTable, getImageDirAndName, ButtonAction
import os 



class CustomAction(ButtonAction): # extend ButtonAction to inherit the actionPerformed method
	
	def __init__(self, dialog, cat):
		ActionListener.__init__(self)
		self.dialog = dialog
		self.cat=cat
	
	def fillFunction(self, Table):
		if choiceIndex==0: # single category column
			Table.addValue("Category", self.cat)

		else: # 1 column/category with 0/1
			for cat in listCat: 
				if cat == self.cat: 
					Table.addValue(cat, 1) 
				else: 
					Table.addValue(cat, 0)
		 
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
	 
	# Initialize GUI with category buttons 
	WinButton = NonBlockingGenericDialog("Manual classifier - Single class per image") 
	WinButton.addMessage("Click the category of the current image")
		
	# Loop over categories and add a button to the panel for each
	listCat = [] 
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns
	
	for i in range(N_category): 
		 
		# Recover the category name 
		Cat = Win.getNextString() 
		listCat.append(Cat) 
 
		# Create an instance of button action for this category 
		#Action = ButtonAction(Cat) 
		Action = CustomAction(WinButton, Cat)
 
		# Create a Button 
		button = Button(Cat) 
		 
		# Bind action to button 
		button.addActionListener(Action) 
		 
		# Add a button to the gui for this category 
		catPanel.add(button) 
	 
	# Save categories in memory
	pref.put(ij.class, "listCat", listCat)

	# Add Panel to WinButton
	WinButton.addPanel(catPanel)
	
	# Add comment field 
	WinButton.addStringField("Comments", "") 
	
	# Add default fields
	addDefaultOptions(WinButton)
	
	WinButton.showDialog() 
