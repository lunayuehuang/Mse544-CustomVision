![Tux, the Linux mascot](/Images/part1_1.jpeg)


# Azure Custom Vision for Materials Science

Hello2

About Custom Vision 

test2


# Tutorial Part 1 
## Using Azure Custom Vision to do image classification 


# Tutorial Part 2 
## Using Azure Custom Vision to do image object detection 
### 2.1 Using imageJ to label image for Object Detection 
Install ImageJ 

To install ImageJ, check this website [https://imagej.nih.gov/ij/download.html](https://imagej.nih.gov/ij/download.html)
```markdown
If you are mac user, you might need to enable installation of applications from unidentified developers by Mac. To do that, see this website https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unidentified-developer-mh40616/mac
```
 The user interface of ImageJ looks like this:
<img src="./Images/part2_option2_step2_1.png" style="height: 60%; width: 60%;"/>

Before labeling, go to ```Analyze``` $->$ ```Set Measurement```. In the popped window, choose ```Bounding rectangle``` and ```Add to overlay```. and then click ```ok```

<img src="./Images/part2_option2_step2_2.png" style="height: 40%; width: 40%;"/>

Then, use ```File``` $->$ ```Open``` to open one image, and use ```Rectangle``` (the most left one botton) selection tool to select an area with just one molecule, then press M on your keyboard. It should pop out a ```Results``` window that contains the boxes information. Once all the molecule are labeled, save the measurement as a text file (ending with .txt).

<img src="./Images/part2_option2_step2_3.png" style="height: 80%; width: 70%;"/>

### 2.2 Upload labeled data for training 
 


 