import os
from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain


def pdf_summarizer(pdf_url, chunk_size, chunk_overlap, prompt_text, api_key):
    OpenAI.api_key = api_key
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
    loader = PyPDFLoader(pdf_url)
    file = loader.load_and_split()
    file_text = [content.page_content for content in file]
    file_text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    file_chunks = file_text_splitter.create_documents(file_text)
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt_text)
    summary = chain.invoke(file_chunks, return_only_outputs=True)
    return summary['output_text']
