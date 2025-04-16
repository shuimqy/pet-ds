import requests
import json


url = "https://openrouter.ai/api/v1/chat/completions"


def completions(content: str):
    response = requests.post(
        url=url,
        headers={
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
            # "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            # "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps(
            {
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                "stream": True,
            }
        ),
    )
    return response


# {
#     "model": "text-davinci-003",
#     "prompt": "Say this is a test",
#     "max_tokens": 7,
#     "temperature": 0,
#     "top_p": 1,
#     "n": 1,
#     "stream": false,
#     "logprobs": null,
#     "stop": "n",
# }
