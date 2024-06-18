
from tkinter import *
from tkinter import messagebox, filedialog
import os
from PyPDF4 import PdfFileReader
import pyttsx3

class PDFToAudioConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF to Audio Converter")
        self.master.geometry("500x300")
        self.master.configure(bg="lightblue")

        self.pdf_path = StringVar()
        self.start_page = IntVar()
        self.end_page = IntVar()

        Label(self.master, text="PDF to Audio Converter", fg="black", font=("Courier", 15), bg="lightblue").pack(pady=10)

        Label(self.master, text="PDF File Path:", bg="lightblue").pack()
        self.pdf_path_entry = Entry(self.master, textvariable=self.pdf_path, width=50)
        self.pdf_path_entry.pack()

        Label(self.master, text="Start Page:", bg="lightblue").pack()
        self.start_page_entry = Entry(self.master, textvariable=self.start_page)
        self.start_page_entry.pack()

        Label(self.master, text="End Page:", bg="lightblue").pack()
        self.end_page_entry = Entry(self.master, textvariable=self.end_page)
        self.end_page_entry.pack()

        Button(self.master, text="Browse", command=self.browse_pdf, bg="ivory3").pack(pady=10)
        Button(self.master, text="Convert", command=self.read_pdf, bg="ivory3").pack()

    def browse_pdf(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filename:
            self.pdf_path.set(filename)

    def read_pdf(self):
        pdf_file = self.pdf_path.get()
        if not os.path.exists(pdf_file):
            messagebox.showerror("Error", "PDF file not found.")
            return

        start_page = self.start_page.get()
        end_page = self.end_page.get()

        if end_page < start_page or end_page < 0:
            messagebox.showerror("Error", "Invalid page range.")
            return

        speaker = pyttsx3.init()
        pdf_reader = PdfFileReader(open(pdf_file, "rb"))

        if end_page >= pdf_reader.numPages:
            messagebox.showerror("Error", "Invalid page range.")
            return

        for page_num in range(start_page, end_page + 1):
            page = pdf_reader.getPage(page_num)
            try:
                text = page.extractText()
                speaker.say(text)
                speaker.runAndWait()
            except KeyError:
                # Skip pages that do not contain text content
                pass

def main():
    root = Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

