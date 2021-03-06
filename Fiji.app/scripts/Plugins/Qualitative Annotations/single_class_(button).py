'''
This script can be used to manually classify full images from a stack into N user-defined categories.  
A first window pops up to request:
- the number of categories N
- the structure of the table (single/multi category column)
- the image browsing mode (stack or directory)
- if the category names should be read from an active table (better than having a browse button, then I dont have to handle issue loading the table)

A second window follows with N text fields for the category names.
Finally the annotation GUI will show up with one button per category.  
Clicking on the button will generate a new entry in a table with the image name and the category.  
It will also skip to the next slice for stacks.  
'''
#@ String  (Label="Read categories from", choices={"Text file", "Active table", "Memory"}, value="Memory" ) categorySource 
#@ File    (label="Text file (if selected above)", style="file", required=false) textFile
#@ String  (label="Browsing mode", choices={"stack", "directory"}) browse_mode
#@ String  (Label="Table structure", choices={"single category column","one column per category"}) table_structure
#@ Boolean (label="Run measure", value=false) run_measure 

from ij 			import IJ, WindowManager, Prefs
from fiji.util.gui  import GenericDialogPlus
from java.awt 		import GridLayout, Button, Panel 
from java.awt.event import ActionListener
from javax.swing    import JButton
from QualiAnnotations.utils          import CustomDialog, getTable, getCategoriesFrom
from QualiAnnotations.CategoryDialog import CategoryDialog
from QualiAnnotations.Charts         import PieChart
import os  

# Make a dictionary for keycode and shortcut name for button F1-F12
listKeyCodes  = range(112, 124) # see https://docs.oracle.com/javase/7/docs/api/constant-values.html#java.awt.event.KeyEvent.VK_F1
listF1_F12    = ["F"+str(x) for x in range(1,13) ]      # simply F1-F12
dicoShortcuts = dict(zip(listKeyCodes, listF1_F12))  # keyCode:"FX" value

class PlotAction(ActionListener):
	"""Display a PieChart of the data in the category column upon click"""
	
	def actionPerformed(self, event):
		
		if IJ.getFullVersion() < "1.53g": 
			IJ.error("This plugin requires ImageJ version 1.53g minimum.\n Update using Help > Update ImageJ...")
			return
			
		tableWindow = WindowManager.getActiveTable() # this function requires the 1.53g (or at least not working with 1.53c)

		if not tableWindow: return

		# Get column Category
		table   = tableWindow.getResultsTable()
		column       = table.getColumnAsVariables("Category")
		columnString = [str(item) for item in column]
		
		# Plot Pie Plot for this column
		pieChart = PieChart("Category", columnString)
		pieChart.showFrame("Data-distribution")


class CategoryAction(ActionListener): 
	'''Define what happens when a category button is clicked'''
	
	def actionPerformed(self, event): 
		'''Update the selected category and defaultActionSequence to fill the table'''
		winButton.selectedCategory = event.getSource().getLabel() 
		winButton.defaultActionSequence() 

class SaveAction(ActionListener):
	"""Define what happens when the save category button is pressed."""
	
	def actionPerformed(self, event):

		outDir   = IJ.getDirectory("Save category file in directory...")
		if not outDir: return # when cancelled
		
		filename = IJ.getString("Filename", "categories.txt")
		if not filename: return # when cancelled
		
		outPath  = os.path.join(outDir, filename)

		listButtons = winButton.getPanel().getComponents()
		with open(outPath, "w") as catFile:
			for button in listButtons:
				catFile.write(button.getLabel().encode("utf-8") + "\n") # important to use UTF-8 otherwise troubles

		
# Define global button action listener
# Need to be global since the panel is built out of the dialog constructor (ie no access to self)
# Surely not the cleanest but it works
categoryAction = CategoryAction()
saveAction     = SaveAction()

