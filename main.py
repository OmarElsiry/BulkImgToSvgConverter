import os
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import svgwrite

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image to SVG Converter")
        self.geometry("600x400")

        self.input_dir = ""
        self.convert_folder = "ConvertedToSvg"
        self.reduce_folder = "ReducedSvg"
        self.reduction_scale = 1.0

        self.create_widgets()

    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Main Tab
        self.main_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.main_frame, text="Main")

        # Settings Tab
        self.settings_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")

        self.create_main_tab_widgets()
        self.create_settings_tab_widgets()

    def create_main_tab_widgets(self):
        # Input Folder Button
        self.input_button = ctk.CTkButton(self.main_frame, text="Select Input Folder", command=self.select_input_folder)
        self.input_button.pack(pady=10)

        # Process Options
        self.convert_checkbox = ctk.CTkCheckBox(self.main_frame, text="Convert Images to SVG")
        self.convert_checkbox.pack(pady=10)

        self.reduce_checkbox = ctk.CTkCheckBox(self.main_frame, text="Reduce SVG Size")
        self.reduce_checkbox.pack(pady=10)

        self.start_button = ctk.CTkButton(self.main_frame, text="Start", command=self.start_process)
        self.start_button.pack(pady=10)

        self.view_output_button = ctk.CTkButton(self.main_frame, text="View Output Folder", command=self.view_output_folder)
        self.view_output_button.pack(pady=10)

    def create_settings_tab_widgets(self):
        # Create frame for radio buttons and vertical line
        self.settings_container = ctk.CTkFrame(self.settings_frame)
        self.settings_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Vertical line
        self.canvas = ctk.CTkCanvas(self.settings_container, width=2, bg="black")
        self.canvas.pack(side="left", fill="y", padx=(0, 10))

        # Frame for settings options
        self.settings_options_frame = ctk.CTkFrame(self.settings_container)
        self.settings_options_frame.pack(side="left", fill="both", expand=True)

        # Conversion Options
        self.convert_option_label = ctk.CTkLabel(self.settings_options_frame, text="Conversion Options:")
        self.convert_option_label.pack(pady=5)
        
        self.convert_option = ctk.StringVar(value="keep_both")

        self.replace_option = ctk.CTkRadioButton(self.settings_options_frame, text="Replace Images with SVG", variable=self.convert_option, value="replace")
        self.replace_option.pack(pady=5)

        self.keep_both_option = ctk.CTkRadioButton(self.settings_options_frame, text="Keep Both Images and SVGs", variable=self.convert_option, value="keep_both")
        self.keep_both_option.pack(pady=5)

        self.convert_folder_option = ctk.CTkRadioButton(self.settings_options_frame, text="Save SVGs in 'ConvertedToSvg' Folder", variable=self.convert_option, value="convert_folder")
        self.convert_folder_option.pack(pady=5)

        # Size Reduction Options
        self.reduce_option_label = ctk.CTkLabel(self.settings_options_frame, text="Size Reduction Options:")
        self.reduce_option_label.pack(pady=5)

        self.reduce_option = ctk.StringVar(value="reduce_folder")

        self.reduce_folder_option = ctk.CTkRadioButton(self.settings_options_frame, text="Save Reduced SVGs in 'ReducedSvg' Folder", variable=self.reduce_option, value="reduce_folder")
        self.reduce_folder_option.pack(pady=5)

        self.keep_original_option = ctk.CTkRadioButton(self.settings_options_frame, text="Keep Original SVGs", variable=self.reduce_option, value="keep_original")
        self.keep_original_option.pack(pady=5)

        # Scale Entry
        self.scale_label = ctk.CTkLabel(self.settings_frame, text="SVG Reduction Scale:")
        self.scale_label.pack(pady=10)

        self.scale_entry = ctk.CTkEntry(self.settings_frame)
        self.scale_entry.pack(pady=10)

        self.save_settings_button = ctk.CTkButton(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_settings_button.pack(pady=10)

    def select_input_folder(self):
        self.input_dir = filedialog.askdirectory()
        if self.input_dir:
            messagebox.showinfo("Selected Folder", f"Input Folder: {self.input_dir}")

    def start_process(self):
        if not self.input_dir:
            messagebox.showerror("Error", "Please select an input folder.")
            return

        # Set output directory to the same as input directory
        self.output_dir = self.input_dir

        # Create folders if needed
        if self.convert_option.get() == "convert_folder":
            convert_folder_path = os.path.join(self.output_dir, self.convert_folder)
            os.makedirs(convert_folder_path, exist_ok=True)

        if self.reduce_option.get() == "reduce_folder":
            reduce_folder_path = os.path.join(self.output_dir, self.reduce_folder)
            os.makedirs(reduce_folder_path, exist_ok=True)

        if self.convert_checkbox.get():
            self.convert_images()
        
        if self.reduce_checkbox.get():
            self.reduce_svgs()

        messagebox.showinfo("Process Complete", "The selected processes have been completed.")

    def convert_images(self):
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                img_path = os.path.join(self.input_dir, filename)
                if self.convert_option.get() == "convert_folder":
                    output_path = os.path.join(self.output_dir, self.convert_folder)
                else:
                    output_path = self.output_dir
                convert_to_svg(img_path, output_path)

                if self.convert_option.get() == "replace":
                    os.remove(img_path)

    def reduce_svgs(self):
        for filename in os.listdir(self.output_dir):
            if filename.lower().endswith('.svg'):
                svg_path = os.path.join(self.output_dir, filename)
                if self.reduce_option.get() == "reduce_folder":
                    output_path = os.path.join(self.output_dir, self.reduce_folder)
                else:
                    output_path = self.output_dir
                reduce_svg_size(svg_path, output_path)

    def view_output_folder(self):
        if self.output_dir:
            os.startfile(self.output_dir)

    def save_settings(self):
        try:
            self.reduction_scale = float(self.scale_entry.get())
            messagebox.showinfo("Settings", "Settings saved successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid scale value. Please enter a number.")

def convert_to_svg(img_path, output_path):
    img = Image.open(img_path)
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    svg_path = os.path.join(output_path, img_name + '.svg')
    
    width, height = img.size
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(width, height))
    dwg.add(dwg.image(href=img_path, insert=(0, 0), size=(width, height)))
    dwg.save()

def reduce_svg_size(svg_path, output_path):
    # This is a placeholder function. SVG size reduction would typically involve optimization steps
    # like removing unnecessary elements or attributes, which would require a more sophisticated approach.
    svg_name = os.path.splitext(os.path.basename(svg_path))[0]
    output_file = os.path.join(output_path, svg_name + '_reduced.svg')
    
    # Simply copy the SVG file for now
    with open(svg_path, 'r') as original_svg:
        svg_content = original_svg.read()
    
    with open(output_file, 'w') as reduced_svg:
        reduced_svg.write(svg_content)

if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
