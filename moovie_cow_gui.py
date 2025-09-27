from moovie_cow import open_movie
import tkinter as tk
from PIL import Image, ImageTk
import os


MATERIALS_PATH = os.path.join(os.path.dirname(__file__), "materials")

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MOO-vie Cow")
        self.geometry("600x415")
        
        # Set canvas
        canvas = tk.Canvas(self, width= 600, height= 4150, bd= 0, highlightthickness= 0)
        canvas.pack(fill= 'both', expand= True)
        
        # Set background
        background_path = os.path.join(MATERIALS_PATH, "cows.webp")
        background_pil = Image.open(background_path)
        self.bg_img = ImageTk.PhotoImage(background_pil)
        canvas.create_image(0, 0, image= self.bg_img, anchor= "nw")
        
        # Set title
        title_path = os.path.join(MATERIALS_PATH, "MOOVIE-COW-9-27-2025.png")
        title_pil = Image.open(title_path)
        title_pil = title_pil.resize((550, 200), Image.Resampling.LANCZOS)
        self.title_img = ImageTk.PhotoImage(title_pil)
        canvas.create_image(30, -10, image= self.title_img, anchor= "nw")
        
        # Set prompt
        prompt_path = os.path.join(MATERIALS_PATH, "Watcha-in-the-mood-for-9-27-2025.png")
        prompt_pil = Image.open(prompt_path)
        prompt_pil = prompt_pil.resize((475, 115), Image.Resampling.LANCZOS)
        self.prompt_img = ImageTk.PhotoImage(prompt_pil)
        canvas.create_image(70, 150, image= self.prompt_img, anchor= "nw")

        # User entry  
        entry = tk.Entry(self, font= ("Ubuntu", 15), width= 25, fg= "hot pink", bd= 3)
        canvas.create_window(160, 240, anchor= "nw", window= entry)

        # Go Button #
        btn_path = os.path.join(MATERIALS_PATH, "go-9-27-2025.png")
        btn_pil = Image.open(btn_path)
        btn_pil = btn_pil.resize((180, 160), Image.Resampling.LANCZOS)
        self.btn_img = ImageTk.PhotoImage(btn_pil)
        btn_click = canvas.create_image(215, 265, image= self.btn_img, anchor= "nw")
        
        # Button functionality: starts script
        def on_click(event):
            movie_title = entry.get()
            open_movie(movie_title)
            self.destroy()
            
        # Embed click functionality in 'go' button image
        canvas.tag_bind(btn_click, "<Button-1>", on_click)        


if __name__ == "__main__":
    main()