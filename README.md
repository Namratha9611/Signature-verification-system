# ✍️ Signature Verification System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Overview
The **Signature Verification System** is a full-stack application that verifies handwritten signatures using image processing techniques. It compares two signatures and determines whether they match using the **Structural Similarity Index (SSIM)**.

This system can be used in real-world scenarios such as:
- Banking authentication
- Document verification
- Fraud detection

---

## 🚀 Features
- ✍️ Register handwritten signatures
- 🔍 Verify signatures using SSIM algorithm
- 📊 Generate similarity score (0–100)
- 📄 Automatic PDF report generation
- 🖥️ Simple and interactive UI
- ⚡ Fast and efficient processing

---

## 🛠️ Tech Stack

### 🔹 Backend
- Python
- Flask

### 🔹 Frontend
- HTML
- CSS
- JavaScript

### 🔹 Image Processing
- OpenCV
- NumPy
- scikit-image (SSIM)

### 🔹 Database
- SQLite

---

## ⚙️ How It Works

1. User registers their signature
2. Signature is stored in the database
3. User uploads a new signature for verification
4. System preprocesses images (grayscale, resize)
5. SSIM algorithm calculates similarity
6. Result is displayed (Match / Not Match)
7. PDF report is generated

---

## 📊 Algorithm Used

Structural Similarity Index (SSIM) is used to compare two images:

- Value range: **0 to 1**
- Higher value = more similarity

Threshold used:
```python
SSIM score = 0..1 (converted to 0..100)
MATCH_THRESHOLD = 82
if score >= MATCH_THRESHOLD:
    result = "Signature Match"
else:
    result = "Signature Not Match"




