from pydantic_settings import BaseSettings, SettingsConfigDict

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
    BUCKET_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        env_prefix="AWS_"
    )