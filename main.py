from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

@app.post("/comment")
async def analyze_comment(data: CommentRequest):

    if not data.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis API. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this comment: {data.comment}"
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print("FULL ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))