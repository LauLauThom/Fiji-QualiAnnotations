from QualiAnnotations.Charts import PieChart
from ij.gui import GenericDialog
from ij import IJ, WindowManager

if IJ.getFullVersion() < "1.53g": 
	IJ.error("This plugin requires ImageJ version 1.53g minimum.\n Update using Help > Update ImageJ...")
	raise Exception("ImageJ version 1.53g minimum required")

tableWindow = WindowManager.getActiveTable() # this function requires the 1.53g (or at least not working with 1.53c)
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
	dialog.addMessage("""Hover the mouse over the plot to view absolute and relative (%) values\n
	Right-click to set colors, export to PNG...\n
	Note: BarCharts usually provide better distinction than PieCharts for sectors with similar sizes (see Help).""")
	dialog.addHelp(r"https://www.data-to-viz.com/caveat/pie.html")
	dialog.showDialog()
	
	# Generate PieChart with data column
	if dialog.wasOKed():
	
		# Get the data column as string
		selectedHeader = dialog.getNextChoice()
		column         = table.getColumnAsVariables(selectedHeader)
		columnString   = [str(item)[1:-1] for item in column] # [1:-1] to remove the ""
	
		# Make the PieChart for this data column
		if columnString:
			chart = PieChart(selectedHeader, columnString)
			chart.showFrame("PieChart")
