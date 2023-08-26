# %%
from langchain.llms import Clarifai
from dotenv import load_dotenv
import os

load_dotenv()

CLARIFAI_API_KEY = os.environ['CLARIFAI_API_KEY']

# %%
llm = Clarifai(pat=CLARIFAI_API_KEY,
               user_id='meta',
               app_id='Llama-2',
               model_id="llama2-70b-chat")

# %%
llm("write me a pizza recipe")
# %%
