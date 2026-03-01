from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware

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

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Analyze the sentiment of this comment: {data.comment}",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "sentiment_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "sentiment": {
                                "type": "string",
                                "enum": ["positive", "negative", "neutral"]
                            },
                            "rating": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5
                            }
                        },
                        "required": ["sentiment", "rating"],
                        "additionalProperties": False
                    }
                }
            }
        )

        print("RAW RESPONSE:", response)
        return response.output_parsed

    except Exception as e:
        print("FULL ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))