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
    "app_theme": "Dark",
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
    "bg": "#0D1117",
    "surface": "#151B24",
    "surface2": "#1D2633",
    "text": "#F3F6FC",
    "muted": "#AAB5C5",
    "border": "#303B4B",
    "accent": "#C5F477",
    "accent_text": "#15200A",
    "shadow": "rgba(0,0,0,0.20)",
}

LIGHT = {
    "bg": "#F4F6FA",
    "surface": "#FFFFFF",
    "surface2": "#EEF2F7",
    "text": "#182230",
    "muted": "#59677A",
    "border": "#DCE3ED",
    "accent": "#355F16",
    "accent_text": "#FFFFFF",
    "shadow": "rgba(28,39,60,0.07)",
}

C = DARK if st.session_state.app_theme == "Dark" else LIGHT
IS_DARK = st.session_state.app_theme == "Dark"
GLOW = "rgba(197,244,119,0.12)" if IS_DARK else "rgba(53,95,22,0.07)"


# =========================================================
# 4. RESPONSIVE STYLING
# =========================================================
st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: {"dark" if IS_DARK else "light"};
    }}

    .stApp {{
        background: {C["bg"]};
        color: {C["text"]};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1220px;
        padding: 1.1rem 1.45rem 3rem;
    }}

    [data-testid="stSidebar"] {{
        background: {C["surface"]};
    }}

    h1, h2, h3, h4, p, label,
    [data-testid="stMarkdownContainer"],
    [data-testid="stCaptionContainer"] {{
        color: {C["text"]};
    }}

    [data-testid="stCaptionContainer"] p,
    .muted {{
        color: {C["muted"]} !important;
    }}

    .topbar {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 14px;
    }}

    .brand-mark {{
        display: inline-flex;
        width: 35px;
        height: 35px;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background: {C["accent"]};
        color: {C["accent_text"]};
        font-size: 21px;
        font-weight: 900;
    }}

    .brand-name {{
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 1.35px;
        color: {C["text"]};
    }}

    .brand-subtitle {{
        color: {C["muted"]};
        font-size: 11px;
        margin-top: 1px;
    }}

    .hero {{
        padding: clamp(22px, 4vw, 38px);
        margin: 7px 0 27px;
        border: 1px solid {C["border"]};
        border-radius: 23px;
        background:
            radial-gradient(circle at 90% 12%, {GLOW}, transparent 34%),
            {C["surface"]};
        box-shadow: 0 10px 34px {C["shadow"]};
        overflow: hidden;
    }}

    .hero-kicker {{
        color: {C["accent"]};
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}

    .hero h1 {{
        color: {C["text"]};
        font-size: clamp(30px, 4.4vw, 48px);
        font-weight: 900;
        letter-spacing: -1.7px;
        line-height: 1.12;
        margin: 0;
    }}

    .hero h1 span {{
        color: {C["accent"]};
    }}

    .hero p {{
        max-width: 680px;
        margin: 14px 0 0;
        color: {C["muted"]};
        font-size: 15px;
        line-height: 1.75;
    }}

    .feature-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 20px;
    }}

    .feature-pill {{
        border: 1px solid {C["border"]};
        background: {C["surface2"]};
        color: {C["text"]};
        border-radius: 999px;
        padding: 7px 11px;
        font-size: 12px;
        font-weight: 700;
    }}

    .step-label {{
        color: {C["accent"]};
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}

    .section-title {{
        font-size: 23px;
        font-weight: 850;
        letter-spacing: -0.6px;
        color: {C["text"]};
        margin: 0 0 4px;
    }}

    .section-help {{
        color: {C["muted"]};
        font-size: 13px;
        line-height: 1.65;
        margin-bottom: 16px;
    }}

    .soft-card {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 12px;
        padding: 9px 11px;
        margin-bottom: 8px;
    }}

    .soft-card-title {{
        font-size: 14px;
        font-weight: 800;
        color: {C["text"]};
        margin-bottom: 3px;
    }}

    .soft-card-copy {{
        color: {C["muted"]};
        font-size: 12px;
        line-height: 1.5;
    }}

    .info-box {{
        border: 1px solid {C["border"]};
        background: {C["surface2"]};
        color: {C["muted"]};
        border-radius: 10px;
        padding: 8px 10px;
        font-size: 12px;
        line-height: 1.5;
    }}

    .info-box strong {{
        color: {C["text"]};
    }}

    .preview-tag {{
        display: inline-block;
        border: 1px solid {C["border"]};
        background: {C["surface2"]};
        color: {C["muted"]};
        border-radius: 7px;
        padding: 5px 9px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 5px 0 8px;
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
        padding: 10px;
    }}

    [data-testid="stFileUploader"] section {{
        background: transparent;
    }}

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {{
        color: {C["text"]} !important;
    }}

    [data-testid="stFileUploader"] button {{
        border-radius: 9px;
        color: {C["text"]} !important;
        border-color: {C["border"]} !important;
    }}

    [data-testid="stFileUploader"] button:hover {{
        border-color: {C["accent"]} !important;
    }}

    [data-testid="stImage"] img {{
        border-radius: 10px;
        max-height: 340px;
        object-fit: contain;
    }}

    /* Keep Step 3 previews compact; downloads retain original pixel dimensions. */
    [data-testid="stImage"] {{
        margin-bottom: 0.25rem;
    }}

    [data-testid="stMetric"] {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 13px;
        padding: 13px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {C["muted"]} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {C["text"]} !important;
    }}

    /* Compact Step 2 adjustment panel without changing controls or processing. */
    [data-testid="stVerticalBlockBorderWrapper"] > div {{
        padding: 0.45rem 0.6rem !important;
        border-radius: 12px !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stVerticalBlockBorderWrapper"] h4 {{
        font-size: 0.95rem !important;
        margin: 0.15rem 0 0.25rem !important;
        line-height: 1.3 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p {{
        margin-bottom: 0.25rem !important;
    }}

    [data-testid="stSlider"] {{
        padding-bottom: 0 !important;
        margin-bottom: 0 !important;
    }}

    [data-testid="stSlider"] [data-testid="stSliderTrack"] {{
        margin-top: 0.2rem;
    }}

    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label {{
        color: {C["text"]} !important;
        font-weight: 650;
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
        padding-top: 22px;
        margin-top: 35px;
        border-top: 1px solid {C["border"]};
        color: {C["muted"]};
        font-size: 12px;
        line-height: 1.9;
    }}

    @media (max-width: 700px) {{
        [data-testid="stMainBlockContainer"] {{
            padding: 0.65rem 0.8rem 2rem;
        }}
        .hero {{
            padding: 22px 18px;
            border-radius: 17px;
        }}
        .hero h1 {{
            letter-spacing: -0.9px;
        }}
        .soft-card {{
            padding: 8px 10px;
            margin-bottom: 8px;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div {{
            padding: 0.35rem 0.45rem !important;
        }}
        [data-testid="stImage"] img {{
            max-height: 260px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 5. IMAGE PROCESSING HELPERS
# =========================================================
SUPPORTED_TYPES = ["png", "jpg", "jpeg", "webp", "bmp", "tif", "tiff"]


def load_image(uploaded_file):
    """Load an image and apply its EXIF orientation."""
    uploaded_file.seek(0)
    with Image.open(uploaded_file) as opened:
        image = ImageOps.exif_transpose(opened)
        image.load()

        if (
            "A" in image.getbands()
            or (image.mode == "P" and "transparency" in image.info)
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
        result = ImageEnhance.Brightness(result).enhance(brightness / 100.0)

    if contrast != 100:
        result = ImageEnhance.Contrast(result).enhance(contrast / 100.0)

    if alpha is not None:
        result.putalpha(alpha)
    return result


def image_to_bytes(image, output_format):
    """Encode an image as PNG or JPEG."""
    buffer = io.BytesIO()

    if output_format == "JPEG":
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

        image.save(buffer, format="JPEG", quality=95, optimize=True)
    else:
        image.save(buffer, format="PNG", optimize=True)

    return buffer.getvalue()


def safe_stem(filename):
    stem = Path(filename).stem
    cleaned = "".join(
        char if char.isalnum() or char in ("-", "_") else "_"
        for char in stem
    ).strip("_")
    return cleaned or "image"


def make_unique_name(filename, used_names):
    """Prevent duplicate filenames in ZIP downloads."""
    path = Path(filename)
    base, suffix = path.stem, path.suffix
    candidate = filename
    counter = 2

    while candidate.lower() in used_names:
        candidate = f"{base}_{counter}{suffix}"
        counter += 1

    used_names.add(candidate.lower())
    return candidate


def make_zip(items):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
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
# 6. TOP BAR + THEME SELECTOR
# =========================================================
brand_col, theme_col = st.columns([4, 1])

with brand_col:
    st.markdown(
        """
        <div class="topbar">
            <span class="brand-mark">◐</span>
            <div>
                <div class="brand-name">MONO STUDIO</div>
                <div class="brand-subtitle">BLACK & WHITE PHOTO WORKSPACE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with theme_col:
    selected_theme = st.selectbox(
        "Choose theme",
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
            Bring out the character in your photos. Upload images, fine-tune
            the look, compare the original with your edit, and download your
            finished work — all in one simple workspace.
        </p>
        <div class="feature-row">
            <span class="feature-pill">✦ Easy adjustments</span>
            <span class="feature-pill">◫ Before / after</span>
            <span class="feature-pill">⇩ Individual & ZIP downloads</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 8. UPLOAD
# =========================================================
st.markdown(
    """
    <div class="step-label">STEP 1 · UPLOAD</div>
    <div class="section-title">Start with your photos</div>
    <div class="section-help">
        Choose one image or select multiple photos to edit together.
        Supported formats: PNG, JPG, WEBP, BMP and TIFF.
    </div>
    """,
    unsafe_allow_html=True,
)

uploads = st.file_uploader(
    "Drag images here or browse files",
    type=SUPPORTED_TYPES,
    accept_multiple_files=True,
    key="image_uploads",
    help="You can select more than one image.",
)

if not uploads:
    st.markdown(
        """
        <div class="info-box">
            <strong>Quick guide</strong><br>
            1. Upload your photos.<br>
            2. Adjust black & white intensity, brightness and contrast.<br>
            3. Compare the result and download your edited images.
        </div>
        """,
        unsafe_allow_html=True,
    )
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
    st.stop()


# =========================================================
# 9. ADJUSTMENTS
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div class="step-label">STEP 2 · CUSTOMIZE</div>
    <div class="section-title">Make it your own</div>
    <div class="section-help">
        These settings are applied to every uploaded photo. Try the sliders
        and review the preview below before downloading.
    </div>
    """,
    unsafe_allow_html=True,
)

reset_col, format_col = st.columns([1, 2])

with reset_col:
    if st.button("↺ Reset adjustments", use_container_width=True):
        st.session_state["bw_intensity"] = 100
        st.session_state["brightness"] = 100
        st.session_state["contrast"] = 110
        st.rerun()

with format_col:
    output_format = st.selectbox(
        "Output format",
        options=["PNG", "JPEG"],
        help="PNG preserves transparency. JPEG uses a white background for transparent areas.",
    )

settings_col, summary_col = st.columns([1.45, 1], gap="large")

with settings_col:
    with st.container(border=True):
        st.markdown("#### 🖤 Black & white intensity")
        bw_intensity = st.slider(
            "Original color → grayscale",
            min_value=0,
            max_value=100,
            step=5,
            key="bw_intensity",
            help="0% keeps the original colors; 100% applies full grayscale.",
        )
        st.caption("0% Original color · 100% Full black & white")

        st.markdown("#### ☀️ Brightness")
        brightness = st.slider(
            "Darker → brighter",
            min_value=25,
            max_value=200,
            step=5,
            key="brightness",
            help="100% keeps the original brightness.",
        )

        st.markdown("#### ◐ Contrast")
        contrast = st.slider(
            "Softer → bolder",
            min_value=25,
            max_value=200,
            step=5,
            key="contrast",
            help="100% keeps the original contrast.",
        )

with summary_col:
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="step-label">CURRENT SETTINGS</div>
            <div style="font-size:31px;font-weight:900;color:{C["text"]};margin:7px 0 2px">
                {bw_intensity}%
            </div>
            <div class="soft-card-copy">Black & white intensity</div>
            <hr style="border:0;border-top:1px solid {C["border"]};margin:16px 0">
            <div style="display:flex;justify-content:space-between;gap:10px;margin:9px 0">
                <span style="color:{C["muted"]};font-size:13px">Brightness</span>
                <b style="color:{C["text"]}">{brightness}%</b>
            </div>
            <div style="display:flex;justify-content:space-between;gap:10px;margin:9px 0">
                <span style="color:{C["muted"]};font-size:13px">Contrast</span>
                <b style="color:{C["text"]}">{contrast}%</b>
            </div>
            <div style="display:flex;justify-content:space-between;gap:10px;margin:9px 0">
                <span style="color:{C["muted"]};font-size:13px">Photos selected</span>
                <b style="color:{C["text"]}">{len(uploads)}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="info-box">
            <strong>Tip for a classic look</strong><br>
            Start with 100% intensity, 100% brightness and 110% contrast.
            Adjust from there to suit each photo.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 10. PROCESS IMAGES
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div class="step-label">STEP 3 · REVIEW & DOWNLOAD</div>
    <div class="section-title">Your edited photos</div>
    <div class="section-help">
        Your preview updates with the current settings. Review the result,
        then download one image or the full batch.
    </div>
    """,
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
        output_data = image_to_bytes(converted, output_format)
        extension = "jpg" if output_format == "JPEG" else "png"
        proposed_name = f"{safe_stem(uploaded.name)}_black_white.{extension}"
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
        "You can still download successfully converted images."
    )
    with st.expander("View files that could not be processed"):
        for filename, error in failed_items:
            st.write(f"**{filename}**")
            st.caption(error)

if not preview_records:
    st.error("No images could be converted. Please upload valid image files.")
    st.stop()


# =========================================================
# 11. SUMMARY METRICS
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
# 12. BEFORE / AFTER PREVIEW
# =========================================================
st.markdown("### Compare before and after")

if len(preview_records) > 1:
    selected_name = st.selectbox(
        "Choose a photo to preview",
        options=[f'{i + 1}. {item["name"]}' for i, item in enumerate(preview_records)],
        key="preview_choice",
    )
    selected_index = int(selected_name.split(".", 1)[0]) - 1
    record = preview_records[selected_index]
else:
    record = preview_records[0]

st.caption(
    f'{record["name"]} · {record["size"][0]} × {record["size"][1]} pixels'
)

before_col, after_col = st.columns(2, gap="medium")

with before_col:
    st.markdown('<div class="preview-tag">BEFORE</div>', unsafe_allow_html=True)
    st.markdown("**Original photo**")
    st.image(record["original"], width=320)

with after_col:
    st.markdown('<div class="preview-tag">AFTER</div>', unsafe_allow_html=True)
    st.markdown("**Black & white result**")
    st.image(record["converted"], width=320)


# =========================================================
# 13. DOWNLOAD SELECTED IMAGE
# =========================================================
st.markdown("---")
st.markdown("### Download your edited photo")

st.markdown(
    f"""
    <div class="info-box">
        <strong>{record["output_name"]}</strong><br>
        {record["size"][0]} × {record["size"][1]} pixels
        &nbsp; · &nbsp; {human_size(len(record["output"]))}<br>
        Your edited image is ready to save.
    </div>
    """,
    unsafe_allow_html=True,
)

st.download_button(
    label="⬇ Download edited photo",
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
        <div class="soft-card">
            <div class="soft-card-title">📦 Your batch is ready</div>
            <div class="soft-card-copy">
                Download all {len(converted_items)} converted photos together
                in one ZIP file, or download individual images below.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    zip_data = make_zip(converted_items)
    st.download_button(
        label=f"⬇ Download all {len(converted_items)} photos (ZIP)",
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
                st.write(f'**{item["output_name"]}**')
                st.caption(human_size(len(item["output"])))
            with button_col:
                st.download_button(
                    label="Download",
                    data=item["output"],
                    file_name=item["output_name"],
                    mime="image/png" if output_format == "PNG" else "image/jpeg",
                    key=f'individual_{item["output_name"]}',
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
