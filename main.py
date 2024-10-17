import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import cv2
import easyocr
import matplotlib.pyplot as plt
import os

#easyOCR functionality:
reader = easyocr.Reader(['en', 'fr', 'de', 'it'])
def easyOCR_text_reader(file):
    """
    Extracts text from a jpg image file using the EasyOCR library.

    This function accepts an image file (in jpg, jpeg, or png format), uses EasyOCR to read the text within the image, 
    and returns the extracted text as a string. If the file format is not supported, it returns a warning message.

    Args:
            `file` (str): The path to the image file you want to process. Must be in jpg, jpeg, or png format.

    Returns:
            str: A string containing the extracted text from the image, or a warning message if the file type is invalid.

    Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file is not in a supported format (jpg, jpeg, or png).
    """
    _, file_extension = os.path.splitext(file)
    #Check image is jpg/png if not, return error msg: 
    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        img = cv2.imread(file)
        # run OCR:
        results = reader.readtext(img,detail=0)
        ocr_results = " ".join(results)
        print(ocr_results)
        return ocr_results
    else:
        return "WARNING: File type not valid. \n\n Please convert file to jpg, jpeg, or png."

def select_files():
    """
    Opens a file dialog to select a file, processes the file, and updates the UI with its contents.

    Allows the user to select a file via a file dialog window. Then checks if the file exists, 
    clears the current UI content, performs OCR (using easyOCR) on the selected file, and displays the results 
    in the UI. The function also loads and displays the image using Pillow, updating various UI components 
    with the new content and providing an option to save the processed data.

    Args: None: This function does not take any direct arguments but interacts with the application's UI.

    Returns: None: The function does not return any value but updates the application's UI with the selected 
        file's information, including file existence, image display, and OCR results.
    """
    app.update() # Force UI to refresh and handle events
    app.select_files_button.focus_set() #focus on the select_button
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
        # Example of using os module to perform an action with the file
        print(f"File exists: {os.path.exists(file_path)}")
        
        #clear old content from both frames
        for widget in app.frame_1.winfo_children():
            widget.destroy()
        app.doc_results_textbox.delete(1.0, "end")
        if hasattr(app, 'save_button') and app.save_button.winfo_exists():
            app.save_button.destroy()
    
        # Print file info and check if it exists, and get results from easyOCR
        doc_info = f"Selected file: {file_path}\n"
        doc_info += f"File exists: {os.path.exists(file_path)}\n"
        results = easyOCR_text_reader(file_path)
        app.doc_results_textbox.insert("end", f"File Information:\n\n {doc_info}\n Scanned Text:\n\n {results}")
    

        # Load and display the image using Pillow
        image = Image.open(file_path)
        image = image.resize((400, 300))  # Resize image to fit the frame
        photo = ImageTk.PhotoImage(image)  # Convert to Tkinter-compatible image

        # Display the image in a label inside frame_1
        image_label = ctk.CTkLabel(app.frame_1, image=photo, text="")
        image_label.image = photo 
        image_label.grid(row=0, column=0, sticky="nsew")

        # Insert OCR results into the textbox
        app.save_button = ctk.CTkButton(app.frame_2, text="Save", fg_color="#ff9900", text_color="black")
        app.save_button.grid(row= 1, column = 0, padx =10, pady=10,sticky='se')

class Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lucas")
        self.geometry("800x600")

        #Main window/Frame layout
        self.grid_rowconfigure(1, weight=1) # Allows row 1 (frames) to expand
        self.grid_columnconfigure(0, weight=1) # Allows column 0 to expand
        self.grid_columnconfigure(1, weight=1) # Allows column 1 to expand
    
        #Header Button Frame:
        self.button_frame_1= Frame(self)
        self.button_frame_1.configure(fg_color="#404040")	 
        self.button_frame_1.grid(row=0, column=0, columnspan= 2, pady=0, sticky='new')
        self.button_frame_1.grid_columnconfigure(0, weight=1)

        #Inner Header Button Frame:
        self.inner_button_frame= Frame(self.button_frame_1)
        self.inner_button_frame.configure(fg_color="#404040")	
        self.inner_button_frame.grid(row=0, column=0, columnspan= 1, sticky='w')
        self.inner_button_frame.grid_columnconfigure(0, weight=1)

        # select files button:
        self.select_files_button = ctk.CTkButton(self.inner_button_frame, text="Select From Files", command=select_files, fg_color='#33cccc', text_color="black")
        self.select_files_button.grid(row= 0, column = 0,columnspan=1,padx= 10, pady=5,sticky='w')

        #Column Frame 1 (left):
        self.frame_1 = Frame(self)
        self.frame_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.frame_1.grid_rowconfigure(0, weight=1) # Makes content inside frame expandable
        self.frame_1.grid_columnconfigure(0, weight=1)

        #Column Frame 2 (right):
        self.frame_2 = Frame(self)
        self.frame_2.configure(fg_color="black")  
        self.frame_2.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="nsew")
        self.frame_2.grid_rowconfigure(0, weight=1)
        self.frame_2.grid_columnconfigure(0, weight=1)

        #Column Frame 2 TextBox:
        self.doc_results_textbox = ctk.CTkTextbox(self.frame_2)
        self.doc_results_textbox.configure(fg_color="black") 
        self.doc_results_textbox.grid(row=0, column=0, sticky="nsew")

app = App()
app.mainloop()