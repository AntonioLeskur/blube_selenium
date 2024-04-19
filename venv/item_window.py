import tkinter
from download import Download
from upload import Upload
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen


class ItemWindow:
        def __init__(self, download_driver, upload_driver):

                self.item_window = tkinter.Toplevel()
                ICON = tkinter.PhotoImage(file="venv\Blube---B.png")
                self.item_window.title("Item entry")
                self.item_window.config(pady=20, padx=20, bg="white")
                self.item_window.config(width=300, height=200)
                self.item_window.iconphoto(False, ICON)

                response = requests.get(download_driver.image_source)
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                resized_image = img.resize((200, 200), Image.LANCZOS)
                self.new_image = ImageTk.PhotoImage(master=self.item_window, image=resized_image)

                label_photo = tkinter.Label(master=self.item_window, image=self.new_image)
                label_photo.grid(column=0, row=0)
                label_photo.image = self.new_image

                self.product_name = tkinter.Label(master=self.item_window,\
                                                  text=f"NAME: {download_driver.product_name_promo}", bg="white")
                self.product_name.config(font=('Arial', 15))
                self.product_name.grid(sticky="W", column=0, row=1)

                self.weight = tkinter.Label(master=self.item_window, text=f"WEIGHT: {download_driver.weight}",\
                                            bg="white")
                self.weight.config(font=('Arial', 15))
                self.weight.grid(sticky="W", column=0, row=2)

                self.dimensions = tkinter.Label(master=self.item_window,\
                                                text=f"DIMENSIONS: {download_driver.dimensions}", bg="white")
                self.dimensions.config(font=('Arial', 15))
                self.dimensions.grid(sticky="W", column=0, row=3)

                self.box_dimensions = tkinter.Label(master=self.item_window, \
                                                    text=f"BOX DIMENSIONS: {download_driver.box_dimensions}",
                                                    bg="white")
                self.box_dimensions.config(font=('Arial', 15))
                self.box_dimensions.grid(sticky="W", column=0, row=4)

                self.packaging = tkinter.Label(master=self.item_window, \
                                               text=f"PACKAGING: {download_driver.packaging}", bg="white")
                self.packaging.config(font=('Arial', 15))
                self.packaging.grid(sticky="W", column=0, row=5)

                self.min_packaging = tkinter.Label(master=self.item_window, \
                                                   text=f"MIN PACKAGING: {download_driver.min_packaging}", bg="white")
                self.min_packaging.config(font=('Arial', 15))
                self.min_packaging.grid(sticky="W", column=0, row=6)

                self.short_description = tkinter.Label(master=self.item_window, \
                                                       text=f"SHORT DESCRIPTION: {download_driver.short_description}",
                                                       bg="white")
                self.short_description.config(font=('Arial', 15))
                self.short_description.grid(sticky="W", column=0, row=7)

                self.long_description = tkinter.Label(master=self.item_window, \
                                                      text=f"LONG DESCRIPTION: {download_driver.long_description}",
                                                      bg="white")
                self.long_description.config(font=('Arial', 15))
                self.long_description.grid(sticky="W", column=0, row=8)

                def save_and_quit():
                        import time
                        upload_driver.save_and_close()
                        time.sleep(3)
                        self.item_window.destroy()

                        
                self.submit_button = tkinter.Button(master=self.item_window, text="Submit", height=3, width=10,
                                                    bg="#bbdefc", bd=1, command=save_and_quit)
                self.submit_button.grid(sticky="W", column=0, row=9)

                self.cancel_button = tkinter.Button(master=self.item_window, text="Cancel", height=3, width=10, bd=1,
                                                    command=self.quit)
                self.cancel_button.grid(sticky="E", column=0, row=9)

        def quit(self):
                self.item_window.destroy()
