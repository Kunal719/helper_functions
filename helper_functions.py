# -*- coding: utf-8 -*-
"""helper_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lap-XKzes72mZutKjGShNdXhG_KkOUhD

# Helper Functions
"""

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Plot Loss and Accuracy graphs separately.

def plot_loss_curves(history):
  """
  Returns separate curves for training and validation metrics
  """
  loss = history.history["loss"]
  accuracy = history.history["accuracy"]
  val_loss = history.history["val_loss"]
  val_accuracy = history.history["val_accuracy"]
  
  # Number of epochs
  epochs = range(len(history.history["loss"]))

  # Plot the loss
  plt.plot(epochs,loss,label="Training Loss")
  plt.plot(epochs,val_loss,label="Validation Loss")
  plt.title("Loss")
  plt.xlabel("Epochs")
  plt.legend()

  # Plot the accuracy
  plt.figure()
  plt.plot(epochs,accuracy,label="Training Accuracy")
  plt.plot(epochs,val_accuracy,label="Validation Accuracy")
  plt.title("Accuracy")
  plt.xlabel("Epochs")
  plt.legend();

# Preprocesses images and reshapes into a shape which can be recognized by model to predict

def load_and_prep_image(filename, img_shape=224, scale=True):
  """
  Reads an image from filename, turns it into a tensor and reshapes it to (img_shape,img_shape,color_channels)
  """
  # Read an image
  img = tf.io.read_file(filename)
  # Decode the read file into tensor
  img = tf.image.decode_image(img, channels=3) # added channels param if it's a png file because png has 4 color channels
  # Resize the image
  img = tf.image.resize(img,[img_shape,img_shape])
  # Rescale the image and get all values between 0 and 1
  if scale:
    img = img / 255.
    return img
  else:
    return img

# Predict and Plot the reshaped image

def pred_and_plot(model,filename,class_names):
  """
  Imports image located in filename, predicts image class with model, and plots the image with the predicted class as the title
  """
  # Preprocess the image
  img = load_and_prep_image(filename)
  # Make prediction on the image
  pred_prob = model.predict(tf.expand_dims(img, axis=0))
  # Find the prediction class
  pred_class = class_names[int(tf.round(pred_prob)[0][0])]
  # Plot the image with the predicted class as title
  plt.imshow(img)
  plt.title(f"Prediction : {pred_class}")
  plt.axis(False);

# View Random Image from a target folder

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_random_image(target_dir,target_class):
  # Setup the target directory (view image from here)
  target_folder = target_dir + target_class

  # Get a random image path
  random_image = random.sample(os.listdir(target_folder),1)
  print(random_image)

  # Read the image and plot it
  img = mpimg.imread(target_folder + "/" + random_image[0]) #random_image[0] gives value without strings
  plt.imshow(img)
  plt.title(target_class)
  plt.axis("off");

  print(f"Image shape : {img.shape}") # Shape of an image

  return img

# Plot Decision Boundary Curve for non-linear data

def plot_decision_boundary(model,X,y):
  """
  Plots the model's performance/decision boundary based on predictions on X
  """
  # Define the axis boundary via a meshgrid
  x_min,x_max = X[:,0].min(),X[:,0].max()
  y_min,y_max = X[:,1].min(),X[:,1].max()
  xx,yy = np.meshgrid(np.linspace(x_min,x_max,100),
                      np.linspace(y_min,y_max,100))
  
  # Creating X values (predicting on these values)
  x_in = np.c_[xx.ravel(),yy.ravel()]

  # Make predictions
  y_preds = model.predict(x_in)

  # Check if it's multiclass
  if len(y_preds[0]) > 1:
    print("Multi-Class Classification Problem")
    y_preds = np.argmax(y_preds,axis=1).reshape(xx.shape)
  else :
    print("Binary Class Classification Problem")
    y_preds = np.round(y_preds).reshape(xx.shape)

  # Plot the curve
  plt.contourf(xx,yy,y_preds,cmap=plt.cm.RdYlBu,alpha=0.7)
  plt.scatter(X[:,0],X[:,1],c=y,s=40,cmap=plt.cm.RdYlBu)
  plt.xlim(xx.min(),xx.max())
  plt.ylim(yy.min(),yy.max());

