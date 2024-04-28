from PIL import Image
import streamlit as st
import os

def ascii(image, img_type, file_name, scale):  

    scale = int(scale)

    # Open the image
    img = Image.open(image)

    # Convert image to RGB mode if it's not PNG
    if img_type != 'png':
        img = img.convert("RGB")

    w, h = img.size

    img.resize((w//scale, h//scale)).save("resized.%s" % img_type)

    img = Image.open("resized.%s" % img_type)
    w, h = img.size

    grid = []
    for i in range(h):
        grid.append(["X"] * w)

    pix = img.load()

    for y in range(h):
        for x in range(w):
            if sum(pix[x, y]) == 0:
                grid[y][x] = "#"
            elif sum(pix[x,y]) in range(1, 100):
                grid[y][x] = "X"
            elif sum(pix[x,y]) in range(100, 200):
                grid[y][x] = "%"
            elif sum(pix[x,y]) in range(200, 300):
                grid[y][x] = "&"
            elif sum(pix[x,y]) in range(300, 400):
                grid[y][x] = "+"
            elif sum(pix[x,y]) in range(400, 500):
                grid[y][x] = "*"
            elif sum(pix[x,y]) in range(500, 600):
                grid[y][x] = "/"
            else:
                grid[y][x] = " "
    
    with open(file_name, "w") as art:
        for row in grid:
            art.write("".join(row)+"\n")

    # Download button
    if os.path.exists(file_name):
        abs_path = os.path.abspath(file_name)
        with open(abs_path, "rb") as file:
            st.download_button(label="Download", data=file, file_name=file_name)

st.title("Convert your image to ASCII_ART")

userimg = st.file_uploader("Upload your image")

filename = st.text_input("Save file as:", "ASCII_ART.txt")

if userimg:
    convert = st.button("Convert")
    if convert:
        if userimg.name.endswith((".png", ".jpg", ".jpeg", ".jfif")):
            img_type = userimg.name.split(".")[-1]
            ascii(userimg, img_type, filename, "3")
        else:
            st.error("File type is not supported")
