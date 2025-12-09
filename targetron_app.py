import streamlit as st
import pandas as pd
from io import BytesIO

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Targetron File Exploder", layout="wide")

# ==============================
# TITLE + SUBTITLE
# ==============================
st.title("💥 Targetron File Exploder")
st.write("Upload your CSV and watch Targetron **EXPLODE** it into clean rows!")

# ==============================
# FIREBALL ANIMATION
# ==============================
fireball_loader = """
<div id="loader" style="display:none;">
    <div class="fireball"></div>
</div>

<style>
.fireball {
    width: 40px;
    height: 40px;
    background: radial-gradient(circle at 30% 30%, #ffcc00, #ff6600);
    border-radius: 50%;
    animation: explode 0.8s infinite ease-in-out alternate;
    margin: 20px auto;
}
@keyframes explode {
    from { transform: scale(1); opacity: 1; }
    to { transform: scale(2.1); opacity: 0.1; }
}
</style>

<script>
function showLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'block';
    setTimeout(() => { loader.style.display = 'none'; }, 1800);
}
</script>
"""

st.markdown(fireball_loader, unsafe_allow_html=True)

# ==============================
# FILE UPLOAD
# ==============================
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
    help="Limit 200MB per file • CSV"
)

# ==============================
# SAFE CSV LOADER
# ==============================
def load_csv_safely(file):
    try:
        df = pd.read_csv(
            file,
            sep=None,                 # auto-detect delimiter
            engine="python",          # tolerant parser
            on_bad_lines="skip"       # skip bad rows instead of crashing
        )
        return df
    except Exception as e:
        st.error(f"❌ CSV loading failed: {e}")
        return None

# ==============================
# DOWNLOAD CSV HELPERS
# ==============================
def download_csv(df):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# ==============================
# EXPLODE LOGIC
# ==============================
def explode_columns(df):
    df_out = df.copy()
    for col in df_out.columns:
        # If cell contains arrays / comma lists, split and explode
        if df_out[col].astype(str).str.contains(',').any():
            df_out[col] = df_out[col].astype(str).str.split(',')
            df_out = df_out.explode(col)
    return df_out


# ==============================
# MAIN ACTION BUTTON
# ==============================
if uploaded_file:
    st.write("### 👀 Preview of uploaded file (first 20 rows)")
    
    df_preview = load_csv_safely(uploaded_file)
    
    if df_preview is not None:
        st.dataframe(df_preview.head(20))

        st.write("---")

        if st.button("🔥 Explode File", use_container_width=True):
            st.markdown("<script>showLoader()</script>", unsafe_allow_html=True)

            with st.spinner("Exploding your file... 💣"):
                df_processed = explode_columns(df_preview)

            st.success("Done! File exploded successfully.")

            st.write("### 🔎 Preview of exploded file (first 20 rows)")
            st.dataframe(df_processed.head(20))

            # DOWNLOAD BUTTON
            csv_data = download_csv(df_processed)
            st.download_button(
                label="⬇️ Download Exploded CSV",
                data=csv_data,
                file_name="exploded_targetron.csv",
                mime="text/csv",
                use_container_width=True
            )
