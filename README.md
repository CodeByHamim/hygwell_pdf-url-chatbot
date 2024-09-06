# FastAPI Application with OpenAI Integration

This is a FastAPI-based application that provides three main APIs:

1. **Process Web URL API**: Fetches and processes content from a URL.
2. **Process PDF API**: Extracts and processes text from an uploaded PDF file.
3. **Chat API**: Uses OpenAI's GPT model to answer questions based on the processed content.

## Features

- FastAPI framework for creating RESTful APIs.
- Fetches content from web URLs and processes it.
- Extracts text from PDF files.
- Uses OpenAI's GPT-3.5-turbo model to provide responses to user questions based on the processed data.
- Dockerized for easy deployment.

## Prerequisites

- Python 3.10+
- Docker
- An OpenAI API key for using the Chat API

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CodeByHamim/hygwell_pdf-url-chatbot.git
   ```

## Requirements

* fastapi==0.95.0
* httpx==0.23.3
* openai==0.27.0
* pydantic==1.10.7
* PyPDF2==3.0.1
* uvicorn==0.22.0
