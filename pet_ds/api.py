import requests
import json
from pet_ds.config import conf

proxies = (
    {
        "http": conf.proxy,
        "https": conf.proxy,
    }
    if conf.proxy
    else None
)


def simplechat(content: str, stream: bool = True) -> requests.Response:
    response = requests.post(
        url=conf.llm_url,
        headers={
            "Authorization": f"Bearer {conf.api_key}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            # "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps(
            {
                "model": conf.model,
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                "stream": stream,
            }
        ),
        proxies=proxies,
    )
    return response


def completions(messages: list[dict], stream: bool = True) -> requests.Response:
    response = requests.post(
        url=conf.llm_url,
        headers={
            "Authorization": f"Bearer {conf.api_key}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            # "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps(
            {
                "model": conf.model,
                "messages": messages,
                "stream": stream,
            }
        ),
        proxies=proxies,
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
