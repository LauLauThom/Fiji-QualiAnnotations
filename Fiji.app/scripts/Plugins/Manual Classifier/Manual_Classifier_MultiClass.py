#@ int (Label = "Number of categories") N_category_ 
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
from ij	            import IJ,WindowManager 
from ij.measure 	import ResultsTable 
from ij.gui		    import GenericDialog, NonBlockingGenericDialog 
from java.awt.event import ActionListener 
from java.awt 		import GridLayout, Button, Panel , Checkbox
 
 
class ButtonAction(ActionListener): # extends action listener  
	'''The function actionPerformed contains code executed upon click of the associated button(s)''' 
	 
	def __init__(self): 
		# use mother class constructor 
		ActionListener.__init__(self) 
				 
	 
	def actionPerformed(self,event): 
		'''Called when associated buttons are clicked''' 
 
		imp = IJ.getImage() # get current image 
		infos = imp.getOriginalFileInfo() 
		 
		# Recover image name 
		if imp.getStackSize()==1:  
			filename = infos.fileName 
		else: 
			Stack = imp.getStack() 
			filename = Stack.getSliceLabel(imp.currentSlice) 
			 
			if filename is None: # the slice label can be empty sometimes 
				filename = 'Slice' + str(imp.currentSlice)	 
					 
			else :  
				filename = filename.split('\n',1)[0] # can be useful when ImagesToStack/Import sequence was used 
					 
		# Fill the result table 
		Table.incrementCounter() # Add one additional row before filling it 
 
		Table.addValue("Index", Table.getCounter() ) 
		Table.addValue("Folder", infos.directory) 
		Table.addValue("Image", filename)	 
		 
		# Read categories
		for cat, box in dicoBox.iteritems(): 
			Table.addValue(cat, box.getState() ) # getNextBoolean would keep growing the index, check only index 0 to N 

		# Read comment
		stringField = WinButton.getStringFields()[0]
		Table.addValue("Comment", stringField.text)
		
		Table.show("Classification (multi)") # Update table	   
		#Table.updateResults() # only for result table but then addValue does not work ! 
		 
		# Go to next slice 
		if imp.getStackSize() != 1 and imp.currentSlice != imp.getStackSize(): # if We have a stack and the current slice is not the last slice 
			imp.setSlice(imp.currentSlice+1) 
			imp.updateStatusbarValue() # update Z and pixel value (called by next slice so we should do it too ?) 
		 
		# Bring back the focus to the button window (otherwise the table is in the front) 
		WindowManager.setWindow(WinButton) 
		 
		 
		 
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
if (Win.wasOKed()):  
	 
	# Initialise result table that will contain slice name and category 
	Table = ResultsTable() 
 
	# Initialise GUI with category buttons 
	WinButton = NonBlockingGenericDialog("Manual classifier - multi-class per image") 
	WinButton.addMessage("Tick the categories corresponding to the current image, then click Add")
	
	# Loop over categories, adding a tickbox to the panel for each
	dicoBox  = {} # need a list for the categories names for persistence
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns
	for i in range(N_category_): 
		 
		# Recover the category name 
		category = Win.getNextString() 
		box = Checkbox(category, False)
		dicoBox[category] = box
		 
		# Add a button to the gui for this category 
		catPanel.add(box) 
	 
	# Save categories in memory 
	pref.put(ij.class, "listCat_", dicoBox.keys() ) 
	 
	# Add Panel to WinButton
	WinButton.addPanel(catPanel)
	
	# Add comment field
	WinButton.addMessage("") # skip line
	WinButton.addStringField("Comments", "")
	
	# Create the Add Button 
	ButtonAdd = Button("Add") 
		 
	# Bind action to Button 
	ButtonAdd.addActionListener(ButtonAction()) 
	 
	# Add button to window 
	#WinButton.addMessage("") # skip line
	WinButton.add(ButtonAdd) 
	WinButton.hideCancelButton() 
	 
	# initialise Layout 
	#Layout = GridLayout(N_category_+2,1) # +2 for OK/Cancel and comment (1 extra row) 
	#WinButton.setLayout(Layout) 
	 
	WinButton.showDialog() 