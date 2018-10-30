required extensions: jieba, tensorflow
1. run **segmentation.py** to filter stop words and split the corpus
2. run **positivenegative.py** to divide train set into positive set and negative set
3. run **train.py** to train a Text_CNN for classifying data and save the corresponding model
4. run **eval.py** to restore the model and make predictions on the test set