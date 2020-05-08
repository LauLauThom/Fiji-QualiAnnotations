# Image-classification with Convolutionnal Neural Network (CNN)
This directory contains KNIME workflows for the training of a deep-learning models for image-classification using the Keras integration in KNIME.  
The trained model can be used for the classification of full-size images into custom categories (__but there is no localization of objects__).  
In addition to KNIME, a python installation with Keras installed should be configured in KNIME (See [KNIME documentation](https://docs.knime.com/2019-06/deep_learning_installation_guide/index.html#keras-integration)).

The workflows allow to train a custom CNN made of a pre-trained frozen base (VGG16, pre-trained on the ImageNet dataset for image-classification) used for feature extraction, coupled to fresh new dense layers which are responsible for the classification.  
Coupling a pre-trained base with custom classification layers is called "transfer-learning", as we use features learned from a different classification problem for a new set of images and different image classes. 

The new fresh dense layers will be trained by the workflow for the prediction of custom image-classes, the VGG16 based is not further trained (frozen).  
The VGG16 base could also be fine-tuned to be more specific to the new set of images, but only once the classification layers have been trained for a number of epochs. This is not proposed here to simplify the workflow.  
