from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class Summarizer:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key)
        self.prompt_template = PromptTemplate(
            input_variables=["results"],
            template="Summarize the following Jira ticket search results: {results}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def summarize(self, results):
        results_text = "\n".join([f"Ticket ID: {result['ticket_id']}, Similarity: {result['similarity']}" for result in results])
        summary = self.chain.run(results=results_text)
        return summary