# Plot Images with true label and pred and color based on pred made

def plot_image(i,model,true_labels,images,classes):

  #Sometimes i = random.randint(0,len(images)) and i is not defined in the function parameters
  target_image = images[i]
  pred_prob = model.predict(target_image.reshape(1,28,28))
  pred = np.argmax(pred_prob)
  pred_label = classes[pred]
  true_label = classes[true_labels[i]]

  plt.imshow(target_image,cmap=plt.cm.binary)
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  if (pred_label == true_label):
    color="green"
  else:
    color="red"
  
  plt.xlabel(f"{pred_label} ({100*tf.reduce_max(pred_prob):0.2f}%) {true_label}",color=color)

# Plot Multiple Images with graph of prediction probabilites, Was made for MultiClass Classification problems

def plot_multiple_predictions():
  n_rows=5
  n_cols=3
  num_images=n_rows*n_cols
  plt.figure(figsize=(n_cols*2*2,n_rows*2))
  plt.title("Plot Prediction -> Left = Pred Label, Right=True Label")
  for i in range(num_images):
    plt.subplot(n_rows,2*n_cols,2*i+1)
    plot_image(i,model_1,test_labels,test_data,class_names)
    plt.subplot(n_rows,2*n_cols,2*i+2)
    plot_value_array(i,y_probs[i],test_labels)
  plt.tight_layout()
  plt.show();

# Make TensorBoard Callback

import datetime

def create_tensorboard_callback(dir_name, experiment_name):
  """
  Creates a TensorBoard callback instand to store log files.
  Stores log files with the filepath:
    "dir_name/experiment_name/current_datetime/"
  Args:
    dir_name: target directory to store TensorBoard log files
    experiment_name: name of experiment directory (e.g. efficientnet_model_1)
  """
  log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=log_dir
  )
  print(f"Saving TensorBoard log files to: {log_dir}")
  return tensorboard_callback

# Unzip data

import zipfile

def unzip_data(filename):
  """
  Unzips filename into the current working directory.
  Args:
    filename (str): a filepath to a target zip folder to be unzipped.
  """
  zip_ref = zipfile.ZipFile(filename, "r")
  zip_ref.extractall()
  zip_ref.close()

# Walkthrough Directories

import os

def walk_through_dir(dir_path):
  """
  Walks through dir_path returning its contents.
  Args:
    dir_path (str): target directory
  
  Returns:
    A print out of:
      number of subdiretories in dir_path
      number of images (files) in each subdirectory
      name of each subdirectory
  """
  for dirpath, dirnames, filenames in os.walk(dir_path):
    print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'.")

# Calculate Results - y_true,y_preds

# Create a function to get few other classification evaluation methods
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
def calculate_results(y_true,y_preds):
  """
  Calculates model accuracy, recall, precision and f1 score of a binary classification model.
  """
  # Calculate model accuracy
  model_accuracy = accuracy_score(y_true,y_preds) * 100
  # Calculate model precision, recall and f1 score
  model_precision, model_recall, model_f1, _ = precision_recall_fscore_support(y_true,y_preds, average="weighted")
  # Add all results in a dictionary
  model_results = {"Accuracy Score" : model_accuracy,
                   "Precision Score" : model_precision,
                   "Recall Score" : model_recall,
                   "F1 Score" : model_f1}
  return model_results

# Comparing Histories

