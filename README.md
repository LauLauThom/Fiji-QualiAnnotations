![Twitter Follow](https://img.shields.io/twitter/follow/LauLauThom?style=social)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/laurent132.thomas@laposte.net)

The plugins allow to associate images or image-regions to 1 or a set of user-defined keywords (or categories/classes).  
They can be used to perform routine description of sample images, or to generate ground-truth category annotations for the training of a classifier for instance.  

There are 3 plugins: 
- __Annotate with buttons__  
A single class is associated to each image.  
The result table can be chosen to either have a single category column with the name of the assigned category for each image.  
Or like with the checkbox annotation plugin, the table can have one column per category with 0/1 for negative/positive cases.
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Button-Plugin.png" alt="Plugin-Button" width="1000" height="340">     

- __Annotate with checkboxes__  
An image can be assigned to multiple descriptive keywords.    
The result table contains 1 column per category with 0 if the image is not in the category and 1 if it is.

- __Annotate with lists of choices__  
This plugin allows to describe multiple features and for each features to have a list of choices.  
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Dropdown-plugin.png" alt="Plugin-dropdown" width="900" height="300">     

# Installation
- Activate the *** update site in Fiji
- The plugins appear in the `Plugins > `menu

# Citation
If you use these plugins, please cite:
***
