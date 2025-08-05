import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - by Saai Murugan")

        self.pdf_files = []

        # Folder selection
        self.select_folder_btn = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack(pady=10)

        # Listbox for files
        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack()

        # Move buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.up_btn = tk.Button(btn_frame, text="Move Up", command=self.move_up)
        self.up_btn.grid(row=0, column=0, padx=5)

        self.down_btn = tk.Button(btn_frame, text="Move Down", command=self.move_down)
        self.down_btn.grid(row=0, column=1, padx=5)

        # Merge button
        self.merge_btn = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_btn.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.pdf_files = sorted(
                [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
            )
            self.folder_path = folder_path
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.listbox.insert(tk.END, file)

    def move_up(self):
        idx = self.listbox.curselection()
        if not idx or idx[0] == 0:
            return
        i = idx[0]
        self.pdf_files[i - 1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i - 1]
        self.update_listbox()
        self.listbox.select_set(i - 1)

    def move_down(self):
        idx = self.listbox.curselection()
        if not idx or idx[0] == len(self.pdf_files) - 1:
            return
        i = idx[0]
        self.pdf_files[i + 1], self.pdf_files[i] = self.pdf_files[i], self.pdf_files[i + 1]
        self.update_listbox()
        self.listbox.select_set(i + 1)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "No PDF files selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        try:
            for file in self.pdf_files:
                merger.append(os.path.join(self.folder_path, file))
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Success", f"PDFs merged into:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()