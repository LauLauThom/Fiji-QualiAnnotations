'''
This plugin takes a csv as input that defines the structure of the classification GUI
The CSV should contain one column per dropdown choice menu
The first line of the CSV contains the label of the category and the following lines the possible choice
example

Tail, Morphology
Straight, Gross
Bent, Slim
Broken, , 
'''
#@ File (label="CSV file for category and choice", style="extension:csv") csvpath
from java.awt.event import ActionListener 
from fiji.util.gui  import GenericDialogPlus
from ij.measure 	import ResultsTable 
from ij             import IJ, WindowManager
import os, csv

### Read CSV to get categories and choices
csvPath = csvpath.getPath()

# Check its a csv (the extension filtering does not work)
if not csvPath.endswith("csv"): raise TypeError("Expected a csv file")

with open(csvPath, "r") as csvFile:
	csvIterator = csv.reader(csvFile)
	headers = csvIterator.next() # read first header line 
	n = len(headers)
	
	dropdown = [ [] for i in range(n)] # [[], [], [], [], []] such that dropdown[i] contains the list of choices for dropdown i
	
	for row in csvIterator:
		for i, entry in enumerate(row): # row is a list
			if entry: dropdown[i].append(entry) # dropdown[i] is the list of choices # if necessary since all columns might not have the same length


## Check if a table called Classification or Classification.csv exists otherwise open a new one
table1 = WindowManager.getWindow("Classification")
table2 = WindowManager.getWindow("Classification.csv")

if table1: # different of None
	Table = table1.getResultsTable()
	tableTitle = "Classification"
	
elif table2 : # different of None
	Table = table2.getResultsTable()
	tableTitle = "Classification.csv"
	
else:
	Table = ResultsTable()
	tableTitle = "Classification"


## Button action for "Add" Button
class ButtonAction(ActionListener): # extends action listener  
	'''The function actionPerformed contains code executed upon click of the associated button(s)'''  
	 
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
		Table.addValue("Folder", infos.directory.rstrip(os.path.sep) )
		Table.addValue("Image", filename)	 
		 
		# Read choices 
		for i, choice in enumerate( win.getChoices() ):
			Table.addValue(headers[i], choice.getSelectedItem() ) 

		# Read comment
		stringField = win.getStringFields()[0]
		Table.addValue("Comment", stringField.text)
		
		Table.show(tableTitle) # Update table	   
		#Table.updateResults() # only for result table but then addValue does not work ! 
		 
		# Go to next slice 
		if imp.getStackSize() != 1 and imp.currentSlice != imp.getStackSize(): # if We have a stack and the current slice is not the last slice 
			imp.setSlice(imp.currentSlice+1) 
			imp.updateStatusbarValue() # update Z and pixel value (called by next slice so we should do it too ?) 
		 
		# Bring back the focus to the button window (otherwise the table is in the front) 
		WindowManager.setWindow(win) 



# Initialize classification GUI
win = GenericDialogPlus("Multi-dropdown Classification") # GenericDialogPlus needed for builtin Button support
win.setModalityType(None) # like non-blocking generic dialog

for i in range(n):
	win.addChoice(headers[i], dropdown[i], dropdown[i][0])

# Add comment field
win.addStringField("Comments", "")
 
# Add button to window 
win.addButton("Add", ButtonAction()) 
win.hideCancelButton() 

win.showDialog()