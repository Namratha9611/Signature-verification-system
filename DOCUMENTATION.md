# Signature Verification Module (SMM) - Documentation

## 1. Introduction
The **Signature Verification Module (SMM)** is a state-of-the-art Web Application designed to verify the similarity between two hand-drawn signatures. Built with an elegant Glassmorphism interface, it connects seamlessly to a SQLite database to verify incoming test signatures against secured reference signatures.

---

## 2. Key Features
- **Database Backend**: Securely registers users and stores encrypted reference signatures using SQLite.
- **Glassmorphism Web Dashboard**: A fluid, responsive web interface built with pure HTML, CSS, and Javascript.
- **Native Browser Capabilities**: 
    - **Webcam Integrations**: Capture signatures natively using Javascript media streams.
    - **Live Canvas**: Draw signatures directly on the screen.
- **Advanced Processing**: Employs **SSIM (Structural Similarity Index)** to focus on stroke patterns rather than just pixel density.
- **Automated Reporting**: Generates a professional PDF report detailing the "Verified User", similarity score, and side-by-side images.

---

## 3. Technology Stack
- **Backend**: Python 3.x, Flask (`app.py`), SQLite (`database.py`)
- **Computer Vision**: `opencv-python`, `scikit-image`
- **PDF Generation**: `reportlab`, `Pillow`
- **Frontend**: HTML5, Vanilla CSS3, Javascript (`app.js`)

---

## 4. Installation & Setup
To run this project locally, ensure you have Python installed, then install the required dependencies:

```bash
pip install flask flask-cors opencv-python scikit-image pillow reportlab numpy
```

---

## 5. Usage Guide

### Starting the Server
Navigate to the `src/` directory and run the Flask application:
```bash
python app.py
```
> [!NOTE]
> The server runs locally on **`http://localhost:5000`**. Open this URL in Chrome, Firefox, or Edge.

### Registration Workflow
1. Click **Register** in the top navigation bar.
2. Enter a **Full Name**.
3. Provide a Reference Signature using "Upload", "Draw", or "Camera".
4. Click **Register Securely** to save the record in your SQLite database.

### Verification Workflow
1. Click **Verify** in the top navigation bar.
2. Under "System Record", select your registered user from the dropdown menu to load their reference signature.
3. Under "Test Signature", provide the incoming signature you wish to test.
4. Click **Authenticate Signature**.
5. The UI will instantly display whether it is a MATCH or NO MATCH.
6. Check your **Desktop** for a newly generated PDF report associated with that authentication attempt!

---

## 6. Technical Details: The Match Logic
The system evaluates similarity using the following steps:
1. **Grayscale Conversion**: Reduces noise from color gradients.
2. **Normalization**: Resizes both images to $300 \times 300$ pixels for coordinate alignment.
3. **SSIM Calculation**: Mathematically compares luminance ($l$), contrast ($c$), and structure ($s$).
4. **Thresholding**: 
    - **Match**: Score $\geq 82\%$
    - **No Match**: Score $< 82\%$

---

## 7. Project Structure
- `src/app.py`: The Flask server and HTTP API.
- `src/database.py`: Handles SQLite setup, queries, and `database_records/` file saving.
- `src/report_generator.py`: Generates PDFs in-memory and outputs to the `Desktop`.
- `src/templates/`: Contains `index.html` (the stunning web layout).
- `src/static/`: Contains `style.css` matching and `app.js` UI logic.
- `database.sqlite`: Your active database registry.
