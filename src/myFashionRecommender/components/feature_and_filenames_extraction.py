from contextlib import contextmanager
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm
from tensorflow.keras.models import load_model
import pickle
from PIL import Image
from myFashionRecommender.entity.config_entity import ExtractionConfig
import os
import sys

# Suppress TensorFlow warnings and info ( But the below lines do not work atleast for this code even though It is supposed to work.)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# Below code is the alternate way to suppress the warnings and info because the above code does not work.
@contextmanager
def suppress_tf_output():
    # Suppress stdout and stderr
    try:
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        yield
    finally:
        sys.stdout = stdout
        sys.stderr = stderr

class FeatureExtraction:
    def __init__(self, config: ExtractionConfig):
        self.config = config

    def extract_features(self,img_path,model):
        img = image.load_img(img_path,target_size=(224,224))
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)
        with suppress_tf_output():
            result = model.predict(preprocessed_img).flatten()
        normalized_result = result / norm(result)

        return normalized_result

    def main_extraction(self):
        filenames = []

        for file in os.listdir(self.config.training_data):
            filenames.append(os.path.join(self.config.training_data,file))

        feature_list = []
        model = load_model(self.config.updated_base_model_path)

        for file in tqdm(filenames):
            feature_list.append(self.extract_features(file,model))

        feature_list_path = os.path.join(self.config.features_root_dir, 'model.pkl')
        filenames_path = os.path.join(self.config.files_root_dir, 'filenames.pkl')

        pickle.dump(feature_list, open(feature_list_path, 'wb'))
        pickle.dump(filenames, open(filenames_path, 'wb'))