from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from lightrag.kg.json_kv_impl import JsonKVStorage
import asyncio

load_dotenv()
gemini_key = os.getenv("GOOGLE_API_KEY")
async def llm_model_func(prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs) -> str:
    client = genai.Client(api_key=gemini_key)

    if history_messages is None:
        history_messages = []
    combined_prompt = ""
    if system_prompt:
        combined_prompt += f"{system_prompt}\n"
    for msg in history_messages:
        combined_prompt += f"{msg['role']}: {msg['content']}\n"
        
    combined_prompt += f"user: {prompt}"
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )
    return response.text


async def embedding_func(texts):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings



async def process_query(user_query: str) -> str:
    
    rag = LightRAG(
        working_dir="./data_indexing",
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=embedding_func,
        ),
    )
    
    result = await rag.aquery(
        query=user_query,
        param=QueryParam(mode="hybrid", top_k=5, response_type="single line"),
    )

    return result
