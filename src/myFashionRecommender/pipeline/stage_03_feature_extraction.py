from myFashionRecommender.config.configuration import ConfigurationManager
from myFashionRecommender.components.feature_and_filenames_extraction import FeatureExtraction
from myFashionRecommender import logger

STAGE_NAME = "Filenames and Feature Extraction"

class FeatureExtractionPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        extraction_config = config_manager.get_extraction_config()
        feature_extraction = FeatureExtraction(extraction_config)
        feature_extraction.main_extraction()

if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = FeatureExtractionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e