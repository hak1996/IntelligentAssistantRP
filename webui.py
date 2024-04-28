
import streamlit as st
from KB_function.RetriverQuery import RetriverQuery

@st.cache_resource
def ConstructQueryContext(top_k=5):
    r = RetriverQuery()
    r.ConstructContext(top_k)
    return r


def get_response(r, query):
    return r.query(query)



def ui_demo(context):

    topk = st.sidebar.slider('How many commits to retrieve', 1, 10, 3)
    if "config_topk" not in st.session_state.keys() or topk != st.session_state.config_topk:
        context.ConstructContext(topk)
        st.session_state.config_topk = topk

    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Ask me a question!"}
        ]

    if "show_ref" not in st.session_state.keys():
        st.session_state.show_ref = False

    if "references" not in st.session_state.keys():
        st.session_state.references = ""

    if st.sidebar.button("Clear chat history"):
        st.session_state.messages.clear()
        st.session_state.show_ref = False
        st.session_state.messages.append(
            {"role": "assistant",
             "content": "Ask me a question!"})

    if st.sidebar.button("Show references"):
        st.session_state.show_ref = True

    if st.sidebar.button("Hide references"):
        st.session_state.show_ref = False


    if query := st.chat_input("Your question"):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": query})

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        st.session_state.show_ref = False
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                human_input = st.session_state.messages[-1]["content"]
                response, ref = context.query(human_input)
                st.session_state.references = ref
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

    if st.session_state.show_ref == True:
        with st.chat_message("Reference"):
            st.write(st.session_state.references)

st.set_page_config(page_title="Intelligent assistant in radiation protection")
st.markdown("# Chat with intelligent assistant in radiation protection")
st.sidebar.header("Configurations")
context = ConstructQueryContext()

ui_demo(context)
