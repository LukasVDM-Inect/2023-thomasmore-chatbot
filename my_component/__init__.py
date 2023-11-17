import streamlit as st
from PIL import Image
from pathlib import Path
from image_generator import generate_images_with_icons
import base64


def get_image_base64(image_name):
    media_folder = Path(__file__).parent.parent / 'assets'
    image_path = media_folder / image_name
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def get_image_html(image_path):
    return f"""
    <img 
        src="{image_path}" 
        style="cursor: pointer;" 
        onclick="openFullscreen(this);" 
        width="300"  <!-- Adjust width as needed -->
    />
    <script>
    function openFullscreen(elem) {{
        if (elem.requestFullscreen) {{
            elem.requestFullscreen();
        }} else if (elem.webkitRequestFullscreen) {{ /* Safari */
            elem.webkitRequestFullscreen();
        }} else if (elem.msRequestFullscreen) {{ /* IE11 */
            elem.msRequestFullscreen();
        }}
    }}
    </script>
    """

user_icon = Image.open("./assets/user_icon.png")
ai_icon = Image.open("./assets/ai_icon.png")
tm_logo = Image.open("./assets/thomas_more_logo.png")
inect_logo = Image.open("./assets/inect_logo.png")


st.title('AI Job-fair Assistant')

footer = f"""<style>
a:link , a:visited{{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
}}

a:hover,  a:active {{
    color: red;
    background-color: transparent;
    text-decoration: underline;
}}

.footer {{
    padding-top: 40px;
    z-index: 99;
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    background-color: white;
    color: black;
    text-align: center;
    padding-bottom: 10px;
}}

.footer .logo {{
    height: 40px;
    object-fit: contain;
    padding-left: 10px;
    padding-right: 10px;
}}

.st-emotion-cache-j7ljls {{
    bottom: 80px;
    padding-bottom: 5px
}}

.st-emotion-cache-1y4p8pa {{
    padding: 3rem 1rem 10rem;
}}

.st-emotion-cache-1c7y2kd {{
    flex-direction: row-reverse;
    text-align: right;
}}

</style>
<div class="footer">
    <img class="logo" src="data:image/png;base64,{get_image_base64('thomas_more_logo.png')}"  />
    <img class="logo" src="data:image/png;base64,{get_image_base64('inect_logo.png')}"  />
</div>
<script>
    console.log({tm_logo})
</script>
"""

st.markdown(footer, unsafe_allow_html=True)

prompt = st.chat_input("Ask me something...")

# # Set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#
# # Set a default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

with st.container():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm your job-fair assistant. You can ask me anything but be aware all data is being captured.",
                "avatar": ai_icon
            },
            {
                "role": "assistant",
                "content":
                    '''Ask me something like:  
                    :gray[*Which companies are looking for chemical process engineers?*]  
                    :gray[*Where are the companies that operate in the contruction sector?*]''',
                "avatar": ai_icon
            },
        ]

    # Display chat messages from history on app rerun
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(name=message["role"], avatar=message["avatar"]):
            with st.container():
                st.write(message["content"])
                if hasattr(message, "image"):
                    map_with_icons = Image.open(message["image"])
                    st.image(map_with_icons, width=200)

    # Accept user input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_icon})
        # Display user message in chat message container
        with st.chat_message(name="user", avatar=user_icon):
            st.markdown(prompt)

        # Extract numbers as list
        numbers = [int(num.strip()) for num in prompt.split()]

        # Generate the image
        output_image_path = 'assets/generated/generated_image.png'
        result_image = generate_images_with_icons(numbers, output_image_path)

        # Display the image as a chat message
        with st.chat_message(name="assistant", avatar=ai_icon):
            st.markdown("You can find companies " + prompt + " on the below plan:")
            map_with_icons = Image.open("./assets/generated/generated_image.png")
            # st_image = st.image(image=map_with_icons, width=200)
            image_html = get_image_html("./assets/generated/generated_image.png")
            st.markdown(image_html, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": "You can find companies " + prompt + " on the below plan:",
            "avatar": ai_icon,
            "image": "./assets/generated/generated_image.png"
         })
