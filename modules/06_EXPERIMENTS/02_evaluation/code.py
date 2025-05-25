import time
import phoenix as px
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from phoenix.experiments.types import Example
from phoenix.experiments import run_experiment
from phoenix.evals.default_templates import HALLUCINATION_PROMPT_BASE_TEMPLATE
from phoenix.experiments.evaluators import create_evaluator


client = px.Client(endpoint="http://127.0.0.1:6006")
dataset = client.get_dataset(name="hallucinations")

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    mistral_api_key="..."
)
prompt = PromptTemplate.from_template(HALLUCINATION_PROMPT_BASE_TEMPLATE)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


def get_output(example: Example) -> dict:
    return dict(example.output)


@create_evaluator(name="hallucinations rate", kind="LLM")
def hallucination_evaluator(input: dict, output: dict, metadata: dict) -> int:
    verdict = chain.invoke({
        "input": input["input"],
        "reference": metadata["reference"],
        "output": output["output"]
    })
    time.sleep(2)
    return 1 if verdict == "factual" else 0


run_experiment(
    dataset, get_output,
    evaluators=[hallucination_evaluator],
    experiment_name="hallucination-v1"
)
