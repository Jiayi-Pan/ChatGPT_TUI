import httpx
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
timeout = httpx.Timeout(60.0) # for long messages, the API can take a while to respond

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY environment variable not set")

async def get_openai_response(content)-> tuple[bool, str]:
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": content
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return (True, response.json()['choices'][0]['message']['content'])
        except Exception as e:
            return (False, repr(e))