import streamlit as st
import llama
import blip
from PIL import Image

st.title("BLIP2 | Llama2 project")


##########################################################################
# Context upload
##########################################################################
# Visual
file_data = st.file_uploader(
    "Upload Images", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

if file_data == None:
    st.warning("File needs to be uploaded")
    st.stop()

# Written
user_instructions = st.text_input("Anything else you want to add...")

# holds until the done button is pushed haha
result = st.button("Generate")
if not result:
    st.stop()

image_bytes = []
for f in file_data:
    image = Image.open(f)
    # st.image(image) #plots the image
    image_bytes.append(f.getvalue())


##########################################################################
# INFERENCE
##########################################################################

with st.spinner('Extracting visual info from images...'):
    visual_concepts = [blip.extract_visual_queues(ib) for ib in image_bytes]

visual_concepts = ', '.join(visual_concepts)
context = f'{user_instructions}. {visual_concepts}'

with st.spinner('Generating letter...'):
    love_letter = llama.generate_letter(context)

# with open("./theodore.txt", 'r') as f:
#     style_reference = f.read()
# with st.spinner('Refining initial renderings...'):
#     love_letter = llama.style_transfer(love_letter, style_reference)

st.write(love_letter)
