from ij import IJ, Prefs
from fiji.util.gui import GenericDialogPlus 
from java.awt import Panel, Button, GridLayout, TextField 
 
class CategoryDialog(GenericDialogPlus): 
	"""
	Dialog prompting the category names, used by the single class button and checkbox plugins. 
	It is filled with an initial list of categorie names passed via the constructor.
	Additional categories can be added once the dialog is shown by clicking the add
	"""
	ADD_CATEGORY = "Add category" # Label used for the button
	
	def __init__(self, listCategories): 
		"""
		listCategories: initial list of categories to fill the fields
		"""
		GenericDialogPlus.__init__(self, "Category names") 
		 
		self.addPanel( Panel(GridLayout(0,1)) )  
		self.panel = self.getComponent(0) 
		for category in listCategories:  
			self.panel.add( TextField(category) ) # Add string input to GUI 
		 
		self.addButton(CategoryDialog.ADD_CATEGORY, self) 
	 
	def getListCategories(self): 
		"""
		Read the new category names entered by user in the GUI.
		Save the values as a comma-separated string in persistence.
		"""
		listCategories = [] 
		for textField in self.panel.getComponents(): 
				newCategory = textField.getText() 
				if newCategory: listCategories.append(newCategory) 
		
		Prefs.set("annot.listCat", ",".join(listCategories) ) # save the new list of categories 
		 
		return listCategories 
	 
	def actionPerformed(self, event): 
		 
		source = event.getSource() # test here if it is a button 
		 
		if isinstance(source, Button): # if type is a button get label, and check command, otherwise pass to GenericDialogPlus.actionPeformed 
			 
			sourceLabel = source.getLabel() 
			 
			if sourceLabel == CategoryDialog.ADD_CATEGORY: 
				newCategory = IJ.getString("Enter new category name", "new category") 
				if not newCategory: return # if Cancelled (ie newCat=="") or empty field just dont go further  
				 
				self.panel.add(TextField(newCategory)) # Add new text field with the new category 
				self.pack() # recompute the layout and update the display 
		 
		# Anyway do the mother class usual action handling 
		GenericDialogPlus.actionPerformed(self, event) 
 
if __name__ in ["__main__", "__builtin__"]: 
	 
	dialog = CategoryDialog(["A","B"]) 
	dialog.showDialog()

	if dialog.wasOKed():
		print dialog.getListCategories()