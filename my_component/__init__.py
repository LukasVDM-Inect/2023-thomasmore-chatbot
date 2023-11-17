import streamlit.components.v1 as components
import streamlit as st

st.title("Component Tutorial!")

_chat = components.declare_component(
    "chat",
    url="http://localhost:3001"
)

return_value = _chat(greeting="Jow", name="Streamlit")
st.write("return value: ", return_value)
