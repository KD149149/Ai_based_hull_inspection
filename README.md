
# AI-Based Ship Hull Inspection Dashboard

## Overview

AI-Based Ship Hull Inspection Dashboard is a Streamlit-based application for automated ship hull inspection reporting. It enables image capture, multi-image upload, defect visualization, ship-level summary generation, and structured PDF report creation.

The system simulates AI-based defect detection and provides maintenance recommendations in a professional report format.

---

## Features

### Camera Capture

* Capture image from system camera
* Display image in UI
* Store snapshot locally
* Does not generate report unless uploaded

### Multi-Image Upload

* Upload multiple hull images
* Generate report only for uploaded images
* Separate inspection page for each image

### Ship-Level Summary

* First page contains overall summary
* Average defect percentage across all images
* Consolidated pie chart
* Maintenance recommendation table

### Per-Image Report

Each uploaded image generates:

* Original image
* Defect-highlighted image
* Pie chart
* Defect percentage table
* Recommended maintenance actions

---

## Defect Categories

* Corrosion
* Cracks
* Paint Degradation
* Barnacles
* Algae
* Sediment

---

## Project Structure

```
hull_reports/
│
├── captured_hull_images/
├── report_images/
└── reports/
```

---

# Installation Guide

## Step 1: Clone Repository

```
git clone <your-repository-url>
cd <project-folder>
```

---

## Step 2: Create Virtual Environment (Recommended)

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Requirements

Create a file named:

requirements.txt

Add the following:

```
streamlit
opencv-python
numpy
matplotlib
fpdf
```

Then install:

```
pip install -r requirements.txt
```

---

# Code Execution Command

Run the application using:

```
streamlit run app.py
```

After running, Streamlit will provide a local URL such as:

```
http://localhost:8501
```

Open it in your browser.

---

# Output Location

Generated reports are saved in:

```
hull_reports/reports/
```

Captured images are stored in:

```
hull_reports/captured_hull_images/
```

---

# Technologies Used

* Python
* Streamlit
* OpenCV
* NumPy
* Matplotlib
* FPDF

---

# Future Improvements

* Replace simulated detection with YOLOv8 segmentation
* Add severity classification (Low, Moderate, Severe)
* Add defect surface area percentage calculation
* Add cost and maintenance time estimation
* Integrate cloud deployment with Docker
* Add database logging for inspection history

---