def compare_historys(original_history, new_history, initial_epochs=5):
    """
    Compares two TensorFlow model History objects.
    
    Args:
      original_history: History object from original model (before new_history)
      new_history: History object from continued model training (after original_history)
      initial_epochs: Number of epochs in original_history (new_history plot starts from here) 
    """
    
    # Get original history measurements
    acc = original_history.history["accuracy"]
    loss = original_history.history["loss"]

    val_acc = original_history.history["val_accuracy"]
    val_loss = original_history.history["val_loss"]

    # Combine original history with new history
    total_acc = acc + new_history.history["accuracy"]
    total_loss = loss + new_history.history["loss"]

    total_val_acc = val_acc + new_history.history["val_accuracy"]
    total_val_loss = val_loss + new_history.history["val_loss"]

    # Make plots
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(total_acc, label='Training Accuracy')
    plt.plot(total_val_acc, label='Validation Accuracy')
    plt.plot([initial_epochs-1, initial_epochs-1],
              plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(total_loss, label='Training Loss')
    plt.plot(total_val_loss, label='Validation Loss')
    plt.plot([initial_epochs-1, initial_epochs-1],
              plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()

# Best Confusion Matrix (MultiClass with percentages)

import itertools
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=15, norm=False, savefig=False): 
  """Makes a labelled confusion matrix comparing predictions and ground truth labels.
  If classes is passed, confusion matrix will be labelled, if not, integer class values
  will be used.
  Args:
    y_true: Array of truth labels (must be same shape as y_pred).
    y_pred: Array of predicted labels (must be same shape as y_true).
    classes: Array of class labels (e.g. string form). If `None`, integer labels are used.
    figsize: Size of output figure (default=(10, 10)).
    text_size: Size of output figure text (default=15).
    norm: normalize values or not (default=False).
    savefig: save confusion matrix to file (default=False).
  
  Returns:
    A labelled confusion matrix plot comparing y_true and y_pred.
  Example usage:
    make_confusion_matrix(y_true=test_labels, # ground truth test labels
                          y_pred=y_preds, # predicted labels
                          classes=class_names, # array of class label names
                          figsize=(15, 15),
                          text_size=10)
  """  
  # Create the confustion matrix
  cm = confusion_matrix(y_true, y_pred)
  cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
  n_classes = cm.shape[0] # find the number of classes we're dealing with

  # Plot the figure and make it pretty
  fig, ax = plt.subplots(figsize=figsize)
  cax = ax.matshow(cm, cmap=plt.cm.Blues) # colors will represent how 'correct' a class is, darker == better
  fig.colorbar(cax)

  # Are there a list of classes?
  if classes:
    labels = classes
  else:
    labels = np.arange(cm.shape[0])
  
  # Label the axes
  ax.set(title="Confusion Matrix",
         xlabel="Predicted label",
         ylabel="True label",
         xticks=np.arange(n_classes), # create enough axis slots for each class
         yticks=np.arange(n_classes), 
         xticklabels=labels, # axes will labeled with class names (if they exist) or ints
         yticklabels=labels)
  
  # Make x-axis labels appear on bottom
  ax.xaxis.set_label_position("bottom")
  ax.xaxis.tick_bottom()

  # Set the threshold for different colors
  threshold = (cm.max() + cm.min()) / 2.

  # Plot the text on each cell
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    if norm:
      plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
              horizontalalignment="center",
              color="white" if cm[i, j] > threshold else "black",
              size=text_size)
    else:
      plt.text(j, i, f"{cm[i, j]}",
              horizontalalignment="center",
              color="white" if cm[i, j] > threshold else "black",
              size=text_size)

  # Save the figure to the current working directory
  if savefig:
    fig.savefig("confusion_matrix.png")

# Create a function to read the lines of a document

def get_lines(filename):
  """
  Reads a text filename, and returns the lines of that text file as a list
  Args:
   filename: A string containing the target file path
  Returns:
   A list of strings with one string per line from the filename
  """
  with open(filename,"r") as f:
    return f.readlines()

# Preprocessing text with line numbers

