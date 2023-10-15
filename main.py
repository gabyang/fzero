import os
import openai
import pandas as pd
from dotenv import load_dotenv
# from sklearn.metrics import classification_report

load_dotenv()

api_key = os.getenv('OPEN_AI_API_KEY')
openai.api_key = api_key
models = openai.Model.list()
data = pd.DataFrame(models['data'])

text = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "France is most famous for its"}
    ]
)

print(text)

## Text embeddings

