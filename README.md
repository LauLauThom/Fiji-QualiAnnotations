![Twitter Follow](https://img.shields.io/twitter/follow/LauLauThom?style=social)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/laurent132.thomas@laposte.net)

Those Fiji plugins allow to __describe images or image-regions (outlined by ROI) to 1 or a set of user-defined keywords (or categories/classes)__.  
They can be used to perform routine description of sample images, or to generate ground-truth category annotations for the training of a classifier for instance.  
Besides qualitative annotations, any measurement as selected in the Fiji `set Measurements`menu is reported to the table if the option `run Measure` is selected in the plugin.  
The measurements and annotations are reported for the full-image by default.  
To annotate ROI, either draw a new one before making a new annotation (it should be the actively selected ROI), or select existing Roi in the RoiManager before annotating. 

# Installation
- Activate the `Qualitative Annotations` update site in Fiji
- The plugins appear in the `Plugins > Qualitative Annotations` menu

__NB__: The plugins are not compatible with ImageJ, as they rely on some Fiji-specific funcitonalities (script parameters, GenericDialogPlus...)

# Description
There are 3 plugins: 

- __Annotate with buttons__  
A single class is associated to each image.  
The result table can be chosen to either have a single category column with the name of the assigned category for each image.  
Or like with the checkbox annotation plugin, the table can have one column per category with 0/1 for negative/positive cases.
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Button-Plugin.png" alt="Plugin-Button" width="1250" height="300">     

- __Annotate with checkboxes__  
An image can be assigned to multiple descriptive keywords.    
The result table contains 1 column per category with 0 if the image is not in the category and 1 if it is.

- __Annotate with lists of choices__  
This plugin allows to describe multiple features and for each features to have a list of choices.  
When started, the plugin requires a comma-separated value (csv, with comma or semi-column separator) file or tsv (tab-separated) value file with the name of the features and the associated choices.  
Such files can be easily generated in a tabular software like excel (just select saving as csv).  
See the [example csv](https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/KNIMEworkflows/SunburstPlot/DropDownChoices.csv) 
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Dropdown-plugin.png" alt="Plugin-dropdown" width="1000" height="300">     

# Annotate image-regions with ROI
You can annotate image-regions by either drawing or activating an existing ROI before clicking the "Add" or category button.  
The name of the ROI is thus appended to the result table in a dedicated ROI column.  
If you draw new ROI, tick the "Add to Manager" option, otherwise the ROI name will be none (new ROI do not have a name, until saved in the RoiManager).  
If you annotate ROI already stored in the RoiManager, dont tick the "Add To Manager", otherwise you will duplicate each annotated ROI.  

The annotations and measurements (if selected) are saved in the ROI object as properties.  
They can be retrieved using scripting or macro-programing via `Roi.getProperty(key)` or `Roi.getProperties()`.  
With scripting languages, replace Roi with the roi-instance of interest.  
`key` here should be one of the column header of the corresponding annotation table, so if you selected `run Measure` and Mean intensity was selected in Fiji measurement, you can recover `Roi.getProperty("Mean")`.  


# KNIME Worfklows
You can find examples of analysis from the annotation table with KNIME in the `KNIMEworkflows` folder.  
The workflows are documented with README files in their respective folders, especially pay attention to which annotation table is expected by the workflow (ie generated with which plugin).  
To use the worklfow, simply download the knwf file and double-click it to open it in KNIME.  
To download all the workflows at once from GitHub, either clone the repository, or if you dont have github, choose download as zip.
To download single worklfow from GitHub, click the workflow file and choose download on the next page.

Currently there are workflows for:
- [__Image and annotation vizualization__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/ViewImagesAndAnnotations)   
Simply view the image and their annotation in a table. That should be the starting point if you are not familiar with KNIME

- [__Sunburst plot__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/SunburstPlot)    
View the distribution of the qualitative features as concentric circles (like a multi-level pie chart)  

-  [__Deep learning classification__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/DeepLearning-Classification)    
Workflows for the training of a deep-learning model for image-classification, there are 2 subfolders for binary or multi-class classification.   
Workflows for the prediction given a trained network are also provided.



# Citation
If you use these plugins, please cite:
***
