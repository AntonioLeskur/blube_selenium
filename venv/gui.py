import tkinter
from tkinter import messagebox
from item_window import ItemWindow
from download import Download
from upload import Upload
import threading


class Gui:
    def __init__(self):
        self.part_in = 0
        self.download = None
        self.upload = None

        window = tkinter.Tk()
        # window.eval('tk::PlaceWindow . center')
        ICON = tkinter.PhotoImage(file="venv\Blube---B.png")
        window.title("Item entry")
        window.config(pady=20, padx=20, bg="white")
        window.config(width=300, height=200)
        window.iconphoto(False, ICON)

        canvas = tkinter.Canvas(width=530, height=200, bg="white", highlightthickness=0)
        image = tkinter.PhotoImage(file="venv\Blube-logo.png")
        canvas.create_image(250, 100, image=image)
        canvas.grid(column=1, row=1, columnspan=2)

        self.note_label = tkinter.Label(text="", bg="white")
        self.note_label.config(font=('Arial', 15))
        self.note_label.grid(sticky="W", column=1, row=0)


        self.text_label = tkinter.Label(text="Enter item number:", bg="white")
        self.text_label.config(font=('Arial', 15))
        self.text_label.grid(sticky="E",column=1, row=2)

        self.item_entry = tkinter.Entry(width=33)
        self.item_entry.grid(sticky="W", column=2, row=2)

        self.start_button = tkinter.Button(text="START", command=self.t2_start)
        self.start_button.grid(sticky="W", column=3, row=2)

        self.t1_start(self.create_dow_upl_ob)

        print("DONE")
        window.mainloop()

    def t1_start(self, x):
        self.t1 = threading.Thread(target=x, daemon=True)
        self.t1.start()


    def t2_start(self):
        self.t2 = threading.Thread(target=self.transfer_item, daemon=True)
        self.t2.start()

    def create_dow_upl_ob(self):
        self.note_label.config(text="Status: Preparing Download module...")
        self.download = Download()
        self.note_label.config(text="Status: Preparing Upload module...")
        self.upload = Upload()
        self.note_label.config(text="Status: Ready for use")

        print("GOTOVO")

        
    def transfer_item(self):
        self.note_label.config(text="Status: Working...")
        item = self.item_entry.get()
        print(f"entered:{item}")
        self.download.start_download(item)
        self.upload.start_upload(self.download)
        self.note_label.config(text="Status: Done.")
        check_window = ItemWindow(self.download, self.upload)


