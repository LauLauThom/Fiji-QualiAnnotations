# Pie Chart JFreeChart Jython Fiji 
from javax.swing import JPanel , JFrame
from org.jfree.chart import JFreeChart, ChartPanel, ChartFactory
from org.jfree.data.general import DefaultPieDataset, PieDataset
from org.jfree.ui import ApplicationFrame, RefineryUtilities 

from collections import Counter

test = ["1","1","1","2","2","3","3","3","3","3"] # convert to string otherwise issue
counts = Counter(test)
#print counts # value: counts OK
 
# Create a Pie dataset
data = DefaultPieDataset() 
for key, value in counts.items(): 
	#print key, value 
	data.setValue(key, value) 
 
print data 
 
# Create a JFreeChartInstance 
title = "Category distribution"
legend = True 
tooltips = True 
urls = False
chart = ChartFactory.createPieChart(title, data, legend, tooltips, urls) 
panel = ChartPanel(chart) 
 
class PieFrame(JFrame): 
	 
	def __init__(self, frameTitle):
		JFrame.__init__(self, frameTitle)
		self.setContentPane(panel)
		
	def showFrame(self):
		"""Put the dimension in the show command"""
		self.setSize( 560 , 367 )    
		RefineryUtilities.centerFrameOnScreen(self)
		self.setVisible(True)
		
frame = PieFrame("MyFirstFrame")
frame.showFrame()