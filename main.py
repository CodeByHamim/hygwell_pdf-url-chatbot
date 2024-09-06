from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Dict
import httpx
import openai
from io import BytesIO
from pypdf import PdfReader
import os

app = FastAPI()

content_store: Dict[int, str] = {}

chat_id_counter = 1

class URLRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    chat_id: int
    question: str

def generate_chat_id() -> int:
    global chat_id_counter
    current_id = chat_id_counter
    chat_id_counter += 1
    return current_id

@app.post("/process_url")
async def process_url(request: URLRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request.url)
            response.raise_for_status()

        cleaned_content = response.text.strip()

        chat_id = generate_chat_id()

        content_store[chat_id] = cleaned_content

        return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching URL: {str(e)}")

@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        pdf_reader = PdfReader(BytesIO(pdf_bytes))

        text = ""
        for page in pdf_reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            except Exception as e:
                print(f"Error extracting text from page: {str(e)}")

        cleaned_text = text.strip().replace("\n", " ")

        chat_id = generate_chat_id()

        content_store[chat_id] = cleaned_text

        return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if request.chat_id not in content_store:
            raise HTTPException(status_code=404, detail="Chat ID not found")

        content = content_store[request.chat_id]

        prompt = f"Here is some information: {content}\n\nNow answer this question: {request.question}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        answer = response['choices'][0]['message']['content'].strip()

        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
