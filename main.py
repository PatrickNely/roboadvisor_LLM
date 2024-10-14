from openai import OpenAI
import streamlit as st
import static.constants as constants

st.title('RoboAdvisor Chatbot')

client = OpenAI(
    api_key=st.secrets['BAICHUAN_KEY'],
    base_url="https://api.baichuan-ai.com/v1/",
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', 'content': constants.WELCOME_MESSAGE_EN}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="Baichuan3-Turbo",
            messages=[
                # {"role": "user", "content": "西游记里有多少妖怪？"}
                {'role': 'system', 'content': constants.SYSTEM_PROMPT_EN}] + 
            [ 
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=0.3,
            stream=True,
            extra_body={
                "tools": [{
                    "type": "retrieval",
                    "retrieval": {
                        "kb_ids": [
                            "kb-123"
                        ]
                    }
                }]
            }
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# completion = client.chat.completions.create(
#     model="Baichuan2-Turbo",
#     messages=[
#         {"role": "user", "content": "西游记里有多少妖怪？"}
#     ],
#     temperature=0.3,
#     stream=True,
#     extra_body={
#         "tools": [{
#             "type": "retrieval",
#             "retrieval": {
#                 "kb_ids": [
#                     "kb-123"
#                 ]
#             }
#         }]
#     }
# )

# for chunk in completion:
#     print(chunk.choices[0].delta)