import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageTk
import os
from datetime import datetime
import random
import math

# --- Konfigurasi Global ---
OUTPUT_RESOLUTION = (4000, 4000)
OUTPUT_DPI = 300

class GeometricPatternGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Generator Pola Geometris Seamless")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        self.background_color = "#8B4513"
        self.line_color = "#DAA520"
        self.line_width = tk.IntVar(value=3)

        # Hapus opsi kubah
        self.pattern_type_options = [
            "Garis Geometris Acak", 
            "Garis Diagonal Sederhana", 
            "Grid Diagonal Bersilang",
            "Pola Gelombang 3D (Kompleks)" # Nama baru dan fokus pada kompleksitas
        ]
        self.selected_pattern_type = tk.StringVar(value="Garis Geometris Acak")

        self.tile_size_options = [
            "50x50 px", "100x100 px", "200x200 px", "250x250 px",
            "400x400 px", "500x500 px", "600x600 px", "800x800 px", "1000x1000 px"
        ]
        self.selected_tile_size_str = tk.StringVar(value="400x400 px")

        self.randomness_level = tk.IntVar(value=50) 

        # --- Opsi untuk Pola Gelombang 3D Kompleks ---
        self.wave_base_color_top = "#ADD8E6" 
        self.wave_base_color_bottom = "#1E90FF" 
        self.wave_line_color = "#FFFFFF"     
        self.wave_amplitude = tk.DoubleVar(value=0.2) 
        self.wave_frequency = tk.DoubleVar(value=2.0) 
        self.wave_line_spacing_ratio = tk.DoubleVar(value=0.1) 
        self.wave_distortion_strength = tk.DoubleVar(value=0.1) # Kekuatan distorsi acak
        self.wave_distortion_scale = tk.DoubleVar(value=0.5) # Skala noise distorsi
        self.wave_seed = tk.StringVar(value="") # Untuk mengunci seed atau membuatnya acak

        self.current_pattern_image = None

        self.create_widgets()

    def create_widgets(self):
        self.control_frame = ttk.LabelFrame(self.root, text="Pengaturan Pola", padding="10")
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Baris 0: Warna Latar Belakang & Jenis Pola
        ttk.Label(self.control_frame, text="Warna Latar Belakang:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.bg_color_btn = ttk.Button(self.control_frame, text="Pilih Warna", command=self.choose_bg_color)
        self.bg_color_btn.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.bg_color_display = tk.Canvas(self.control_frame, width=20, height=20, bg=self.background_color, relief=tk.RIDGE, bd=1)
        self.bg_color_display.grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(self.control_frame, text="Jenis Pola:").grid(row=0, column=3, sticky=tk.W, pady=2, padx=15)
        self.pattern_type_menu = ttk.OptionMenu(self.control_frame, self.selected_pattern_type, 
                                                self.selected_pattern_type.get(), 
                                                *self.pattern_type_options,
                                                command=self.on_pattern_type_change)
        self.pattern_type_menu.grid(row=0, column=4, sticky=tk.EW, padx=5, columnspan=2)

        # Baris 1: Warna Garis & Ukuran Tile Pola
        ttk.Label(self.control_frame, text="Warna Garis:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        self.line_color_btn = ttk.Button(self.control_frame, text="Pilih Warna", command=self.choose_line_color)
        self.line_color_btn.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.line_color_display = tk.Canvas(self.control_frame, width=20, height=20, bg=self.line_color, relief=tk.RIDGE, bd=1)
        self.line_color_display.grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(self.control_frame, text="Ukuran Tile Pola:").grid(row=1, column=3, sticky=tk.W, pady=2, padx=15)
        self.tile_size_menu = ttk.OptionMenu(self.control_frame, self.selected_tile_size_str, 
                                            self.selected_tile_size_str.get(), 
                                            *self.tile_size_options)
        self.tile_size_menu.grid(row=1, column=4, sticky=tk.EW, padx=5, columnspan=2)

        # Baris 2: Ketebalan Garis
        ttk.Label(self.control_frame, text="Ketebalan Garis:").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
        self.line_width_slider = ttk.Scale(self.control_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.line_width, command=self.update_line_width_label)
        self.line_width_slider.grid(row=2, column=1, sticky=tk.EW, padx=5)
        self.line_width_label = ttk.Label(self.control_frame, text=str(self.line_width.get()))
        self.line_width_label.grid(row=2, column=2, padx=5, pady=2)

        # Baris 3 & 4: Kerapatan/Variasi Acak (untuk pola garis)
        self.randomness_label_title = ttk.Label(self.control_frame, text="Kerapatan/Variasi Acak (0=Padat, 100=Jarang/Berlubang):")
        self.randomness_label_title.grid(row=3, column=0, sticky=tk.W, pady=2, padx=5, columnspan=3)
        self.randomness_slider = ttk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.randomness_level, command=self.update_randomness_label)
        self.randomness_slider.grid(row=4, column=0, sticky=tk.EW, padx=5, columnspan=2)
        self.randomness_label = ttk.Label(self.control_frame, text=str(self.randomness_level.get()))
        self.randomness_label.grid(row=4, column=2, padx=5, pady=2)

        # --- Hapus Opsi Spesifik untuk Pola Kubah Sederhana ---
        # self.dome_options_frame tidak lagi dibuat

        # --- Opsi Spesifik untuk Pola Gelombang 3D Kompleks ---
        self.wave_options_frame = ttk.LabelFrame(self.control_frame, text="Pengaturan Gelombang 3D", padding="5")
        
        ttk.Label(self.wave_options_frame, text="Warna Dasar Atas:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_base_color_top_btn = ttk.Button(self.wave_options_frame, text="Pilih Warna", command=self.choose_wave_base_color_top)
        self.wave_base_color_top_btn.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.wave_base_color_top_display = tk.Canvas(self.wave_options_frame, width=20, height=20, bg=self.wave_base_color_top, relief=tk.RIDGE, bd=1)
        self.wave_base_color_top_display.grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Warna Dasar Bawah:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_base_color_bottom_btn = ttk.Button(self.wave_options_frame, text="Pilih Warna", command=self.choose_wave_base_color_bottom)
        self.wave_base_color_bottom_btn.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.wave_base_color_bottom_display = tk.Canvas(self.wave_options_frame, width=20, height=20, bg=self.wave_base_color_bottom, relief=tk.RIDGE, bd=1)
        self.wave_base_color_bottom_display.grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(self.wave_options_frame, text="Warna Garis Gelombang:").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_line_color_btn = ttk.Button(self.wave_options_frame, text="Pilih Warna", command=self.choose_wave_line_color)
        self.wave_line_color_btn.grid(row=2, column=1, sticky=tk.EW, padx=5)
        self.wave_line_color_display = tk.Canvas(self.wave_options_frame, width=20, height=20, bg=self.wave_line_color, relief=tk.RIDGE, bd=1)
        self.wave_line_color_display.grid(row=2, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Amplitudo Gelombang (0.0-0.5):").grid(row=3, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_amplitude_slider = ttk.Scale(self.wave_options_frame, from_=0.0, to=0.5, orient=tk.HORIZONTAL, variable=self.wave_amplitude, command=self.update_wave_amplitude_label)
        self.wave_amplitude_slider.grid(row=3, column=1, sticky=tk.EW, padx=5)
        self.wave_amplitude_label = ttk.Label(self.wave_options_frame, text=f"{self.wave_amplitude.get():.1f}")
        self.wave_amplitude_label.grid(row=3, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Frekuensi Gelombang (Puncak per Tile):").grid(row=4, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_frequency_slider = ttk.Scale(self.wave_options_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL, variable=self.wave_frequency, command=self.update_wave_frequency_label)
        self.wave_frequency_slider.grid(row=4, column=1, sticky=tk.EW, padx=5)
        self.wave_frequency_label = ttk.Label(self.wave_options_frame, text=f"{self.wave_frequency.get():.1f}")
        self.wave_frequency_label.grid(row=4, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Jarak Garis Gelombang (0.01-0.2):").grid(row=5, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_line_spacing_slider = ttk.Scale(self.wave_options_frame, from_=0.01, to=0.2, orient=tk.HORIZONTAL, variable=self.wave_line_spacing_ratio, command=self.update_wave_line_spacing_label)
        self.wave_line_spacing_slider.grid(row=5, column=1, sticky=tk.EW, padx=5)
        self.wave_line_spacing_label = ttk.Label(self.wave_options_frame, text=f"{self.wave_line_spacing_ratio.get():.2f}")
        self.wave_line_spacing_label.grid(row=5, column=2, padx=5, pady=2)
        
        ttk.Label(self.wave_options_frame, text="Kekuatan Distorsi (0.0-1.0):").grid(row=6, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_distortion_strength_slider = ttk.Scale(self.wave_options_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.wave_distortion_strength, command=self.update_wave_distortion_strength_label)
        self.wave_distortion_strength_slider.grid(row=6, column=1, sticky=tk.EW, padx=5)
        self.wave_distortion_strength_label = ttk.Label(self.wave_options_frame, text=f"{self.wave_distortion_strength.get():.1f}")
        self.wave_distortion_strength_label.grid(row=6, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Skala Distorsi (0.1-2.0):").grid(row=7, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_distortion_scale_slider = ttk.Scale(self.wave_options_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL, variable=self.wave_distortion_scale, command=self.update_wave_distortion_scale_label)
        self.wave_distortion_scale_slider.grid(row=7, column=1, sticky=tk.EW, padx=5)
        self.wave_distortion_scale_label = ttk.Label(self.wave_options_frame, text=f"{self.wave_distortion_scale.get():.1f}")
        self.wave_distortion_scale_label.grid(row=7, column=2, padx=5, pady=2)

        ttk.Label(self.wave_options_frame, text="Seed Acak (Kosongkan untuk Acak):").grid(row=8, column=0, sticky=tk.W, pady=2, padx=5)
        self.wave_seed_entry = ttk.Entry(self.wave_options_frame, textvariable=self.wave_seed)
        self.wave_seed_entry.grid(row=8, column=1, sticky=tk.EW, padx=5, columnspan=2)

        self.wave_options_frame.grid_columnconfigure(1, weight=1)

        # Baris Tombol Generate dan Save (terakhir, di bawah semua pengaturan)
        # Baris ini akan disesuaikan di on_pattern_type_change
        self.generate_btn = ttk.Button(self.control_frame, text="Hasilkan Pola Geometris", command=self.generate_geometric_pattern)
        self.save_btn = ttk.Button(self.control_frame, text="Simpan Gambar (JPG)", command=self.save_image, state=tk.DISABLED)

        # Konfigurasi kolom agar melebar
        for i in [1, 4]:
            self.control_frame.grid_columnconfigure(i, weight=1)

        self.status_label = ttk.Label(self.root, text="Siap. Resolusi Output: 4000x4000 px.", anchor=tk.W)
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 5))

        # --- Frame Pratinjau Gambar ---
        preview_frame = ttk.LabelFrame(self.root, text="Pratinjau Pola", padding="10")
        preview_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(preview_frame, bg="lightgray", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        
        self.on_pattern_type_change(None) 
        self.update_button_states()

    def update_button_states(self):
        self.generate_btn.config(state=tk.NORMAL) 
        self.save_btn.config(state=tk.NORMAL if self.current_pattern_image is not None else tk.DISABLED)

    def on_canvas_resize(self, event):
        if self.current_pattern_image:
            self.display_image(self.current_pattern_image)

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Latar Belakang")
        if color_code[1]:
            self.background_color = color_code[1]
            self.bg_color_display.config(bg=self.background_color)

    def choose_line_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Garis")
        if color_code[1]:
            self.line_color = color_code[1]
            self.line_color_display.config(bg=self.line_color)
            
    def update_line_width_label(self, event=None):
        self.line_width_label.config(text=str(int(self.line_width.get())))

    def update_randomness_label(self, event=None):
        self.randomness_label.config(text=str(int(self.randomness_level.get())))
    
    # --- Fungsi untuk pengaturan gelombang ---
    def choose_wave_base_color_top(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Dasar Atas Gelombang")
        if color_code[1]:
            self.wave_base_color_top = color_code[1]
            self.wave_base_color_top_display.config(bg=self.wave_base_color_top)

    def choose_wave_base_color_bottom(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Dasar Bawah Gelombang")
        if color_code[1]:
            self.wave_base_color_bottom = color_code[1]
            self.wave_base_color_bottom_display.config(bg=self.wave_base_color_bottom)

    def choose_wave_line_color(self):
        color_code = colorchooser.askcolor(title="Pilih Warna Garis Gelombang")
        if color_code[1]:
            self.wave_line_color = color_code[1]
            self.wave_line_color_display.config(bg=self.wave_line_color)

    def update_wave_amplitude_label(self, event=None):
        self.wave_amplitude_label.config(text=f"{self.wave_amplitude.get():.1f}")

    def update_wave_frequency_label(self, event=None):
        self.wave_frequency_label.config(text=f"{self.wave_frequency.get():.1f}")

    def update_wave_line_spacing_label(self, event=None):
        self.wave_line_spacing_label.config(text=f"{self.wave_line_spacing_ratio.get():.2f}")

    def update_wave_distortion_strength_label(self, event=None):
        self.wave_distortion_strength_label.config(text=f"{self.wave_distortion_strength.get():.1f}")

    def update_wave_distortion_scale_label(self, event=None):
        self.wave_distortion_scale_label.config(text=f"{self.wave_distortion_scale.get():.1f}")


    def on_pattern_type_change(self, selected_pattern):
        current_pattern = self.selected_pattern_type.get()

        # Sembunyikan semua opsi spesifik yang mungkin tidak relevan
        self.randomness_label_title.grid_remove()
        self.randomness_slider.grid_remove()
        self.randomness_label.grid_remove()
        self.line_color_btn.grid_remove()
        self.line_color_display.grid_remove()
        self.line_width_slider.grid_remove()
        self.line_width_label.grid_remove()
        self.wave_options_frame.grid_remove() 

        # Atur posisi tombol Generate/Save default dulu (baris 5)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=10, sticky=tk.EW, padx=5)
        self.save_btn.grid(row=5, column=3, columnspan=3, pady=10, sticky=tk.EW, padx=5)

        if current_pattern == "Pola Gelombang 3D (Kompleks)":
            self.wave_options_frame.grid(row=3, column=0, columnspan=6, sticky=tk.EW, padx=5, pady=5)
            # Sesuaikan grid tombol Generate dan Save di bawah frame gelombang (row 9 atau 10 tergantung isian)
            self.generate_btn.grid(row=9, column=0, columnspan=3, pady=10, sticky=tk.EW, padx=5)
            self.save_btn.grid(row=9, column=3, columnspan=3, pady=10, sticky=tk.EW, padx=5)
            # Ketebalan garis (line_width) masih bisa digunakan untuk garis gelombang
            self.line_width_slider.grid(row=2, column=1, sticky=tk.EW, padx=5)
            self.line_width_label.grid(row=2, column=2, padx=5, pady=2)
        else: # Untuk pola garis standar
            self.line_color_btn.grid(row=1, column=1, sticky=tk.EW, padx=5)
            self.line_color_display.grid(row=1, column=2, padx=5, pady=2)
            self.line_width_slider.grid(row=2, column=1, sticky=tk.EW, padx=5)
            self.line_width_label.grid(row=2, column=2, padx=5, pady=2)
            self.randomness_label_title.grid(row=3, column=0, sticky=tk.W, pady=2, padx=5, columnspan=3)
            self.randomness_slider.grid(row=4, column=0, sticky=tk.EW, padx=5, columnspan=2)
            self.randomness_label.grid(row=4, column=2, padx=5, pady=2)
            # Tombol generate/save tetap di baris 5 seperti default

        # Atur ulang bobot kolom di self.control_frame
        for i in [1, 4]:
            self.control_frame.grid_columnconfigure(i, weight=1)


    def generate_geometric_pattern(self):
        self.status_label.config(text="Menghasilkan pola geometris... Mohon tunggu.")
        self.root.update_idletasks()

        try:
            output_width, output_height = OUTPUT_RESOLUTION
            
            selected_size_str = self.selected_tile_size_str.get().split('x')[0].strip()
            tile_dim = int(selected_size_str)
            
            tile_image = Image.new("RGB", (tile_dim, tile_dim), self.background_color)
            tile_draw = ImageDraw.Draw(tile_image)

            pattern_type = self.selected_pattern_type.get()
            
            randomness_prob = self.randomness_level.get() / 100.0

            # --- Inisialisasi Seed Acak ---
            current_seed = self.wave_seed.get()
            if not current_seed:
                # Jika kosong, buat seed acak baru dan tampilkan di entry
                new_seed = str(random.randint(0, 1000000))
                self.wave_seed.set(new_seed)
                random.seed(new_seed)
            else:
                random.seed(current_seed)


            # --- Logika Menggambar Tile Pola ---
            if pattern_type == "Garis Geometris Acak":
                self._draw_random_geometric_lines_tile(tile_draw, tile_dim, randomness_prob)
            elif pattern_type == "Garis Diagonal Sederhana":
                self._draw_simple_diagonal_tile(tile_draw, tile_dim, randomness_prob) 
            elif pattern_type == "Grid Diagonal Bersilang":
                self._draw_crossing_diagonal_grid_tile(tile_draw, tile_dim, randomness_prob)
            elif pattern_type == "Pola Gelombang 3D (Kompleks)":
                self._draw_3d_complex_wave_pattern_tile(tile_image, tile_draw, tile_dim) # Panggil fungsi kompleks
            
            # --- Duplikasi Tile ke Kanvas Output ---
            seamless_canvas = Image.new("RGB", OUTPUT_RESOLUTION, self.background_color)
            num_cols = (output_width + tile_dim - 1) // tile_dim
            num_rows = (output_height + tile_dim - 1) // tile_dim

            for y in range(num_rows):
                for x in range(num_cols):
                    seamless_canvas.paste(tile_image, (x * tile_dim, y * tile_dim))
            
            self.current_pattern_image = seamless_canvas
            self.display_image(self.current_pattern_image)
            
            self.status_label.config(text=f"Pola '{pattern_type}' berhasil dihasilkan! Resolusi: {output_width}x{output_height} px.")
            self.update_button_states()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghasilkan pola: {e}")
            self.status_label.config(text="Gagal menghasilkan pola.")

    # --- Fungsi Helper untuk Noise Perlin (Sederhana, untuk ilustrasi) ---
    # Ini bukan implementasi Perlin noise yang sebenarnya atau sangat efisien,
    # tapi cukup untuk memberikan variasi acak yang mulus.
    def _interpolate(self, a, b, x):
        ft = x * math.pi
        f = (1 - math.cos(ft)) * 0.5
        return a * (1 - f) + b * f

    def _generate_smooth_noise(self, width, height, scale, seed):
        # Gunakan random dengan seed lokal untuk noise
        local_random = random.Random(seed)
        
        noise_grid = {}
        for y in range(height + 1):
            for x in range(width + 1):
                noise_grid[(x, y)] = local_random.random()

        # Fungsi untuk mendapatkan nilai noise di (x,y)
        def get_noise(px, py):
            ix, iy = int(px), int(py)
            fx, fy = px - ix, py - iy

            v1 = noise_grid.get((ix, iy), 0)
            v2 = noise_grid.get((ix + 1, iy), 0)
            v3 = noise_grid.get((ix, iy + 1), 0)
            v4 = noise_grid.get((ix + 1, iy + 1), 0)

            i1 = self._interpolate(v1, v2, fx)
            i2 = self._interpolate(v3, v4, fx)
            return self._interpolate(i1, i2, fy)
        
        return get_noise


    # --- Fungsi untuk Menggambar Masing-masing Tipe Pola dalam Satu Tile ---
    # (Fungsi untuk Garis Geometris Acak, Garis Diagonal Sederhana, Grid Diagonal Bersilang tetap sama)
    def _draw_random_geometric_lines_tile(self, draw, tile_dim, randomness_prob):
        line_w = self.line_width.get()
        line_c = self.line_color

        num_main_segments = 10 
        
        edge_points = []
        num_edge_points_per_side = 5 
        for i in range(num_edge_points_per_side):
            pos_y = int(tile_dim / num_edge_points_per_side * i)
            if i > 0: 
                edge_points.append(((0, pos_y), (tile_dim, pos_y))) 
                edge_points.append(((pos_y, 0), (pos_y, tile_dim))) 
            
            edge_points.append(((0,0), (tile_dim, tile_dim)))
            edge_points.append(((tile_dim,0), (0, tile_dim)))

        draw.line([(0, 0), (tile_dim, tile_dim)], fill=line_c, width=line_w)
        draw.line([(tile_dim, 0), (0, tile_dim)], fill=line_c, width=line_w)

        for _ in range(num_main_segments):
            if random.random() > randomness_prob:
                x1, y1 = random.randint(0, tile_dim), random.randint(0, tile_dim)
                x2, y2 = random.randint(0, tile_dim), random.randint(0, tile_dim)
                draw.line([(x1, y1), (x2, y2)], fill=line_c, width=line_w)

        for p1, p2 in edge_points:
             if random.random() > randomness_prob * 0.7: 
                 draw.line([p1, p2], fill=line_c, width=line_w)


    def _draw_simple_diagonal_tile(self, draw, tile_dim, randomness_prob):
        line_w = self.line_width.get()
        line_c = self.line_color
        
        step = tile_dim // 4 
        if step == 0: step = 1

        for i in range(-tile_dim, tile_dim * 2, step):
            if random.random() > randomness_prob: 
                draw.line([(i, 0), (i + tile_dim, tile_dim)], fill=line_c, width=line_w)

        for i in range(-tile_dim, tile_dim * 2, step):
            if random.random() > randomness_prob: 
                draw.line([(i, tile_dim), (i + tile_dim, 0)], fill=line_c, width=line_w)


    def _draw_crossing_diagonal_grid_tile(self, draw, tile_dim, randomness_prob):
        line_w = self.line_width.get()
        line_c = self.line_color
        
        grid_step = tile_dim // 3
        if grid_step == 0: grid_step = 1

        for i in range(-tile_dim, 2 * tile_dim, grid_step):
            if random.random() > randomness_prob:
                draw.line([(i, 0), (i + tile_dim, tile_dim)], fill=line_c, width=line_w)
        
        for i in range(-tile_dim, 2 * tile_dim, grid_step):
            if random.random() > randomness_prob:
                draw.line([(i, tile_dim), (i + tile_dim, 0)], fill=line_c, width=line_w)

    def _draw_3d_complex_wave_pattern_tile(self, tile_image, tile_draw, tile_dim):
        """
        Menggambar pola gelombang 3D yang lebih kompleks dengan gradien warna,
        garis kontur, dan distorsi acak (berbasis noise).
        """
        line_w = self.line_width.get()
        wave_line_c = self.wave_line_color
        base_color_top = self.wave_base_color_top
        base_color_bottom = self.wave_base_color_bottom
        amplitude_ratio = self.wave_amplitude.get()
        frequency = self.wave_frequency.get()
        line_spacing_ratio = self.wave_line_spacing_ratio.get()
        distortion_strength = self.wave_distortion_strength.get()
        distortion_scale = self.wave_distortion_scale.get()

        # Konversi warna hex ke RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        rgb_top = hex_to_rgb(base_color_top)
        rgb_bottom = hex_to_rgb(base_color_bottom)

        # Inisialisasi generator noise untuk distorsi
        # Kita pakai seed yang sama untuk noise agar seamless
        # Gunakan seed numerik atau hash dari string seed
        current_seed_val = self.wave_seed.get()
        if not current_seed_val:
            # Ini seharusnya sudah diatur di generate_geometric_pattern
            # Tapi sebagai fallback
            current_seed_val = str(random.randint(0, 1000000)) 
            self.wave_seed.set(current_seed_val)
        
        noise_seed = hash(current_seed_val) % (2**32 - 1) # Pastikan seed numerik

        # Generate smooth noise untuk distorsi. Skala noise relatif terhadap tile_dim
        # Noise_grid_size akan mempengaruhi "ukuran" blob distorsi
        noise_grid_size_x = int(tile_dim / (tile_dim * distortion_scale)) 
        noise_grid_size_y = int(tile_dim / (tile_dim * distortion_scale))
        if noise_grid_size_x < 1: noise_grid_size_x = 1
        if noise_grid_size_y < 1: noise_grid_size_y = 1

        get_distortion_noise = self._generate_smooth_noise(noise_grid_size_x, noise_grid_size_y, distortion_scale, noise_seed)

        # 1. Gambar gradien latar belakang
        for y in range(tile_dim):
            t = y / tile_dim
            r = int(rgb_top[0] * (1 - t) + rgb_bottom[0] * t)
            g = int(rgb_top[1] * (1 - t) + rgb_bottom[1] * t)
            b = int(rgb_top[2] * (1 - t) + rgb_bottom[2] * t)
            tile_draw.line([(0, y), (tile_dim, y)], fill=(r, g, b))

        # 2. Gambar garis gelombang yang kompleks
        amplitude_px = tile_dim * amplitude_ratio 
        line_spacing_px = tile_dim * line_spacing_ratio
        if line_spacing_px < 1: line_spacing_px = 1 

        # Ini adalah jumlah garis yang akan digambar
        num_lines = int(tile_dim / line_spacing_px) + 2 # +2 untuk memastikan menutupi seluruh tinggi tile

        # Offset awal untuk membuat garis-garis sedikit acak secara vertikal di tile awal
        # Ini penting untuk seamlessness vertikal jika ada distorsi global.
        # Untuk pola ini, fokus seamlessness ada pada gelombang itu sendiri, bukan offset garis.
        # Jadi, kita tidak perlu random_offset_y yang berubah per tile.

        for i in range(num_lines):
            y_base_line = i * line_spacing_px 
            
            points = []
            for x in range(tile_dim + 1): 
                # Posisi x dan y yang dinormalisasi untuk noise
                norm_x = x / tile_dim
                norm_y = y_base_line / tile_dim

                # Dapatkan nilai distorsi dari noise
                # Kalikan dengan skala agar noise mencakup area yang tepat
                distortion_val = get_distortion_noise(norm_x * noise_grid_size_x, norm_y * noise_grid_size_y) 
                
                # Ubah nilai noise dari 0-1 menjadi -1.0 - 1.0
                distortion_val_mapped = (distortion_val * 2) - 1 

                # Terapkan gelombang utama
                wave_y_offset = amplitude_px * math.cos(2 * math.pi * frequency * norm_x)
                
                # Tambahkan distorsi ke offset Y
                # Distorsi diterapkan sebagai pergeseran tambahan pada Y
                # Kekuatan distorsi dikontrol oleh distortion_strength
                y_point_distorted = y_base_line + wave_y_offset + (distortion_val_mapped * distortion_strength * amplitude_px)
                
                points.append((x, int(y_point_distorted)))
            
            # Gambar garis gelombang
            if len(points) > 1:
                tile_draw.line(points, fill=wave_line_c, width=line_w)


    def display_image(self, img_to_display):
        if img_to_display:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width < 100 or canvas_height < 100:
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
        if not self.current_pattern_image:
            messagebox.showwarning("Peringatan", "Tidak ada pola yang dihasilkan untuk disimpan.")
            return

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        suggested_filename = f"pola_geometris_{timestamp}.jpg"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG files", "*.jpg"), ("All files", "*.*")],
            initialfile=suggested_filename
        )
        if file_path:
            try:
                self.current_pattern_image.save(file_path, quality=95, dpi=(OUTPUT_DPI, OUTPUT_DPI))
                messagebox.showinfo("Sukses", 
                                    f"Pola berhasil disimpan ke:\n{file_path}\nDengan DPI {OUTPUT_DPI}.")
                self.status_label.config(text=f"Pola disimpan ke: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")
                self.status_label.config(text="Gagal menyimpan gambar.")

    def reset_app_state(self):
        self.current_pattern_image = None
        self.canvas.delete("all")
        self.status_label.config(text="Siap. Resolusi Output: 4000x4000 px.")
        self.update_button_states()

# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GeometricPatternGeneratorApp(root)
    root.mainloop()