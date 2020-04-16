#@ File (label="CSV file for category and choice", style="extension:csv") csvpath

from ij.gui import GenericDialog
import csv

csvPath = csvpath.getPath()

# Check its a csv (the extension filtering does not work)
if not csvPath.endswith("csv"): raise TypeError("Expected a csv file")

with open(csvPath, "r") as csvFile:
	csvIterator = csv.reader(csvFile)
	header = csvIterator.next() # read first header line 
	n = len(header)
	#print header
	
	#dico = {name:[] for name in header}
	dropdown = [ [] for i in range(n)] # [[], [], [], [], []] such that dropdown[i] is a list of choices for dropdown i
	#print dropdown
	
	for row in csvIterator:
		for i, entry in enumerate(row): # row is a list
			dropdown[i].append(entry) # dropdown[i] is the list of choices

# Initialize GUI
win = GenericDialog("Multi-dropdown Classification")

for i in range(n):
	win.addChoice(header[i], dropdown[i], dropdown[i][0])

win.showDialog()