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
from fiji.util.gui  import GenericDialogPlus
from ij.measure 	import ResultsTable 
from ij             import IJ, WindowManager
from QualiAnnotations import addDefaultOptions, AddButtonAction
import os, csv, codecs

### Read CSV to get categories and choices
csvPath = csvpath.getPath()

# Check its a csv (the extension filtering does not work)
if not csvPath.endswith("csv"): raise TypeError("Expected a csv file")

with open(csvPath, "r") as csvFile:
	#csvIterator = csv.reader(csvFile)
	csvIterator = csv.reader( codecs.EncodedFile(csvFile, "utf8", "utf_8_sig") ) # Prevent weird character with utf_8_sig encoding, generated by excel sometime
	
	headers = csvIterator.next() # read first header line 
	n = len(headers)
	
	dropdown = [ [] for i in range(n)] # [[], [], [], [], []] such that dropdown[i] contains the list of choices for dropdown i
	
	for row in csvIterator:
		for i, entry in enumerate(row): # row is a list
			if entry: dropdown[i].append(entry) # dropdown[i] is the list of choices # if necessary since all columns might not have the same length




# Initialize classification GUI
win = GenericDialogPlus("Multi-dropdown Classification") # GenericDialogPlus needed for builtin Button support
win.setModalityType(None) # like non-blocking generic dialog
win.addMessage("""Select the descriptors corresponding to the current image, then click Add.
To annotate ROI, draw or select a ROI before clicking Add.""") 

for i in range(n):
	win.addChoice(headers[i], dropdown[i], dropdown[i][0])

# Add comment field 
win.addStringField("Comments", "") 
	  
# Define custom action on button click (in addition to default)
def fillTable(Table):
	'''Called when Add is clicked'''
	for i, choice in enumerate( win.getChoices()[:-1] ): # Does not take last dropdown (stackMode)
		Table.addValue(headers[i], choice.getSelectedItem() ) 

# Add button to window 
win.addButton("Add", AddButtonAction(win, fillTable))

# Add defaults
addDefaultOptions(win)
win.showDialog()