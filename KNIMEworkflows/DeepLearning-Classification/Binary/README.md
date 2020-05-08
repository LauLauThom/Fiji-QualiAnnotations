# Binary classification
This directory contains 2 workflows :
- the first one is for the training of a deep-learning model for binary image-classication  
- the second one is for prediction of images classes for new images using the trained model

__NB__: Binary classification means that there are 2 possible categories for images only, therefore the category column of the annotation table
should contain only 2 possible values. For more categories use the Multi-Class workflow.

The training workflow is inspired by the KNIME example workflow by Christian Dietz for the cats and dog Kaggle classification challenge ([Fine-tune VGG16](https://kni.me/w/EUWPBdnVuIxuFMGf)).
