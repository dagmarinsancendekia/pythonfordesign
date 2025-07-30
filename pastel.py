from PIL import Image, ImageDraw
import random
import math

# --- Fungsi untuk Skema Warna Pastel ---
def get_pastel_color_scheme(name):
    """
    Mengembalikan daftar kode warna RGB untuk skema warna pastel tertentu.
    Warna pertama dalam daftar adalah warna latar belakang, sisanya adalah warna elemen pola.
    """
    schemes = {
        "pastel_green_mix": [
            (220, 240, 220),  # Light Mint Background
            (170, 220, 170),  # Muted Green
            (140, 200, 140),  # Soft Green
            (190, 250, 190)   # Pale Green
        ],
        "pastel_purple_mix": [
            (230, 220, 240),  # Light Lavender Background
            (190, 170, 220),  # Muted Purple
            (160, 140, 200),  # Soft Purple
            (210, 190, 250)   # Pale Purple
        ],
        "pastel_blue_mix": [
            (220, 235, 240),  # Light Sky Blue Background
            (170, 200, 220),  # Muted Blue
            (140, 170, 200),  # Soft Blue
            (190, 220, 250)   # Pale Blue
        ],
        "pastel_pink_mix": [
            (240, 220, 235),  # Light Rose Background
            (220, 170, 200),  # Muted Pink
            (200, 140, 170),  # Soft Pink
            (250, 190, 220)   # Pale Pink
        ],
        "multi_pastel": [
            (245, 245, 240),  # Creamy White Background
            (255, 204, 153),  # Peach
            (153, 204, 255),  # Sky Blue
            (204, 153, 255),  # Lilac
            (153, 255, 204)   # Mint Green
        ],
        "neutral_earth_tones": [
            (245, 245, 235),  # Off-white Background
            (220, 200, 180),  # Light Beige
            (180, 160, 140),  # Muted Brown
            (200, 180, 160)   # Sandy Brown
        ]
    }
    return schemes.get(name, [])

