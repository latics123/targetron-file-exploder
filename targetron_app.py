
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Targetron File Exploder", layout="centered")

st.title("💥 Targetron File Exploder")
st.write("Upload your CSV and watch Targetron EXPLODE it into clean rows!")

# ---------------- FIREBALL LOADING ANIMATION ---------------- #

fireball_loader = """
<div id="loader" style="display:none;">
    <div class="fireball"></div>
</div>

<style>
    .fireball {
        width: 40px;
        height: 40px;
        background: radial-gradient(circle, #ff4500 0%, #ff8c00 40%, #ff0000 70%);
        border-radius: 50%;
        animation: fire-move 1s infinite ease-in-out, fire-glow 0.4s infinite alternate;
        margin: 20px auto;
    }

    @keyframes fire-move {
        0% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-10px) scale(1.2); }
        100% { transform: translateY(0px) scale(1); }
    }

    @keyframes fire-glow {
        from { box-shadow: 0 0 10px #ff4500; }
        to   { box-shadow: 0 0 25px #ff0000; }
    }
</style>

<script>
function showLoader() {
    document.getElementById("loader").style.display = "block";
}
</script>
"""

st.markdown(fireball_loader, unsafe_allow_html=True)

# ---------------- EXPLOSION EFFECT ---------------- #

explosion_animation = """
<div class="explosion"></div>

<style>
    .explosion {
        width: 60px;
        height: 60px;
        background: radial-gradient(circle, #ff0000 0%, #ffa500 40%, #ffff00 70%);
        border-radius: 50%;
        opacity: 0;
        margin: 20px auto;
        animation: explode 0.8s forwards ease-out;
    }

    @keyframes explode {
        0%   { transform: scale(0.3); opacity: 1;   }
        70%  { transform: scale(2.5); opacity: 0.8; }
        100% { transform: scale(3.5); opacity: 0;   }
    }
</style>
"""

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Trigger fireball loader when user clicks "Process"
process_button = st.button("🔥 Explode File", on_click=lambda: st.markdown("<script>showLoader()</script>", unsafe_allow_html=True))

if uploaded_file and process_button:

    st.markdown("<script>showLoader()</script>", unsafe_allow_html=True)

    df = pd.read_csv(uploaded_file)

    rows = []

    full_name_cols = ["Full name", "Full Name 1", "Full Name 2", "Full Name 3"]
    linkedin_cols = ["LinkedIn Profile URL", "LinkedIn Profile URL (2)", "LinkedIn Profile URL (3)"]
    exclude_cols = full_name_cols + linkedin_cols

    def safe_get(row, col):
        return row[col] if col in df.columns else None

    for _, r in df.iterrows():

        base_cols = [
            c for c in df.columns
            if not (c.startswith("email_") or c in exclude_cols)
        ]
        base = r[base_cols].to_dict()

        mapping = [
            ("email_1", "email_1_first_name", "email_1_last_name", "email_1_title",
             "Full Name 1", "LinkedIn Profile URL"),

            ("email_2", "email_2_first_name", "email_2_last_name", "email_2_title",
             "Full Name 2", "LinkedIn Profile URL (2)"),

            ("email_3", "email_3_first_name", "email_3_last_name", "email_3_title",
             "Full Name 3", "LinkedIn Profile URL (3)")
        ]

        for email_col, fn_col, ln_col, title_col, fullname_col, linkedin_col in mapping:
            email = safe_get(r, email_col)

            if isinstance(email, str) and email.strip():

                rows.append({
                    "first_name": safe_get(r, fn_col),
                    "last_name": safe_get(r, ln_col),
                    "full_name": safe_get(r, fullname_col),
                    "title": safe_get(r, title_col),
                    "linkedin_url": safe_get(r, linkedin_col),
                    "email": email,
                    **base
                })

    out = pd.DataFrame(rows).drop_duplicates(subset=["email"])

    # ---------------- SHOW EXPLOSION ---------------- #
    st.markdown(explosion_animation, unsafe_allow_html=True)

    # ---------------- ALLOW DOWNLOAD ---------------- #
    csv_buffer = BytesIO()
    out.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.success("💥 Targetron has exploded your file!")
    st.download_button(
        label="📥 Download exploded CSV",
        data=csv_buffer,
        file_name="targetron_exploded.csv",
        mime="text/csv"
    )

    st.write("Preview of exploded data:")
    st.dataframe(out.head(20))
