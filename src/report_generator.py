from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, white, black
from reportlab.graphics.barcode import code128
import datetime
import os
import cv2
from pathlib import Path
from PIL import Image
from io import BytesIO

def get_desktop_path():
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    return desktop

def generate_pdf_report(img1, img2, score, is_match, user_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Signature_Report_{timestamp}.pdf"

    desktop_path = get_desktop_path()
    full_path = str(desktop_path / filename)

    # Convert to PIL and memory stream
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    pil_img1 = Image.fromarray(img1_rgb)
    pil_img2 = Image.fromarray(img2_rgb)

    buf1 = BytesIO()
    buf2 = BytesIO()
    pil_img1.save(buf1, format='PNG')
    pil_img2.save(buf2, format='PNG')
    buf1.seek(0)
    buf2.seek(0)

    c = canvas.Canvas(full_path, pagesize=A4)
    width, height = A4

    # 1. Header Banner (Dark Mode Theme)
    c.setFillColor(HexColor("#09090b"))
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, height - 55, "Identity Authentication Certificate")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor("#94a3b8"))
    c.drawString(40, height - 75, "SYSTEM-GENERATED COMPLIANCE REPORT")

    # Draw Barcode representing report ID in the header space on the right
    c.setFillColor(white)
    c.roundRect(width - 200, height - 85, 160, 70, 5, fill=1, stroke=0)
    try:
        barcode = code128.Code128(timestamp.replace("_", ""), barHeight=45, barWidth=1.2)
        barcode.drawOn(c, width - 190, height - 80)
        c.setFont("Helvetica", 8)
        c.setFillColor(black)
        c.drawCentredString(width - 120, height - 30, f"AUTH-ID: {timestamp}")
    except Exception as e:
        print("Barcode exception:", e)

    # 2. Status Banner (Pass/Fail)
    status_y = height - 180
    if is_match:
        c.setFillColor(HexColor("#10b981")) # Success Green
        status_text = "STATUS: PASS (AUTHENTICATED)"
    else:
        c.setFillColor(HexColor("#ef4444")) # Danger Red
        status_text = "STATUS: FAIL (UNAUTHORIZED)"
        
    c.roundRect(40, status_y, width - 80, 50, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, status_y + 18, status_text)

    # 3. Request Metadata (Grid Box)
    meta_y = height - 350
    c.setFillColor(HexColor("#f8fafc"))
    c.setStrokeColor(HexColor("#e2e8f0"))
    c.roundRect(40, meta_y, width - 80, 130, 8, fill=0, stroke=1)
    
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(55, meta_y + 100, "Verification Details")
    
    c.setFont("Helvetica", 12)
    c.drawString(55, meta_y + 65, f"Verified Identity    : {user_name}")
    c.drawString(55, meta_y + 40, f"Timestamp            : {now.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(55, meta_y + 15, f"Operator / Node ID   : OP-AUTH-NODE-01")
    
    # SSIM Score in a large vibrant font on the right of the meta box
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(HexColor("#6366f1"))
    c.drawRightString(width - 60, meta_y + 45, f"{score:.1f}%")
    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    c.drawRightString(width - 60, meta_y + 25, "Similarity Index")

    # 4. Image Displays (Framed Boxes)
    img_y = meta_y - 280
    img_width = 230
    img_height = 200
    
    # Left Box (Reference)
    c.setStrokeColor(HexColor("#cbd5e1"))
    c.roundRect(40, img_y, img_width, img_height, 5, stroke=1)
    c.drawImage(ImageReader(buf1), 40, img_y, width=img_width, height=img_height)
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(black)
    c.drawString(40, img_y - 25, "System Record (Reference)")
    
    # Right Box (Test)
    c.roundRect(width - 40 - img_width, img_y, img_width, img_height, 5, stroke=1)
    c.drawImage(ImageReader(buf2), width - 40 - img_width, img_y, width=img_width, height=img_height)
    
    c.drawString(width - 40 - img_width, img_y - 25, "Captured Signature (Test Input)")

    # 5. Footer Line
    c.setStrokeColor(HexColor("#94a3b8"))
    c.line(40, 50, width - 40, 50)
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#94a3b8"))
    c.drawString(40, 35, "SigVerify Professional Verification System")
    c.drawRightString(width - 40, 35, f"Report ID: {timestamp}")

    c.save()
    print(f"✅ Premium PDF saved to Desktop: {full_path}")
    return full_path
