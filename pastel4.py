from PIL import Image, ImageDraw
import random
import os
import math
from datetime import datetime

def get_pastel_palette(palette_name="random"):
    """
    Mengembalikan palet warna pastel yang telah ditentukan atau acak.
    Setiap palet berisi 3 warna.
    """
    palettes = {
        "random_pastel": [
            # Pastel Acak 1
            [(255, 204, 204), (204, 255, 204), (204, 204, 255)], # Merah muda, hijau muda, biru muda
            # Pastel Acak 2
            [(255, 223, 186), (186, 255, 223), (223, 186, 255)], # Peach, mint, lavender
            # Pastel Acak 3
            [(255, 240, 245), (240, 255, 245), (245, 240, 255)], # Lavender Blush, Mint Cream, Thistle
        ],
        "green_pastel": [
            [(198, 255, 198), (170, 255, 170), (142, 255, 142)], # shades of light green
            [(220, 255, 220), (200, 240, 200), (180, 225, 180)] # lighter shades of green
        ],
        "purple_pastel": [
            [(229, 204, 255), (204, 153, 255), (178, 102, 255)], # shades of light purple
            [(240, 220, 255), (220, 200, 245), (200, 180, 230)] # lighter shades of purple
        ],
        "blue_pastel": [
            [(204, 229, 255), (153, 204, 255), (102, 178, 255)], # shades of light blue
            [(220, 240, 255), (200, 220, 245), (180, 200, 230)] # lighter shades of blue
        ],
        "yellow_pastel": [
            [(255, 255, 204), (255, 255, 153), (255, 255, 102)], # shades of light yellow
            [(255, 255, 220), (240, 240, 200), (220, 220, 180)] # lighter shades of yellow
        ]
    }

    if palette_name == "random":
        all_palettes_flat = [color_list for sublist in palettes.values() for color_list in sublist if color_list]
        if not all_palettes_flat:
            return [(240, 240, 240), (180, 180, 180), (120, 120, 120)]
        return random.choice(all_palettes_flat)
    elif palette_name in palettes:
        return random.choice(palettes[palette_name])
    else:
        print(f"Peringatan: Palet '{palette_name}' tidak ditemukan. Menggunakan palet random_pastel.")
        return random.choice(palettes["random_pastel"])

def draw_diagonal_lines_in_area(
    img, colors, x_start, y_start, x_end, y_end, line_thickness, line_spacing, direction
):
    """
    Menggambar garis diagonal dalam area tertentu dari gambar utama.
    """
    draw = ImageDraw.Draw(img)
    
    line_color1 = colors[1]
    line_color2 = colors[2]

    if direction == "top_left_to_bottom_right":
        min_C = y_start - x_end
        max_C = y_end - x_start
    elif direction == "top_right_to_bottom_left":
        min_C = y_start + x_start
        max_C = y_end + x_end
    else:
        raise ValueError("Arah diagonal tidak valid. Gunakan 'top_left_to_bottom_right' atau 'top_right_to_bottom_left'.")

    current_color_idx = 0
    for C in range(min_C, max_C + 1, line_spacing):
        points = []
        color_to_use = colors[1] if current_color_idx % 2 == 0 else colors[2]

        # Temukan titik potong dengan batas-batas area
        # Perpotongan dengan x = x_start
        if direction == "top_left_to_bottom_right": y_intersect = x_start + C
        else: y_intersect = -x_start + C
        if y_start <= y_intersect <= y_end: points.append((x_start, y_intersect))

        # Perpotongan dengan x = x_end
        if direction == "top_left_to_bottom_right": y_intersect = x_end + C
        else: y_intersect = -x_end + C
        if y_start <= y_intersect <= y_end: points.append((x_end, y_intersect))

        # Perpotongan dengan y = y_start
        if direction == "top_left_to_bottom_right": x_intersect = y_start - C
        else: x_intersect = C - y_start
        if x_start <= x_intersect <= x_end: points.append((x_intersect, y_start))

        # Perpotongan dengan y = y_end
        if direction == "top_left_to_bottom_right": x_intersect = y_end - C
        else: x_intersect = C - y_end
        if x_start <= x_intersect <= x_end: points.append((x_intersect, y_end))

        unique_points = sorted(list(set(points)))

        if len(unique_points) >= 2:
            draw.line([unique_points[0], unique_points[-1]], fill=color_to_use, width=line_thickness)
        
        current_color_idx += 1

