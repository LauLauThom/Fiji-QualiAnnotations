# @int (Label = "Number of categories") N_category
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
from java.awt 		import GridLayout,Button


class ButtonAction(ActionListener): # extends action listener 
	
	def __init__(self,cat): # cat is the category name as a string
		# use mother class constructor
		ActionListener.__init__(self)
		
		# add the category as attribute
		self.cat = cat
		
	
	def actionPerformed(self,event):
		'''Called when Button are clicked'''

		imp = IJ.getImage()

		# recover the image or slice name (getTitle return the name for single image but not for stacks. Hence generic solution is to use Stack object works in bopth cases)
		Stack = imp.getStack()
		SliceName = Stack.getSliceLabel(imp.currentSlice)	  
		
		if SliceName is None: # the slice label can be empty sometime
			SliceName = 'Slice' + str(imp.currentSlice)	  
		
		else : 
			SliceName = SliceName.split('\n',1)[0]
		
		# Fill the result table
		Table.incrementCounter() # Add one additional row before filling it
		Table.addValue("Image", SliceName)	
		Table.addValue("Category", self.cat)
		Table.show("Classification") # Update table	  
		#Table.updateResults() # only for result table but then addValue does not work !
		
		# Go to next slice
		if imp.getStackSize() != 1 and imp.currentSlice != imp.getStackSize(): # if We have a stack and the current slice is not the last slice
			imp.setSlice(imp.currentSlice+1)
			imp.updateStatusbarValue() # update Z-position and pixel value (called by next slice so we should do it too ?)
		
		# Bring back the focus to the button window (otherwise the table is in the front)
		WindowManager.setWindow(WinButton)
		
		
		
############### GUI - CATEGORY DIALOG - collect N classes names (N define at first line)  #############

Win = GenericDialog("Categories names")

# Add N string field to get class names
for i in range(N_category):
	Win.addStringField("Category: ","Category_"+str(i))
	Win.addMessage("") # skip one line
	
Win.showDialog()


################# After OK clicking ###########

# Recover fields from the formular
if (Win.wasOKed()): 
	
	# Initialise result table that will contain slice name and category
	Table = ResultsTable()

	# Initialise GUI with category buttons
	WinButton = NonBlockingGenericDialog("Click to assign an image to a category")
	
	# initialise Layout
	Layout = GridLayout(N_category+1,1) # +1 for OK/Cancel (1 extra row)
		
	# Loop over categories
	for i in range(N_category):
		
		# Recover the category name
		Cat = Win.getNextString()

		# Create an instance of button action for this category
		Action = ButtonAction(Cat)

		
		# Create a Button
		button = Button(Cat)
		
		
		# Bind action to button
		button.addActionListener(Action)
		
		# Add a button to the gui for this category
		WinButton.add(button)
		
	WinButton.setLayout(Layout)
	WinButton.showDialog()
