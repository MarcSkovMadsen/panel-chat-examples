"""
Demonstrates how to use the ChatInterface widget to create a chatbot using
OpenAI's GPT-3 API.
"""

import openai
import panel as pn

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": contents}],
        stream=True,
    )
    message = ""
    for chunk in response:
        message += chunk["choices"][0]["delta"].get("content", "")
        yield message


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="ChatGPT")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)
chat_interface.servable()
