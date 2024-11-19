import os
# from dotenv import dotenv_values
import streamlit as st
from groq import Groq


def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# streamlit page configuration
st.set_page_config(
    page_title="Aramco Chatbot",
    page_icon="🤖",
    layout="centered",
)


try:
    # secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = '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'
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# save the api_key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
# INITIAL_MSG = secrets["INITIAL_MSG"]
# CHAT_CONTEXT = secrets["CHAT_CONTEXT"]


client = Groq()

# initialize the chat history if present as streamlit session
if "chat_history" not in st.session_state:
    # print("message not in chat session")
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": "Hi. Paste your new article for summary and sentiment classification."
         },
    ]

# page title
st.title("Aramco Chatbot")
st.caption("Summary and Sentiment classification")
# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role", avatar='🤖'):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Paste your article here")

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "system", "content": '''You are the PR (Public Relations) agency for Saudi Aramco. Your role is to analyze and interpret the sentiment surrounding the company in news articles, and social media posts, and share the news with a short summary highlighting the discussion points around Aramco. 
        Focus on assessing the tone and intent behind statements, identifying whether they are positive, negative, or neutral toward Saudi Aramco.
        In addition to sentiment classification, identify emerging trends, recurring concerns, or topics that reflect public perception of the company.  
        Provide a summary or insights on the underlying themes driving the sentiment for Aramco, in not more than 100 words.  
        Your responses should be concise, professional, and clear, with specific examples if available. I want you to be especially careful about topics related to environmental sustainability, energy production, economic contributions, and corporate responsibility, as these often influence public perception significantly.
        If sentiment is unclear or mixed, categorize it as neutral and specify any positive or negative aspects present. Always ensure that your analysis is objective and fact-based.'''
         },
        {"role": "assistant", "content": ""},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🤖'):
        stream = client.chat.completions.create(
            model = "llama-3.2-3b-preview",
            # model="llama3-8b-8192",
            # model="llama-3.1-70b-versatile",
            messages=messages,
            stream=True  # for streaming the message
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})