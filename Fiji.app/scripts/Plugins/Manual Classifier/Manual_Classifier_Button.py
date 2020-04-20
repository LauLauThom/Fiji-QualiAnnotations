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
from ij.measure 	import ResultsTable 
from ij.gui		    import GenericDialog, NonBlockingGenericDialog 
from java.awt.event import ActionListener 
from java.awt 		import GridLayout, Button, Panel
import os 
 
class ButtonAction(ActionListener): # extends action listener  
	 
	def __init__(self, cat): # cat is the category name as a string 
		# use mother class constructor 
		ActionListener.__init__(self)
		
		# add the category as attribute 
		self.cat = cat
		 
	 
	def actionPerformed(self, event): 
		'''Called when Button are clicked''' 
 
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
				filename = filename.split('\n',1)[0] # can be useful when ImagesToStack/Import Sequence was used  
			 
		 
		# Fill the result table 
		Table.incrementCounter() # Add one additional row before filling it 
		 
		Table.addValue("Index", Table.getCounter() ) 
		Table.addValue("Folder", infos.directory.rstrip(os.path.sep) )
		Table.addValue("Image", filename) 

		if choiceIndex==0: # single category column
			Table.addValue("Category", self.cat)

		else: # 1 column/category with 0/1
			for cat in listCat: 
				if cat == self.cat: 
					Table.addValue(cat, 1) 
				else: 
					Table.addValue(cat, 0)
		 
		# Read comment
		stringField = WinButton.getStringFields()[0]
		Table.addValue("Comment", stringField.text)
		
		Table.show(tableTitle) # Update table	   
		#Table.updateResults() # only for result table but then addValue does not work ! 
		 
		# Go to next slice 
		if imp.getStackSize() != 1 and imp.currentSlice != imp.getStackSize(): # if We have a stack and the current slice is not the last slice 
			imp.setSlice(imp.currentSlice+1) 
			imp.updateStatusbarValue() # update Z and pixel value (called by next slice so we should do it too ?) 
		 
		# Bring back the focus to the button window (otherwise the table is in the front) 
		WindowManager.setWindow(WinButton) 
		 
		 
		 
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
	
	# Check if a table called Classification or Classification.csv exists otherwise open a new one
	win  = WindowManager.getWindow("Classification")
	win2 = WindowManager.getWindow("Classification.csv")
	
	if win: # different of None
		Table = win.getResultsTable()
		tableTitle = "Classification"
		
	elif win2 : # different of None
		Table = win2.getResultsTable()
		tableTitle = "Classification.csv"
		
	else:
		Table = ResultsTable()
		tableTitle = "Classification"
 
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
		Action = ButtonAction(Cat) 
 
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

	WinButton.hideCancelButton() 
	WinButton.showDialog() 
