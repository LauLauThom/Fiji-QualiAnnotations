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
from java.awt 		import GridLayout, Button, Panel , Checkbox  
from collections 	import OrderedDict 
from QualiAnnotations import AddDialog, ButtonAction
import os 
 
 
 
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############   
Win = GenericDialog("Categories names")   
   
# Add N string fields for class names   
for i in range(N_category_):   
	listCat = pref.getList(ij.class, "listCat_")            # try to retrieve the list of categories from the persistence, if not return [] - ij.class workaround see https://forum.image.sc/t/store-a-list-using-the-persistence-prefservice/26449   
	  
	if listCat and i<=len(listCat)-1:  
		catName = listCat[i]  
	else:  
		catName = "Category_" + str(i+1)   
	  
	Win.addStringField("Category: ", catName)   
	Win.addMessage("") # skip one line   
	   
Win.showDialog()   
 
 
################# After OK clicking ###########   
# Recover fields from the formular   
if Win.wasOKed():    
	
	# Loop over categories, adding a tickbox to the panel for each  
	dicoBox  = OrderedDict()          # contains (categoryName: CheckBox) 
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns  
	for i in range(N_category_):   
		   
		# Recover the category name   
		category = Win.getNextString()   

		# Make a checkbox with the category name
		box = Checkbox(category, False)
		box.setFocusable(False) # important to have the keybard shortcut working
		dicoBox[category] = box  

		# Add checkbox to the gui for this category   
		catPanel.add(box)   
	   
	# Save categories in memory   
	pref.put(ij.class, "listCat_", dicoBox.keys() )   
	
	## Initialize dialog
	title = "Qualitative Annotations - Annotate with checkboxes"
	message = """Tick the categories corresponding to the current image, then click Add or press the + key.
	To annotate ROI, draw or select a ROI before validating."""
	
	def fillTable(Table): 
		'''Read checkbox state and update table'''  
		for cat, box in dicoBox.iteritems():   
			Table.addValue(cat, box.getState() ) 
	
	winButton = AddDialog(title, message, catPanel, fillTable)
	winButton.addButton("Add", ButtonAction(winButton))   
	 
	# Add defaults 
	winButton.addDefaultOptions() 
	winButton.showDialog()
  