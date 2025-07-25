import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import os

# --- Konfigurasi Aplikasi ---
OUTPUT_RESOLUTION = (4000, 4000)
DEFAULT_TILE_SIZE = 50 # Ukuran default satu "blok" pola dalam piksel

class PatternGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Generator Pola Seamless")
        self.root.geometry("800x700") # Ukuran jendela aplikasi

        self.primary_color = "#FF0000" # Merah default
        self.secondary_color = "#0000FF" # Biru default
        self.current_pattern_type = tk.StringVar(value="Kotak-Kotak")
        self.tile_size = tk.IntVar(value=DEFAULT_TILE_SIZE)

        self.image = None # Untuk menyimpan objek gambar PIL
        self.photo_image = None # Untuk menampilkan gambar di Tkinter

        self.create_widgets()

    def create_widgets(self):
        # --- Frame Kontrol ---
        control_frame = ttk.LabelFrame(self.root, text="Pengaturan Pola", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Pemilihan Pola
        ttk.Label(control_frame, text="Jenis Pola:").grid(row=0, column=0, sticky=tk.W, pady=5)
        pattern_options = ["Kotak-Kotak", "Garis Diagonal", "Lingkaran Dot", "Labirin (WIP)", "Batik (WIP)"]
        pattern_menu = ttk.OptionMenu(control_frame, self.current_pattern_type, self.current_pattern_type.get(), *pattern_options, command=self.on_pattern_change)
        pattern_menu.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # Pemilihan Warna
        ttk.Label(control_frame, text="Warna Primer:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.primary_color_btn = ttk.Button(control_frame, text="Pilih Warna", command=self.choose_primary_color)
        self.primary_color_btn.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.primary_color_display = tk.Canvas(control_frame, width=20, height=20, bg=self.primary_color, relief=tk.RIDGE, bd=1)
        self.primary_color_display.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(control_frame, text="Warna Sekunder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.secondary_color_btn = ttk.Button(control_frame, text="Pilih Warna", command=self.choose_secondary_color)
        self.secondary_color_btn.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self.secondary_color_display = tk.Canvas(control_frame, width=20, height=20, bg=self.secondary_color, relief=tk.RIDGE, bd=1)
        self.secondary_color_display.grid(row=2, column=2, padx=5, pady=5)

        # Ukuran Pola
        ttk.Label(control_frame, text="Ukuran Pola (px):").grid(row=3, column=0, sticky=tk.W, pady=5)
        tile_size_slider = ttk.Scale(control_frame, from_=10, to=200, orient=tk.HORIZONTAL, variable=self.tile_size, command=self.update_tile_size_label)
        tile_size_slider.grid(row=3, column=1, sticky=tk.EW, pady=5)
        self.tile_size_label = ttk.Label(control_frame, text=str(self.tile_size.get()))
        self.tile_size_label.grid(row=3, column=2, padx=5, pady=5)

        # Tombol Aksi
        generate_btn = ttk.Button(control_frame, text="Generate Pola", command=self.generate_pattern)
        generate_btn.grid(row=4, column=0, columnspan=3, pady=10, sticky=tk.EW)

        save_btn = ttk.Button(control_frame, text="Simpan Gambar (JPG)", command=self.save_image)
        save_btn.grid(row=5, column=0, columnspan=3, pady=5, sticky=tk.EW)

        # --- Frame Pratinjau Gambar ---
        preview_frame = ttk.LabelFrame(self.root, text="Pratinjau Gambar", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(preview_frame, bg="white", width=500, height=500, relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def choose_primary_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Primer")
        if color_code[1]: # color_code[1] adalah hex string
            self.primary_color = color_code[1]
            self.primary_color_display.config(bg=self.primary_color)

    def choose_secondary_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Sekunder")
        if color_code[1]:
            self.secondary_color = color_code[1]
            self.secondary_color_display.config(bg=self.secondary_color)

    def update_tile_size_label(self, event=None):
        self.tile_size_label.config(text=str(int(self.tile_size.get())))

    def on_pattern_change(self, *args):
        # Ini bisa digunakan untuk mengaktifkan/menonaktifkan opsi tertentu
        # tergantung pada pola yang dipilih (misal, labirin mungkin butuh seed)
        pass

    def generate_pattern(self):
        width, height = OUTPUT_RESOLUTION
        tile_s = self.tile_size.get()

        self.image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(self.image)

        pattern_type = self.current_pattern_type.get()

        if pattern_type == "Kotak-Kotak":
            self.draw_checkerboard(draw, width, height, tile_s)
        elif pattern_type == "Garis Diagonal":
            self.draw_diagonal_lines(draw, width, height, tile_s)
        elif pattern_type == "Lingkaran Dot":
            self.draw_dot_circles(draw, width, height, tile_s)
        elif pattern_type == "Labirin (WIP)":
            # Placeholder untuk logika labirin yang kompleks
            draw.text((width/2 - 50, height/2), "Labirin Belum Diimplementasi", fill="black")
        elif pattern_type == "Batik (WIP)":
            # Placeholder untuk logika batik yang kompleks
            draw.text((width/2 - 50, height/2), "Batik Belum Diimplementasi", fill="black")

        self.display_image()
        print(f"Pola {pattern_type} dihasilkan dengan ukuran {tile_s}x{tile_s} px.")

    def draw_checkerboard(self, draw, width, height, tile_s):
        """Menggambar pola kotak-kotak."""
        for y in range(0, height, tile_s):
            for x in range(0, width, tile_s):
                # Pola seamless checkerboard
                if ((x // tile_s) % 2 == 0 and (y // tile_s) % 2 == 0) or \
                   ((x // tile_s) % 2 != 0 and (y // tile_s) % 2 != 0):
                    draw.rectangle([x, y, x + tile_s, y + tile_s], fill=self.primary_color)
                else:
                    draw.rectangle([x, y, x + tile_s, y + tile_s], fill=self.secondary_color)

    def draw_diagonal_lines(self, draw, width, height, tile_s):
        """Menggambar pola garis diagonal seamless."""
        line_width = max(1, tile_s // 10) # Lebar garis menyesuaikan ukuran tile

        # Isi dengan warna primer
        draw.rectangle([0, 0, width, height], fill=self.primary_color)

        for y in range(-tile_s, height + tile_s, tile_s): # Mulai dari negatif untuk seamless
            for x in range(-tile_s, width + tile_s, tile_s):
                # Gambar garis diagonal dari kiri bawah ke kanan atas
                draw.line([(x, y + tile_s), (x + tile_s, y)], fill=self.secondary_color, width=line_width)

    def draw_dot_circles(self, draw, width, height, tile_s):
        """Menggambar pola lingkaran dot."""
        radius = tile_s // 3
        
        # Isi dengan warna primer
        draw.rectangle([0, 0, width, height], fill=self.primary_color)

        for y in range(tile_s // 2, height, tile_s):
            for x in range(tile_s // 2, width, tile_s):
                # Gambar lingkaran di tengah setiap "tile"
                draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.secondary_color)


    def display_image(self):
        """Menampilkan gambar di canvas pratinjau."""
        if self.image:
            # Resize gambar untuk pratinjau agar tidak terlalu besar
            preview_width = self.canvas.winfo_width()
            preview_height = self.canvas.winfo_height()
            
            # Pastikan preview_width dan preview_height tidak 0
            if preview_width == 0: preview_width = 500
            if preview_height == 0: preview_height = 500

            # Hitung rasio untuk menjaga aspek rasio
            img_width, img_height = self.image.size
            ratio = min(preview_width / img_width, preview_height / img_height)
            
            display_img = self.image.resize((int(img_width * ratio), int(img_height * ratio)), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(display_img)
            
            self.canvas.delete("all")
            self.canvas.create_image(preview_width / 2, preview_height / 2, anchor=tk.CENTER, image=self.photo_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))


    def save_image(self):
        """Menyimpan gambar yang dihasilkan."""
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPG files", "*.jpg"), ("All files", "*.*")],
                initialfile="pola_seamless.jpg"
            )
            if file_path:
                try:
                    self.image.save(file_path, quality=95) # quality=95 untuk kualitas tinggi
                    tk.messagebox.showinfo("Sukses", f"Gambar berhasil disimpan ke:\n{file_path}")
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")
        else:
            tk.messagebox.showwarning("Peringatan", "Belum ada gambar yang dihasilkan untuk disimpan.")

# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PatternGeneratorApp(root)
    root.mainloop()