class ButtonDialog(CustomDialog): 
	'''
	Annotation dialog, also define keyboard shortcut and function to fill the table
	defaultActionSequence() is defined in the mother class customDialog
	'''
	# define constant used for input (must match script parameters above)
	TABLE_SINGLE_COLUMN = "single category column"
	TABLE_MULTI_COLUMN  = "one column per category"
	
	def __init__(self,
				 panel,
				 browseMode="stack",
				 runMeasure=False,
				 tableStructure=TABLE_SINGLE_COLUMN):
		"""
		browseMode: "stack" or "directory"
		tableStructure: "single category column" or anything else, such as "one column per category"
		"""
		title   = "Qualitative Annotations - single class (buttons)"
		message = "Click the category of the current image or ROI, or use the F1-F12 keyboard shortcuts.\nTo annotate ROI, draw a new ROI or select some ROI in the RoiManager before clicking the category button." 
		CustomDialog.__init__(self, title, message, panel)
		self.addButton("Add new category", self) 
		self.addToSameRow()
		self.addButton("Save categories to file", saveAction)
		self.addStringField("Comments", "")
		
		#self.addButton("Add", self) # no add button for button-plugin
		self.browseMode = browseMode # important to define it before adding defaultOptions
		self.runMeasure = runMeasure
		self.addDefaultOptions()
		#if choiceIndex == 0: self.addButton("Make PieChart from category column", PlotAction()) # Remov this button: risk of cherry picking to improve the plot
		#self.addCitation()

		# Variable used by instance methods
		self.tableStructure = tableStructure
		self.selectedCategory = ""		
	 
	def fillTable(self, table): 
		if self.tableStructure == self.TABLE_SINGLE_COLUMN: # single category column 
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
		code = keyEvent.getKeyCode()		#print "Pressed key", code # just for debugging in case
		
		if code in dicoShortcuts: # check if the code is in the dicos keys
			index = code - 112 # switch back from keyCode index starting at 112 with F1, to 0-based list index
		else: 
			return # prevent issue otherwise index variable non-existing

		if index >= 0 and index < len(listCat):
			self.selectedCategory = listCat[index] 
			self.defaultActionSequence() 	 

	def makeCategoryComponent(self, category):
		"""Return a button with the new category name, and mapped to the action"""
		listCat.append(category)
		
		# Save the new category in memory
		Prefs.set("annot.listCat", ",".join(listCat) )
		
		button = JButton(category)
		button.addActionListener(categoryAction)
		button.setFocusable(False)

		# Add button tooltip if fit in the F1-F12 button range
		nCat = len(listCat)
		if nCat <= 12: button.setToolTipText("Keyboard shortcut: F" + str(nCat)) # F shortcut labels are 1-based, ie match the len value

		return button
  
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############  
textFilePath   = textFile.getPath() if textFile else "" 
listCategories = getCategoriesFrom(categorySource, textFilePath) # initial list, before user-edit
catDialog      = CategoryDialog(listCategories)
catDialog.showDialog()


################# After OK clicking ###########  
  
# Recover fields from the formular  
if catDialog.wasOKed():   
	
	# Loop over categories and add a button to the panel for each  
	catPanel = Panel(GridLayout(0,4)) # Unlimited number of rows - fix to 4 columns - not possible to use a JPanel, not supported by GenericDialog
	
	listCat = catDialog.getListCategories()
	listShortcut = range( 112, 112+len(listCat) )
	
	for index, category in enumerate(listCat): 
		  
		# Create a Button  
		button = JButton(category) # button label 
		if index<12: button.setToolTipText( "Keyboard shortcut: F" + str(index+1) ) # index is 0-based, F shortcut are 1-based
		
		# Bind action to button  
		button.addActionListener(categoryAction)  
		
		# Add a button to the gui for this category  
		button.setFocusable(False) # prevent the button to take the focus, only the window should be able to take the keyboard shortcut
		catPanel.add(button)
	
	
	# Initialize classification gui
	winButton = ButtonDialog(catPanel, browse_mode, run_measure, table_structure)
	winButton.showDialog()
