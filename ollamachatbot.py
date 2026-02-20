import os
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant. respond to QnA"),
        ("user", "Question: {question}")
    ]
)

st.title("Langchain demo with gemma model")
input_text = st.text_input("whats question")

llm = Ollama(model="gemma2:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))