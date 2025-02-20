"""
Demonstrates how to use the ChatInterface widget to create
a math chatbot using OpenAI's text-davinci-003 model with LangChain.
"""

import panel as pn
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.widgets.ChatInterface):
    final_answer = await llm_math.arun(question=contents)
    instance.stream(final_answer, entry=instance.value[-1])


chat_interface = pn.widgets.ChatInterface(callback=callback, callback_user="Langchain")
chat_interface.send(
    "Send a message to get a reply from ChatGPT!", user="System", respond=False
)

callback_handler = pn.widgets.langchain.PanelCallbackHandler(
    chat_interface=chat_interface
)
llm = OpenAI(streaming=True, callbacks=[callback_handler])
llm_math = LLMMathChain.from_llm(llm, verbose=True)
chat_interface.servable()
