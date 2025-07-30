from PIL import Image, ImageDraw
import random
import os
import math

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
        # Mengambil satu palet acak dari semua yang tersedia
        all_palettes_flat = [color_list for sublist in palettes.values() for color_list in sublist if color_list]
        if not all_palettes_flat: # Jika tidak ada palet yang tersedia
            return [(240, 240, 240), (180, 180, 180), (120, 120, 120)] # Default fallback
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
    area_width = x_end - x_start
    area_height = y_end - y_start
    
    # Warna garis kedua dan ketiga dari palet
    line_color1 = colors[1]
    line_color2 = colors[2]

    # Menghitung rentang konstanta C untuk garis y = x + C (atau y = -x + C)
    # Rentang C harus mencakup seluruh area
    if direction == "top_left_to_bottom_right":
        # y = x + C  => C = y - x
        min_C = y_start - x_end
        max_C = y_end - x_start
    elif direction == "top_right_to_bottom_left":
        # y = -x + C => C = y + x
        min_C = y_start + x_start
        max_C = y_end + x_end
    else:
        raise ValueError("Arah diagonal tidak valid. Gunakan 'top_left_to_bottom_right' atau 'top_right_to_bottom_left'.")

    # Iterasi melalui nilai C untuk menggambar setiap garis
    current_color_idx = 0
    for C in range(min_C, max_C + 1, line_spacing):
        points = []
        
        # Tentukan warna garis untuk iterasi saat ini
        color_to_use = colors[1] if current_color_idx % 2 == 0 else colors[2]

        # Temukan titik potong dengan batas-batas area (x_start, x_end, y_start, y_end)
        # 1. Perpotongan dengan garis vertikal x = x_start
        if direction == "top_left_to_bottom_right": # y = x + C => y = x_start + C
            y_intersect = x_start + C
            if y_start <= y_intersect <= y_end:
                points.append((x_start, y_intersect))
        elif direction == "top_right_to_bottom_left": # y = -x + C => y = -x_start + C
            y_intersect = -x_start + C
            if y_start <= y_intersect <= y_end:
                points.append((x_start, y_intersect))

        # 2. Perpotongan dengan garis vertikal x = x_end
        if direction == "top_left_to_bottom_right": # y = x + C => y = x_end + C
            y_intersect = x_end + C
            if y_start <= y_intersect <= y_end:
                points.append((x_end, y_intersect))
        elif direction == "top_right_to_bottom_left": # y = -x + C => y = -x_end + C
            y_intersect = -x_end + C
            if y_start <= y_intersect <= y_end:
                points.append((x_end, y_intersect))

        # 3. Perpotongan dengan garis horizontal y = y_start
        if direction == "top_left_to_bottom_right": # y = x + C => x = y_start - C
            x_intersect = y_start - C
            if x_start <= x_intersect <= x_end:
                points.append((x_intersect, y_start))
        elif direction == "top_right_to_bottom_left": # y = -x + C => x = C - y_start
            x_intersect = C - y_start
            if x_start <= x_intersect <= x_end:
                points.append((x_intersect, y_start))

        # 4. Perpotongan dengan garis horizontal y = y_end
        if direction == "top_left_to_bottom_right": # y = x + C => x = y_end - C
            x_intersect = y_end - C
            if x_start <= x_intersect <= x_end:
                points.append((x_intersect, y_end))
        elif direction == "top_right_to_bottom_left": # y = -x + C => x = C - y_end
            x_intersect = C - y_end
            if x_start <= x_intersect <= x_end:
                points.append((x_intersect, y_end))

        # Filter titik unik dan pastikan ada dua titik untuk menggambar garis
        # Urutkan berdasarkan koordinat x, lalu y untuk konsistensi
        unique_points = sorted(list(set(points)))

        if len(unique_points) >= 2:
            # Kita hanya perlu dua titik paling ujung dari garis yang melintasi area
            # Karena garis diagonal akan memotong batas persegi di maksimal dua titik
            draw.line([unique_points[0], unique_points[-1]], fill=color_to_use, width=line_thickness)
        
        current_color_idx += 1


