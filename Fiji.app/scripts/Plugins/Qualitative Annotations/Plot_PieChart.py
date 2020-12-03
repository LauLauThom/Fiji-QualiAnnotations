from PieChart import PieChart
from ij.gui import GenericDialog
from ij import IJ, WindowManager

tableWindow = WindowManager.getActiveTable()
#print tableWindow

if not tableWindow: 
	IJ.error("No open table")

else:

	# List column headers
	table   = tableWindow.getResultsTable()
	headers = table.getHeadings()
	
	# Generate dialog with dropdown for column selection
	dialog = GenericDialog("PieChart from table column")
	dialog.addChoice("Data column", headers, headers[0])
	dialog.addMessage("Hover the mouse over the plot to view absolute and relative (%) values\nRight-click to set colors, export to PNG...")
	dialog.showDialog()
	
	# Generate PieChart with data column
	if dialog.wasOKed():
	
		# Get the data column as string
		selectedHeader = dialog.getNextChoice()
		column         = table.getColumnAsVariables(selectedHeader)
		columnString   = [str(item) for item in column]
	
		# Make the PieChart for this data column
		if columnString:
			chart = PieChart(selectedHeader, columnString)
			chart.showFrame("PieChart")