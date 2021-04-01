[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4063891.svg)](https://doi.org/10.5281/zenodo.4063891)
![Twitter Follow](https://img.shields.io/twitter/follow/LauLauThom?style=social)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/laurent132.thomas@laposte.net)

Those Fiji plugins allow the __annotations of images or image-regions (outlined by ROI) with user-defined keywords (categories/classes)__.  
They can be used to perform routine description of sample images, or to generate ground-truth category annotations for the training of a classifier for instance.  
Besides qualitative annotations, any measurement as selected in the Fiji `Analyze > set Measurements`menu is reported to the table if the option `run Measure` is selected in the initial configuration window.  
The measurements and annotations are reported for the full-image by default.  
To annotate ROI, either draw a new one before making a new annotation (it should be the actively selected ROI), or select existing Roi in the RoiManager before annotating. 

# Installation
- Activate the `Qualitative Annotations` update site in Fiji (Help > Update > Manage Update sites)
- The plugins appear in the `Plugins > Qualitative Annotations` menu

__NB__: The plugins are not compatible with ImageJ, as they rely on some Fiji-specific funcitonalities (script parameters, GenericDialogPlus...)

# Citation
The plugins are extensively described in the following article (open-access).  
Supplementary Figures are available on Zenodo (click the DOI badge at the top of this page).  

Thomas LSV, Schaefer F and Gehrig J.   
_Fiji plugins for qualitative image annotations: routine analysis and application to image classification_ [version 1; peer review: awaiting peer review].   
F1000Research 2020, 9:1248   
https://doi.org/10.12688/f1000research.26872.1

# Video Tutorials
Check the dedicated [youtube playlist](https://www.youtube.com/playlist?list=PLbBgXlYof3_YVqR80jhFPCkc0M3GQMAq4) covering from the introduction of the plugins to the use of the analysis workflows.  
Or click on the image below to open the first tuto in youtube.  

[![YouTube](https://img.youtube.com/vi/TUzjM7n4fb8/0.jpg)](https://www.youtube.com/watch?v=TUzjM7n4fb8)


# Description
The update site provides 3 annotations plugins and 2 visualization plugins: 

## Annotation plugins
__NOTE__  
For the single-class and checkbox plugins, you can now specify if you want to populate the initial set of categories by :  
- recalling the values from the previous session (memory)
- parsing a previous annotation table currently opened in Fiji
- reading a text file containing 1 category name per row (see [example](https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/category-dialog/Fiji.app/lib/CategoryTextFile.txt))

---


- __Single class (buttons)__  
A single class is associated to each image.  
The result table can be chosen to either have a single category column with the name of the assigned category for each image.  
Or like with the checkbox annotation plugin, the table can have one column per category with 0/1 for negative/positive cases.
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Button-Plugin.png" alt="Plugin-Button" width="1250" height="300">     

- __Multi-class (checkboxes)__  
An image can be assigned to multiple descriptive keywords.    
The result table contains 1 column per category with 0 if the image is not in the category and 1 if it is.

- __Multi-class (dropdown)__  
This plugin allows to describe multiple features and for each features to have a list of choices.  
When started, the plugin requires a comma-separated value (csv, with comma or semi-column separator) file or tsv (tab-separated) value file with the name of the features and the associated choices.  
Such files can be easily generated in a tabular software like excel (just select "Saving as csv").  
An example of csv is shipped with the update site, and should be in your Fiji installation at *Fiji.app/lib*.  
Also see the [example input files](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/Fiji.app/lib) (click the "raw" button to see the file content) and the associated [wiki section ](https://github.com/LauLauThom/Fiji-QualiAnnotations/wiki/Input-for-the-dropdown-plugin).  
<img src="https://github.com/LauLauThom/Fiji-QualiAnnotations/blob/master/images/Dropdown-plugin.png" alt="Plugin-dropdown" width="1000" height="300">     

## Visualization plugins

- __Pie Chart from data-column__  
Allows the visualization of the data-distribution from a table column in Fiji.  
The plugin uses the JFreeChart library and is macro-recrodable.  
See Supplementary Figure 2 on Zenodo (click the DOI link at the top of this page).   
__NOTE__: As pointed out on [Twitter](https://twitter.com/MarionLouveaux/status/1362145060922482689), it's difficult to distinguish pie charts section with similar sizes, while it's more obvious with a bar chart

- __Bar Chart from data-column__  
Similar to the Pie chart plotting. With this one you get one bar per category, which is a bit more readable if the population for each bar have similar sizes.  

# Annotate image-regions with ROI
You can annotate image-regions by either drawing a new roi or selecting one or multiple existing ROI stored in the RoiManager before clicking the "Add" or category button.  
Newly drawn roi are automatically added to the Roi Manager.  
The name of the ROI(s) is thus appended to the result table in a dedicated ROI column.  

Besides, the annotations and measurements (if selected) are saved in the ROI object as properties.  
They can be retrieved using scripting or macro-programing via `Roi.getProperty(key)` or `Roi.getProperties()`.  
With scripting languages, replace Roi with the roi-instance of interest.  
`key` here should be one of the column header of the corresponding annotation table, so if you selected `run Measure` and Mean intensity was selected in Fiji measurement, you can recover `Roi.getProperty("Mean")`.  


# KNIME Worfklows
You can find examples of analysis from the annotation table with KNIME in the `KNIMEworkflows` folder.  
The workflows are documented with README files in their respective folders, especially pay attention to which annotation table is expected by the workflow (ie generated with which plugin).  
To use the worklfows, simply download the knwf file and double-click it to open it in KNIME.   
To download all the workflows at once from GitHub, either clone the repository, or if you dont have github, choose download as zip.  
To download a single workflow from GitHub, click the workflow file and choose download on the next page.  
The workflows can also be downloaded directly from the [KNIME Hub](https://hub.knime.com/l.thomas/spaces/Exploitation%20of%20qualitative%20image%20annotations/latest/).   

Currently there are workflows for:
- [__Image and annotation vizualization__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/ViewImagesAndAnnotations)   
Simply view the image and their annotation in a table. That should be the starting point if you are not familiar with KNIME

- [__Sunburst chart__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/SunburstPlot)    
View the distribution of the qualitative features as concentric circles (like a multi-level pie chart)  

-  [__Deep learning classification__](https://github.com/LauLauThom/Fiji-QualiAnnotations/tree/master/KNIMEworkflows/DeepLearning-Classification)    
Workflows for the training of a deep-learning model for image-classification (1 class per image), there are 2 subfolders wether the images can be classified into 1 class out 2 classes (binary) or into 1 class out of 2 or more classes (multi-class).     
Workflows for the prediction given a trained network are also provided.  
Also see the wiki page about the [Keras Network learner node](https://github.com/LauLauThom/Fiji-QualiAnnotations/wiki/Keras-Network-Learner-node), and Supplementary Figure 4 and 5 on Zenodo.   

# Example dataset  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3997728.svg)](https://doi.org/10.5281/zenodo.3997728)  
An example of images from a related screening project in Zebrafish is available on Zenodo.  
The Zenodo repository contains a zip archive with the images, ground-truth category annotations for the images (generated with the plugins) and a trained deep-learening model for classification of the images.  
