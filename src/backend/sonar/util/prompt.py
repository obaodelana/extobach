from typing import Any
from functools import wraps, partial
from inspect import getdoc
import os
import requests


def prompt(func=None, *,
           max_tokens=500,
           temperature=0.1,
           json_schema: dict[str, Any] | None = None):
    """
    Transforms a function that returns a string into
    a function that returns Sonar's response in JSON.

    - It uses the original function's docstring as the system instruction.
    - It uses the return value of the original function as the user prompt.

    The decorated function returns Sonar's JSON response.
    """

    """
    - When `prompt` is applied without any arguments, so just "@prompt",
      the function next to it is automatically passed in, so `func`
      will not be "None".
    - On the other hand, when we have "@prompt(country_code="us", ...),
      then `func` is "None". But since arguments are included, we are 
      effectively calling the function `prompt`. So we then return
      a decorator function with no arguments. That is, we return
      "@prompt" with all the arguments already applied.
      (That's what `partial` does.)
    """
    if func is None:
        return partial(prompt,
                       max_tokens=max_tokens,
                       temperature=temperature,
                       json_schema=json_schema)

    @wraps(func)
    def wrapper(*args, **kwargs) -> dict:
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": getdoc(func)
                },
                {
                    "role": "user",
                    "content": func(*args, **kwargs)
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "return_images": True,
            "response_format": ({
                "type": "json_schema",
                "json_schema": {"schema": json_schema}
            } if json_schema else None),
            "web_search_options": {
                "search_context_size": "low",
            }
        }

        api_key = os.getenv("PERPLEXITY_API_KEY", None)
        assert api_key is not None, "Can't find 'PERPLEXITY_API_KEY' environment variable"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json()

    return wrapper
