import streamlit as st
from PIL import Image, ImageDraw
import random
import io
import math

# --- Fungsi untuk Skema Warna Pastel ---
def get_pastel_color_scheme(name):
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
    colors = get_pastel_color_scheme(color_scheme_name)
    bg_color = colors[0] if colors else (255, 255, 255)
    dot_colors = colors[1:] if colors and len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    base_grid_size = random.randint(min(width, height) // 8, min(width, height) // 4)
    buffer = base_grid_size
    extended_width = width + buffer * 2
    extended_height = height + buffer * 2

    for x in range(-buffer, extended_width, base_grid_size):
        for y in range(-buffer, extended_height, base_grid_size):
            offset_x = random.randint(-base_grid_size // 5, base_grid_size // 5)
            offset_y = random.randint(-base_grid_size // 5, base_grid_size // 5)

            dot_center_x = x + offset_x
            dot_center_y = y + offset_y

            dot_size = random.randint(dot_size_range[0], dot_size_range[1])
            dot_radius = dot_size // 2
            dot_color = random.choice(dot_colors)

            for dx in [-width, 0, width]:
                for dy in [-height, 0, height]:
                    left = dot_center_x - dot_radius + dx
                    top = dot_center_y - dot_radius + dy
                    right = dot_center_x + dot_radius + dx
                    bottom = dot_center_y + dot_radius + dy
                    draw.ellipse((left, top, right, bottom), fill=dot_color)
    return img

# --- Fungsi untuk Menghasilkan Pola Garis-garis (Horizontal/Vertical) Seamless ---
def generate_seamless_stripes(width, height, dpi, orientation, stripe_thickness_range, gap_range, color_scheme_name):
    colors = get_pastel_color_scheme(color_scheme_name)
    bg_color = colors[0] if colors else (255, 255, 255)
    stripe_colors = colors[1:] if colors and len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    current_position = 0
    max_dimension = max(width, height) * 2

    while current_position < max_dimension:
        stripe_thickness = random.randint(stripe_thickness_range[0], stripe_thickness_range[1])
        gap = random.randint(gap_range[0], gap_range[1])

        available_stripe_colors = [c for c in stripe_colors if c != bg_color]
        stripe_color = random.choice(available_stripe_colors) if available_stripe_colors else (0, 0, 0)

        if orientation == 'horizontal':
            for dy_wrap in [-height, 0, height]:
                draw.rectangle((0, current_position + dy_wrap, width, current_position + stripe_thickness + dy_wrap), fill=stripe_color)
        else: # vertical
            for dx_wrap in [-width, 0, width]:
                draw.rectangle((current_position + dx_wrap, 0, current_position + stripe_thickness + dx_wrap, height), fill=stripe_color)

        current_position += stripe_thickness + gap
        if current_position > max_dimension + max(stripe_thickness_range) + max(gap_range):
            break
    return img

# --- Fungsi Baru: Menghasilkan Pola Segitiga Seamless ---
def generate_seamless_triangles(width, height, dpi, triangle_size_range, rotation_range, color_scheme_name):
    colors = get_pastel_color_scheme(color_scheme_name)
    bg_color = colors[0] if colors else (255, 255, 255)
    triangle_colors = colors[1:] if colors and len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Base grid size for triangle placement
    grid_spacing = random.randint(min(width, height) // 10, min(width, height) // 5)
    
    # Buffer for seamless drawing
    buffer = grid_spacing * 2
    extended_width = width + buffer * 2
    extended_height = height + buffer * 2

    for x_grid in range(-buffer, extended_width, grid_spacing):
        for y_grid in range(-buffer, extended_height, grid_spacing):
            # Apply random offset for more organic look
            offset_x = random.randint(-grid_spacing // 4, grid_spacing // 4)
            offset_y = random.randint(-grid_spacing // 4, grid_spacing // 4)
            
            center_x = x_grid + offset_x
            center_y = y_grid + offset_y

            triangle_side = random.randint(triangle_size_range[0], triangle_size_range[1])
            rotation_angle = random.randint(rotation_range[0], rotation_range[1]) # in degrees
            triangle_color = random.choice(triangle_colors)

            # Calculate triangle vertices from center
            # Start with an upright equilateral triangle
            h = triangle_side * math.sqrt(3) / 2 # height
            
            p1_base = (center_x, center_y - 2 * h / 3)
            p2_base = (center_x - triangle_side / 2, center_y + h / 3)
            p3_base = (center_x + triangle_side / 2, center_y + h / 3)

            # Rotate points
            points = [p1_base, p2_base, p3_base]
            rotated_points = []
            
            for px, py in points:
                # Translate point to origin
                temp_x = px - center_x
                temp_y = py - center_y

                # Rotate point
                rotated_x = temp_x * math.cos(math.radians(rotation_angle)) - temp_y * math.sin(math.radians(rotation_angle))
                rotated_y = temp_x * math.sin(math.radians(rotation_angle)) + temp_y * math.cos(math.radians(rotation_angle))

                # Translate point back
                rotated_points.append((rotated_x + center_x, rotated_y + center_y))

            # Draw the triangle and its wrapped counterparts
            for dx in [-width, 0, width]:
                for dy in [-height, 0, height]:
                    wrapped_points = [(p[0] + dx, p[1] + dy) for p in rotated_points]
                    draw.polygon(wrapped_points, fill=triangle_color)
    return img

# --- Fungsi Baru: Menghasilkan Pola Kotak/Wajik Seamless ---
def generate_seamless_squares(width, height, dpi, square_size_range, rotation_angle, color_scheme_name):
    colors = get_pastel_color_scheme(color_scheme_name)
    bg_color = colors[0] if colors else (255, 255, 255)
    square_colors = colors[1:] if colors and len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    grid_spacing = random.randint(min(width, height) // 10, min(width, height) // 5)
    
    buffer = grid_spacing * 2
    extended_width = width + buffer * 2
    extended_height = height + buffer * 2

    for x_grid in range(-buffer, extended_width, grid_spacing):
        for y_grid in range(-buffer, extended_height, grid_spacing):
            offset_x = random.randint(-grid_spacing // 4, grid_spacing // 4)
            offset_y = random.randint(-grid_spacing // 4, grid_spacing // 4)
            
            center_x = x_grid + offset_x
            center_y = y_grid + offset_y

            square_side = random.randint(square_size_range[0], square_size_range[1])
            
            # Vertices of an unrotated square centered at (0,0)
            half_side = square_side / 2
            p1_base = (-half_side, -half_side)
            p2_base = (half_side, -half_side)
            p3_base = (half_side, half_side)
            p4_base = (-half_side, half_side)

            points = [p1_base, p2_base, p3_base, p4_base]
            rotated_points = []
            
            for px, py in points:
                # Rotate around (center_x, center_y)
                rotated_x = px * math.cos(math.radians(rotation_angle)) - py * math.sin(math.radians(rotation_angle)) + center_x
                rotated_y = px * math.sin(math.radians(rotation_angle)) + py * math.cos(math.radians(rotation_angle)) + center_y
                rotated_points.append((rotated_x, rotated_y))

            square_color = random.choice(square_colors)

            # Draw the square and its wrapped counterparts
            for dx in [-width, 0, width]:
                for dy in [-height, 0, height]:
                    wrapped_points = [(p[0] + dx, p[1] + dy) for p in rotated_points]
                    draw.polygon(wrapped_points, fill=square_color)
    return img

# --- Fungsi Baru: Menghasilkan Pola Garis Diagonal Seamless ---
def generate_seamless_diagonal_stripes(width, height, dpi, stripe_thickness_range, gap_range, color_scheme_name, angle):
    colors = get_pastel_color_scheme(color_scheme_name)
    bg_color = colors[0] if colors else (255, 255, 255)
    stripe_colors = colors[1:] if colors and len(colors) > 1 else [(0, 0, 0)]

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Calculate the max length needed to cover the diagonal
    max_diag = math.sqrt(width**2 + height**2)
    
    current_offset = -max_diag # Start drawing far left/top to ensure coverage
    
    # Cosine and sine of the angle for rotation
    cos_angle = math.cos(math.radians(angle))
    sin_angle = math.sin(math.radians(angle))

    while current_offset < max_diag * 2: # Draw well beyond visible area
        stripe_thickness = random.randint(stripe_thickness_range[0], stripe_thickness_range[1])
        gap = random.randint(gap_range[0], gap_range[1])
        stripe_color = random.choice(stripe_colors)

        # Define points for a long rectangle covering the entire canvas when rotated
        # Base rectangle for a stripe, wider than diagonal to ensure coverage
        # Start X, Start Y, End X, End Y
        x0 = -max_diag
        y0 = current_offset
        x1 = max_diag * 2
        y1 = current_offset + stripe_thickness

        # Rotate the four corners around the center of the canvas (width/2, height/2)
        cx, cy = width / 2, height / 2

        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        rotated_corners = []

        for px, py in corners:
            temp_x = px - cx
            temp_y = py - cy
            
            rotated_x = temp_x * cos_angle - temp_y * sin_angle + cx
            rotated_y = temp_x * sin_angle + temp_y * cos_angle + cy
            rotated_corners.append((rotated_x, rotated_y))
        
        # Draw the rotated stripe. Need to account for seamlessness by drawing multiple copies
        # The rotation makes seamlessness complex. A common approach is to draw the pattern
        # on an image larger than the final canvas, and then crop it.
        # For simplicity in this direct drawing method, we rely on the large stripe to cover
        # enough area to appear seamless on a small tile, but for perfect seamlessness
        # with rotation, a different algorithm (e.g., drawing on 3x3 tiles and cropping the center)
        # would be more robust. For general patterns, this approach is usually sufficient.

        for dx in [-width, 0, width]:
            for dy in [-height, 0, height]:
                wrapped_points = [(p[0] + dx, p[1] + dy) for p in rotated_corners]
                draw.polygon(wrapped_points, fill=stripe_color)

        current_offset += stripe_thickness + gap
        if current_offset > max_diag * 2 + max(stripe_thickness_range) + max(gap_range):
            break
            
    return img


# --- Pengaturan Umum ---
CANVAS_WIDTH = 4000
CANVAS_HEIGHT = 4000
OUTPUT_DPI = 300

# Skema warna yang tersedia
COLOR_SCHEMES = {
    "Pastel Hijau": "pastel_green_mix",
    "Pastel Ungu": "pastel_purple_mix",
    "Pastel Biru": "pastel_blue_mix",
    "Pastel Pink": "pastel_pink_mix",
    "Multi-Pastel": "multi_pastel",
    "Netral/Earth Tones": "neutral_earth_tones"
}

# --- Antarmuka Pengguna Streamlit ---
st.set_page_config(
    page_title="Generator Pola Seamless",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Generator Pola Seamless (Seamless Pattern Generator)")
st.markdown("Buat pola *seamless* (mulus) geometris dengan kombinasi warna pastel yang menarik!")

# --- Sidebar untuk Pengaturan ---
st.sidebar.header("Pengaturan Pola")

selected_pattern_type = st.sidebar.selectbox(
    "Pilih Tipe Pola:",
    ("Polka Dot", "Garis-garis (Horizontal/Vertikal)", "Garis-garis (Diagonal)", "Segitiga", "Kotak/Wajik")
)

selected_color_scheme_name = st.sidebar.selectbox(
    "Pilih Skema Warna:",
    list(COLOR_SCHEMES.keys())
)
actual_color_scheme_key = COLOR_SCHEMES[selected_color_scheme_name]

# Pengaturan spesifik pola
if selected_pattern_type == "Polka Dot":
    st.sidebar.subheader("Pengaturan Polka Dot")
    dot_min_size = st.sidebar.slider("Ukuran Titik Minimum", 10, 300, 80, 10)
    dot_max_size = st.sidebar.slider("Ukuran Titik Maksimum", dot_min_size, 500, 200, 10)
    dot_size_range = (dot_min_size, dot_max_size)

elif selected_pattern_type == "Garis-garis (Horizontal/Vertikal)":
    st.sidebar.subheader("Pengaturan Garis-garis Horizontal/Vertikal")
    stripe_orientation = st.sidebar.radio("Orientasi Garis:", ("horizontal", "vertical"))
    stripe_min_thickness = st.sidebar.slider("Ketebalan Garis Minimum", 10, 500, 100, 10)
    stripe_max_thickness = st.sidebar.slider("Ketebalan Garis Maksimum", stripe_min_thickness, 800, 300, 10)
    stripe_thickness_range = (stripe_min_thickness, stripe_max_thickness)

    gap_min_size = st.sidebar.slider("Jarak Antar Garis Minimum", 5, 300, 50, 5)
    gap_max_size = st.sidebar.slider("Jarak Antar Garis Maksimum", gap_min_size, 500, 150, 5)
    gap_range = (gap_min_size, gap_max_size)

elif selected_pattern_type == "Garis-garis (Diagonal)":
    st.sidebar.subheader("Pengaturan Garis-garis Diagonal")
    diag_stripe_min_thickness = st.sidebar.slider("Ketebalan Garis Minimum", 10, 300, 80, 10)
    diag_stripe_max_thickness = st.sidebar.slider("Ketebalan Garis Maksimum", diag_stripe_min_thickness, 500, 200, 10)
    diag_stripe_thickness_range = (diag_stripe_min_thickness, diag_stripe_max_thickness)

    diag_gap_min_size = st.sidebar.slider("Jarak Antar Garis Minimum", 5, 200, 40, 5)
    diag_gap_max_size = st.sidebar.slider("Jarak Antar Garis Maksimum", diag_gap_min_size, 300, 100, 5)
    diag_gap_range = (diag_gap_min_size, diag_gap_max_size)
    
    diag_angle = st.sidebar.slider("Sudut Diagonal (derajat)", 1, 89, 45, 1) # 45 degrees is common

elif selected_pattern_type == "Segitiga":
    st.sidebar.subheader("Pengaturan Segitiga")
    triangle_min_size = st.sidebar.slider("Ukuran Sisi Minimum", 20, 400, 150, 10)
    triangle_max_size = st.sidebar.slider("Ukuran Sisi Maksimum", triangle_min_size, 600, 300, 10)
    triangle_size_range = (triangle_min_size, triangle_max_size)
    
    rotation_min_angle = st.sidebar.slider("Rotasi Minimum (derajat)", 0, 360, 0, 1)
    rotation_max_angle = st.sidebar.slider("Rotasi Maksimum (derajat)", rotation_min_angle, 360, 360, 1)
    rotation_range = (rotation_min_angle, rotation_max_angle)


elif selected_pattern_type == "Kotak/Wajik":
    st.sidebar.subheader("Pengaturan Kotak/Wajik")
    square_min_size = st.sidebar.slider("Ukuran Sisi Minimum", 20, 400, 150, 10)
    square_max_size = st.sidebar.slider("Ukuran Sisi Maksimum", square_min_size, 600, 300, 10)
    square_size_range = (square_min_size, square_max_size)
    
    # Rotation for squares to make diamonds
    square_rotation_angle = st.sidebar.slider("Rotasi Kotak (derajat, 45 untuk Wajik)", 0, 90, 0, 1) # Often 0 or 45


# Tombol Generate
if st.sidebar.button("Generate Pola", key="generate_button"):
    with st.spinner("Menggenerasi pola, mohon tunggu..."):
        generated_image = None
        filename = "pattern.jpg" # Default filename

        if selected_pattern_type == "Polka Dot":
            generated_image = generate_seamless_polka_dot(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                dot_size_range, actual_color_scheme_key
            )
            filename = f"polka_dot_{actual_color_scheme_key}.jpg"
        elif selected_pattern_type == "Garis-garis (Horizontal/Vertikal)":
            generated_image = generate_seamless_stripes(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                stripe_orientation, stripe_thickness_range, gap_range, actual_color_scheme_key
            )
            filename = f"stripes_{stripe_orientation}_{actual_color_scheme_key}.jpg"
        elif selected_pattern_type == "Garis-garis (Diagonal)":
            generated_image = generate_seamless_diagonal_stripes(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                diag_stripe_thickness_range, diag_gap_range, actual_color_scheme_key, diag_angle
            )
            filename = f"stripes_diagonal_{diag_angle}deg_{actual_color_scheme_key}.jpg"
        elif selected_pattern_type == "Segitiga":
            generated_image = generate_seamless_triangles(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                triangle_size_range, rotation_range, actual_color_scheme_key
            )
            filename = f"triangles_{actual_color_scheme_key}.jpg"
        elif selected_pattern_type == "Kotak/Wajik":
            generated_image = generate_seamless_squares(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                square_size_range, square_rotation_angle, actual_color_scheme_key
            )
            filename = f"squares_{square_rotation_angle}deg_{actual_color_scheme_key}.jpg"


        if generated_image:
            st.session_state['generated_image'] = generated_image
            st.session_state['filename'] = filename
            st.success("Pola berhasil digenerasi!")
        else:
            st.error("Gagal menggenerasi pola. Silakan coba lagi.")


# Tampilkan dan unduh gambar jika sudah digenerasi
if 'generated_image' in st.session_state and st.session_state['generated_image'] is not None:
    st.subheader("Pola yang Dihasilkan:")
    st.image(st.session_state['generated_image'], caption="Pola Seamless Anda", use_column_width=True)

    # Persiapan untuk tombol download
    buf = io.BytesIO()
    st.session_state['generated_image'].save(buf, format="JPEG", dpi=(OUTPUT_DPI, OUTPUT_DPI), quality=95)
    byte_im = buf.getvalue()

    # Tombol Download
    st.download_button(
        label="Download Pola",
        data=byte_im,
        file_name=st.session_state['filename'],
        mime="image/jpeg",
        key="download_button"
    )

st.markdown("---")
st.info(f"Ukuran kanvas output: {CANVAS_WIDTH}x{CANVAS_HEIGHT} piksel dengan {OUTPUT_DPI} DPI.")