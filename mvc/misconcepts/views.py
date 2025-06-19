from django.shortcuts import render

from django.shortcuts import render
from .forms import WatsonPromptForm
import os
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import APIClient
import dotenv
from django.conf import settings
import html

dotenv.load_dotenv()

def page_misconcept_pqc(request):
    result = None
    if request.method == 'POST':
        form = WatsonPromptForm(request.POST)
        if form.is_valid():
            topic1 = form.cleaned_data['topic1']
            print(f"Received topics: {topic1}")
            API_KEY = settings.SECRET_KEY_IBM_WATSON

            wml_credentials = {
                "apikey": API_KEY,
                "url": "https://us-south.ml.cloud.ibm.com"
            }

            project_id = "e0d34c6f-df4d-490c-95c3-ef722dda90b0"

            client = APIClient(wml_credentials)
            client.set.default_project(project_id)

            model = ModelInference(
                model_id="meta-llama/llama-3-3-70b-instruct",
                params={
                    GenParams.MAX_NEW_TOKENS: 400,
                    GenParams.TEMPERATURE: 0.8,
                    GenParams.TOP_P: 0.8
                },
                credentials=wml_credentials,
                project_id=project_id,
            )

            prompt = (
                "You are an expert in quantum computing. "
                "A user has asked a question or made a statement: \"{topic1}\" "
                "First, answer with 'Yes' or 'No' to indicate if the statement is correct. "
                "Then, provide a brief correction or explanation using concepts from PQC, QDK, Quantum Computing, or related topics. "
                "Keep your answer concise and easy to understand for someone new to technology."
            )

            filled_prompt = prompt.format(topic1=topic1)
            try:
                response = model.generate(filled_prompt)
                result = response["results"][0]["generated_text"]
            except Exception as e:
                result = f"Error: {str(e)}"
                # Optionally, you can preprocess the error message for HTML display
                # For example, escape HTML special characters
                result = html.escape(result)

    else:
        form = WatsonPromptForm()

    return render(request, 'misconcepts/misconceptions_pqc.html', {'form': form, 'result': result})
