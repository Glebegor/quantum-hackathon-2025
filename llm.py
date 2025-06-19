from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import APIClient

wml_credentials = {
    "apikey": "sxwRHiDBd1g47b1lZDGEImMWmboGfTalzdansJz9Yjr0",
    "url": "https://us-south.ml.cloud.ibm.com"
}

project_id = "e0d34c6f-df4d-490c-95c3-ef722dda90b0"

client = APIClient(wml_credentials)
client.set.default_project(project_id)

model_id = "meta-llama/llama-3-3-70b-instruct"
model = ModelInference(
    model_id=model_id,
    params={
        GenParams.MAX_NEW_TOKENS: 800,
        GenParams.TEMPERATURE: 0.7,
        GenParams.TOP_P: 0.9
    },
    credentials=wml_credentials,
    project_id=project_id
)

prompt = "Explain how {topic1} differs from {topic2}."
prompt = prompt.format(topic1="quantum computing", topic2="classical computing")
response = model.generate(prompt)

print("Model Response:\n", response["results"][0]["generated_text"])