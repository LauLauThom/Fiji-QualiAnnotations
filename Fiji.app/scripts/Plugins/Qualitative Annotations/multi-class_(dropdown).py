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
#@ File    (label="CSV file for category and choice", style="extension:csv") csvpath
#@ Boolean (label="Run measure", value=false) run_measure
#@ String  (label="Browsing mode", choices={"stack", "directory"}) browse_mode
#@ String  (visibility=MESSAGE, value="Example of input csv at Fiji.app/lib/QualiAnnotations-ExampleDropDown.csv", required=false) comment
from java.awt 		        import Panel, Choice, Label, GridLayout
from fiji.util.gui	        import GenericDialogPlus
from QualiAnnotations.utils import CustomDialog
import os, csv, codecs

class MainDialog(CustomDialog):
	"""
	Main annotation dialog for this plugin
	In this case the panel contains dropdowns
	"""

	def __init__(self, panel, browseMode, runMeasure):
		
		title   = "Qualitative Annotations - multi-classes (dropdown)"
		message = """Select the descriptors corresponding to the current image, then click 'Add' or press one of the '+' key.
		To annotate ROI, draw a new ROI or select some ROI(s) from the RoiManager before clicking 'Add'/pressing '+'."""
		CustomDialog.__init__(self, title, message, panel)

		#self.addButton("Add new category", self) # no add new category button for dropdown
		self.addStringField("Comments", "")
		self.addButton(CustomDialog.LABEL_ADD, self)
		
		self.browseMode = browseMode # important to define it before addDefaultOptions
		self.runMeasure = runMeasure
		self.addDefaultOptions()
		#self.addCitation()
		
		
	def fillTable(self, table):
		'''Read dropdown states and update table'''  
		for dropdown in ( self.getPanel().getComponents()[n:] ): # n first elements are the labels
			table.addValue( dropdown.getName(), dropdown.getSelectedItem() )
	
	def keyPressed(self, keyEvent):
		"""Define shortcut: pressing any of the + key also adds to the table like the Add button""" 
		code = keyEvent.getKeyCode()
		if code == keyEvent.VK_ADD or code==keyEvent.VK_PLUS: 
			self.defaultActionSequence()
	
	def makeCategoryComponent(self, category):
		"""
		Could return a new dropdown, but not implemented
		"""
		return None


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
		csvIterator = csv.reader( codecs.EncodedFile(csvFile, "utf8", "utf_8_sig"), dialect ) # Prevent weird character with utf_8 + BOM, generated by excel mostly when exporting as csv + utf8
		
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


# Initialize classification GUI
win = MainDialog(panel, browse_mode, run_measure)
win.showDialog()
