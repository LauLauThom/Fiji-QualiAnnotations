This directory contains the workflows to train a multi-class image-classifier, and to use a trained model to classify new images.  
It is the same VGG16 base than for the binary classification.  
However, for the training it takes as input a table generated with the "button" plugin but with one column per category and the binary values (0/1).  
The architecture for the classification layers follows the recommandation of this [PyImageSearch blog post](https://www.pyimagesearch.com/2019/06/03/fine-tuning-with-keras-and-deep-learning/).
