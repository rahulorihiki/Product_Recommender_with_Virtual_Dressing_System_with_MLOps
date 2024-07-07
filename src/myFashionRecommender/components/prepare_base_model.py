import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from myFashionRecommender.entity.config_entity import PrepareBaseModelConfig
from pathlib import Path

class PrepareBaseModel:
    def __init__(self,config: PrepareBaseModelConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = tf.keras.applications.resnet50.ResNet50(
            include_top = self.config.params_include_top,
            weights = self.config.params_weights,
            input_shape = self.config.params_image_size
        )
        self.model.trainable = False
        
        self.save_model(path=self.config.base_model_path,model = self.model)
    
    @staticmethod
    def _prepare_full_model(base_model):
        model = tf.keras.Sequential(
            [
                base_model,
                tf.keras.layers.GlobalMaxPooling2D()
            ]
        )
        model.summary()
        return model

    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            base_model= self.model
        )
        self.save_model(path=self.config.updated_base_model_path,model=self.full_model)
    
    @staticmethod
    def save_model(path: Path,model: tf.keras.Model):
        model.save(path)