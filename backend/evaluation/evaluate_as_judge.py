import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_fireworks import Fireworks, FireworksEmbeddings
from pydantic import SecretStr

import mlflow
from mlflow.deployments import set_deployments_target
from mlflow.metrics.genai import EvaluationExample, faithfulness, relevance

load_dotenv()
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
mlflow.set_experiment("RAG Evaluation")
mlflow.langchain.autolog()
loader = WebBaseLoader("https://mlflow.org/docs/latest/index.html")

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = FireworksEmbeddings(model='nomic-ai/nomic-embed-text-v1.5')
docsearch = Chroma.from_documents(texts, embeddings)

qa = RetrievalQA.from_chain_type(
  llm=Fireworks(
        model="accounts/fireworks/models/llama-v3p1-8b-instruct",
        max_tokens=None,
        temperature=0,
        api_key=SecretStr(os.environ.get("FIREWORKS_API_KEY"))),
  chain_type="stuff",
  retriever=docsearch.as_retriever(),
  return_source_documents=True,
)

def model(input_df):
  answer = []
  for index, row in input_df.iterrows():
      answer.append(qa(row["questions"]))

  return answer

eval_df = pd.DataFrame(
  {
      "questions": [
          "What is MLflow?",
          "How to run mlflow.evaluate()?",
          "How to log_table()?",
          "How to load_table()?",
      ],
  }
)

faithfulness_examples = [
  EvaluationExample(
      input="How do I disable MLflow autologging?",
      output="mlflow.autolog(disable=True) will disable autologging for all functions. In Databricks, autologging is enabled by default. ",
      score=2,
      justification="The output provides a working solution, using the mlflow.autolog() function that is provided in the context.",
      grading_context={
          "context": "mlflow.autolog(log_input_examples: bool = False, log_model_signatures: bool = True, log_models: bool = True, log_datasets: bool = True, disable: bool = False, exclusive: bool = False, disable_for_unsupported_versions: bool = False, silent: bool = False, extra_tags: Optional[Dict[str, str]] = None) → None[source] Enables (or disables) and configures autologging for all supported integrations. The parameters are passed to any autologging integrations that support them. See the tracking docs for a list of supported autologging integrations. Note that framework-specific configurations set at any point will take precedence over any configurations set by this function."
      },
  ),
  EvaluationExample(
      input="How do I disable MLflow autologging?",
      output="mlflow.autolog(disable=True) will disable autologging for all functions.",
      score=5,
      justification="The output provides a solution that is using the mlflow.autolog() function that is provided in the context.",
      grading_context={
          "context": "mlflow.autolog(log_input_examples: bool = False, log_model_signatures: bool = True, log_models: bool = True, log_datasets: bool = True, disable: bool = False, exclusive: bool = False, disable_for_unsupported_versions: bool = False, silent: bool = False, extra_tags: Optional[Dict[str, str]] = None) → None[source] Enables (or disables) and configures autologging for all supported integrations. The parameters are passed to any autologging integrations that support them. See the tracking docs for a list of supported autologging integrations. Note that framework-specific configurations set at any point will take precedence over any configurations set by this function."
      },
  ),
]

faithfulness_metric = faithfulness(
  model="openai:/gpt-4o", examples=faithfulness_examples
)
print(faithfulness_metric)

relevance_metric = relevance(model="openai:/gpt-4o")
print(relevance_metric)

results = mlflow.evaluate(
  model,
  eval_df,
  model_type="question-answering",
  evaluators="default",
  predictions="result",
  extra_metrics=[faithfulness_metric, relevance_metric, mlflow.metrics.latency()],
  evaluator_config={
      "col_mapping": {
          "inputs": "questions",
          "context": "source_documents",
      }
  },
)
print(results.metrics)
print(results.tables["eval_results_table"])

