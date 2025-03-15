import mlflow
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset
import pandas as pd
from dotenv import load_dotenv
from ragas import EvaluationDataset


load_dotenv()
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Sample data (replace with your actual data)
data = [{
    'question': ['What is MLflow?', 'How does RAGAS work?'],
    'context': ['MLflow is an open source platform for managing the end-to-end machine learning lifecycle.', 
                'RAGAS provides metrics for evaluating retrieval augmented generation systems.'],
    'answer': ['MLflow is a platform for ML lifecycle management.', 
               'RAGAS evaluates RAG systems using various metrics.'],
    'ground_truth': ['MLflow is an open source platform for ML lifecycle management.', 
                     'RAGAS evaluates RAG systems with metrics like faithfulness and relevancy.']
}]


# Create a dataset
#dataset = Dataset.from_pandas(pd.DataFrame(data))
dataset = EvaluationDataset.from_list(data)

# Set up MLflow
mlflow.set_experiment("LLM_Evaluation_RAGAS")

# Start an MLflow run
with mlflow.start_run():
    # Run RAGAS evaluation
    result = evaluate(
        llm="gpt-4o-mini",
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ]
    )
    
    # Log RAGAS metrics to MLflow
    for metric_name, metric_value in result.items():
        mlflow.log_metric(metric_name, metric_value)
    
    # Log the dataset as an artifact
    mlflow.log_dict(data, "evaluation_data.json")
    
    # Optional: Log any parameters
    mlflow.log_param("model_name", "GPT-3.5")
    mlflow.log_param("dataset_size", len(dataset))

print("Evaluation complete. Results logged to MLflow.")
