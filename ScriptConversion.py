import deepl
import tkinter as tk
from tkinter import filedialog, messagebox
from time import sleep

class FAVORITE_Unpacker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Input file:")
        self.input_label.pack(side="top")
        self.input_textbox = tk.Text(self, height=1)
        self.input_textbox.pack(side="top")
        self.input_button = tk.Button(self, text="Browse", command=self.browse_input_file)
        self.input_button.pack(side="top")
        self.output_label = tk.Label(self, text="Output file:")
        self.output_label.pack(side="top")
        self.output_textbox = tk.Text(self, height=1)
        self.output_textbox.pack(side="top")
        self.output_button = tk.Button(self, text="Browse", command=self.browse_output_file)
        self.output_button.pack(side="top")
        self.translate_button = tk.Button(self, text="Translate", command=self.translate)
        self.translate_button.pack(side="left")
        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit_button.pack(side="left")
        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack(side="bottom")
        self.textbox = tk.Text(self.master)
        self.textbox.pack(side="bottom")

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.input_file_path = file_path
            self.input_textbox.delete('1.0', tk.END)
            self.input_textbox.insert(tk.END, self.input_file_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")], defaultextension=".txt")
        if file_path:
            self.output_file_path = file_path
            self.output_textbox.delete('1.0', tk.END)
            self.output_textbox.insert(tk.END, self.output_file_path)
    def translate(self):
        try:
            input_file_path = self.input_textbox.get('1.0', tk.END).strip()
            output_file_path = self.output_textbox.get('1.0', tk.END).strip()
            with open(input_file_path, mode='r', encoding='UTF-8') as input_file, open(output_file_path, mode='w', encoding='UTF-8') as output_file:
                lines = input_file.readlines()
                num_lines = len(lines)
                self.progress_label.config(text="Translating...")
                for i, line in enumerate(lines):
                    self.textbox.insert(tk.END, f"Line {i+1}: Original text: {line.strip()}")
                    try:
                        translated = deepl.translate(source_language="JA", target_language="EN", text=line)
                        self.textbox.insert(tk.END, f" - Translated text: {translated.strip()}\n")
                        output_file.write(translated.strip() + "\n")
                    except Exception as e:
                        self.textbox.insert(tk.END, f" - Error: {str(e)}\n")
                        sleep(5)
                    self.progress_label.config(text=f"Translated {i+1}/{num_lines} lines")
                    self.progress_label.update()
                messagebox.showinfo("Translation Complete", "Translation completed successfully.")
                self.progress_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()
app = FAVORITE_Unpacker(master=root)
app.mainloop()
