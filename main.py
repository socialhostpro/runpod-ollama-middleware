from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

RUNPOD_API_URL = "https://api.runpod.ai/v2/d0mny4xqj8mbgh/run"  # <— your actual endpoint
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    prompt = body["messages"][-1]["content"]

    # Send to RunPod
    response = requests.post(
        RUNPOD_API_URL,
        headers={
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"input": {"prompt": prompt}}
    )

    output = response.json()

    return {
        "id": "runpod-completion",
        "object": "chat.completion",
        "choices": [{
            "message": {
                "role": "assistant",
                "content": output.get("output", "[⚠️ RunPod returned no output]")
            },
            "finish_reason": "stop",
            "index": 0
        }],
        "model": "runpod-proxy",
    }
