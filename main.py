from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

RUNPOD_API_URL = "https://api.runpod.ai/v2/d0mny4xqj8mbgh/run"
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

@app.get("/")
def root():
    return {"message": "Ollama proxy is up"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        prompt = body["messages"][-1]["content"]

        response = requests.post(
            RUNPOD_API_URL,
            headers={
                "Authorization": f"Bearer {RUNPOD_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"input": {"prompt": prompt}},
            timeout=60
        )

        output = response.json()
        result = output.get("output", "[⚠️ No output from RunPod]")

        return {
            "id": "runpod-completion",
            "object": "chat.completion",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": result
                },
                "finish_reason": "stop",
                "index": 0
            }],
            "model": "runpod-proxy"
        }

    except Exception as e:
        return {
            "id": "exception",
            "object": "chat.completion",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"[⚠️ Exception: {str(e)}]"
                },
                "finish_reason": "stop",
                "index": 0
            }],
            "model": "runpod-proxy"
        }
