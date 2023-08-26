import streamlit as st
import description_generator
from PIL import Image
import io

st.title("Instagram Photo Description Generator")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("Writing the description...")

    # Convert image to bytes
    byte_img = io.BytesIO()
    image.save(byte_img, format="PNG")
    byte_img = byte_img.getvalue()

    # Get predictions from Clarifai
    response = description_generator.get_response(byte_img)
    concepts = response.outputs

    concepts = concepts[-1].data.text.raw

    print(concepts)

    st.write(f"{concepts}")
