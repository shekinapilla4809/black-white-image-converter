
import io
import zipfile
from pathlib import Path

import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Mono Studio | Black & White Converter",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# 2. SESSION STATE
# =========================================================
DEFAULTS = {
    "app_theme": "Light",
    "bw_intensity": 100,
    "brightness": 100,
    "contrast": 110,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 3. THEME COLORS
# =========================================================
DARK = {
    "bg": "#0E1117",
    "surface": "#171B24",
    "surface2": "#202633",
    "text": "#F4F6FA",
    "muted": "#A5ADBB",
    "border": "#303746",
    "accent": "#C5F477",
    "accent_text": "#17200B",
    "shadow": "rgba(0,0,0,0.18)",
}

LIGHT = {
    "bg": "#F5F7FB",
    "surface": "#FFFFFF",
    "surface2": "#F0F3F8",
    "text": "#1B2432",
    "muted": "#626F82",
    "border": "#DDE3ED",
    "accent": "#355F16",
    "accent_text": "#FFFFFF",
    "shadow": "rgba(28,39,60,0.06)",
}

C = DARK if st.session_state.app_theme == "Dark" else LIGHT


# =========================================================
# 4. USER-FRIENDLY RESPONSIVE CSS
# =========================================================
st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: {"dark" if st.session_state.app_theme == "Dark" else "light"};
    }}

    .stApp {{
        background: {C["bg"]};
        color: {C["text"]};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1250px;
        padding: 1.2rem 1.5rem 3rem;
    }}

    h1, h2, h3, h4, p, label,
    [data-testid="stMarkdownContainer"] {{
        color: {C["text"]};
    }}

    [data-testid="stSidebar"] {{
        background: {C["surface"]};
    }}

    .brand {{
        font-size: 15px;
        font-weight: 850;
        letter-spacing: 1.5px;
        color: {C["text"]};
        padding-top: 9px;
    }}

    .brand-mark {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 10px;
        margin-right: 8px;
        background: {C["accent"]};
        color: {C["accent_text"]};
        font-size: 19px;
    }}

    .hero {{
        padding: 30px;
        margin: 14px 0 25px;
        border-radius: 23px;
        border: 1px solid {C["border"]};
        background:
            radial-gradient(
                circle at 92% 8%,
                {"rgba(197,244,119,0.13)" if st.session_state.app_theme == "Dark" else "rgba(53,95,22,0.08)"},
                transparent 36%
            ),
            {C["surface"]};
        box-shadow: 0 8px 28px {C["shadow"]};
    }}

    .hero-kicker {{
        color: {C["accent"]};
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}

    .hero h1 {{
        font-size: clamp(31px, 4.5vw, 49px);
        font-weight: 850;
        line-height: 1.1;
        letter-spacing: -1.8px;
        margin: 0;
        color: {C["text"]};
    }}

    .hero h1 span {{
        color: {C["accent"]};
    }}

    .hero p {{
        color: {C["muted"]};
        font-size: 15px;
        line-height: 1.75;
        max-width: 660px;
        margin-top: 13px;
        margin-bottom: 0;
    }}

    .section-title {{
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 12px 0 3px;
        color: {C["text"]};
    }}

    .section-help {{
        font-size: 13px;
        line-height: 1.65;
        color: {C["muted"]};
        margin-bottom: 14px;
    }}

    .step {{
        color: {C["accent"]};
        font-size: 11px;
        letter-spacing: 1.5px;
        font-weight: 850;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}

    .surface-card {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 17px;
        padding: 18px;
        margin-bottom: 14px;
    }}

    .hint-card {{
        background: {C["surface2"]};
        color: {C["muted"]};
        border: 1px solid {C["border"]};
        border-radius: 13px;
        padding: 13px 15px;
        font-size: 13px;
        line-height: 1.7;
    }}

    .hint-card strong {{
        color: {C["text"]};
    }}

    .upload-title {{
        color: {C["text"]};
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 5px;
    }}

    .upload-help {{
        color: {C["muted"]};
        font-size: 13px;
        line-height: 1.7;
    }}

    .preview-heading {{
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.4px;
        color: {C["text"]};
        margin: 8px 0;
    }}

    .preview-tag {{
        display: inline-block;
        border: 1px solid {C["border"]};
        background: {C["surface2"]};
        color: {C["muted"]};
        border-radius: 7px;
        padding: 5px 9px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 8px;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        min-height: 44px;
        border-radius: 11px;
        font-weight: 750;
        border: 1px solid {C["border"]};
        transition: border-color .15s ease, transform .15s ease;
    }}

    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {{
        background: {C["accent"]};
        color: {C["accent_text"]};
        border-color: {C["accent"]};
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        border-color: {C["accent"]};
        transform: translateY(-1px);
    }}

    [data-testid="stFileUploader"] {{
        background: {C["surface"]};
        border: 1.5px dashed {C["accent"]};
        border-radius: 15px;
        padding: 9px;
    }}

    [data-testid="stFileUploader"] section {{
        background: transparent;
    }}

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span {{
        color: {C["muted"]};
    }}

    [data-testid="stFileUploader"] button {{
        border-radius: 9px;
    }}

    [data-testid="stImage"] img {{
        border-radius: 12px;
    }}

    [data-testid="stMetric"] {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 13px;
        padding: 13px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {C["muted"]};
    }}

    [data-testid="stSlider"] {{
        padding-bottom: 5px;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    [data-testid="stExpander"] {{
        border-color: {C["border"]};
        border-radius: 12px;
    }}

    .footer {{
        text-align: center;
        padding-top: 20px;
        margin-top: 35px;
        border-top: 1px solid {C["border"]};
        color: {C["muted"]};
        font-size: 12px;
        line-height: 1.9;
    }}

    @media (max-width: 700px) {{
        [data-testid="stMainBlockContainer"] {{
            padding: 0.7rem 0.8rem 2rem;
        }}

        .hero {{
            padding: 22px 18px;
            border-radius: 17px;
        }}

        .hero h1 {{
            letter-spacing: -1px;
        }}

        .surface-card {{
            padding: 14px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 5. IMAGE PROCESSING HELPERS
# =========================================================
SUPPORTED_TYPES = [
    "png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"
]


def load_image(uploaded_file):
    """Load an image and apply its EXIF orientation."""
    uploaded_file.seek(0)

    with Image.open(uploaded_file) as opened:
        image = ImageOps.exif_transpose(opened)
        image.load()

        if (
            "A" in image.getbands()
            or (
                image.mode == "P"
                and "transparency" in image.info
            )
        ):
            return image.convert("RGBA")

        return image.convert("RGB")


def convert_to_bw(image, intensity, brightness, contrast):
    """Apply grayscale intensity, brightness, and contrast."""
    has_alpha = image.mode == "RGBA"

    if has_alpha:
        alpha = image.getchannel("A")
        rgb = image.convert("RGB")
    else:
        alpha = None
        rgb = image.convert("RGB")

    grayscale = ImageOps.grayscale(rgb).convert("RGB")
    blend_amount = max(0, min(100, int(intensity))) / 100.0

    result = Image.blend(rgb, grayscale, blend_amount)

    if brightness != 100:
        result = ImageEnhance.Brightness(result).enhance(
            brightness / 100.0
        )

    if contrast != 100:
        result = ImageEnhance.Contrast(result).enhance(
            contrast / 100.0
        )

    if alpha is not None:
        result.putalpha(alpha)

    return result


def image_to_bytes(image, output_format):
    """Encode an image in PNG or JPEG format."""
    buffer = io.BytesIO()

    if output_format == "JPEG":
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(
                image,
                mask=image.getchannel("A"),
            )
            image = background
        else:
            image = image.convert("RGB")

        image.save(
            buffer,
            format="JPEG",
            quality=95,
            optimize=True,
        )
    else:
        image.save(
            buffer,
            format="PNG",
            optimize=True,
        )

    return buffer.getvalue()


def safe_stem(filename):
    stem = Path(filename).stem

    cleaned = "".join(
        char if char.isalnum() or char in ("-", "_") else "_"
        for char in stem
    ).strip("_")

    return cleaned or "image"


def make_unique_name(filename, used_names):
    """Prevent duplicate filenames in batch ZIP downloads."""
    path = Path(filename)
    base = path.stem
    suffix = path.suffix
    candidate = filename
    counter = 2

    while candidate.lower() in used_names:
        candidate = f"{base}_{counter}{suffix}"
        counter += 1

    used_names.add(candidate.lower())
    return candidate


def make_zip(items):
    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for filename, data in items:
            archive.writestr(filename, data)

    return buffer.getvalue()


def human_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.2f} MB"


# =========================================================
# 6. HEADER + THEME SELECTOR
# =========================================================
header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">◐</span> MONO STUDIO
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    selected_theme = st.selectbox(
        "Theme",
        options=["Light", "Dark"],
        index=0 if st.session_state.app_theme == "Light" else 1,
        key="theme_picker",
        label_visibility="collapsed",
    )

    if selected_theme != st.session_state.app_theme:
        st.session_state.app_theme = selected_theme
        st.rerun()


# =========================================================
# 7. HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">YOUR SIMPLE PHOTO WORKSPACE</div>
        <h1>Make every photo<br><span>timeless in black & white.</span></h1>
        <p>
            Upload your pictures, fine-tune the look, compare the result,
            and download your finished images. No complicated editing skills needed.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 8. UPLOAD
# =========================================================
st.markdown(
    '<div class="step">STEP 1 OF 3</div>'
    '<div class="section-title">Upload your photos</div>'
    '<div class="section-help">Start with one photo or select multiple images at once.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="surface-card">
        <div class="upload-title">Choose images to get started</div>
        <div class="upload-help">
            Drag and drop your images into the upload area below,
            or click Browse files.<br>
            Supported formats: PNG, JPG, WEBP, BMP and TIFF.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploads = st.file_uploader(
    "Browse or drag images here",
    type=SUPPORTED_TYPES,
    accept_multiple_files=True,
    key="image_uploads",
    help="You can select multiple image files.",
)

if not uploads:
    st.markdown(
        """
        <div class="hint-card">
            <strong>How it works</strong><br>
            1. Upload your images.<br>
            2. Adjust black & white intensity, brightness and contrast.<br>
            3. Compare your photo and download the result.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer">
            <b>MONO STUDIO</b><br>
            Simple photo editing, with a timeless monochrome finish.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# =========================================================
# 9. ADJUSTMENTS
# Reset button comes BEFORE the keyed sliders so state resets safely.
# =========================================================
st.markdown("---")

st.markdown(
    '<div class="step">STEP 2 OF 3</div>'
    '<div class="section-title">Adjust your image</div>'
    '<div class="section-help">Move the sliders and preview the result below. Changes apply to all uploaded photos.</div>',
    unsafe_allow_html=True,
)

reset_col, format_col = st.columns([1, 2])

with reset_col:
    if st.button(
        "↺ Reset settings",
        use_container_width=True,
        help="Restore the default adjustment values.",
    ):
        st.session_state["bw_intensity"] = 100
        st.session_state["brightness"] = 100
        st.session_state["contrast"] = 110
        st.rerun()

with format_col:
    output_format = st.selectbox(
        "Download format",
        options=["PNG", "JPEG"],
        help="PNG keeps transparent backgrounds. JPEG uses a white background for transparent areas.",
    )

settings_col, guide_col = st.columns([1.6, 1], gap="large")

with settings_col:
    with st.container(border=True):
        st.markdown("#### Black & white intensity")
        bw_intensity = st.slider(
            "Color to monochrome",
            min_value=0,
            max_value=100,
            value=st.session_state.bw_intensity,
            step=5,
            key="bw_intensity",
            help="0% keeps the original colors. 100% makes the image fully grayscale.",
        )

        st.caption(
            "0% = Original color     ·     100% = Full black & white"
        )

        st.markdown("#### Brightness")
        brightness = st.slider(
            "Light or dark",
            min_value=25,
            max_value=200,
            value=st.session_state.brightness,
            step=5,
            key="brightness",
            help="100% means the original brightness.",
        )

        st.markdown("#### Contrast")
        contrast = st.slider(
            "Soft or bold",
            min_value=25,
            max_value=200,
            value=st.session_state.contrast,
            step=5,
            key="contrast",
            help="100% means the original contrast.",
        )

with guide_col:
    st.markdown(
        f"""
        <div class="surface-card">
            <div class="step">YOUR CURRENT LOOK</div>
            <div style="font-size:27px;font-weight:850;color:{C["text"]};margin:8px 0">
                {bw_intensity}%
            </div>
            <div style="color:{C["muted"]};font-size:13px">
                Black & white intensity
            </div>
            <hr style="border:0;border-top:1px solid {C["border"]};margin:17px 0">
            <div style="font-size:14px;color:{C["text"]};margin-bottom:9px">
                <b>Brightness</b>
                <span style="float:right">{brightness}%</span>
            </div>
            <div style="font-size:14px;color:{C["text"]}">
                <b>Contrast</b>
                <span style="float:right">{contrast}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hint-card">
            <strong>Need a starting point?</strong><br>
            Try 100% intensity, 100% brightness and 110% contrast
            for a classic black & white appearance.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 10. PROCESS ALL UPLOADED IMAGES
# =========================================================
st.markdown("---")

st.markdown(
    '<div class="step">STEP 3 OF 3</div>'
    '<div class="section-title">Preview your results</div>'
    '<div class="section-help">Compare the original with the edited image before downloading.</div>',
    unsafe_allow_html=True,
)

converted_items = []
preview_records = []
failed_items = []
used_names = set()

progress = st.progress(0, text="Preparing your images...")

for index, uploaded in enumerate(uploads):
    try:
        original = load_image(uploaded)

        converted = convert_to_bw(
            original,
            intensity=bw_intensity,
            brightness=brightness,
            contrast=contrast,
        )

        output_data = image_to_bytes(
            converted,
            output_format,
        )

        extension = "jpg" if output_format == "JPEG" else "png"

        proposed_name = (
            f"{safe_stem(uploaded.name)}_black_white.{extension}"
        )
        output_name = make_unique_name(proposed_name, used_names)

        item = {
            "name": uploaded.name,
            "original": original,
            "converted": converted,
            "output": output_data,
            "output_name": output_name,
            "size": original.size,
            "input_size": uploaded.size,
        }

        preview_records.append(item)
        converted_items.append((output_name, output_data))

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
    ) as exc:
        failed_items.append((uploaded.name, str(exc)))

    progress.progress(
        (index + 1) / len(uploads),
        text=f"Processing image {index + 1} of {len(uploads)}...",
    )

progress.empty()


if failed_items:
    st.warning(
        f"{len(failed_items)} image(s) could not be processed. "
        "You can still download the successfully converted images."
    )

    with st.expander("See files that could not be processed"):
        for filename, error in failed_items:
            st.write(f"**{filename}**")
            st.caption(error)


if not preview_records:
    st.error("No images could be converted. Please upload valid image files.")
    st.stop()


# =========================================================
# 11. SIMPLE SUMMARY
# =========================================================
metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Images uploaded", len(uploads))

with metric2:
    st.metric("Ready to download", len(converted_items))

with metric3:
    total_size = sum(len(data) for _, data in converted_items)
    st.metric("Total output size", human_size(total_size))


# =========================================================
# 12. BEFORE / AFTER COMPARISON
# =========================================================
st.markdown("### Compare your photo")

if len(preview_records) > 1:
    selected_name = st.selectbox(
        "Choose which photo to preview",
        options=[item["name"] for item in preview_records],
        key="preview_choice",
    )

    record = next(
        item for item in preview_records
        if item["name"] == selected_name
    )
else:
    record = preview_records[0]

st.caption(
    f'{record["name"]}  ·  '
    f'{record["size"][0]} × {record["size"][1]} pixels'
)

before_col, after_col = st.columns(2, gap="medium")

with before_col:
    st.markdown(
        '<div class="preview-tag">BEFORE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="preview-heading">Original photo</div>',
        unsafe_allow_html=True,
    )
    st.image(
        record["original"],
        use_container_width=True,
    )

with after_col:
    st.markdown(
        '<div class="preview-tag">AFTER</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="preview-heading">Black & white result</div>',
        unsafe_allow_html=True,
    )
    st.image(
        record["converted"],
        use_container_width=True,
    )


# =========================================================
# 13. DOWNLOAD THE SELECTED PREVIEW
# =========================================================
st.markdown("---")
st.markdown("### Download your edited photo")

st.markdown(
    f"""
    <div class="hint-card">
        <strong>{record["output_name"]}</strong><br>
        {record["size"][0]} × {record["size"][1]} pixels
        &nbsp; · &nbsp; {human_size(len(record["output"]))}<br>
        Your edited image is ready.
    </div>
    """,
    unsafe_allow_html=True,
)

st.download_button(
    label="⬇  Download edited photo",
    data=record["output"],
    file_name=record["output_name"],
    mime="image/png" if output_format == "PNG" else "image/jpeg",
    type="primary",
    use_container_width=True,
    key="download_selected",
)


# =========================================================
# 14. BATCH DOWNLOAD
# =========================================================
if len(converted_items) > 1:
    st.markdown("---")
    st.markdown("### Download all photos")

    st.markdown(
        f"""
        <div class="surface-card">
            <div style="font-size:17px;font-weight:800;color:{C["text"]}">
                Your batch is ready
            </div>
            <div style="font-size:13px;line-height:1.7;color:{C["muted"]};margin-top:6px">
                Download all {len(converted_items)} converted photos together
                in one ZIP file, or download individual images below.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    zip_data = make_zip(converted_items)

    st.download_button(
        label=f"⬇  Download all {len(converted_items)} photos (ZIP)",
        data=zip_data,
        file_name="mono_studio_black_white_images.zip",
        mime="application/zip",
        type="primary",
        use_container_width=True,
        key="download_batch_zip",
    )

    with st.expander("View and download individual images"):
        for item in preview_records:
            file_col, button_col = st.columns([2, 1])

            with file_col:
                st.write(f"**{item['output_name']}**")
                st.caption(human_size(len(item["output"])))

            with button_col:
                st.download_button(
                    label="Download",
                    data=item["output"],
                    file_name=item["output_name"],
                    mime=(
                        "image/png"
                        if output_format == "PNG"
                        else "image/jpeg"
                    ),
                    key=f"individual_{item['output_name']}",
                    use_container_width=True,
                )


# =========================================================
# 15. FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        <b>◐ MONO STUDIO</b><br>
        Simple editing. Timeless results.<br>
        Built with Streamlit and Pillow.
    </div>
    """,
    unsafe_allow_html=True,
)
