import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, bg="#f0f8ff", fg="#000080", font=("Arial", 10))

        self.initialize_ui()

    def initialize_ui(self):
        # Set background color for the main window
        self.root.configure(bg="#dbe7f0")

        # Title label
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"), bg="#dbe7f0", fg="#003366")
        title_label.pack(pady=10)

        # Button to select images
        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images, bg="#87cefa", fg="white", activebackground="#4682b4", activeforeground="white", relief="flat")
        select_images_button.pack(pady=(0, 10))

        # Listbox for selected images
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        # Label for PDF name entry
        label = tk.Label(self.root, text="Enter output PDF name:", bg="#dbe7f0", fg="#003366", font=("Arial", 12))
        label.pack()

        # Entry for output PDF name
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center", bg="#f0f8ff", fg="#000080", font=("Arial", 10))
        pdf_name_entry.pack()

        # Button to convert to PDF
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf, bg="#ffa07a", fg="white", activebackground="#cd5c5c", activeforeground="white", relief="flat")
        convert_button.pack(pady=(20, 40))

        # Add hover effects to buttons
        self.add_hover_effects(select_images_button, "#87cefa", "#4682b4")
        self.add_hover_effects(convert_button, "#ffa07a", "#cd5c5c")

    def add_hover_effects(self, widget, normal_color, hover_color):
        """Adds hover effect to a button widget."""
        def on_enter(event):
            widget["bg"] = hover_color

        def on_leave(event):
            widget["bg"] = normal_color

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)

        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_path)

    def convert_images_to_pdf(self):
        if not self.image_paths:
            return

        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            pdf.setFillColorRGB(1, 1, 1)  # Set the background to white
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(image_path, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()
