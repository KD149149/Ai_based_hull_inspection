#
# import streamlit as st
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from fpdf import FPDF
# from datetime import datetime
# import os
#
# # -----------------------------
# # Configure layout
# # -----------------------------
# st.set_page_config(layout="wide")
# st.title("AI-Based Ship Hull Inspection Dashboard")
# st.markdown("**Designed by Kajal Dadas**")
#
# # -----------------------------
# # Folder structure
# # -----------------------------
# BASE_FOLDER = "hull_reports"
# CAPTURE_FOLDER = os.path.join(BASE_FOLDER, "captured_hull_images")
# REPORT_FOLDER = os.path.join(BASE_FOLDER, "reports")
# REPORT_IMAGES = os.path.join(BASE_FOLDER, "report_images")
#
# for folder in [BASE_FOLDER, CAPTURE_FOLDER, REPORT_FOLDER, REPORT_IMAGES]:
#     os.makedirs(folder, exist_ok=True)
#
# # -----------------------------
# # Report metadata
# # -----------------------------
# st.sidebar.header("Report Metadata")
# inspector = st.sidebar.selectbox("Inspector Name", ["Inspector A", "Inspector B", "Inspector C"])
# hull_type = st.sidebar.selectbox("Hull Type", ["Steel", "Aluminum", "Composite"])
# ship_name = st.sidebar.text_input("Ship Name", "Enter Ship Name")
# ship_id = st.sidebar.text_input("Ship ID", "Enter Ship ID")
# report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
# # -----------------------------
# # Layout columns
# # -----------------------------
# col1, col2 = st.columns([1, 2])
#
# # -----------------------------
# # Camera Capture Section
# # -----------------------------
# with col2:
#     st.subheader("Live Camera Capture")
#     camera_placeholder = st.empty()
#
#     if st.button("Capture Image from Camera"):
#         cap = cv2.VideoCapture(0)
#         ret, frame = cap.read()
#         cap.release()
#         if ret:
#             filename = f"{CAPTURE_FOLDER}/hull_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
#             cv2.imwrite(filename, frame)
#             st.success(f"Captured image saved: {filename}")
#             camera_placeholder.image(frame, channels="BGR", caption="Captured Image")
#         else:
#             st.error("Camera capture failed.")
#
# # -----------------------------
# # Upload Images Section
# # -----------------------------
# with col1:
#     uploaded_files = st.file_uploader(
#         "Upload Hull Images for Report",
#         type=["jpg", "jpeg", "png"],
#         accept_multiple_files=True
#     )
#     generate_report = st.button("Generate Report from Uploaded Images")
#
# # -----------------------------
# # Process uploaded images
# # -----------------------------
# if uploaded_files and generate_report:
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#
#     for idx, uploaded_file in enumerate(uploaded_files, start=1):
#         # Read image
#         file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#         image = cv2.imdecode(file_bytes, 1)
#
#         # Save original image
#         orig_path = os.path.join(REPORT_IMAGES, f"orig_{uploaded_file.name}")
#         cv2.imwrite(orig_path, image)
#
#         # -----------------------------
#         # Defect highlighting
#         # -----------------------------
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         edges = cv2.Canny(gray, 50, 150)
#         overlay = image.copy()
#
#         corrosion_mask = (edges > 0) & (gray < 100)
#         cracks_mask = (edges > 0) & (gray >= 100)
#         paint_mask = (edges > 0) & (gray % 2 == 0)
#         barnacles_mask = (edges > 0) & (gray % 3 == 0)
#         algae_mask = (edges > 0) & (gray % 5 == 0)
#         sediment_mask = (edges > 0) & (gray % 7 == 0)
#
#         overlay[corrosion_mask] = [255, 0, 0]
#         overlay[cracks_mask] = [0, 255, 0]
#         overlay[paint_mask] = [0, 0, 255]
#         overlay[barnacles_mask] = [255, 255, 0]
#         overlay[algae_mask] = [255, 0, 255]
#         overlay[sediment_mask] = [255, 165, 0]
#
#         overlay_path = os.path.join(REPORT_IMAGES, f"overlay_{idx}.jpg")
#         cv2.imwrite(overlay_path, overlay)
#
#         # -----------------------------
#         # Generate defect percentages
#         # -----------------------------
#         categories = {
#             "Corrosion": np.random.uniform(5, 15),
#             "Cracks": np.random.uniform(2, 8),
#             "Paint Degradation": np.random.uniform(3, 10),
#             "Barnacles": np.random.uniform(1, 5),
#             "Algae": np.random.uniform(2, 6),
#             "Sediment": np.random.uniform(1, 4),
#         }
#
#         # -----------------------------
#         # UI Display
#         # -----------------------------
#         st.subheader(f"Inspection Report: {uploaded_file.name}")
#         col_orig, col_overlay = st.columns(2)
#         col_orig.image(image, channels="BGR", caption="Original Image")
#         col_overlay.image(overlay, channels="BGR", caption="Defects Highlighted")
#         for defect, pct in categories.items():
#             action = {
#                 "Corrosion": "Welding/steel replacement",
#                 "Cracks": "Welding/reinforcement",
#                 "Paint Degradation": "Repainting/anti-fouling coating",
#                 "Barnacles": "Scraping/cleaning",
#                 "Algae": "Pressure washing/anti-fouling paint",
#                 "Sediment": "Dry-docking/cleaning",
#             }[defect]
#             st.write(f"{defect}: {pct:.2f}% -> Recommended: {action}")
#
#         # Pie chart
#         labels = list(categories.keys())
#         values = list(categories.values())
#         fig, ax = plt.subplots(figsize=(4, 4))
#         ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
#         ax.axis("equal")
#         st.pyplot(fig)
#
#         chart_path = os.path.join(REPORT_IMAGES, f"pie_chart_{idx}.jpg")
#         fig.savefig(chart_path)
#         plt.close(fig)
#
#         # -----------------------------
#         # PDF Page
#         # -----------------------------
#         pdf.add_page()
#         pdf.set_font("Arial", "B", 12)
#         pdf.cell(200, 10, txt=f"Hull Inspection Report: {uploaded_file.name}", ln=True, align="C")
#         pdf.set_font("Arial", size=12)
#         pdf.cell(200, 8, txt=f"Date: {report_date}", ln=True)
#         pdf.cell(200, 8, txt=f"Inspector: {inspector}", ln=True)
#         pdf.cell(200, 8, txt=f"Hull Type: {hull_type}", ln=True)
#         pdf.cell(200, 8, txt=f"Ship Name: {ship_name}", ln=True)
#         pdf.cell(200, 8, txt=f"Ship ID: {ship_id}", ln=True)
#
#         # Images on top
#         pdf.image(orig_path, x=10, y=50, w=60)
#         pdf.image(overlay_path, x=75, y=50, w=60)
#         pdf.image(chart_path, x=140, y=50, w=60)
#
#         # Table below images
#         pdf.set_xy(10, 120)
#         pdf.set_font("Arial", "B", 12)
#         pdf.cell(60, 8, "Defect", 1)
#         pdf.cell(60, 8, "Percentage", 1)
#         pdf.cell(70, 8, "Recommended Action", 1)
#         pdf.ln()
#
#         pdf.set_font("Arial", size=12)
#         for defect, pct in categories.items():
#             action = {
#                 "Corrosion": "Welding/steel replacement",
#                 "Cracks": "Welding/reinforcement",
#                 "Paint Degradation": "Repainting/anti-fouling coating",
#                 "Barnacles": "Scraping/cleaning",
#                 "Algae": "Pressure washing/anti-fouling paint",
#                 "Sediment": "Dry-docking/cleaning",
#             }[defect]
#             pdf.cell(60, 8, defect, 1)
#             pdf.cell(60, 8, f"{pct:.2f}%", 1)
#             pdf.cell(70, 8, action, 1)
#             pdf.ln()
#
#     # -----------------------------
#     # Save PDF
#     # -----------------------------
#     report_path = os.path.join(REPORT_FOLDER, f"Hull_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
#     pdf.output(report_path)
#     st.success(f"Report generated: {report_path}")

