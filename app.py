import json
from langchain_community.llms import Cohere
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts  import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import ast

import ast
import base_utilites as bu
from langchain_cohere import CohereEmbeddings

import json
from langchain_community.llms import Cohere
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts  import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import ast


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_answer(question) : 

    with open(bu.format_path(
        '''
        Assets/
            JSONs/
                data.json
        '''
    )) as fil : data = json.load(fil)
    data = ast.literal_eval(data)

    prompt = open(bu.format_path(
        '''
        Assets/
            Prompts/
                Context.txt
        '''
    )).read()

    chunks = [
        prompt.format(key , data[key])
        for key 
        in data.keys()
    ]

    cohere_api_key = open(bu.format_path(
        '''
        Assets/
            Prompts/
                api_key.txt
        '''
    )).read()

    embeddings = CohereEmbeddings(cohere_api_key = cohere_api_key)
    vectorstore = FAISS.from_texts(chunks , embedding = embeddings)
    retriever = vectorstore.as_retriever(search_type = 'similarity' , search_kwargs = {'k' : 1})

    prompt = PromptTemplate.from_template(template=open(bu.format_path(
        '''
        Assets/
            Prompts/
                Main.txt
        '''
    )).read())

    cohere_llm = Cohere(model = 'command' , temperature = 0.1 , cohere_api_key = cohere_api_key)
    
    rag_chain = (
        {'context' : retriever | format_docs , 'question' : RunnablePassthrough()}
        | prompt
        | cohere_llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)

import streamlit as st 

def check_prompt(prompt) : 

    try : 
        prompt.replace('' , '')
        return True 
    except : return False


def check_mesaage() : 
    '''
    Function to check the messages
    '''

    if 'messages' not in st.session_state : st.session_state.messages = []

check_mesaage()

for message in st.session_state.messages : 

    with st.chat_message(message['role']) : st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')

if check_prompt(prompt) :

    with st.chat_message('user') : st.markdown(prompt)

    st.session_state.messages.append({
        'role' : 'user' , 
        'content' : prompt
    })

    if prompt != None or prompt != '' : 

        response = get_answer(prompt)

        with st.chat_message('assistant') : st.markdown(response)


        st.session_state.messages.append({
            'role' : 'assistant' , 
            'content' : response
        })
