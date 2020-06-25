# Image-classification with Convolutionnal Neural Network (CNN)

This directory contains KNIME workflows for the training of a deep-learning models for image-classification using the Keras integration in KNIME.  
The trained model can be used for the classification of full-size images into custom categories (__but there is no localization of objects__).  
In addition to KNIME, a python installation with Keras installed should be configured in KNIME (See [KNIME documentation](https://docs.knime.com/2019-06/deep_learning_installation_guide/index.html#keras-integration)).

The workflows allow to train a custom CNN made of a pre-trained frozen base (VGG16, pre-trained on the ImageNet dataset for image-classification) used for feature extraction, coupled to fresh new dense layers which are responsible for the classification.  
Coupling a pre-trained base with custom classification layers is called "transfer-learning", as we use features learned from a different classification problem for a new set of images and different image classes. 

The new fresh dense layers will be trained by the workflow for the prediction of custom image-classes, the VGG16 based is not further trained (frozen).  
The VGG16 base could also be fine-tuned to be more specific to the new set of images, but only once the classification layers have been trained for a number of epochs. This is not proposed here to simplify the workflow.  

# Binary and MultiClass ?
The Binary folder contains the workflow to train a binary image-classifier, ie for which the images get classified into possibly 2 categories only.   
The Multiclass folder is the same reasoning, for the training of a model for classification in multiple image classes (2 or more).  
The folder also contains the respective workflows for prediction.   
The difference binary/multiclass is a difference in the classification layers (binary = single sigmoid output, multiclass = multiple categorical outputs).

# Requirements
This workflow requires both a KNIME installation with correct KNIME dependencies AND a python environment with also the right python packages (See below).  
It is also advised to have a CUDA-compatible NVIDIA GPU to speed up the training (2Gb GPU memory should be enough, but more is better).   
The GPU is automatically recognized in KNIME If you have installed the gpu version of tensorflow and keras in python AND if you have installed CUDA on your machine.  

### KNIME
All KNIME dependencies are installed automatically when opening one of the published workflow, except the __KNIME Image Processing - Deep Learning extension__.    
Click [here](https://hub.knime.com/BioML-Konstanz/extensions/org.knime.knip.dl.feature/latest) to install it.  

### Python
The best is to let KNIME install a preconfigured anaconda environment (anaconda should be installed already).  
Go to `File > Preferences > KNIME > Python Deep Learning`
or manually (but tends to fail with tensorflow conflicts...)
- python 3.6.9 or 3.6.10
- tensorflow (or tensorflow-gpu) __version 1.12.0 max__ !
- keras 2.2.4
- pandas 0.24.5

# Training
__The explanations in this section are valid for both the binary and multi-class classifier.__

## Ground-truth data
The ground-truth data is provided by the annotation table which contains the image path and the image-categories.  

- there should be a sufficient amount of ground-truth data (at least a few dozen, no data-augmentation is performed)

- the annotated images (also for prediction) should be single-channel grayscale images (for this workflow and this particular pre-processing)  

- there should be annotated images for each category (relatively obvious) 

- there should be a similar anmount of annotated images for each category, if there are many more images for one category, then the model might not predict well the others

## Image Pre-processing
Deep-learning model do not work on 2048x2048 grayscale full resolution images for instance.  
The workflows takes care of image pre-processing (downscaling, intensity normalization, RGB conversion) and of splitting the dataset into training, validation and test fraction (which proportion can be changed by entering the _Split dataset_ node.  

## Model architecture
The trained model is a hybrid model made of a pre-trained VGG16 base, and new dense layers appended on top.  
Only the dense layers are trained, the base is frozen.  
The base could also be further trained to have features more specific to the new images (fine tuning), but only once the dense layers have been trained for a number of epochs.  This is not proposed in the workflow for simplicity. 

## Training parameters
The parameters for the training (number of epochs, batch size, learning rate...) can be adjusted in the __Keras Network Learner node__.  
The progress of the training (loss and accuracy curves) can be monitored live by opening the training monitor (right-click the Keras Network learner node during training).    

## Exporting the trained model
After the training has completed, the trained model can be saved as a h5 file to use for prediction of image-categories on new images.  
A text file containing the categories names is also saved along the trained model (YourModelFile-classes.txt).  

__Nota Bene__ : Both the trained model and the text file with categories names are necessary for the prediction of image-category for new images using the prediction workflow.


# Prediction
__The explanation in this section are valid for both the binary and multi-class classifier.__

The workflows take as input a list of grayscale images for which one wants to predict the image-categories, provided a model trained using the training workflow.  
The model inputs are the trained model as a h5 file, and the text file containing the image-category names, both of them were generated during training.  
