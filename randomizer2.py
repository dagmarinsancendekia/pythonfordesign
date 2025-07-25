import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import random
import numpy as np
import os
from datetime import datetime # Import modul datetime

class ImagePatternGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Generator Pola Gambar")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        self.original_image = None
        self.original_pixels = None
        self.current_display_image = None
        self.image_width = 0
        self.image_height = 0

        self.pattern_type = tk.StringVar(value="Acak Murni")
        self.tile_size = tk.IntVar(value=20)

        self.create_widgets()

    def create_widgets(self):
        # --- Frame Kontrol ---
        control_frame = ttk.LabelFrame(self.root, text="Kontrol", padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Button(control_frame, text="Muat Gambar", command=self.load_image).pack(side=tk.LEFT, padx=5, pady=5)

        # Pemilihan Pola
        ttk.Label(control_frame, text="Jenis Pola:").pack(side=tk.LEFT, padx=(10,0), pady=5)
        pattern_options = ["Acak Murni", "Baris Warna (Terurut)", "Kolom Warna (Terurut)", "Mozaik Kotak"]
        self.pattern_menu = ttk.OptionMenu(control_frame, self.pattern_type, self.pattern_type.get(), *pattern_options, command=self.on_pattern_change)
        self.pattern_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # Slider untuk ukuran tile mozaik
        self.tile_size_label = ttk.Label(control_frame, text=f"Ukuran Kotak Mozaik ({self.tile_size.get()}px):")
        self.tile_size_label.pack(side=tk.LEFT, padx=(10,0), pady=5)
        self.tile_size_slider = ttk.Scale(control_frame, from_=5, to=100, orient=tk.HORIZONTAL, variable=self.tile_size, command=self.update_tile_size_label)
        self.tile_size_slider.pack(side=tk.LEFT, padx=5, pady=5)
        self.tile_size_label.pack_forget()
        self.tile_size_slider.pack_forget()


        self.generate_pattern_btn = ttk.Button(control_frame, text="Hasilkan Pola", command=self.generate_pattern, state=tk.DISABLED)
        self.generate_pattern_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_btn = ttk.Button(control_frame, text="Simpan Gambar (JPG)", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = ttk.Label(control_frame, text="Siap.", anchor=tk.W)
        self.status_label.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

        # --- Frame Pratinjau Gambar ---
        preview_frame = ttk.LabelFrame(self.root, text="Pratinjau Gambar", padding="10")
        preview_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(preview_frame, bg="lightgray", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
        self.update_button_states()

    def update_button_states(self):
        is_image_loaded = self.original_image is not None
        self.generate_pattern_btn.config(state=tk.NORMAL if is_image_loaded else tk.DISABLED)
        self.save_btn.config(state=tk.NORMAL if self.current_display_image is not None else tk.DISABLED)

    def on_canvas_resize(self, event):
        if self.current_display_image:
            self.display_image(self.current_display_image)

    def update_tile_size_label(self, event=None):
        self.tile_size_label.config(text=f"Ukuran Kotak Mozaik ({int(self.tile_size.get())}px):")
        
    def on_pattern_change(self, selected_pattern):
        if selected_pattern == "Mozaik Kotak":
            self.tile_size_label.pack(side=tk.LEFT, padx=(10,0), pady=5)
            self.tile_size_slider.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            self.tile_size_label.pack_forget()
            self.tile_size_slider.pack_forget()
        self.update_button_states()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Pilih File Gambar",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert("RGB")
                self.image_width, self.image_height = self.original_image.size
                
                self.original_pixels = list(self.original_image.getdata())
                
                self.current_display_image = self.original_image.copy()
                self.display_image(self.original_image)
                
                self.status_label.config(text=f"Gambar '{os.path.basename(file_path)}' dimuat. Resolusi: {self.image_width}x{self.image_height} piksel.")
                messagebox.showinfo("Berhasil", "Gambar berhasil dimuat!")
                self.update_button_states()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat gambar: {e}")
                self.reset_app_state()

    def generate_pattern(self):
        if not self.original_pixels:
            messagebox.showwarning("Peringatan", "Muat gambar terlebih dahulu.")
            return

        self.status_label.config(text="Menghasilkan pola... Mohon tunggu.")
        self.root.update_idletasks()

        try:
            pattern = self.pattern_type.get()
            new_image_data = None
            
            shuffled_pixels = list(self.original_pixels)
            random.shuffle(shuffled_pixels)

            if pattern == "Acak Murni":
                new_image_data = shuffled_pixels
            elif pattern == "Baris Warna (Terurut)":
                shuffled_pixels.sort(key=lambda p: sum(p))
                new_image_data = shuffled_pixels
            elif pattern == "Kolom Warna (Terurut)":
                shuffled_pixels.sort(key=lambda p: sum(p))
                new_image_data = self._fill_columns_with_sorted_pixels(shuffled_pixels)
            elif pattern == "Mozaik Kotak":
                new_image_data = self._generate_mosaic_pattern()
            
            if new_image_data is not None:
                if pattern in ["Acak Murni", "Baris Warna (Terurut)"]:
                    self.current_display_image = Image.new("RGB", (self.image_width, self.image_height))
                    self.current_display_image.putdata(new_image_data)
                elif pattern in ["Kolom Warna (Terurut)", "Mozaik Kotak"]:
                    if isinstance(new_image_data, np.ndarray):
                        self.current_display_image = Image.fromarray(new_image_data.astype(np.uint8))
                    else:
                        self.current_display_image = new_image_data

            self.display_image(self.current_display_image)
            self.status_label.config(text=f"Pola '{pattern}' berhasil dihasilkan!")
            self.update_button_states()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghasilkan pola: {e}")
            self.status_label.config(text="Gagal menghasilkan pola.")

    def _fill_columns_with_sorted_pixels(self, sorted_pixels):
        img_array = np.zeros((self.image_height, self.image_width, 3), dtype=np.uint8)
        pixel_idx = 0
        for x in range(self.image_width):
            for y in range(self.image_height):
                if pixel_idx < len(sorted_pixels):
                    img_array[y, x] = sorted_pixels[pixel_idx]
                    pixel_idx += 1
        return img_array

    def _generate_mosaic_pattern(self):
        tile_s = self.tile_size.get()
        if tile_s == 0: tile_s = 1

        img_np = np.array(self.original_image)
        mosaic_np = np.zeros_like(img_np)

        for y in range(0, self.image_height, tile_s):
            for x in range(0, self.image_width, tile_s):
                x_end = min(x + tile_s, self.image_width)
                y_end = min(y + tile_s, self.image_height)
                
                block = img_np[y:y_end, x:x_end]
                
                if block.size > 0:
                    avg_color = block.mean(axis=(0, 1)).astype(np.uint8)
                else:
                    avg_color = [0, 0, 0]

                mosaic_np[y:y_end, x:x_end] = avg_color
        
        return Image.fromarray(mosaic_np)

    def display_image(self, img_to_display):
        if img_to_display:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width == 1 or canvas_height == 1:
                canvas_width = 500
                canvas_height = 500

            img_width, img_height = img_to_display.size
            if img_width == 0 or img_height == 0: return

            ratio_w = canvas_width / img_width
            ratio_h = canvas_height / img_height
            ratio = min(ratio_w, ratio_h)

            display_width = int(img_width * ratio)
            display_height = int(img_height * ratio)

            if display_width == 0: display_width = 1
            if display_height == 0: display_height = 1

            display_img_pil = img_to_display.resize((display_width, display_height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(display_img_pil)
            
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=self.photo_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def save_image(self):
        if not self.current_display_image:
            messagebox.showwarning("Peringatan", "Tidak ada gambar yang dihasilkan untuk disimpan.")
            return

        # Dapatkan timestamp saat ini (tahun, bulan, tanggal, jam, menit, detik)
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S") # Format: YYYYMMDD_HHMMSS

        # Dapatkan nama file yang diusulkan, tambahkan timestamp
        # Misalnya: pola_gambar_20250725_211530.jpg
        suggested_filename = f"pola_gambar_{timestamp}.jpg"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG files", "*.jpg"), ("All files", "*.*")],
            initialfile=suggested_filename # Gunakan nama file yang disarankan
        )
        if file_path:
            try:
                # Simpan gambar dengan kualitas tinggi (95) dan atur DPI ke 300
                self.current_display_image.save(file_path, quality=95, dpi=(300, 300))
                messagebox.showinfo("Sukses", f"Gambar berhasil disimpan ke:\n{file_path}\nDengan DPI 300.")
                self.status_label.config(text=f"Gambar disimpan ke: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")
                self.status_label.config(text="Gagal menyimpan gambar.")

    def reset_app_state(self):
        self.original_image = None
        self.original_pixels = None
        self.current_display_image = None
        self.image_width = 0
        self.image_height = 0
        self.canvas.delete("all")
        self.status_label.config(text="Siap.")
        self.update_button_states()

# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ImagePatternGeneratorApp(root)
    root.mainloop()