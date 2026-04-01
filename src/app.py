import os
import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from skimage.metrics import structural_similarity as ssim
from database import register_user, get_user_signature, get_all_users
from report_generator import generate_pdf_report

app = Flask(__name__)
CORS(app)

def base64_to_cv2(base64_string):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def cv2_to_base64(img):
    _, buffer = cv2.imencode('.png', img)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(get_all_users())

@app.route('/api/user/signature', methods=['POST'])
def get_signature():
    data = request.json
    name = data.get('name')
    img = get_user_signature(name)
    if img is not None:
        return jsonify({'success': True, 'image': cv2_to_base64(img)})
    return jsonify({'success': False, 'message': 'Signature not found'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    b64_img = data.get('image')
    if not name or not b64_img:
        return jsonify({'success': False, 'message': 'Name and signature required.'})
    
    img = base64_to_cv2(b64_img)
    if img is None:
        return jsonify({'success': False, 'message': 'Invalid image format.'})
        
    success, msg = register_user(name, img)
    return jsonify({'success': success, 'message': msg})

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    user_name = data.get('name')
    b64_test_img = data.get('image')
    
    if not user_name or not b64_test_img:
        return jsonify({'success': False, 'message': 'Missing data.'})

    test_img = base64_to_cv2(b64_test_img)
    ref_img = get_user_signature(user_name)
    
    if ref_img is None:
        return jsonify({'success': False, 'message': 'User reference not found.'})

    # Compare
    gray1 = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.resize(gray1, (300, 300))
    gray2 = cv2.resize(gray2, (300, 300))

    score = ssim(gray1, gray2) * 100
    is_match = score >= 82

    # Generate Report
    try:
        pdf_path = generate_pdf_report(ref_img, test_img, score, is_match, user_name)
    except Exception as e:
        pdf_path = f"Error generating PDF: {str(e)}"

    return jsonify({
        'success': True,
        'similarity': score,
        'is_match': bool(is_match),
        'pdf_path': pdf_path
    })

@app.route('/api/view_report', methods=['GET'])
def view_report():
    path = request.args.get('path')
    if path and os.path.exists(path):
        return send_file(path, as_attachment=False)
    return "Report not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
