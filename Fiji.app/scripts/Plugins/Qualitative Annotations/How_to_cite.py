from ij.gui import GenericDialog

gd = GenericDialog("How to cite the plugins")
gd.addMessage("""If you use these plugins, please cite : 
		
		Thomas LSV, Schaefer F and Gehrig J. 
		Fiji plugins for qualitative image annotations: routine analysis and application to image classification
		[version 2; peer review: 2 approved, 1 approved with reservations]. 
		F1000Research 2021, 9:1248 
		doi : 10.12688/f1000research.26872.2""")

#URL = r"https://doi.org/10.12688/f1000research.26872.1/" # mind the last slash at the end of URL, otherwise not working
URL = r"https://f1000research.com/articles/9-1248"
gd.addHelp(URL)
gd.setHelpLabel("Article page")
gd.hideCancelButton()
gd.showDialog()