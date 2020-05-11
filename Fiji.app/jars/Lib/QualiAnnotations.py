from ij 			import WindowManager 
from ij.measure 	import ResultsTable 

def addDefaultOptions(dialog):
	'''Add stack mode choice, message and help button'''
	# Add mode for stacks
	choice = ["slice", "stack"]
	dialog.addChoice("Stack mode : 1 table entry per", choice, choice[0])
	
	# Add message about citation and doc
	dialog.addMessage("If you use this plugin, please cite : ***")
	dialog.addMessage("Documentation and generic analysis workflows available on the GitHub repo (click Help)")
	
	# Add Help button pointing to the github
	dialog.addHelp(r"https://github.com/LauLauThom/ImageJ-ManualClassifier")

	dialog.hideCancelButton() 
	

def getTable():
	'''Check if a table is open and get its name'''
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
	
	return tableTitle, Table
		
def nextSlice(imp, stackMode):
	'''Go to next slice if stackMode=slice''' 
	if (stackMode=="slice" and imp.getStackSize()!=1 and imp.currentSlice!=imp.getStackSize() ): # if We have a stack and the current slice is not the last slice
		imp.setSlice(imp.currentSlice+1) 
	
