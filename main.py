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

    text = data.comment.lower()

    positive_words = [
        "good", "great", "excellent", "amazing", "love",
        "awesome", "fantastic", "best", "wonderful"
    ]

    negative_words = [
        "bad", "worst", "terrible", "awful", "hate",
        "poor", "horrible", "disappointing"
    ]

    score = 3  # neutral baseline

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    # clamp between 1 and 5
    score = max(1, min(5, score))

    if score >= 4:
        sentiment = "positive"
    elif score <= 2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "rating": score
    }