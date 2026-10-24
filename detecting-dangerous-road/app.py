import json
import re
from datetime import datetime
from pathlib import Path

import ollama
import streamlit as st
from PIL import Image, UnidentifiedImageError

# ---------------- CONFIGURATION ----------------

APP_DIR = Path(__file__).resolve().parent
REPORTS_DIR = APP_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

MODEL_NAME = "gemma3:4b"

st.set_page_config(
    page_title="RoadEye AI | Road Damage Detection",
    page_icon="🛣️",
    layout="wide",
)

# ---------------- DESIGN ----------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1220;
        color: #f1f5f9;
    }
    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #102b46, #174b50);
        border: 1px solid #28566a;
        margin-bottom: 22px;
    }
    .hero h1 {
        color: #ffffff;
        margin-bottom: 8px;
    }
    .hero p {
        color: #cbd5e1;
        font-size: 16px;
    }
    .note {
        background: #172438;
        padding: 14px;
        border-radius: 10px;
        border-left: 4px solid #38bdf8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HEADER ----------------

st.markdown(
    """
    <div class="hero">
        <h1>🛣️ RoadEye AI</h1>
        <p>AI-assisted road damage screening and preliminary risk assessment.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="note">⚠️ This tool provides a preliminary assessment from an '
    'image. It cannot certify road safety or replace an on-site inspection.</div>',
    unsafe_allow_html=True,
)

st.write("")

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("⚙️ Project Settings")
    st.write("**AI Model:**", MODEL_NAME)
    st.write("**Analysis:** Road image screening")
    st.divider()
    st.caption("RoadEye AI | College Hackathon Project")
    st.caption("Reports are saved locally on this computer.")

# ---------------- INPUTS ----------------

left, right = st.columns([1, 1])

with left:
    st.subheader("📷 Upload Road Image")

    uploaded_file = st.file_uploader(
        "Choose a road photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload a clear road image showing the road surface.",
    )

    location = st.text_input(
        "📍 Road location (optional)",
        placeholder="Example: Main gate road, Faridabad",
    )

    notes = st.text_area(
        "Additional notes (optional)",
        placeholder="Example: Photo taken during daytime.",
    )

with right:
    st.subheader("🖼️ Image Preview")

    image = None

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image.verify()

            uploaded_file.seek(0)
            image = Image.open(uploaded_file).convert("RGB")

            st.image(
                image,
                caption="Uploaded road image",
                use_container_width=True,
            )

        except (UnidentifiedImageError, OSError, ValueError):
            st.error("Image open nahi ho rahi. Please valid JPG, PNG or WEBP upload karo.")
            image = None
    else:
        st.info("Road image upload karne par preview yahan dikhega.")

# ---------------- ANALYSIS ----------------

st.divider()
st.subheader("🔎 Road Damage Analysis")

if st.button("🚀 Analyze Road Image", type="primary", use_container_width=True):

    if uploaded_file is None or image is None:
        st.error("Please pehle ek valid road image upload karo.")

    else:
        with st.spinner("Gemma AI image analyze kar raha hai. Please wait..."):

            try:
                # Send the actual uploaded image to Ollama.
                uploaded_file.seek(0)
                image_bytes = uploaded_file.getvalue()

                response = ollama.chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                "You are assisting with preliminary road damage "
                                "screening. Inspect the provided road image. "
                                "Describe only visible evidence of possible "
                                "potholes, cracks, broken pavement, erosion, or "
                                "other visible damage. Mention uncertainty and "
                                "limitations. Do not claim that you have measured "
                                "damage, verified real-world conditions, or "
                                "certified the road safe. "
                                "End your answer with exactly one line in this "
                                "format: RISK: LOW, RISK: MODERATE, RISK: HIGH, "
                                "or RISK: INDETERMINATE. Use INDETERMINATE if "
                                "the image is unclear or insufficient. Risk is "
                                "only a preliminary visual screening estimate."
                            ),
                            "images": [image_bytes],
                        }
                    ],
                )

                analysis_text = response["message"]["content"].strip()

                match = re.search(
                    r"RISK:\s*(LOW|MODERATE|HIGH|INDETERMINATE)\b",
                    analysis_text,
                    re.IGNORECASE,
                )

                if match:
                    risk = match.group(1).upper()
                else:
                    risk = "INDETERMINATE"
                    analysis_text += (
                        "\n\nRisk could not be reliably extracted from the "
                        "model response. Further review is needed."
                    )

                if risk == "HIGH":
                    next_step = (
                        "Possible significant damage is indicated. Avoid "
                        "approaching the suspected hazard when possible and "
                        "report the location to the relevant road authority "
                        "for prompt inspection."
                    )
                elif risk == "MODERATE":
                    next_step = (
                        "Arrange a closer inspection and report the suspected "
                        "damage to the relevant road maintenance authority."
                    )
                elif risk == "LOW":
                    next_step = (
                        "No major damage may be apparent in this image, but "
                        "this does not establish that the road is safe. "
                        "Normal caution and appropriate inspection remain necessary."
                    )
                else:
                    next_step = (
                        "The image does not support a reliable risk estimate. "
                        "Try a clearer photo and request an on-site inspection "
                        "if you suspect damage."
                    )

                report = {
                    "project": "RoadEye AI",
                    "report_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                    "created_at": datetime.now().astimezone().isoformat(),
                    "model": MODEL_NAME,
                    "location": location.strip() or "Not provided",
                    "additional_notes": notes.strip(),
                    "image_filename": Path(uploaded_file.name).name,
                    "preliminary_risk_level": risk,
                    "analysis": analysis_text,
                    "suggested_next_step": next_step,
                    "disclaimer": (
                        "AI-generated preliminary visual screening only. "
                        "Not a verified diagnosis or road safety certification."
                    ),
                }

                # Save the report locally.
                report_path = REPORTS_DIR / (
                    f"road_report_{report['report_id']}.json"
                )

                report_path.write_text(
                    json.dumps(report, indent=4, ensure_ascii=False),
                    encoding="utf-8",
                )

                # Store results so they remain visible after reruns.
                st.session_state["roadeye_report"] = report
                st.session_state["roadeye_report_path"] = str(report_path)

            except Exception as error:
                st.error(
                    "Analysis complete nahi ho paya. Check karo ki Ollama "
                    "running hai aur required model installed hai."
                )
                st.code(f"{type(error).__name__}: {error}")

# ---------------- RESULTS ----------------

report = st.session_state.get("roadeye_report")

if report:
    st.divider()
    st.subheader("📊 Preliminary Assessment")

    risk = report["preliminary_risk_level"]

    if risk == "HIGH":
        st.error(f"⚠️ Preliminary Risk: {risk}")
    elif risk == "MODERATE":
        st.warning(f"⚠️ Preliminary Risk: {risk}")
    elif risk == "LOW":
        st.success(f"Preliminary Risk: {risk} — not a safety certification")
    else:
        st.info(f"Preliminary Risk: {risk}")

    st.markdown("### 🧠 AI Observations")
    st.write(report["analysis"])

    st.markdown("### 🛠️ Suggested Next Step")
    st.write(report["suggested_next_step"])

    st.markdown("### 📍 Report Details")
    st.write("**Location:**", report["location"])
    st.write("**Model:**", report["model"])
    st.write("**Image:**", report["image_filename"])

    st.download_button(
        label="⬇️ Download JSON Report",
        data=json.dumps(report, indent=4, ensure_ascii=False),
        file_name=f"roadeye_report_{report['report_id']}.json",
        mime="application/json",
        use_container_width=True,
    )

    st.success("Report locally save ho gayi hai.")
    st.code(st.session_state["roadeye_report_path"])

st.divider()
st.caption(
    "RoadEye AI is a prototype. Image analysis can be wrong; "
    "actual road conditions require appropriate real-world inspection."
)
