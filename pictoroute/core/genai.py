"""Module for generating AI responses."""

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI()


async def generate_ai_response_given_messages_and_obtain_chat_response(
    messages, model="gpt-4o"
):
    """Generate an AI response given messages."""
    chat_completion = await client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion.choices[0].message.content


async def generate_ai_response_given_messages_and_obtain_json_response(
    messages, model="gpt-4o"
):
    """Generate an AI response given messages."""
    chat_completion = await client.chat.completions.create(
        messages=messages,
        model=model,
        response_format={"type": "json_object"},
        temperature=0,
    )
    return chat_completion.choices[0].message.content


async def generate_ai_response_user_only(prompt, model="gpt-4o"):
    """Generate an AI response with only user message."""
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content


async def generate_ai_response_user_only_json(prompt, model="gpt-4o"):
    """Generate an AI response with only user message."""
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        response_format={"type": "json_object"},
    )
    return json.loads(chat_completion.choices[0].message.content)


async def generate_ai_response_with_system_message_json(
    prompt, system_message, model="gpt-4o"
):
    """Generate an AI response with a system message."""
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model,
        response_format={"type": "json_object"},
        timeout=30,
    )
    return json.loads(chat_completion.choices[0].message.content)


async def generate_ai_response_with_system_message(
    prompt, system_message, model="gpt-4o"
):
    """Generate an AI response with a system message."""
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1,
        model=model,
        timeout=30,
    )
    return chat_completion.choices[0].message.content


async def vision_response_with_json_response(
    prompt: str, base64_images: list[bytes], model="gpt-4o-mini"
):
    """Generate an AI response with a system message."""
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}] + [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
            ],
        }
        for base64_image in base64_images
    ]

    chat_completion = await client.chat.completions.create(
        messages=messages,
        model=model,
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(chat_completion.choices[0].message.content)


async def claude_vision_response_with_json_response(
    prompt: str, base64_images: list[bytes], model="claude-3-5-sonnet-20241022"
):
    """Generate an AI response with images using Claude 3.5 Sonnet."""
    client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    content = [{"type": "text", "text": prompt}]

    # Add each image to the content array
    for base64_image in base64_images:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image,
                },
            }
        )

    messages = [
        {"role": "user", "content": content},
        {"role": "assistant", "content": "Here is the JSON requested:\n{"},
    ]

    chat_completion = client.messages.create(
        messages=messages,
        model=model,
        max_tokens=8192,
        temperature=0,
    )
    chat_completion = chat_completion.content[0].text

    return json.loads("{" + chat_completion[: chat_completion.rfind("}") + 1])
