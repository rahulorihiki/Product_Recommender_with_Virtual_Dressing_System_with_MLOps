from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_include_top: bool
    params_weights: str

@dataclass(frozen=True)
class ExtractionConfig:
    features_root_dir: Path
    files_root_dir: Path
    training_data: Path
    updated_base_model_path: Path

@dataclass(frozen=True)
class DatabaseConfig:
    secret_key: str
    database_uri: str
    fashion_database_path: str
    user_database_path: str

@dataclass(frozen=True)
class AppConfig:
    extracted_features_path: Path
    filenames_path: Path
    model_path: Path
    knn_neighbors: int
    knn_algorithm: str
    knn_metric: str
    image_df_path: Path

    