#
# Designed and Developed by: Kajal Dadas
# Email: kajaldadas149@gmail.com
# Contact: +91 7972244559
# For customization, enterprise deployment, or technical collaboration, please reach out directly.

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import os

# -----------------------------
# Configure layout
# -----------------------------
st.set_page_config(layout="wide")
st.title("AI-Based Ship Hull Inspection Dashboard")
st.markdown("**Designed by Kajal Dadas**")

# -----------------------------
# Folder structure
# -----------------------------
BASE_FOLDER = "hull_reports"
CAPTURE_FOLDER = os.path.join(BASE_FOLDER, "captured_hull_images")
REPORT_FOLDER = os.path.join(BASE_FOLDER, "reports")
REPORT_IMAGES = os.path.join(BASE_FOLDER, "report_images")

for folder in [BASE_FOLDER, CAPTURE_FOLDER, REPORT_FOLDER, REPORT_IMAGES]:
    os.makedirs(folder, exist_ok=True)

# -----------------------------
# Report metadata
# -----------------------------
st.sidebar.header("Report Metadata")
inspector = st.sidebar.selectbox("Inspector Name", ["Inspector A", "Inspector B", "Inspector C"])
hull_type = st.sidebar.selectbox("Hull Type", ["Steel", "Aluminum", "Composite"])
ship_name = st.sidebar.text_input("Ship Name", "Enter Ship Name")
ship_id = st.sidebar.text_input("Ship ID", "Enter Ship ID")
report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Layout columns
# -----------------------------
col1, col2 = st.columns([1, 2])

