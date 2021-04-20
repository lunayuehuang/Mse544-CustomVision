<img src="./Images/AzureCustomVision.png" style = "width:100%;">


# Azure Custom Vision for Materials Science

Before getting started, git clone or download this repository (https://github.com/lunayuehuang/Mse544-CustomVision.git) to have all the test data on your local machine.


# Tutorial Part 1
## Using Azure Custom Vision to do Image Classification 

### 1.1 Create resources on Azure Custom Vision.

Go to the Azure Custom Vision portal: [https://www.customvision.ai/](https://www.customvision.ai/) and sign in with your uw-email (it will automatically re-direct you to the UWID authentication page). The main page of the Azure Custom Vision looks like this:
<img src="./Images/AzureCVInterface.png" style="height: 90%; width: 90%;"/>

Click the gear-like setting button, and then in the following page click ```create new``` to create a resource to host projects.  
<img src="./Images/CV_create_resources_step1.png" style="height: 90%; width: 90%;"/>

In the follwoing prompts, fill out the entries for creating the resources as:
<img src="./Images/CV_create_resources_step2.png" style="height: 90%; width: 90%;"/>
the name of the resoure is recommanded as ```cv_<your_UWNetID>```.

Once the resource is created, you can find out the ```Key```, ```Endpoint``` and ```Resource Id``` as following, which will be useful when you incorporate projects using python scripts.
 <img src="./Images/CV_create_resources_step3.png" style="height: 90%; width: 90%;"/>


### 1.2 Create a image classification project using Azure Custom Vision web interface

Use the the eye-like botton on the upper right cornor to navigate back to the project gallery page (the main page). Then click ```New Project``` to create a project. 

<img src="./Images/CV_create_classification_project.png" style="height: 100%; width: 70%;"/>

Once a project is created, go into the project page, it will looks like this:
<img src="./Images/CV_classification_project_page.png" style="height: 90%; width: 90%;"/>
The most important takeaway information is that the buttons on top bar navigates you to different stages of a project. 


### 1.3 Upload images with tags and train model

In this tutorial, we will be using a very small subset, with 10 clear and 10 crystals images, from MARCO to train a model. All the images are stored in ```marco_subset``` folder in this repository. Go the project page, select ```Training Images``` from the top bar, and then ```Add images```. 
<img src="./Images/CV_classification_add_images.png" style="height: 90%; width: 90%;"/>

Then firstly, select all images (using ```shift``` on your keyboard) from ```macro_subset/crystatls_train``` to upload them. 
<img src="./Images/CV_select_crystals_images.png" style="height: 90%; width: 90%;"/>

In the following prompt, type ```crystals``` in the field of ```My Tags```, and then click upload.
<img src="./Images/CV_upload_tag_crystals_images.png" style="height: 90%; width: 90%;"/>

Repeat the same step for images in ```macro_subset/clear_train``` with another tag ```clear```.

Once you finish uploading and taging the images, you will find out on the left side bar, there is a summary of pictures uploaded.
<img src="./Images/CV_classification_tags.png" style="height: 40%; width: 40%;"/>

Now the model is ready for training, click the ```Train``` button on top bar and use ```Quick Training``` to train the model.
<img src="./Images/CV_classification_train_1.png" style="height: 90%; width: 90%;"/>
<img src="./Images/CV_classification_train_2.png" style="height: 60%; width: 60%;"/>

When Training is finished (it will takes less than 5 minutes), you will obtain a page summarizing the training results and metrics.
<img src="./Images/CV_classification_train_results.png" style="height: 90%; width: 90%;"/>

### 1.4 Quick test on the prediction of the model

Once you have a model, you can do ```Quick Test``` with images in ```macro_subset/clear_test``` and ```macro_subset/crystals_test``` to see how is this simple model performs.

For example, click ```Quick Test```,  
<img src="./Images/CV_classification_prediction.png" style="height: 100%; width: 100%;"/>

Then in the propmted window, choose ```Browse local files```, and select one of the image from test folders.
<img src="./Images/CV_classification_prediction_window.png" style="height: 100%; width: 100%;"/>

It will automatically run the image classification on the selected image, and output results as this:
<img src="./Images/CV_classification_prediction_result.png" style="height: 100%; width: 100%;"/>




# Tutorial Part 2 
## Using Azure Custom Vision to do image object detection 

### 2.1 Create a object detection project using Azure Custom Vision web interface 

Similar as step 1.2, we will create a object detection project instead, and the entries of prompted window are filled as:

<img src="./Images/CV_create_object_detection_project.png" style="height: 70%; width: 70%;"/>


### 2.2 Using imageJ to label images for Object Detection 
#### Install ImageJ 

To install ImageJ, check this website [https://imagej.nih.gov/ij/download.html](https://imagej.nih.gov/ij/download.html)
```markdown
If you are mac user, you might need to enable installation of applications from unidentified developers by Mac. To do that, see this website https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unidentified-developer-mh40616/mac
```
 The user interface of ImageJ looks like this:
<img src="./Images/part2_option2_step2_1.png" style="height: 60%; width: 60%;"/>

#### Change measurement settings
Before labeling, go to ```Analyze``` > ```Set Measurement```: 
<img src="./Images/imagej_set_measurement.png" style="height: 60%; width: 60%;"/>

In the prompted window, choose ```Bounding rectangle``` and ```Add to overlay```, then click ```ok```

<img src="./Images/part2_option2_step2_2.png" style="height: 40%; width: 40%;"/>

#### Label molecules in images

For each of the images, the labeling work flow is generally:

- i. Open images using ```File``` > ```Open```, and locate a image in the folder ```molecules```
<img src="./Images/imagej_open_an_image.png" style="height: 60%; width: 60%;"/>


- ii. Use ```Rectangle``` selection tool and select on image with only one molecule, and then press M on your keyboard. A ```Results``` window will be prompted out with all the rectangle coordinates. Repeat this step until all the molecules in the image are labeled.
<img src="./Images/imagej_label_molecules.png" style="height: 80%; width: 80%;"/>
<img src="./Images/imagej_results.png" style="height: 50%; width: 50%;"/>

- iii. Select the ```Results``` window and right click, choose the ```Save``` to save labels as a text file. Normally file name will be same as the image but with an extention as  ```.txt```.
<img src="./Images/imagej_save_results_1.png" style="height: 50%; width: 50%;"/>
<img src="./Images/imagej_save_results_2.png" style="height: 90%; width: 90%;"/>

To save time for this tutorial, we have labeled all images under ```molecules/labels```. However, to ensure you familiar with this work flow, choose at least 3 images for practice this workflow. 

### 2.3 Upload images with labels for training





 