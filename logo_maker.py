import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(text, bg_color, text_color, font_style):
    # Create a blank image with the background color
    image = Image.new('RGB', (800, 400), bg_color)
    draw = ImageDraw.Draw(image)

    # Load a font
    font_path = f"./fonts/{font_style}.ttf"  # Ensure you have fonts in a 'fonts' folder
    try:
        font = ImageFont.truetype(font_path, 150)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position using textbbox()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) / 2
    text_y = (image.height - text_height) / 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return image

# Streamlit app interface
st.title("Logo Maker App")

# User input for logo details
st.subheader("Enter your logo details:")
logo_text = st.text_input("Enter the text for the logo:", "Your Logo")
bg_color = st.color_picker("Choose a background color:", "#FF6347")  # Default is coral red
text_color = st.color_picker("Choose a text color:", "#FFFFFF")
font_style = st.selectbox("Select a font style:", ["Arial", "Times New Roman", "Courier", "Verdana"])

# Button to create a logo
if st.button("Generate Logo"):
    logo_image = create_logo(logo_text, bg_color, text_color, font_style)
    st.image(logo_image, caption="Generated Logo")

    # Asking user feedback on the logo
    st.write("Do you like this logo?")
    like_logo = st.radio("", ("Yes", "No"))

    if like_logo == "Yes":
        # Allow user to download the logo
        logo_image_path = f"{logo_text.replace(' ', '_')}_logo.png"
        logo_image.save(logo_image_path)
        with open(logo_image_path, "rb") as file:
            btn = st.download_button(
                label="Download Logo",
                data=file,
                file_name=logo_image_path,
                mime="image/png"
            )
    else:
        st.write("Let's create another one!")
