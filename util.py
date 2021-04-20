from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
from skimage import io

def read_measurements(filename):
    
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
    return [inp[0] / shape[1], inp[1] / shape[0], 
            inp[2] / shape[1], inp[3] / shape[0]]

# a data structure class to store data of Images
class labeledImage():
    def __init__(self, image_path):
        self.path = image_path
        self.name = image_path.split('/')[-1] 
        self.shape = io.imread(image_path).shape
        self.labels = {}
    
        return

    def add_labels(self, tag, regions):
        if tag not in self.labels.keys():
            self.labels[tag] = regions
        else:
            self.labels[tag] += regions

        return

    def __str__(self):
        print_str = 'Labeled image ' + self.name + '\n'
        print_str += '    location: ' + self.path + '\n'
        print_str += '    shape: ' + str(self.shape) + '\n'
        print_str += '    lables:'  + '\n'
        for t, labels in self.labels.items():
            print_str += '    - ' + str(t) + ': \n'
            for l in labels:
                print_str += '      ' + str(l) + '\n'
        
        return print_str 

class AzureCVObjectDetectionAPI(object):
    """
     A warper class for simplifying the use of Azure Custom Vision Object Detections
    """
    

    def __init__(self, endpoint, key, resource_id, project_id=None):

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
        # Find the object detection domain
        obj_detection_domain = next(domain for domain in trainer.get_domains() 
                                    if domain.type == "ObjectDetection" and domain.name == "General")

        # Create a new project
        print ("Creating project...")
        project = trainer.create_project(project_name, domain_id=obj_detection_domain.id)
        self.project_id = project.id

        return

    def create_tag(self, tag_name):
        assert (self.project_id is not None)
        tag = self.trainer.create_tag(self.project_id, tag_name)
        self.tags[tag.name] = tag.id
        
        return

    def _upload_one_batch_training_images(self, tagged_images_with_regions):
        upload_result = self.trainer.create_images_from_files(
            self.project_id, ImageFileCreateBatch(images=tagged_images_with_regions))
        
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
            for image in upload_result.images:
                print("Image status: ", image.status)

        return

    def upload_training_images(self, training_labeled_images):
        
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

