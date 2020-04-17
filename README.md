# Personal note
Currently drag and drop the code on Fiji window for testing purposes.

# Plugins for manual classification of full images
The plugin allow to associate images to 1 or a set of user-defined categories (also called classes).  
It can be used to classifiy images in group suitable for the training of a classifier, or simply to describe the content of an image with defined criterium.  
The categories selected for each image are stored in a result table together with the image name and directory.  
An optional comment can also be added specific for each image.

There are 2 plugins: 
- __Manual_Classifier_Single__ : a single class is associated to each image  
The result table can be chosen to either have a single category column with the name of the assigned category for each image.  
Or like for the multi-classifier, the table can have one column per category with 0/1 for negative/positive cases.

- __Manual_Classifier_Multi__  : an image can be assigned to multiple classes (or descriptive "fields").  
The result table contains 1 column per category with 0 if the image is not in the category and 1 if it is.

# Examples

- Single class per image - single category column

| Index | Folder | Image     | Category | Comments |
|-------|--------|-----------|----------|----------|
| 1     | C:/    | test1.jpg | banana   | blurry   |
| 2     | C:/    | test2.jpg | tomato   |          |

- Single class per image - 1 column per category

| Index | Folder | Image     | Banana | Tomato | Comments |
|-------|--------|-----------|--------|--------|----------|
| 1     | C:/    | test1.jpg | 1      | 0      | blurry   |
| 2     | C:/    | test2.jpg | 0      | 1      |          |

This generates so-called 1-hot encoding and is typically what you need to train a multi-class classifier.  

- Multiple classes per image

| Index | Folder | Image     | Fruit | Red | Yellow | Comments |
|-------|--------|-----------|-------|-----|--------|----------|
| 1     | C:/    | test1.jpg | 1     | 0   | 1      | blurry   |
| 2     | C:/    | test2.jpg | 1     | 1   | 0      |          |