def preprocess_text_with_line_numbers(filename):
  """
  Returns the list of dictionaries of abstract line data.
  Takes a filename, reads it contents and sorts through each line,
  extracting things like the target label, the text of the sentence, how many sentences
  are there in the current abstract and what sentence number the target line is.
  """
  input_lines = get_lines(filename) # get all the lines from the file
  abstract_lines = "" # create an empty abstract
  abstract_samples = [] # create an empty list of abstracts

  for line in input_lines:
    if line.startswith("###"): # check to see if the line is and ID line
      abstract_id = line
      abstract_lines = "" # reset the abstract string if the line is an ID line
    elif line.isspace(): # check if its a new line
      abstract_line_split = abstract_lines.splitlines() # split abstract into separate lines

      # Iterate through each line in a single abstract and count them at the same time
      for abstract_line_number, abstract_line in enumerate(abstract_line_split):
        line_data = {} # create an empty dictionary for each line
        target_text_split = abstract_line.split("\t") # split target label from text
        line_data["target"] = target_text_split[0] # get the label for the text
        line_data["text"] = target_text_split[1].lower() # get target text and lower the string
        line_data["line_number"] = abstract_line_number # what number line does the line appear in the abstract
        line_data["total_lines"] = len(abstract_line_split) - 1 # how many total lines are in the abstract, starting from 0 so -1
        abstract_samples.append(line_data) # add line data to the abstract samples list
    else: # If the above conditions aren't fulfilled, the lines contain a labeled sentence
      abstract_lines += line # this means all the lines between the id line and the new line belongs to the same abstract

  return abstract_samples

# Plot Time Series Data

def plot_time_series(timesteps,values,format=".",start=0,end=None,label=None):
  """
  Plots timesteps vs values (values across timesteps)

  Parameters
  -----------
  timesteps: array of timesteps values
  values: array of values across timesteps
  format: type of graph, eg - . for scatter, - for line, default = .
  start: start of plot - setting a value will index from the particular timestep
  end: end of plot - setting a value will end the plot at particular timestep
  label: a label to show plot about the values
  """
  # Plot the series
  plt.plot(timesteps[start:end], values[start:end], format, label=label)
  plt.xlabel("Time")
  plt.ylabel("Bitcoin Price")
  if label:
    plt.legend(fontsize=14); # make label bigger
  plt.grid(True);

# MASE Implementation
def mean_absolute_scaled_error(y_true,y_preds):
  """
  Implement MASE provided no seasonality of data is there
  """
  mae = tf.reduce_mean(tf.abs(y_true-y_preds))

  # Find MAE of naive forecast
  mae_naive_no_seasonality = tf.reduce_mean(tf.abs(y_true[1:] - y_true[:-1]))

  return mae / mae_naive_no_seasonality

# Create a function to evaluate all evaluation metrics

def calculate_results_time_series(y_true,y_preds):
  """
  Returns a dictionary of MAE, MSE, RMSE, MAPE, MASE metrics for evaluation
  """
  # Make sure the data is in float32 format
  y_true = tf.cast(y_true, tf.float32)
  y_preds = tf.cast(y_preds, tf.float32)
  
  # Calculate different evaluation scores
  mae = tf.keras.metrics.mean_absolute_error(y_true, y_preds)
  mse = tf.keras.metrics.mean_squared_error(y_true, y_preds)
  rmse = tf.math.sqrt(mse)
  mape = tf.keras.metrics.mean_absolute_percentage_error(y_true, y_preds)
  mase = mean_absolute_scaled_error(y_true, y_preds)
  
  # Check for different horizons by checking the ndims
  if mae.ndim > 0:
    mae = tf.reduce_mean(mae)
    mse = tf.reduce_mean(mse)
    rmse = tf.reduce_mean(rmse)
    mape = tf.reduce_mean(mape)
    mase = tf.reduce_mean(mase)

  return {"MAE":mae.numpy(),
          "MSE": mse.numpy(),
          "RMSE": rmse.numpy(),
          "MAPE": mape.numpy(),
          "MASE": mase.numpy()}

# Create function to label windowed data

def get_labelled_windows(x, horizon=HORIZON):
  """
  Creates labels for windowed dataset

  Example : if horizon=1 then
  Input = [1, 2, 3, 4, 5, 6, 7, 8] -> Output = ([1, 2, 3, 4, 5, 6, 7], [8])
  """
  return x[:,:-horizon],x[:,-horizon:]

# Create function to view Numpy arrays as windows

