from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class DatasetSettings(BaseSettings):
    TRAIN_FILE: str
    TEST_FILE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_prefix="DATASET_"
    )

class AWSSettings(BaseSettings):
    EXECUTION_ROLE: str
    BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_prefix="AWS_"
    )

class APISettings(BaseSettings):
    ROBERTA_URL: str
    TINYBERT_URL: str 
    TAC_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_prefix="API_"
    )