def draw_straight_lines_in_area(
    img, colors, x_start, y_start, x_end, y_end, line_thickness, line_spacing, orientation="random"
):
    """
    Menggambar garis lurus (horizontal atau vertikal) dalam area tertentu.
    """
    draw = ImageDraw.Draw(img)
    line_color1 = colors[1]
    line_color2 = colors[2]

    if orientation == "random":
        actual_orientation = random.choice(["horizontal", "vertical"])
    else:
        actual_orientation = orientation

    current_color_idx = 0
    if actual_orientation == "horizontal":
        for y_pos in range(y_start, y_end + 1, line_spacing):
            color_to_use = colors[1] if current_color_idx % 2 == 0 else colors[2]
            draw.line([(x_start, y_pos), (x_end, y_pos)], fill=color_to_use, width=line_thickness)
            current_color_idx += 1
    elif actual_orientation == "vertical":
        for x_pos in range(x_start, x_end + 1, line_spacing):
            color_to_use = colors[1] if current_color_idx % 2 == 0 else colors[2]
            draw.line([(x_pos, y_start), (x_pos, y_end)], fill=color_to_use, width=line_thickness)
            current_color_idx += 1

def draw_checkerboard_in_area(
    img, colors, x_start, y_start, x_end, y_end, square_size=None
):
    """
    Menggambar pola papan catur dalam area tertentu.
    """
    draw = ImageDraw.Draw(img)
    color1 = colors[1] # Warna kotak pertama
    color2 = colors[2] # Warna kotak kedua

    if square_size is None:
        area_dim = min(x_end - x_start, y_end - y_start)
        square_size = max(20, area_dim // random.randint(5, 15)) # Ukuran kotak acak

    # Pastikan square_size tidak terlalu kecil
    square_size = max(1, square_size)

    for y in range(y_start, y_end, square_size):
        for x in range(x_start, x_end, square_size):
            # Tentukan warna berdasarkan posisi kotak
            if ((x // square_size) % 2 == 0 and (y // square_size) % 2 == 0) or \
               ((x // square_size) % 2 != 0 and (y // square_size) % 2 != 0):
                fill_color = color1
            else:
                fill_color = color2
            
            draw.rectangle([x, y, x + square_size, y + square_size], fill=fill_color)


def generate_seamless_pattern(
    canvas_width=4000,
    canvas_height=4000,
    dpi=300,
    output_format="jpeg",
    output_basename="seamless_pattern", # Nama dasar file, timestamp akan ditambahkan
    palette_type="random_pastel",
    custom_colors=None,
    randomize_line_props_per_quadrant=True,
    pattern_type_per_quadrant="random" # "random", "diagonal", "straight_lines", "checkerboard"
):
    """
    Menghasilkan gambar seamless berukuran besar dengan pola bervariasi.
    Gambar dibagi menjadi 4 kuadran, masing-masing dengan pola/arah yang bisa berbeda.
    """
    if not os.path.exists("output"):
        os.makedirs("output")

    # Ambil palet warna
    if palette_type == "custom":
        if custom_colors is None or len(custom_colors) != 3:
            print("Error: Untuk palet 'custom', 'custom_colors' harus berupa daftar 3 tuple (R, G, B).")
            return
        colors = custom_colors
    else:
        colors = get_pastel_palette(palette_type)
    
    if len(colors) < 3:
        print("Peringatan: Palet warna harus memiliki minimal 3 warna. Menambahkan warna placeholder.")
        while len(colors) < 3:
            colors.append((200, 200, 200)) # Placeholder grey

    # Buat gambar kanvas utama
    full_img = Image.new("RGB", (canvas_width, canvas_height), colors[0])

    # Membagi kanvas menjadi 4 kuadran
    half_width = canvas_width // 2
    half_height = canvas_height // 2

    # Properti garis default atau acak
    default_line_thickness = max(2, min(5, canvas_width // 400))
    default_line_spacing = max(20, min(50, canvas_width // 100))
    default_square_size = max(20, min(100, canvas_width // 40))

    quadrants = [
        (0, 0, half_width, half_height),          # Kuadran 1 (Kiri Atas)
        (half_width, 0, canvas_width, half_height), # Kuadran 2 (Kanan Atas)
        (0, half_height, half_width, canvas_height), # Kuadran 3 (Kiri Bawah)
        (half_width, half_height, canvas_width, canvas_height) # Kuadran 4 (Kanan Bawah)
    ]

    # Menentukan jenis pola untuk setiap kuadran
    for i, (x1, y1, x2, y2) in enumerate(quadrants):
        current_pattern_type = pattern_type_per_quadrant
        if pattern_type_per_quadrant == "random":
            current_pattern_type = random.choice(["diagonal", "straight_lines", "checkerboard"])
        
        print(f"Menggambar Kuadran {i+1} ({current_pattern_type})...")

        if current_pattern_type == "diagonal":
            q_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
            q_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
            
            # Arah diagonal seperti contoh Anda untuk pola dasar
            if i == 0 or i == 3: # Kuadran Kiri Atas & Kanan Bawah
                direction = "top_left_to_bottom_right"
            else: # Kuadran Kanan Atas & Kiri Bawah
                direction = "top_right_to_bottom_left"
            
            # Tambahkan sedikit pengacakan arah jika benar-benar random
            if randomize_line_props_per_quadrant: # Menggunakan parameter ini untuk pengacakan arah juga
                 direction = random.choice(["top_left_to_bottom_right", "top_right_to_bottom_left"])

            draw_diagonal_lines_in_area(full_img, colors, x1, y1, x2, y2,
                                         line_thickness=q_line_thickness,
                                         line_spacing=q_line_spacing,
                                         direction=direction)
        
        elif current_pattern_type == "straight_lines":
            q_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
            q_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
            orientation = random.choice(["horizontal", "vertical"]) if randomize_line_props_per_quadrant else "horizontal" # Default horizontal jika tidak diacak
            draw_straight_lines_in_area(full_img, colors, x1, y1, x2, y2,
                                        line_thickness=q_line_thickness,
                                        line_spacing=q_line_spacing,
                                        orientation=orientation)
        
        elif current_pattern_type == "checkerboard":
            q_square_size = random.randint(default_square_size // 2, default_square_size * 2) if randomize_line_props_per_quadrant else default_square_size
            draw_checkerboard_in_area(full_img, colors, x1, y1, x2, y2,
                                      square_size=q_square_size)
        
        else:
            print(f"Peringatan: Jenis pola '{current_pattern_type}' tidak dikenal. Melanjutkan tanpa menggambar di kuadran ini.")


    # Simpan gambar dengan timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename_with_timestamp = f"{output_basename}_{timestamp}.{output_format}"
    output_path = os.path.join("output", output_filename_with_timestamp)
    
    if output_format == "jpeg":
        full_img.save(output_path, format="JPEG", quality=95, dpi=(dpi, dpi))
    else:
        full_img.save(output_path, format=output_format.upper())

    print(f"Gambar seamless berhasil dibuat: {output_path}")


# --- Contoh Penggunaan ---
if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")

    print("Memulai pembuatan gambar dengan variasi dan timestamp...")

    # Contoh 1: Pola campuran acak per kuadran (diagonal, garis lurus, checkerboard)
    print("\n--- Contoh 1: Pola campuran acak ---")
    generate_seamless_pattern(
        output_basename="random_mixed_pattern",
        palette_type="random_pastel",
        randomize_line_props_per_quadrant=True,
        pattern_type_per_quadrant="random"
    )

    # Contoh 2: Hanya pola garis lurus (horizontal/vertikal diacak per kuadran)
    print("\n--- Contoh 2: Hanya pola garis lurus ---")
    generate_seamless_pattern(
        output_basename="straight_lines_pattern",
        palette_type="blue_pastel",
        randomize_line_props_per_quadrant=True,
        pattern_type_per_quadrant="straight_lines"
    )

    # Contoh 3: Hanya pola checkerboard
    print("\n--- Contoh 3: Hanya pola checkerboard ---")
    generate_seamless_pattern(
        output_basename="checkerboard_pattern",
        palette_type="green_pastel",
        randomize_line_props_per_quadrant=True,
        pattern_type_per_quadrant="checkerboard"
    )

    # Contoh 4: Pola diagonal seperti contoh awal, dengan warna custom
    print("\n--- Contoh 4: Pola diagonal custom ---")
    generate_seamless_pattern(
        output_basename="diagonal_custom_pattern",
        palette_type="custom",
        custom_colors=[(255, 230, 240), (200, 150, 180), (100, 50, 70)], # Background, Garis 1, Garis 2
        randomize_line_props_per_quadrant=True,
        pattern_type_per_quadrant="diagonal"
    )

    print("\nSelesai membuat semua gambar.")