def make_windows(x, window_size=WINDOW_SIZE, horizon=HORIZON):
  """
  Turns a 1D array to a 2D array of sequential labelled windows with window_size and horizon size labels
  """
  # 1. Create a window of specific window_size (add the horizon at the end for labelling later)
  window_step = np.expand_dims(np.arange(window_size+horizon), axis=0)

  # 2. Create a 2D array of multiple window steps (minus 1 to account for 0 indexing)
  window_indexes = window_step + np.expand_dims(np.arange(len(x) - (window_size+horizon-1)), axis=0).T # create 2D array of windows of size window_size
  # print(f"Window Indexes : \n {window_indexes, window_indexes.shape}")

  # 3. Index on the target array (time series) with 2D array of multiple window steps
  windowed_array = x[window_indexes]
  
  # 4. Get the labelled windows
  windows, labels = get_labelled_windows(windowed_array, horizon=horizon)
  
  return windows,labels

# Create function to make predictions in the future
def make_future_forecasts(values, model, into_future, window_size=WINDOW_SIZE):
  """
  Make future forecasts into_future steps after value ends.
  
  Returns a list of future forecasts
  """
  # 2. Create an empty list for future forecasts/prepare data to forecast on
  future_forecast = []
  last_window = values[-WINDOW_SIZE:]

  # 3. Make into_future number of predictions, altering the data which gets predicted on each
  for _ in range(into_future):
    # Predict on the last window then append it again and again and again (our model will eventually make forecasts on its own forecast)
    future_pred = model.predict(tf.expand_dims(last_window, axis=0))
    print(f"Predicting on : \n {last_window} -> Prediction : {tf.squeeze(future_pred).numpy()}\n")

    # Append predictions to future forecast
    future_forecast.append(tf.squeeze(future_pred).numpy())

    # Update last window with new pred and get WINDOW_SIZE most recent preds
    last_window = np.append(last_window, future_pred)[-WINDOW_SIZE:]
  
  return future_forecast

def get_future_dates(start_date, into_future, offset=1):
  """
  Returns an array of datetime values ranging from start_data to start_data + into_future
  """
  start_date = start_date + np.timedelta64(offset, "D")
  end_date = start_date + np.timedelta64(into_future, "D")
  return np.arange(start_date, end_date, dtype="datetime64[D]")

# Making future forecastts of Bitcoins (using the whole data)
def pred_model_run(values , X, model , into_future , window_size  , horizon, epochs ):

  '''
  This function train a model for every updated predictions. 

  Arguments:
  ----------
      - values --> labels / truth values. Bitcoin prices 
      - X --> Windowed data of the bitcoin prices (default window size is 7)
      - model --> compiled model with default horizon 1 
      - into_future -->  how many time steps to predict in the future? 
      - window_size --> default is 7 (using the 7 days prices of bitcoin)
      - horizon --> default is 1 (predicting the price of next day)

  Returns: 
  --------
      - model --> a model that has been trained on all the previous predictions + the data
  '''
  future_forecast=[]
  last_window = values[-window_size:]
  X_all = X
  y_all = values
  for _ in range(into_future): 

      # Each time the model is trained for 5 epochs with the updated data
      model.fit(x = X_all , y = y_all , epochs = epochs , verbose = 0)

      future_pred = model.predict(tf.expand_dims(last_window, axis= 0))
      #future_pred = model.predict(last_window)
      print(f'Predicing on: \n {last_window} --> Prediction: {tf.squeeze(future_pred).numpy()}\n')

      future_forecast.append(tf.squeeze(future_pred).numpy())
      #values = np.append(values , tf.squeeze(future_pred).numpy())
      for i in range(0 , len(X_all)):
        x = X_all[i][1:]  # removing the 0th index of the X window ()
        y = y_all[1:] # removing the 0th index  of y 
        X = np.append(x , future_pred) # append the future pred at last to X window
        values = np.append(y , future_pred) # appending the future pred to y 

      # Update the last window 
      last_window = np.append(last_window , future_pred)[-window_size:]


  return model,future_forecast