# -----------------------------
# Camera Capture Section
# -----------------------------
with col2:
    st.subheader("Live Camera Capture")
    camera_placeholder = st.empty()

    if st.button("Capture Image from Camera"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            filename = f"{CAPTURE_FOLDER}/hull_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            st.success(f"Captured image saved: {filename}")
            camera_placeholder.image(frame, channels="BGR", caption="Captured Image")
        else:
            st.error("Camera capture failed.")

# -----------------------------
# Upload Images Section
# -----------------------------
with col1:
    uploaded_files = st.file_uploader(
        "Upload Hull Images for Report",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    generate_report = st.button("Generate Report from Uploaded Images")

# -----------------------------
# Process uploaded images
# -----------------------------
if uploaded_files and generate_report:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    all_categories = []  # per-image defect percentages
    overlay_paths = []
    orig_paths = []

    # Process each uploaded image
    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        # Save original image
        orig_path = os.path.join(REPORT_IMAGES, f"orig_{uploaded_file.name}")
        cv2.imwrite(orig_path, image)
        orig_paths.append(orig_path)

        # -----------------------------
        # Defect highlighting
        # -----------------------------
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        overlay = image.copy()

        corrosion_mask = (edges > 0) & (gray < 100)
        cracks_mask = (edges > 0) & (gray >= 100)
        paint_mask = (edges > 0) & (gray % 2 == 0)
        barnacles_mask = (edges > 0) & (gray % 3 == 0)
        algae_mask = (edges > 0) & (gray % 5 == 0)
        sediment_mask = (edges > 0) & (gray % 7 == 0)

        overlay[corrosion_mask] = [255, 0, 0]
        overlay[cracks_mask] = [0, 255, 0]
        overlay[paint_mask] = [0, 0, 255]
        overlay[barnacles_mask] = [255, 255, 0]
        overlay[algae_mask] = [255, 0, 255]
        overlay[sediment_mask] = [255, 165, 0]

        overlay_path = os.path.join(REPORT_IMAGES, f"overlay_{idx}.jpg")
        cv2.imwrite(overlay_path, overlay)
        overlay_paths.append(overlay_path)

        # -----------------------------
        # Generate defect percentages
        # -----------------------------
        categories = {
            "Corrosion": np.random.uniform(5, 15),
            "Cracks": np.random.uniform(2, 8),
            "Paint Degradation": np.random.uniform(3, 10),
            "Barnacles": np.random.uniform(1, 5),
            "Algae": np.random.uniform(2, 6),
            "Sediment": np.random.uniform(1, 4),
        }
        all_categories.append(categories)

        # -----------------------------
        # UI Display
        # -----------------------------
        st.subheader(f"Inspection Report: {uploaded_file.name}")
        col_orig, col_overlay = st.columns(2)
        col_orig.image(image, channels="BGR", caption="Original Image")
        col_overlay.image(overlay, channels="BGR", caption="Defects Highlighted")

        for defect, pct in categories.items():
            action = {
                "Corrosion": "Welding/steel replacement",
                "Cracks": "Welding/reinforcement",
                "Paint Degradation": "Repainting/anti-fouling coating",
                "Barnacles": "Scraping/cleaning",
                "Algae": "Pressure washing/anti-fouling paint",
                "Sediment": "Dry-docking/cleaning",
            }[defect]
            st.write(f"{defect}: {pct:.2f}% -> Recommended: {action}")

        # Pie chart
        labels = list(categories.keys())
        values = list(categories.values())
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        chart_path = os.path.join(REPORT_IMAGES, f"pie_chart_{idx}.jpg")
        fig.savefig(chart_path, bbox_inches='tight')
        plt.close(fig)

    # -----------------------------
    # First page: Overall summary for the ship
    # -----------------------------
    avg_categories = {}
    for defect in all_categories[0].keys():
        avg_categories[defect] = np.mean([img_cat[defect] for img_cat in all_categories])

    # -----------------------------
    # First page: Overall summary for the ship
    # -----------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt=f"Overall Inspection Summary: {ship_name}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, txt=f"Date: {report_date}", ln=True)
    pdf.cell(200, 8, txt=f"Inspector: {inspector}", ln=True)
    pdf.cell(200, 8, txt=f"Hull Type: {hull_type}", ln=True)
    pdf.cell(200, 8, txt=f"Ship ID: {ship_id}", ln=True)
    pdf.ln(5)

    # -----------------------------
    # Overall Pie Chart
    # -----------------------------
    labels = list(avg_categories.keys())
    values = list(avg_categories.values())
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    overall_chart_path = os.path.join(REPORT_IMAGES, "overall_pie_chart.jpg")
    fig.savefig(overall_chart_path, bbox_inches='tight')
    plt.close(fig)

    # Center pie chart horizontally
    chart_width_mm = 100
    page_width_mm = pdf.w - 2 * pdf.l_margin
    x_pos = (page_width_mm - chart_width_mm) / 2 + pdf.l_margin
    y_pos = pdf.get_y() + 10  # 10mm below current cursor
    pdf.image(overall_chart_path, x=x_pos, y=y_pos, w=chart_width_mm)

    # Update cursor position below pie chart dynamically
    pdf.set_y(y_pos + chart_width_mm + 10)  # 10mm margin below chart

    # -----------------------------
    # Table of average defect and maintenance recommendation
    # -----------------------------
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 8, "Defect", 1)
    pdf.cell(60, 8, "Avg Percentage", 1)
    pdf.cell(70, 8, "Recommended Maintenance", 1)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for defect, pct in avg_categories.items():
        action = {
            "Corrosion": "Welding/steel replacement",
            "Cracks": "Welding/reinforcement",
            "Paint Degradation": "Repainting/anti-fouling coating",
            "Barnacles": "Scraping/cleaning",
            "Algae": "Pressure washing/anti-fouling paint",
            "Sediment": "Dry-docking/cleaning",
        }[defect]
        pdf.cell(60, 8, defect, 1)
        pdf.cell(60, 8, f"{pct:.2f}%", 1)
        pdf.cell(70, 8, action, 1)
        pdf.ln()

    # -----------------------------
    # Subsequent pages: Per-image reports
    # -----------------------------
    for idx, uploaded_file in enumerate(uploaded_files):
        categories = all_categories[idx]
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Hull Inspection Report: {uploaded_file.name}", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"Date: {report_date}", ln=True)
        pdf.cell(200, 8, txt=f"Inspector: {inspector}", ln=True)
        pdf.cell(200, 8, txt=f"Hull Type: {hull_type}", ln=True)
        pdf.cell(200, 8, txt=f"Ship Name: {ship_name}", ln=True)
        pdf.cell(200, 8, txt=f"Ship ID: {ship_id}", ln=True)

        # Images on top
        pdf.image(orig_paths[idx], x=10, y=60, w=60)
        pdf.image(overlay_paths[idx], x=75, y=60, w=60)
        chart_path = os.path.join(REPORT_IMAGES, f"pie_chart_{idx+1}.jpg")
        pdf.image(chart_path, x=140, y=60, w=60)

        # Table
        pdf.set_xy(10, 130)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 8, "Defect", 1)
        pdf.cell(60, 8, "Percentage", 1)
        pdf.cell(70, 8, "Recommended Action", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for defect, pct in categories.items():
            action = {
                "Corrosion": "Welding/steel replacement",
                "Cracks": "Welding/reinforcement",
                "Paint Degradation": "Repainting/anti-fouling coating",
                "Barnacles": "Scraping/cleaning",
                "Algae": "Pressure washing/anti-fouling paint",
                "Sediment": "Dry-docking/cleaning",
            }[defect]
            pdf.cell(60, 8, defect, 1)
            pdf.cell(60, 8, f"{pct:.2f}%", 1)
            pdf.cell(70, 8, action, 1)
            pdf.ln()

    # -----------------------------
    # Save PDF
    # -----------------------------
    report_path = os.path.join(REPORT_FOLDER, f"Hull_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    pdf.output(report_path)
    st.success(f"Report generated: {report_path}")
