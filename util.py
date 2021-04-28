from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
from skimage import io
import os


def read_measurements(filename):
    """
    A helper function to read all the rectangular boxes
    Args:
    ----
    filename: str, the file path that contains the all rectangular boxes coordinates 
    
    Return:
    ----
    list of list
    """
    measurements = []
    measure = []
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line != "":
            entires = line.split()
            measurements.append(list(map(int, entires[1:])))
            line = f.readline()

    return measurements 

def normalize_coordinates(inp, shape):
    """
    A helper function to normalize the box coordiantes
    Args:
    ----
    inp: list of int with dimension 4, the raw coordiantes of a rectangular box
    shape: a list or tuple with dimension at least 2, contains the shape of the image 

    Return:
    ----
    list of float with dimension 4, the relative coordiantes of a rectangular box 
    """
    
    return [inp[0] / shape[1], inp[1] / shape[0], 
            inp[2] / shape[1], inp[3] / shape[0]]

class labeledImage():
    """
     a data structure class to store information of a labeled images     
    """
    
    def __init__(self, image_path):
        """
        Class Constructor
        Args:
        ----
        image_path: str, a path where an image is stored
        """
        self.path = image_path
        self.name = image_path.split('/')[-1] 
        self.shape = io.imread(image_path).shape
        self.labels = {}
    
        return

    def add_labels(self, tag, regions):
        """
        Add lablels to the image
        Args:
        ----
        tag: str, label name
        regions: list of list, the inner list should have dimension of 4 that
                 contains the [BX, BY, Wihth, Height] of a retangular box 
        """
        
        if tag not in self.labels.keys():
            self.labels[tag] = regions
        else:
            self.labels[tag] += regions

        return
    
    def add_labels_from_file(self, tag, filename):
        """
        Add labels form a file

        """
        self.add_labels(tag, read_measurements(filename)) 
        
        return
        

    def __str__(self):
        """
        Overriding the printing function, such that when calling
        print(labeledImage) will give all the information
        """
        
        print_str = 'Labeled image ' + self.name + '\n'
        print_str += '    location: ' + self.path + '\n'
        print_str += '    shape: ' + str(self.shape) + '\n'
        print_str += '    lables:'  + '\n'
        for t, labels in self.labels.items():
            print_str += '    - ' + str(t) + ': \n'
            for l in labels:
                print_str += '      ' + str(l) + '\n'
        
        return print_str 

def convert_to_yolo_format(labeled_images, output_path=None, tags=None):
    """ 
    This function converts a list of images labels 
      from ImageJ format: absolute coordinates [Begin_X, Begin_Y, Width, Height]
      to yolo format:     relative coordinates [Center_X, Center_Y, Width, Height] 
    
    Args:
    ----
    labeled_images: list of labledImage
    output_path:  str, by default it will save to the same directory when you execute
                       this script
    tags: pre-assigned tags
    """
    
    # collection all the labels
    if tags is None:
        tags = set()
        for img in labeled_images:
            tags.update(img.labels.keys())
    
        tags = list(tags)
    
    # generate yolo labels for each labeled_images
    if output_path is None:
        output_path = '.'
    
    for img in labeled_images:
        fname = os.path.join(output_path, img.name.split('.')[0] + '.txt')
        
        
        with open(fname, 'w') as f:
            for tag, labels in img.labels.items():
                tag_id = tags.index(tag)
                for l in labels:
                    # compute relative coordinates
                    bx, by, w, h = normalize_coordinates(l, img.shape)
                    cx = bx + w / 2.0
                    cy = by + h / 2.0
                    
                    f.write('%d %.6f %.6f %.6f %.6f \n' %(tag_id, cx, cy, w, h)) 
        
        print('successfully generated labels for image ', img.name)
    
    return tags

class AzureCVObjectDetectionAPI(object):
    """
     A warper class for simplifying the use of Azure Custom Vision Object Detections
    """
    

    def __init__(self, endpoint, key, resource_id, project_id=None):
        """ 
        Class Constructor, takes the id from Azure Custom Vision. Here the key will
        be used both for training and predicition
        
        Args:
        ----
        endpoint: str
        key: str
        resource_id: str
        project_id: str
        """

        training_credentials   = ApiKeyCredentials(in_headers={"Training-key": key})
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})

        self.trainer   = CustomVisionTrainingClient(endpoint, training_credentials)
        self.predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
        self.project_id = project_id
        self.tags = {}

        if project_id is not None:
            for t in self.trainer.get_tags(project_id):
                self.tags[t.name] = t.id
        
        return

    def create_project(self, project_name):
        """
        Create a object detection project with name as project_name. Swith to this project
        when creation is complete.

        Args:
        ----
        project_name: str
        """
        # Find the object detection domain
        obj_detection_domain = next(domain for domain in trainer.get_domains() 
                                    if domain.type == "ObjectDetection" and domain.name == "General")

        # Create a new project
        print ("Creating project...")
        project = trainer.create_project(project_name, domain_id=obj_detection_domain.id)
        self.project_id = project.id

        return

    def create_tag(self, tag_name):
        """
        Create a tag at the current object detection project.

        Args:
        ----
        project_name: str
        """
        assert (self.project_id is not None)
        tag = self.trainer.create_tag(self.project_id, tag_name)
        self.tags[tag.name] = tag.id
        
        return

    def _upload_one_batch_training_images(self, tagged_images_with_regions):
        """
        Upload one batch (maximum 64) training images to Azure Custom Vision Object Detection.
        Only for internal use with in this class.
        
        Args:
        ----
        tagged_images_with_regions: list of ImageFileCreateEntry 
        
        """
        
        upload_result = self.trainer.create_images_from_files(
            self.project_id, ImageFileCreateBatch(images=tagged_images_with_regions))
        
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
            for image in upload_result.images:
                print("Image status: ", image.status)

        return

    def upload_training_images(self, training_labeled_images):
        """
        Upload training images to Azure Custom Vision Object Detection.
        
        Args:
        ----
        training_lableded_images: list of labeledImage
        """
        assert (self.project_id is not None)
        
        print ("Adding images...")
        tagged_images_with_regions = []
        batch = 0

        for i in range(len(training_labeled_images)):
            if i > 0 and ( i % 64 ) == 0:
                batch += 1
                print("Adding images: batch ", batch)
                self._upload_one_batch_training_images(tagged_images_with_regions)
                tagged_images_with_regions = []

            # accumulating labels within one batch
            labeled_img = training_labeled_images[i]
            
            for t, labels in labeled_img.labels.items():
                
                if t not in self.tags.keys(): self.create_tag(t)

                tag_id = self.tags[t]
                
                regions = []
                for m in labels:
                    x,y,w,h = normalize_coordinates(m, labeled_img.shape)
                    regions.append(Region(tag_id=tag_id, left=x,top=y,width=w,height=h))
               
            with open(labeled_img.path, mode="rb") as image_contents:
                tagged_images_with_regions.append(
                    ImageFileCreateEntry(name=labeled_img.name, contents=image_contents.read(), regions=regions))
        
        batch += 1
        if len(tagged_images_with_regions) > 0: 
            print ("Adding images: batch ", batch)
            self._upload_one_batch_training_images(tagged_images_with_regions)

        return 

