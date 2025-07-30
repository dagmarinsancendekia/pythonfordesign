import streamlit as st
from PIL import Image, ImageDraw
import random
import io
import base64 # Untuk mengaktifkan fitur download

# --- Fungsi untuk Skema Warna Pastel (sama seperti sebelumnya) ---
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

# --- Fungsi untuk Menghasilkan Pola Garis-garis (Stripes) Seamless ---
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

selected_pattern_type = st.sidebar.radio(
    "Pilih Tipe Pola:",
    ("Polka Dot", "Garis-garis")
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

elif selected_pattern_type == "Garis-garis":
    st.sidebar.subheader("Pengaturan Garis-garis")
    stripe_orientation = st.sidebar.radio("Orientasi Garis:", ("horizontal", "vertical"))
    stripe_min_thickness = st.sidebar.slider("Ketebalan Garis Minimum", 10, 500, 100, 10)
    stripe_max_thickness = st.sidebar.slider("Ketebalan Garis Maksimum", stripe_min_thickness, 800, 300, 10)
    stripe_thickness_range = (stripe_min_thickness, stripe_max_thickness)

    gap_min_size = st.sidebar.slider("Jarak Antar Garis Minimum", 5, 300, 50, 5)
    gap_max_size = st.sidebar.slider("Jarak Antar Garis Maksimum", gap_min_size, 500, 150, 5)
    gap_range = (gap_min_size, gap_max_size)

# Tombol Generate
if st.sidebar.button("Generate Pola"):
    with st.spinner("Menggenerasi pola, mohon tunggu..."):
        if selected_pattern_type == "Polka Dot":
            generated_image = generate_seamless_polka_dot(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                dot_size_range, actual_color_scheme_key
            )
            filename = f"polka_dot_{actual_color_scheme_key}.jpg"
        else: # Garis-garis
            generated_image = generate_seamless_stripes(
                CANVAS_WIDTH, CANVAS_HEIGHT, OUTPUT_DPI,
                stripe_orientation, stripe_thickness_range, gap_range, actual_color_scheme_key
            )
            filename = f"stripes_{stripe_orientation}_{actual_color_scheme_key}.jpg"

        st.session_state['generated_image'] = generated_image
        st.session_state['filename'] = filename
        st.success("Pola berhasil digenerasi!")

# Tampilkan dan unduh gambar jika sudah digenerasi
if 'generated_image' in st.session_state:
    st.subheader("Pola yang Dihasilkan:")
    st.image(st.session_state['generated_image'], caption="Pola Seamless Anda", use_column_width=True)

    # Persiapan untuk tombol download
    # Mengubah gambar PIL menjadi byte agar bisa diunduh
    buf = io.BytesIO()
    st.session_state['generated_image'].save(buf, format="JPEG", dpi=(OUTPUT_DPI, OUTPUT_DPI), quality=95)
    byte_im = buf.getvalue()

    # Tombol Download
    st.download_button(
        label="Download Pola",
        data=byte_im,
        file_name=st.session_state['filename'],
        mime="image/jpeg"
    )

st.markdown("---")
st.info("Catatan: Ukuran kanvas output adalah 4000x4000 piksel dengan 300 DPI.")