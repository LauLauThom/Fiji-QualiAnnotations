'''
This plugin takes a csv as input that defines the structure of the classification GUI
The CSV should contain one column per dropdowns choice menu
The first line of the CSV contains the label of the category and the following lines the possible choice
example

Tail, Morphology
Straight, Gross
Bent, Slim
Broken, , 
'''
#@ File (label="CSV file for category and choice", style="extension:csv") csvpath
from java.awt 		import Panel, Choice, Label, GridLayout
from QualiAnnotations import AddDialog, ButtonAction
import os, csv, codecs

### Read CSV to get categories and choices
csvPath = csvpath.getPath()

with open(csvPath, "r") as csvFile:
	
	# Check extension (script parameter extension filtering above not functionnal)
	if csvPath.endswith("csv"):

		# Guess , or ; separator
		s = csv.Sniffer()
		dialect = s.sniff(csvFile.readline())
		csvFile.seek(0) # come back to the beginning of the file
		
		# Open and parse file
		csvIterator = csv.reader( codecs.EncodedFile(csvFile, "utf8", "utf_8_sig"), dialect ) # Prevent weird character with utf_8_sig encoding, generated by excel sometime 
		
	elif csvPath.endswith("tsv"):
		csvIterator = csv.reader( codecs.EncodedFile(csvFile, "utf8", "utf_8_sig"), delimiter="\t" )
	
	else:
		raise TypeError("Expected a ,-separated or ;-separated (csv) or tab-separated (tsv) file") 
	
	headers = csvIterator.next() # read first header line 
	n = len(headers)
	
	dropdowns = [ [] for i in range(n)] # [[], [], [], [], []] such that dropdowns[i] contains the list of choices for dropdowns i
	
	for row in csvIterator:
		for i, entry in enumerate(row): # row is a list
			if entry: dropdowns[i].append(entry) # dropdown[i] is the list of choices # if necessary since all columns might not have the same length


# Create horizontal panel for dropdowns
panel = Panel( GridLayout(0, n) ) # as many columns (n) as menus, as many rows as necessary (0)

# First panel row -> dropdown labels
for header in headers:
	panel.add( Label(header) )

# Second panel row -> dropdown choices
for i in range(n):
	label = headers[i] 
	
	chooser = Choice()
	chooser.setName(label) # not display but easier to recover infos
	
	dropdown = dropdowns[i]
	for option in dropdown:
		chooser.add(option) 
	
	chooser.setFocusable(False)
	panel.add(chooser)


# Define custom action on button click (in addition to default)
def fillTable(Table):
	'''Called when Add is clicked'''
	for dropdown in ( panel.getComponents()[n:] ): # n first elements are the labels
		Table.addValue(dropdown.getName(), dropdown.getSelectedItem() )


# Initialize classification GUI
title   = "Qualitative Annotations - multi-classes (dropdown)"
message = """Select the descriptors corresponding to the current image, then click Add or press the + key.
To annotate ROI, draw or select a ROI before validating."""

win = AddDialog(title, message, panel, fillTable)

# Add button to window 
win.addButton("Add", ButtonAction(win))

# Add defaults
win.addDefaultOptions()
win.showDialog()