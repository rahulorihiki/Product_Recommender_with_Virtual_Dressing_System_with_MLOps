from myFashionRecommender.constants import *
from myFashionRecommender.utils.common import read_yaml,create_directories
from myFashionRecommender.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig,ExtractionConfig,DatabaseConfig,AppConfig)


class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH,
            secrets_filepath = SECRETS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.secrets = read_yaml(secrets_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:

        config = self.config.prepare_base_model

        create_directories([config.root_dir])
        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir = Path(config.root_dir),
            base_model_path = Path(config.base_model_path),
            updated_base_model_path = Path(config.updated_base_model_path),
            params_image_size = self.params.IMAGE_SIZE,
            params_include_top = self.params.INCLUDE_TOP,
            params_weights = self.params.WEIGHTS
        )
        return prepare_base_model_config
    
    def get_extraction_config(self):
        config = self.config.feature_extraction
        model_config = self.config.prepare_base_model

        create_directories([config.features_root_dir])
        create_directories([config.files_root_dir])

        extraction_config = ExtractionConfig(
            features_root_dir = config.features_root_dir,
            files_root_dir = config.files_root_dir,
            training_data = config.local_data_file,
            updated_base_model_path = model_config.updated_base_model_path,
            
        )
        return extraction_config
    
    def get_database_config(self):
        database_config = self.secrets.database_secrets

        database_config = DatabaseConfig(
            secret_key = database_config.secret_key,
            database_uri = database_config.database_uri,
            fashion_database_path = database_config.fashion_database_path,
            user_database_path = database_config.user_database_path
        )
        return database_config
    
    def get_app_config(self):
        app_config = self.config.flask_app

        app_config = AppConfig(
            extracted_features_path= app_config.extracted_features_path,
            filenames_path= app_config.filenames_path,
            model_path= app_config.model_path,
            knn_neighbors= app_config.knn_neighbors,
            knn_algorithm= app_config.knn_algorithm,
            knn_metric= app_config.knn_metric,
            image_df_path= app_config.image_df_path,
        )
        return app_config