def generate_seamless_pattern(
    canvas_width=4000,
    canvas_height=4000,
    dpi=300,
    output_format="jpeg",
    output_filename="seamless_pattern",
    palette_type="random_pastel", # "random_pastel", "custom", "green_pastel", "purple_pastel", etc.
    custom_colors=None, # List of 3 (R, G, B) tuples if palette_type is "custom"
    randomize_line_props_per_quadrant=True # Mengacak ketebalan dan jarak garis per kuadran
):
    """
    Menghasilkan gambar seamless berukuran besar dengan pola garis diagonal.
    Gambar dibagi menjadi 4 kuadran, masing-masing dengan arah garis yang berbeda.
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
    
    # Pastikan palet memiliki minimal 3 warna (background, line1, line2)
    if len(colors) < 3:
        print("Peringatan: Palet warna harus memiliki minimal 3 warna. Menambahkan warna placeholder.")
        while len(colors) < 3:
            colors.append((200, 200, 200)) # Placeholder grey

    # Buat gambar kanvas utama
    full_img = Image.new("RGB", (canvas_width, canvas_height), colors[0]) # Warna pertama untuk background utama

    # Membagi kanvas menjadi 4 kuadran
    half_width = canvas_width // 2
    half_height = canvas_height // 2

    # Properti garis default atau acak
    default_line_thickness = max(2, min(5, canvas_width // 400)) # Kecil untuk 4000x4000
    default_line_spacing = max(20, min(50, canvas_width // 100)) # Untuk density yang baik

    # Kuadran 1 (Kiri Atas): Diagonal ke kanan bawah
    print("Menggambar Kuadran 1 (Kiri Atas)...")
    q1_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
    q1_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
    draw_diagonal_lines_in_area(full_img, colors, 0, 0, half_width, half_height,
                                 line_thickness=q1_line_thickness,
                                 line_spacing=q1_line_spacing,
                                 direction="top_left_to_bottom_right")

    # Kuadran 2 (Kanan Atas): Diagonal ke kiri bawah
    print("Menggambar Kuadran 2 (Kanan Atas)...")
    q2_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
    q2_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
    draw_diagonal_lines_in_area(full_img, colors, half_width, 0, canvas_width, half_height,
                                 line_thickness=q2_line_thickness,
                                 line_spacing=q2_line_spacing,
                                 direction="top_right_to_bottom_left")

    # Kuadran 3 (Kiri Bawah): Diagonal ke kanan atas
    print("Menggambar Kuadran 3 (Kiri Bawah)...")
    q3_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
    q3_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
    draw_diagonal_lines_in_area(full_img, colors, 0, half_height, half_width, canvas_height,
                                 line_thickness=q3_line_thickness,
                                 line_spacing=q3_line_spacing,
                                 direction="top_right_to_bottom_left") # Sesuai contoh
    
    # Kuadran 4 (Kanan Bawah): Diagonal ke kiri atas
    print("Menggambar Kuadran 4 (Kanan Bawah)...")
    q4_line_thickness = random.randint(default_line_thickness, default_line_thickness * 3) if randomize_line_props_per_quadrant else default_line_thickness
    q4_line_spacing = random.randint(default_line_spacing, default_line_spacing * 2) if randomize_line_props_per_quadrant else default_line_spacing
    draw_diagonal_lines_in_area(full_img, colors, half_width, half_height, canvas_width, canvas_height,
                                 line_thickness=q4_line_thickness,
                                 line_spacing=q4_line_spacing,
                                 direction="top_left_to_bottom_right") # Sesuai contoh

    # Simpan gambar
    output_path = os.path.join("output", f"{output_filename}.{output_format}")
    
    if output_format == "jpeg":
        full_img.save(output_path, format="JPEG", quality=95, dpi=(dpi, dpi))
    else:
        full_img.save(output_path, format=output_format.upper())

    print(f"Gambar seamless berhasil dibuat: {output_path}")


# --- Contoh Penggunaan ---
if __name__ == "__main__":
    # Pastikan direktori output ada
    if not os.path.exists("output"):
        os.makedirs("output")

    print("Memulai pembuatan gambar...")

    # Contoh 1: Pola seperti contoh gambar (4 kuadran dengan arah berbeda), warna pastel acak
    print("\n--- Contoh 1: Pola acak pastel ---")
    generate_seamless_pattern(
        output_filename="seamless_pattern_example",
        palette_type="random_pastel",
        randomize_line_props_per_quadrant=True
    )

    # Contoh 2: Pola dengan warna pastel hijau
    print("\n--- Contoh 2: Pola pastel hijau ---")
    generate_seamless_pattern(
        output_filename="seamless_pattern_green_pastel",
        palette_type="green_pastel",
        randomize_line_props_per_quadrant=True
    )

    # Contoh 3: Pola dengan warna pastel ungu
    print("\n--- Contoh 3: Pola pastel ungu ---")
    generate_seamless_pattern(
        output_filename="seamless_pattern_purple_pastel",
        palette_type="purple_pastel",
        randomize_line_props_per_quadrant=True
    )

    # Contoh 4: Pola dengan warna custom (misal, abu-abu muda, biru muda, pink muda)
    print("\n--- Contoh 4: Pola warna custom ---")
    generate_seamless_pattern(
        output_filename="seamless_pattern_custom_colors",
        palette_type="custom",
        custom_colors=[(230, 230, 230), (190, 220, 240), (240, 190, 220)], # Background, Garis 1, Garis 2
        randomize_line_props_per_quadrant=True
    )

    # Contoh 5: Pola dengan properti garis yang sama di setiap kuadran (tidak diacak)
    print("\n--- Contoh 5: Pola dengan properti garis seragam ---")
    generate_seamless_pattern(
        output_filename="seamless_pattern_uniform_lines",
        palette_type="blue_pastel",
        randomize_line_props_per_quadrant=False # Properti garis akan seragam di semua kuadran
    )

    print("\nSelesai membuat semua gambar.")