# --- Fungsi untuk Menghasilkan Pola Titik-titik (Polka Dot) Seamless ---
def generate_seamless_polka_dot(width, height, dpi, dot_size_range, color_scheme_name):
    """
    Menghasilkan gambar pola titik-titik (polka dot) yang mulus.
    Parameter:
    - width, height: Ukuran kanvas dalam piksel.
    - dpi: Resolusi gambar (dots per inch).
    - dot_size_range: Tuple (min_size, max_size) untuk ukuran titik.
    - color_scheme_name: Nama skema warna dari fungsi get_pastel_color_scheme.
    """
    colors = get_pastel_color_scheme(color_scheme_name)
    if not colors:
        print(f"Skema warna '{color_scheme_name}' tidak ditemukan. Menggunakan default.")
        bg_color = (255, 255, 255)
        dot_colors = [(0, 0, 0)]
    else:
        bg_color = colors[0]
        dot_colors = colors[1:] if len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Menghitung ukuran grid dasar
    # Ukuran grid lebih besar agar pola terlihat lebih bervariasi
    base_grid_size = random.randint(min(width, height) // 8, min(width, height) // 4)

    # Untuk memastikan pola mulus (seamless), kita perlu menggambar elemen
    # yang mungkin meluas di luar kanvas dan kemudian membungkusnya kembali
    # ke sisi yang berlawanan. Oleh karena itu, kita menggambar di area yang sedikit
    # lebih besar dari kanvas dan mempertimbangkan wrapping.
    buffer = base_grid_size # Buffer untuk memastikan titik di tepi juga mulus
    extended_width = width + buffer * 2
    extended_height = height + buffer * 2

    # Iterasi melalui grid yang diperluas
    for x in range(-buffer, extended_width, base_grid_size):
        for y in range(-buffer, extended_height, base_grid_size):
            # Terapkan offset acak untuk tampilan yang lebih organik
            offset_x = random.randint(-base_grid_size // 5, base_grid_size // 5)
            offset_y = random.randint(-base_grid_size // 5, base_grid_size // 5)

            dot_center_x = x + offset_x
            dot_center_y = y + offset_y

            dot_size = random.randint(dot_size_range[0], dot_size_range[1])
            dot_radius = dot_size // 2
            dot_color = random.choice(dot_colors)

            # Gambar titik dan salinannya yang dibungkus untuk tiling seamless
            # Loop melalui -width, 0, width dan -height, 0, height
            # memastikan titik yang melewati batas akan muncul di sisi lain
            for dx in [-width, 0, width]:
                for dy in [-height, 0, height]:
                    left = dot_center_x - dot_radius + dx
                    top = dot_center_y - dot_radius + dy
                    right = dot_center_x + dot_radius + dx
                    bottom = dot_center_y + dot_radius + dy
                    draw.ellipse((left, top, right, bottom), fill=dot_color)

    output_path = f'polka_dot_{color_scheme_name}.jpg'
    img.save(output_path, dpi=(dpi, dpi), quality=95) # quality=95 untuk kualitas baik
    return output_path

# --- Fungsi untuk Menghasilkan Pola Garis-garis (Stripes) Seamless ---
def generate_seamless_stripes(width, height, dpi, orientation, stripe_thickness_range, gap_range, color_scheme_name):
    """
    Menghasilkan gambar pola garis-garis yang mulus.
    Parameter:
    - width, height: Ukuran kanvas dalam piksel.
    - dpi: Resolusi gambar (dots per inch).
    - orientation: 'horizontal' atau 'vertical'.
    - stripe_thickness_range: Tuple (min_thickness, max_thickness) untuk ketebalan garis.
    - gap_range: Tuple (min_gap, max_gap) untuk jarak antar garis.
    - color_scheme_name: Nama skema warna dari fungsi get_pastel_color_scheme.
    """
    colors = get_pastel_color_scheme(color_scheme_name)
    if not colors:
        print(f"Skema warna '{color_scheme_name}' tidak ditemukan. Menggunakan default.")
        bg_color = (255, 255, 255)
        stripe_colors = [(0, 0, 0)]
    else:
        bg_color = colors[0]
        stripe_colors = colors[1:] if len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    current_position = 0
    # Kita menggambar hingga dua kali lebar/tinggi kanvas untuk memastikan wrapping yang mulus
    max_dimension = max(width, height) * 2

    while current_position < max_dimension:
        stripe_thickness = random.randint(stripe_thickness_range[0], stripe_thickness_range[1])
        gap = random.randint(gap_range[0], gap_range[1])

        # Pastikan kita tidak memilih warna background sebagai warna garis
        available_stripe_colors = [c for c in stripe_colors if c != bg_color]
        stripe_color = random.choice(available_stripe_colors) if available_stripe_colors else (0, 0, 0)

        # Gambar garis dan salinannya yang dibungkus
        if orientation == 'horizontal':
            for dy_wrap in [-height, 0, height]: # Pembungkus vertikal
                draw.rectangle((0, current_position + dy_wrap, width, current_position + stripe_thickness + dy_wrap), fill=stripe_color)
        else: # vertical
            for dx_wrap in [-width, 0, width]: # Pembungkus horizontal
                draw.rectangle((current_position + dx_wrap, 0, current_position + stripe_thickness + dx_wrap, height), fill=stripe_color)

        current_position += stripe_thickness + gap
        if current_position > max_dimension + max(stripe_thickness_range) + max(gap_range): # Batas agar tidak terlalu jauh
            break

    output_path = f'stripes_{orientation}_{color_scheme_name}.jpg'
    img.save(output_path, dpi=(dpi, dpi), quality=95)
    return output_path

# --- Pengaturan Utama ---
canvas_width = 4000
canvas_height = 4000
output_dpi = 300

# Skema warna yang tersedia
color_schemes = [
    "pastel_green_mix",
    "pastel_purple_mix",
    "pastel_blue_mix",
    "pastel_pink_mix",
    "multi_pastel",
    "neutral_earth_tones"
]

# --- Hasilkan Pola Titik-titik ---
print("--- Menghasilkan Pola Titik-titik ---")
for color_scheme in color_schemes:
    print(f"Membuat polka dot dengan skema warna: {color_scheme}...")
    # Rentang ukuran titik: (min_radius, max_radius)
    # Anda bisa menyesuaikan rentang ini untuk titik yang lebih besar/kecil
    dot_size_range = (80, 200)
    output_file = generate_seamless_polka_dot(canvas_width, canvas_height, output_dpi, dot_size_range, color_scheme)
    print(f"Tersimpan: {output_file}")

# --- Hasilkan Pola Garis-garis ---
print("\n--- Menghasilkan Pola Garis-garis ---")
for color_scheme in color_schemes:
    # Rentang ketebalan garis: (min_thickness, max_thickness)
    # Rentang jarak antar garis: (min_gap, max_gap)
    # Anda bisa menyesuaikan rentang ini
    stripe_thickness_range = (100, 300)
    gap_range = (50, 150)

    print(f"Membuat garis horizontal dengan skema warna: {color_scheme}...")
    output_file_h = generate_seamless_stripes(canvas_width, canvas_height, output_dpi, 'horizontal', stripe_thickness_range, gap_range, color_scheme)
    print(f"Tersimpan: {output_file_h}")

    print(f"Membuat garis vertikal dengan skema warna: {color_scheme}...")
    output_file_v = generate_seamless_stripes(canvas_width, canvas_height, output_dpi, 'vertical', stripe_thickness_range, gap_range, color_scheme)
    print(f"Tersimpan: {output_file_v}")

print("\nProses pembuatan pola selesai!")