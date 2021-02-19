from javax.swing             import JPanel, JFrame
from org.jfree.chart.plot    import PiePlot
from org.jfree.chart         import JFreeChart, ChartPanel, ChartFactory
from org.jfree.data.general  import DefaultPieDataset
from org.jfree.data.category import DefaultCategoryDataset; 

from org.jfree.ui import ApplicationFrame, RefineryUtilities 
from collections import Counter

class PieChart(JFrame): 
	"""
	Create a Frame holding a PieChart from a list of data, typically a table column
	Values in the data list should be string
	Inspired from https://www.tutorialspoint.com/jfreechart/jfreechart_pie_chart.htm
	Except that the class extends on JFrame and not ApplicationFrame, which causes Fiji to quit completely when plot is closed
	"""
	
	def __init__(self, plotTitle, listData, showLegend=True, showTooltip=True):
		JFrame.__init__(self)
		self.listData = listData
		panel = self.generatePlotPanel(plotTitle, listData, showLegend, showTooltip)
		self.setContentPane(panel) # put the plot panel in the JFrame

	def generatePlotPanel(self, plotTitle, listData, showLegend, showTooltip):
		"""
		1) Create a PieDataset
		2) Create a PieChart (or  Create a PiePlot and put it in a JFreeChart)
		3) Put the PieChart in a ChartPanel
		"""
		# Get a dictionary of value occurence in the list {value1:count, value2:count...}
		dataDico = Counter(listData)
		#print dataDico # value: counts OK
		 
		# Create a Pie dataset from the dicoData
		pieDataset = DefaultPieDataset() 
		for key, value in dataDico.items(): 
			#print key, value 
			pieDataset.setValue(key, value) 
				 
		# Create an instance of JFreeChart 	
		urls = False
		chart = ChartFactory.createPieChart(plotTitle, pieDataset, showLegend, showTooltip, urls) 
		
		# Alternative way
		#piePlot = PiePlot(pieDataset)
		#chart   = JFreeChart(plotTitle, piePlot)
		
		return ChartPanel(chart)
	
	def showFrame(self, title, width=560, height=367):
		"""Put the dimension in the show command"""
		self.setTitle(title)
		self.setSize(width, height)    
		RefineryUtilities.centerFrameOnScreen(self)
		self.setVisible(True)


class BarChart(JFrame): 
	"""
	Create a Frame holding a BarChart from a list of data, typically a table column
	Values in the data list should be string
	Inspired from https://www.tutorialspoint.com/jfreechart/jfreechart_pie_chart.htm
	Except that the class extends on JFrame and not ApplicationFrame, which causes Fiji to quit completely when plot is closed
	"""
	
	def __init__(self, plotTitle, listData, showLegend=True, showTooltip=True):
		JFrame.__init__(self)
		self.listData = listData
		panel = self.generatePlotPanel(plotTitle, listData)
		self.setContentPane(panel) # put the plot panel in the JFrame

	def generatePlotPanel(self, plotTitle, listData):
		"""
		1) Create a CategoryDataset
		2) Create a BarChart (or  Create a BarPlot and put it in a JFreeChart)
		3) Put the BarChart in a ChartPanel
		"""
		# Get a dictionary of value occurence in the list {value1:count, value2:count...}
		dataDico = Counter(listData)
		#print dataDico # value: counts OK
		 
		# Create a Pie dataset from the dicoData
		dataset = DefaultCategoryDataset() 
		for key, value in dataDico.items(): 
			#print key, value 
			dataset.setValue(value, key, "") 
		
		# Create an instance of JFreeChart 	
		chart = ChartFactory.createBarChart(plotTitle, "Categories", "Count", dataset) 
		# Alternative way
		#piePlot = PiePlot(pieDataset)
		#chart   = JFreeChart(plotTitle, piePlot)
		
		return ChartPanel(chart)
	
	def showFrame(self, title, width=560, height=367):
		"""Put the dimension in the show command"""
		self.setTitle(title)
		self.setSize(width, height)    
		RefineryUtilities.centerFrameOnScreen(self)
		self.setVisible(True)

if __name__ in ['__builtin__', '__main__']:

	# Create toy dataset and display the pie plot
	data = ["banana"]*3 + ["apple"]*5 + ["cherry"]*10
	frame = PieChart("Fruits", data)
	frame.showFrame("My Pie chart")
	
	frame2 = BarChart("Fruits", data)
	frame2.showFrame("My Bar chart")