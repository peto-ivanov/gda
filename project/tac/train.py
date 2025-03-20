import sagemaker
from sagemaker.huggingface import HuggingFace

# Initialize SageMaker session and role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Define hyperparameters for RoBERTa fine-tuning
hyperparameters = {
    "model_name_or_path": "roberta-base",
    "task_name": "classification",
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "learning_rate": 2e-5,
    "num_train_epochs": 3,
    "output_dir": "/opt/ml/model",
    "do_train": True,
    "do_eval": True,
}

# Define training and validation dataset S3 paths
training_data_s3 = "s3://your-bucket-name/path-to-training-data"
eval_data_s3 = "s3://your-bucket-name/path-to-eval-data"

# Configure the Hugging Face Estimator
huggingface_estimator = HuggingFace(
    entry_point="train.py",  # Your training script
    source_dir="./scripts",  # Directory containing training script
    instance_type="ml.p3.2xlarge",
    instance_count=1,
    role=role,
    transformers_version="4.6",
    pytorch_version="1.7",
    py_version="py36",
    hyperparameters=hyperparameters,
)

# Launch the training job
huggingface_estimator.fit({
    "train": training_data_s3,
    "eval": eval_data_s3,
})
