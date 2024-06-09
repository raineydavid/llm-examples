import streamlit as st
from anthropic import Anthropic
from openai import OpenAI
st.set_page_config(
    page_title="File Q&A",
    page_icon="📝",
    
)
#layout="wide"
provider_name ="OPENAI"
PROVIDERS = ["OPENAI","Anthropic"] # need to change provider model to dict
MODELS = ["gpt-3.5-turbo", "claude-v1"]
with st.sidebar:
    provider_name = st.selectbox('Select a Provider', options=PROVIDERS)
   
    api_key_label=f'{provider_name} API Key'
    API_KEY = st.text_input(api_key_label, key="file_qa_api_key", type="password")
   
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title(f"📝 File Q&A with {provider_name}")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not API_KEY:
    st.info(f"Please add your {provider_name} API key to continue.")

if uploaded_file and question and API_KEY:
    if provider_name == PROVIDERS[1]:
        client = Anthropic(api_key=API_KEY)
        model = MODELS[1]
        client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": question},
                  {"role": "user", "content": "Here's an article:\n\n:<article>{article}</article>"},
                  {"role": "assistant", "content": "Here's the question:\n\n: {question}"}
                  ],
        model=model,
        max_tokens=100,
        stop_sequence = any
    else:
        client = OpenAI(api_key=API_KEY)
        model=MODELS[0]
        max_tokens=100
        client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": question},
                  {"role": "user", "content": "Here's an article:\n\n:<article>{article}</article>"},
                  {"role": "assistant", "content": "Here's the question:\n\n: {question}"}
                  ],
        model=model,
        max_tokens=100,
        stop = any,

    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": question},
                  {"role": "user", "content": "Here's an article:\n\n:<article>{article}</article>"},
                  {"role": "assistant", "content": "Here's the question:\n\n: {question}"}
                  ],
        model=model,
        max_tokens=100,
        stop = any,
    ) as stream:
      stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                # messages=[
                #     {"role": m["role"], "content": m["content"]}
                #     for m in st.session_state.messages
                # ],
                messages=updated_messages,
                stream=True,
            )
            st.write("### Answer")
            response = st.write_stream(stream)
    
        st.session_state.messages.append({"role": "assistant", "content": response})

 
   l,


