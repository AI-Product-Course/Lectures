import pandas as pd
import phoenix as px


df = pd.DataFrame(
    [
        {
            "reference": "The Eiffel Tower is located in Paris, France. It was constructed in 1889 as the entrance arch to the 1889 World's Fair.",
            "input": "Where is the Eiffel Tower located?",
            "output": "The Eiffel Tower is located in Moscow, Russia.",
        },
        {
            "reference": "The Eiffel Tower is located in Paris, France. It was constructed in 1889 as the entrance arch to the 1889 World's Fair.",
            "input": "When is the Eiffel Tower created?",
            "output": "It was created in 1889",
        },
        {
            "reference": "The Eiffel Tower is located in Paris, France. It was constructed in 1889 as the entrance arch to the 1889 World's Fair.",
            "input": "Who is the Eiffel Tower's author?",
            "output": "The author is Andrew Eiffel",
        },
    ]
)
phoenix_client = px.Client(endpoint="http://127.0.0.1:6006")
dataset = phoenix_client.upload_dataset(
    dataframe=df,
    dataset_name="hallucinations",
    input_keys=["input"],
    output_keys=["output"],
    metadata_keys=["reference"],
)
