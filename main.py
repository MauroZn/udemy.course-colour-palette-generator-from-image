import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

img_array = []

def imageUploader():
    global img_array
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)

    if len(path):
        starting_img = Image.open(path)
        max_width = 1280
        max_height = 720
        width, height = starting_img.size
        if width >= max_width or height >= max_height:
            scale_w = 1280 / width
            scale_h = 720 / height
            scale = min(scale_w, scale_h)

            new_width = int(width * scale)
            new_height = int(height * scale)

            starting_img = starting_img.resize((new_width, new_height))
            window.geometry(f"{new_width + 160}x{new_height + 300}")
        else:
            window.geometry(f"{width + 160}x{height + 300}")

        img = starting_img.convert('RGB')
        pic = ImageTk.PhotoImage(img)
        label.config(image=pic)
        label.image = pic
        img_array = np.array(img)

    else:
        print("No file is chosen, please choose a file.")

def get_image_colors():
    all_colors = ""
    #Transform the 3D Array into a 2D. Row:Pixel, Column: RGB
    pixels = img_array.reshape(-1, img_array.shape[-1])

    #Get Unique Colors and count how many times they are used in the image
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

    #Create a list.
    #Zip is used to combine multiple sequences element by element (In this case the tuple and counts)
    #Tuple is used to convert the color array, "Example:(255,255,255)", into a Python Tuple that is better for data management
    #So with this I create a list of RGB colors paired with counts to see how many of the same there are in the pic
    color_counts = list(zip([tuple(color) for color in unique_colors], counts))

    # Now I sort by count so after this I can get the 10 most used ones
    color_counts.sort(key=lambda x: x[1], reverse=True)

    for i, (color, count) in enumerate(color_counts[:10]):
        #I cycle in the list to get the separated rgb values, so I can convert them to hex
        r = color[0]
        g = color[1]
        b = color[2]
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        all_colors += str(i+1) + str(hex_color) + ":" + str(count) + "\n"
        # print(f"{i+1}. Color {hex_color} appears {count} times")

    colors_list_box.insert(tk.END, all_colors)

if __name__ == "__main__":

    window = tk.Tk()

    window.title("Image Colour Palette Generator")
    window.minsize(560, 270)

    label = tk.Label(window)
    label.pack(pady=10, fill='x', expand=True)

    upload_button = tk.Button(window, text="Upload Image", command=imageUploader)
    upload_button.pack(padx=5, pady=5)

    get_image_colors = tk.Button(window, text="Get Most Used Colors In Image", command=get_image_colors)
    get_image_colors.pack(padx=5, pady=5)

    colors_list_box = tk.Text(window, height=15, width=20)
    colors_list_box.pack(pady=20, padx=5)

    window.mainloop()

