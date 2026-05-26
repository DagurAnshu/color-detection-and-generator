import streamlit as st
import numpy as np
import cv2
from PIL import Image

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Advanced AI Color Studio",
    page_icon="🎨",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.info-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="title">🎨 Advanced AI Color Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload Image OR Create Colors Using RGB</div>',
    unsafe_allow_html=True
)

# =========================================================
# MODE SELECTION
# =========================================================

mode = st.sidebar.radio(
    "Choose Mode",
    [
        "📤 Upload Image Color Detection",
        "🎛️ Create Color Using RGB"
    ]
)

# =========================================================
# COLOR NAME DETECTION FUNCTION
# =========================================================

def detect_color_name(r, g, b):

    if r > 200 and g < 100 and b < 100:
        return "Red"

    elif r < 100 and g > 200 and b < 100:
        return "Green"

    elif r < 100 and g < 100 and b > 200:
        return "Blue"

    elif r > 200 and g > 200 and b < 100:
        return "Yellow"

    elif r > 200 and g > 150 and b < 100:
        return "Orange"

    elif r > 150 and g < 100 and b > 150:
        return "Purple"

    elif r > 180 and g > 180 and b > 180:
        return "White"

    elif r < 50 and g < 50 and b < 50:
        return "Black"

    elif r > 100 and g > 100 and b > 100:
        return "Gray"

    else:
        return "Custom Mixed Color"

# =========================================================
# MODE 1 : IMAGE COLOR DETECTION
# =========================================================

if mode == "📤 Upload Image Color Detection":

    st.header("📤 Upload an Image")

    uploaded_file = st.file_uploader(
        "Choose an Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        # =================================================
        # LOAD IMAGE SAFELY
        # =================================================

        image = Image.open(uploaded_file)

        # Convert image safely to RGB
        img = np.array(image.convert("RGB"))

        # Resize image
        img = cv2.resize(img, (500, 400))

        # =================================================
        # FIND DOMINANT / AVERAGE COLOR
        # =================================================

        pixels = img.reshape((-1, 3))

        avg_color = np.mean(pixels, axis=0)

        red = int(avg_color[0])
        green = int(avg_color[1])
        blue = int(avg_color[2])

        # =================================================
        # CREATE COLOR PREVIEW
        # =================================================

        color_preview = np.zeros((300, 300, 3), dtype=np.uint8)

        color_preview[:] = [red, green, blue]

        # =================================================
        # HEX COLOR
        # =================================================

        hex_color = f"#{red:02X}{green:02X}{blue:02X}"

        # =================================================
        # COLOR NAME
        # =================================================

        color_name = detect_color_name(red, green, blue)

        # =================================================
        # LAYOUT
        # =================================================

        col1, col2 = st.columns(2)

        # =============================================
        # ORIGINAL IMAGE
        # =============================================

        with col1:

            st.subheader("🖼️ Uploaded Image")

            st.image(img)

        # =============================================
        # DETECTED COLOR
        # =============================================

        with col2:

            st.subheader("🎨 Detected Dominant Color")

            st.image(color_preview)

        # =================================================
        # COLOR INFORMATION
        # =================================================

        st.markdown("---")

        st.subheader("📊 Color Information")

        st.markdown(f"""
        <div class="info-box">

        <h2>Detected Color : {color_name}</h2>

        <hr>

        <h3>RGB Values</h3>

        🔴 Red : <b>{red}</b><br><br>

        🟢 Green : <b>{green}</b><br><br>

        🔵 Blue : <b>{blue}</b><br><br>

        <hr>

        <h3>HEX Code</h3>

        <b>{hex_color}</b>

        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # RGB INTENSITY
        # =================================================

        st.markdown("---")

        st.subheader("📈 RGB Intensity")

        st.progress(red / 255, text=f"Red Intensity : {red}")

        st.progress(green / 255, text=f"Green Intensity : {green}")

        st.progress(blue / 255, text=f"Blue Intensity : {blue}")

        # =================================================
        # DOWNLOAD BUTTON
        # =================================================

        success, encoded_image = cv2.imencode(
            ".png",
            cv2.cvtColor(color_preview, cv2.COLOR_RGB2BGR)
        )

        st.download_button(
            label="⬇️ Download Detected Color",
            data=encoded_image.tobytes(),
            file_name="detected_color.png",
            mime="image/png"
        )

    else:

        st.info("📤 Upload an image to detect its dominant color.")

# =========================================================
# MODE 2 : CREATE COLOR USING RGB
# =========================================================

elif mode == "🎛️ Create Color Using RGB":

    st.header("🎛️ Create Your Own Color")

    # =====================================================
    # RGB SLIDERS
    # =====================================================

    red = st.slider("🔴 Red", 0, 255, 0)

    green = st.slider("🟢 Green", 0, 255, 0)

    blue = st.slider("🔵 Blue", 0, 255, 0)

    # =====================================================
    # CREATE COLOR IMAGE
    # =====================================================

    color_img = np.zeros((350, 500, 3), dtype=np.uint8)

    color_img[:] = [red, green, blue]

    # =====================================================
    # HEX COLOR
    # =====================================================

    hex_color = f"#{red:02X}{green:02X}{blue:02X}"

    # =====================================================
    # COLOR NAME
    # =====================================================

    color_name = detect_color_name(red, green, blue)

    # =====================================================
    # SHOW GENERATED COLOR
    # =====================================================

    st.subheader("🎨 Generated Color")

    st.image(color_img)

    # =====================================================
    # COLOR INFORMATION
    # =====================================================

    st.markdown("---")

    st.markdown(f"""
    <div class="info-box">

    <h2>Generated Color : {color_name}</h2>

    <hr>

    <h3>RGB Values</h3>

    🔴 Red : <b>{red}</b><br><br>

    🟢 Green : <b>{green}</b><br><br>

    🔵 Blue : <b>{blue}</b><br><br>

    <hr>

    <h3>HEX Code</h3>

    <b>{hex_color}</b>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # RGB INTENSITY
    # =====================================================

    st.markdown("---")

    st.subheader("📈 RGB Intensity")

    st.progress(red / 255, text=f"Red Intensity : {red}")

    st.progress(green / 255, text=f"Green Intensity : {green}")

    st.progress(blue / 255, text=f"Blue Intensity : {blue}")

    # =====================================================
    # DOWNLOAD BUTTON
    # =====================================================

    success, encoded_image = cv2.imencode(
        ".png",
        cv2.cvtColor(color_img, cv2.COLOR_RGB2BGR)
    )

    st.download_button(
        label="⬇️ Download Generated Color",
        data=encoded_image.tobytes(),
        file_name="generated_color.png",
        mime="image/png"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.success("🚀 Advanced AI Color Studio Running Successfully!")