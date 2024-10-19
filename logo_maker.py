import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random

def create_graphical_logo(text, bg_color, text_color, font_style):
    # Create an image with a gradient background
    width, height = 800, 400
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Create a simple gradient effect on the background
    for i in range(height):
        gradient_color = (
            int(bg_color[1:3], 16) - i % 100,
            int(bg_color[3:5], 16) - i % 100,
            int(bg_color[5:7], 16) - i % 100
        )
        draw.line([(0, i), (width, i)], fill=gradient_color)

    # Draw random graphical elements like circles, lines, and rectangles
    for _ in range(10):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        shape_type = random.choice(['circle', 'rectangle', 'line'])

        if shape_type == 'circle':
            # Workaround for the width issue with ellipse
            for i in range(2):  # Adjust the range for the desired thickness
                draw.ellipse([(x1 - i, y1 - i), (x2 + i, y2 + i)], outline=text_color)
        elif shape_type == 'rectangle':
            draw.rectangle([(x1, y1), (x2, y2)], outline=text_color, width=2)
        elif shape_type == 'line':
            draw.line([(x1, y1), (x2, y2)], fill=text_color, width=2)

    # Load a font and handle text drawing
    font_path = f"./fonts/{font_style}.ttf"
    try:
        font = ImageFont.truetype(font_path, 100)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and center the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # Draw the logo text
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return image

# Streamlit app interface
st.title("Graphical Logo Maker App")

# User input for logo details
st.subheader("Enter your logo details:")
logo_text = st.text_input("Enter the text for the logo:", "Your Logo")
bg_color = st.color_picker("Choose a background color:", "#FF6347")  # Default is coral red
text_color = st.color_picker("Choose a text color:", "#FFFFFF")
font_style = st.selectbox("Select a font style:", ["Arial", "Times New Roman", "Courier", "Verdana"])

# Button to create a logo
if st.button("Generate Graphical Logo"):
    logo_image = create_graphical_logo(logo_text, bg_color, text_color, font_style)
    st.image(logo_image, caption="Generated Graphical Logo")

    # Asking user feedback on the logo
    st.write("Do you like this logo?")
    like_logo = st.radio("", ("Yes", "No"))

    if like_logo == "Yes":
        # Allow user to download the logo
        logo_image_path = f"{logo_text.replace(' ', '_')}_graphical_logo.png"
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
