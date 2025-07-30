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
        return random.choice([color_list for sublist in palettes.values() for color_list in sublist if color_list])
    elif palette_name in palettes:
        return random.choice(palettes[palette_name])
    else:
        print(f"Peringatan: Palet '{palette_name}' tidak ditemukan. Menggunakan palet random_pastel.")
        return random.choice(palettes["random_pastel"])

def create_seamless_diagonal_line_tile(
    tile_size,
    colors,
    line_thickness=None, # Jika None, akan diacak
    line_spacing=None,   # Jika None, akan diacak
    direction="random"   # "top_left_to_bottom_right", "top_right_to_bottom_left", "random"
):
    """
    Membuat satu tile (ubin) gambar dengan pola garis diagonal yang seamless.
    Args:
        tile_size (int): Ukuran sisi tile (misal, 256 untuk tile 256x256).
        colors (list of tuple): Daftar 3 warna (R, G, B) untuk background dan garis.
        line_thickness (int, optional): Ketebalan garis. Jika None, akan diacak.
        line_spacing (int, optional): Jarak antar garis (pusat ke pusat). Jika None, akan diacak.
        direction (str, optional): Arah diagonal.
    Returns:
        PIL.Image.Image: Objek gambar tile.
    """
    img = Image.new("RGB", (tile_size, tile_size), colors[0])
    draw = ImageDraw.Draw(img)

    # Pengacakan properti garis jika tidak ditentukan
    if line_thickness is None:
        line_thickness = random.randint(2, max(5, tile_size // 40)) # Min 2, Max tile_size/40
    if line_spacing is None:
        line_spacing = random.randint(line_thickness * 2, max(line_thickness * 3, tile_size // 10)) # Min 2*thickness, Max tile_size/10

    # Pastikan line_spacing minimal sama dengan line_thickness
    line_spacing = max(line_spacing, line_thickness)

    # Pilih arah diagonal
    if direction == "random":
        actual_direction = random.choice(["top_left_to_bottom_right", "top_right_to_bottom_left"])
    else:
        actual_direction = direction

    # Warna garis kedua dan ketiga
    line_color1 = colors[1]
    line_color2 = colors[2]

    # Menghitung offset untuk garis-garis agar seamless
    # Offset ini penting agar garis yang keluar dari satu sisi tile masuk di sisi lain
    # Untuk diagonal, kita bisa memulai dari luar sudut agar mencakup seluruh tile
    max_dim = tile_size

    if actual_direction == "top_left_to_bottom_right":
        # Garis dari kiri atas ke kanan bawah (y = x + c)
        for i in range(-max_dim, max_dim * 2, line_spacing):
            # Garis pertama (warna 1)
            x1_a, y1_a = 0, i
            x2_a, y2_a = i, 0
            draw.line([(x1_a, y1_a), (x2_a, y2_a)], fill=line_color1, width=line_thickness)

            # Garis kedua (warna 2) - digambar di samping garis pertama untuk efek strip
            # Ini memerlukan perhitungan yang lebih akurat untuk jarak antar dua warna garis
            # Untuk kesederhanaan dan efek seamless yang lebih mudah, kita bisa mengulang satu warna garis
            # atau menggunakan strategi yang berbeda untuk 2 warna.
            # Untuk saat ini, kita akan membuat dua garis terpisah.
            # Jika ingin strip 2 warna, kita bisa menggambar 2 garis berurutan dengan warna berbeda
            # pada setiap 'i' interval, atau membuatnya lebih kompleks.
            # Saya akan membuat pola yang lebih sederhana namun tetap seamless dengan satu warna garis berulang,
            # dan menggunakan warna kedua/ketiga untuk latar belakang atau sebagai variasi per tile.

            # Strategi lebih sederhana: bergantian warna garis pada setiap interval line_spacing
            if (i // line_spacing) % 2 == 0:
                 draw.line([(0, i), (i, 0)], fill=line_color1, width=line_thickness)
                 draw.line([(i, tile_size), (tile_size, i)], fill=line_color1, width=line_thickness) # Menarik garis dari sisi bawah/kanan
            else:
                 draw.line([(0, i), (i, 0)], fill=line_color2, width=line_thickness)
                 draw.line([(i, tile_size), (tile_size, i)], fill=line_color2, width=line_thickness)


    elif actual_direction == "top_right_to_bottom_left":
        # Garis dari kanan atas ke kiri bawah (y = -x + c)
        for i in range(-max_dim, max_dim * 2, line_spacing):
            # Garis pertama (warna 1)
            x1_a, y1_a = i, 0
            x2_a, y2_a = 0, i
            draw.line([(x1_a, y1_a), (x2_a, y2_a)], fill=line_color1, width=line_thickness)

            # Garis kedua (warna 2)
            if (i // line_spacing) % 2 == 0:
                 draw.line([(i, 0), (0, i)], fill=line_color1, width=line_thickness)
                 draw.line([(0, tile_size - i), (tile_size - i, tile_size)], fill=line_color1, width=line_thickness)
            else:
                 draw.line([(i, 0), (0, i)], fill=line_color2, width=line_thickness)
                 draw.line([(0, tile_size - i), (tile_size - i, tile_size)], fill=line_color2, width=line_thickness)


    # Pastikan tidak ada artefak di tepi karena pembulatan atau perhitungan
    # Draw a rectangle outline to trim any lines slightly outside the tile
    # draw.rectangle([0, 0, tile_size - 1, tile_size - 1], outline=None)

    return img

def generate_seamless_pattern(
    canvas_width=4000,
    canvas_height=4000,
    dpi=300,
    output_format="jpeg",
    output_filename="seamless_pattern",
    palette_type="random_pastel", # "random_pastel", "custom", "green_pastel", "purple_pastel", etc.
    custom_colors=None, # List of 3 (R, G, B) tuples if palette_type is "custom"
    tile_size=256, # Ukuran tile dasar, disarankan kelipatan dari ukuran kanvas
    randomize_line_props_per_tile=True, # Mengacak ketebalan dan jarak garis per tile
    randomize_tile_direction=True # Mengacak arah garis per tile
):
    """
    Menghasilkan gambar seamless berukuran besar dengan pola garis diagonal.
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

    # Hitung berapa banyak tile yang dibutuhkan
    num_tiles_x = math.ceil(canvas_width / tile_size)
    num_tiles_y = math.ceil(canvas_height / tile_size)

    # Isi kanvas dengan tile
    for y_tile in range(num_tiles_y):
        for x_tile in range(num_tiles_x):
            current_line_thickness = None
            current_line_spacing = None
            current_direction = None

            if randomize_line_props_per_tile:
                current_line_thickness = random.randint(2, max(5, tile_size // 40))
                current_line_spacing = random.randint(current_line_thickness * 2, max(current_line_thickness * 3, tile_size // 10))
            if randomize_tile_direction:
                current_direction = random.choice(["top_left_to_bottom_right", "top_right_to_bottom_left"])

            # Untuk memastikan seamlessness di batas tile, kita perlu memastikan
            # bahwa sifat garis (ketebalan, jarak) dan arah adalah SAMA untuk semua tile
            # jika kita ingin pola yang seragam.
            # Namun, jika ingin setiap tile punya pola sendiri, maka seamlessness
            # yang sebenarnya (tidak ada jahitan) akan lebih sulit dicapai dengan variasi acak.
            # Untuk gambar seperti contoh Anda, yang punya "kuadran" berbeda, kita bisa membuat
            # setiap kuadran sebagai satu "tile" besar yang berbeda.

            # Untuk mencapai pola seperti contoh (yang tiap 'kuadran' beda arah)
            # sekaligus seamless, kita perlu sedikit penyesuaian pada tile_size.
            # Atau, menganggap seluruh 4000x4000 sebagai satu "tile" raksasa
            # yang dibagi menjadi 4 kuadran, masing-masing dengan arah garis berbeda.
            # Jika tile_size kecil dan diulang, properti acak per tile akan membuat pola
            # terlihat "patchy" dan bukan seamless di seluruh gambar seperti contoh.

            # Mari kita coba pendekatan di mana ada 4 kuadran besar seperti contoh Anda
            # dan setiap kuadran menggunakan arah garis yang berbeda, tetapi garisnya sendiri
            # tetap seamless *di dalam* kuadran tersebut.
            # Ini akan berarti kita menggambar langsung di full_img, bukan tiling kecil.

            # Membagi kanvas menjadi 4 kuadran untuk meniru gambar contoh
            half_width = canvas_width // 2
            half_height = canvas_height // 2

            # Menggambar pola untuk setiap kuadran
            # Kuadran 1 (Kiri Atas): Mirip contoh, diagonal ke kanan bawah
            draw_diagonal_lines_in_area(full_img, colors, 0, 0, half_width, half_height,
                                         line_thickness=random.randint(2, max(5, half_width // 40)),
                                         line_spacing=random.randint(20, max(30, half_width // 10)),
                                         direction="top_left_to_bottom_right")

            # Kuadran 2 (Kanan Atas): Mirip contoh, diagonal ke kiri bawah
            draw_diagonal_lines_in_area(full_img, colors, half_width, 0, canvas_width, half_height,
                                         line_thickness=random.randint(2, max(5, half_width // 40)),
                                         line_spacing=random.randint(20, max(30, half_width // 10)),
                                         direction="top_right_to_bottom_left")

            # Kuadran 3 (Kiri Bawah): Mirip contoh, diagonal ke kiri atas
            draw_diagonal_lines_in_area(full_img, colors, 0, half_height, half_width, canvas_height,
                                         line_thickness=random.randint(2, max(5, half_width // 40)),
                                         line_spacing=random.randint(20, max(30, half_width // 10)),
                                         direction="top_right_to_bottom_left") # Sesuai contoh di kuadran bawah

            # Kuadran 4 (Kanan Bawah): Mirip contoh, diagonal ke kanan atas
            draw_diagonal_lines_in_area(full_img, colors, half_width, half_height, canvas_width, canvas_height,
                                         line_thickness=random.randint(2, max(5, half_width // 40)),
                                         line_spacing=random.randint(20, max(30, half_width // 10)),
                                         direction="top_left_to_bottom_right") # Sesuai contoh di kuadran bawah

    # Simpan gambar
    output_path = os.path.join("output", f"{output_filename}.{output_format}")
    
    # Untuk JPEG, kualitas dan DPI
    if output_format == "jpeg":
        # Pillow menggunakan 'resolution' untuk DPI
        # Ini tidak selalu mempengaruhi ukuran fisik, tapi metadata
        full_img.save(output_path, format="JPEG", quality=95, dpi=(dpi, dpi))
    else:
        full_img.save(output_path, format=output_format.upper())

    print(f"Gambar seamless berhasil dibuat: {output_path}")


def draw_diagonal_lines_in_area(
    img, colors, x_start, y_start, x_end, y_end, line_thickness, line_spacing, direction
):
    """
    Menggambar garis diagonal dalam area tertentu dari gambar utama.
    Ini adalah fungsi pembantu untuk pola 4 kuadran.
    """
    draw = ImageDraw.Draw(img)
    area_width = x_end - x_start
    area_height = y_end - y_start
    line_color1 = colors[1]
    line_color2 = colors[2]
    
    # Menyesuaikan titik awal dan akhir garis agar sesuai dengan area yang diberikan
    max_dim = max(area_width, area_height)

    if direction == "top_left_to_bottom_right":
        # Garis dari kiri atas ke kanan bawah (y = x + c)
        # Offset awal disesuaikan dengan x_start dan y_start
        for i in range(-max_dim + y_start, max_dim + area_height + y_start, line_spacing):
            # Hitung titik-titik garis dalam koordinat global
            p1_x = x_start
            p1_y = i

            p2_x = x_end
            p2_y = i + (x_end - x_start)

            # Batasi garis agar tidak terlalu jauh dari area yang ditentukan
            # Ini bisa disederhanakan dengan menggunakan draw.line saja,
            # tapi memastikan ujungnya tidak keluar terlalu jauh dari area
            # bisa membuat perhitungan lebih akribut.
            # Untuk seamless di area, kita perlu tarik garis yang melintasi area.

            # Strategi: hitung perpotongan garis y = x + C dengan batas area
            # Garis y = x + c
            # Atas: y_start = x + c => x = y_start - c
            # Bawah: y_end = x + c => x = y_end - c
            # Kiri: x_start = y - c => y = x_start + c
            # Kanan: x_end = y - c => y = x_end + c

            # Untuk memastikan seamlessness di dalam area dan di perbatasan kuadran,
            # kita perlu memastikan bahwa semua garis memiliki jarak yang sama,
            # dan dimulai serta berakhir dengan cara yang konsisten.
            # Cara paling mudah untuk pola seperti ini adalah menggambar garis yang melintasi
            # seluruh area dan mengulang offset-nya.

            start_x = -max_dim # Mulai dari luar kiri/atas area
            end_x = area_width + max_dim # Berakhir di luar kanan/bawah area

            if (i // line_spacing) % 2 == 0:
                color_to_use = line_color1
            else:
                color_to_use = line_color2

            # Gambar garis dari luar kiri atas ke luar kanan bawah relatif terhadap area
            for line_offset in range(int(math.sqrt(area_width**2 + area_height**2)) * -1,
                                     int(math.sqrt(area_width**2 + area_height**2)) + max(area_width, area_height),
                                     line_spacing):
                
                # Menghitung titik awal dan akhir garis diagonal
                # Untuk y = x + C, C adalah konstanta
                C = line_offset # Menggunakan line_offset sebagai C
                
                # Titik awal: (x_start, y_start + C) jika C > -y_start
                #             (x_start - C, y_start) jika C <= -y_start
                
                # Ini adalah pendekatan yang lebih baik untuk menggambar garis diagonal
                # yang melewati seluruh area dan memastikan seamlessness di dalamnya.
                # Kita perlu menghitung titik potong dengan batas area.

                # Titik awal di sisi kiri atau atas
                pt1_x = x_start
                pt1_y = y_start + line_offset

                if pt1_y < y_start:
                    pt1_y = y_start
                    pt1_x = x_start - line_offset # Jika dimulai dari atas, x lebih kecil

                # Titik akhir di sisi kanan atau bawah
                pt2_x = x_end
                pt2_y = y_end + line_offset - (x_end - x_start) # y2 = y1 + (x2-x1)
                
                if pt2_y > y_end:
                    pt2_y = y_end
                    pt2_x = x_end - (y_end - (y_start + line_offset)) # Jika berakhir di bawah, x lebih besar

                # Periksa apakah garis ini benar-benar melintasi area
                if not (pt1_x > x_end or pt1_y > y_end or pt2_x < x_start or pt2_y < y_start):
                    draw.line([(pt1_x, pt1_y), (pt2_x, pt2_y)], fill=color_to_use, width=line_thickness)


    elif direction == "top_right_to_bottom_left":
        # Garis dari kanan atas ke kiri bawah (y = -x + c)
        for i in range(-max_dim + y_start, max_dim + area_height + y_start, line_spacing):
            if (i // line_spacing) % 2 == 0:
                color_to_use = line_color1
            else:
                color_to_use = line_color2
            
            # Untuk y = -x + C, C adalah konstanta
            C = i
            
            # Titik awal di sisi kanan atau atas
            pt1_x = x_end
            pt1_y = y_start - (x_end - (x_start + C)) # y = -x + C => x = C - y. x2 = C - y1
            
            if pt1_y < y_start:
                pt1_y = y_start
                pt1_x = x_end - (y_start - i) # Jika dimulai dari atas, x lebih besar

            # Titik akhir di sisi kiri atau bawah
            pt2_x = x_start
            pt2_y = y_end # y2 = -x1 + C
            
            if pt2_x < x_start: # Ini tidak akan terjadi jika pt2_x = x_start
                 pass # do nothing

            if not (pt1_x < x_start or pt1_y > y_end or pt2_x > x_end or pt2_y < y_start):
                 # Gambar garis dari titik yang melintasi area dengan batas x dan y
                 # Menghitung titik perpotongan dengan batas area
                 
                 # Titik yang benar-benar di dalam atau di batas area
                 # Hitung titik potong dengan 4 sisi area (x_start, x_end, y_start, y_end)
                 points = []
                 # Perpotongan dengan x = x_start
                 y_intersect = -x_start + C
                 if y_start <= y_intersect <= y_end:
                     points.append((x_start, y_intersect))
                 # Perpotongan dengan x = x_end
                 y_intersect = -x_end + C
                 if y_start <= y_intersect <= y_end:
                     points.append((x_end, y_intersect))
                 # Perpotongan dengan y = y_start
                 x_intersect = C - y_start
                 if x_start <= x_intersect <= x_end:
                     points.append((x_intersect, y_start))
                 # Perpotongan dengan y = y_end
                 x_intersect = C - y_end
                 if x_start <= x_intersect <= x_end:
                     points.append((x_intersect, y_end))

                 # Hapus duplikat dan pastikan ada dua titik
                 unique_points = []
                 for p in points:
                     if p not in unique_points:
                         unique_points.append(p)
                 
                 if len(unique_points) >= 2:
                     # Urutkan titik untuk memastikan garis digambar dengan benar
                     unique_points.sort() # Mengurutkan berdasarkan x lalu y
                     draw.line([unique_points[0], unique_points[1]], fill=color_to_use, width=line_thickness)


# --- Contoh Penggunaan ---
if __name__ == "__main__":
    # Pastikan direktori output ada
    if not os.path.exists("output"):
        os.makedirs("output")

    # Contoh 1: Pola seperti contoh gambar (4 kuadran dengan arah berbeda), warna pastel acak
    print("Membuat seamless_pattern_example.jpg...")
    generate_seamless_pattern(
        output_filename="seamless_pattern_example",
        palette_type="random_pastel",
        randomize_line_props_per_tile=True, # Properti garis diacak per kuadran
        randomize_tile_direction=False # Arah kuadran sudah ditentukan di dalam fungsi
    )

    # Contoh 2: Pola dengan warna pastel hijau
    print("Membuat seamless_pattern_green_pastel.jpg...")
    generate_seamless_pattern(
        output_filename="seamless_pattern_green_pastel",
        palette_type="green_pastel",
        randomize_line_props_per_tile=True,
        randomize_tile_direction=False
    )

    # Contoh 3: Pola dengan warna pastel ungu
    print("Membuat seamless_pattern_purple_pastel.jpg...")
    generate_seamless_pattern(
        output_filename="seamless_pattern_purple_pastel",
        palette_type="purple_pastel",
        randomize_line_props_per_tile=True,
        randomize_tile_direction=False
    )

    # Contoh 4: Pola dengan warna custom (misal, abu-abu muda, biru muda, pink muda)
    print("Membuat seamless_pattern_custom_colors.jpg...")
    generate_seamless_pattern(
        output_filename="seamless_pattern_custom_colors",
        palette_type="custom",
        custom_colors=[(230, 230, 230), (190, 220, 240), (240, 190, 220)],
        randomize_line_props_per_tile=True,
        randomize_tile_direction=False
    )

    # Catatan: Fungsi ini secara default membuat pola 4 kuadran seperti contoh Anda.
    # Jika Anda ingin pola yang benar-benar bisa diulang dari tile kecil,
    # logika di `generate_seamless_pattern` perlu diubah untuk memanggil
    # `create_seamless_diagonal_line_tile` dan menempelkannya secara berulang.
    # Namun, pola seperti contoh Anda (dengan perubahan arah di tengah)
    # secara teknis bukan "tile" yang bisa diulang tanpa jahitan jika tile_size kecil.
    # Solusinya adalah membuat 4 kuadran besar seperti yang saya implementasikan.