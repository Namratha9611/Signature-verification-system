// Navigation Logic
const sectionVerify = document.getElementById('section-verify');
const sectionRegister = document.getElementById('section-register');
const navVerify = document.getElementById('nav-verify');
const navRegister = document.getElementById('nav-register');

navVerify.addEventListener('click', () => {
    navVerify.classList.add('active'); navRegister.classList.remove('active');
    sectionVerify.classList.remove('hidden-section');
    sectionRegister.classList.add('hidden-section');
    loadUsers();
});

navRegister.addEventListener('click', () => {
    navRegister.classList.add('active'); navVerify.classList.remove('active');
    sectionRegister.classList.remove('hidden-section');
    sectionVerify.classList.add('hidden-section');
});

// Image State Variables
let b64TestImage = null;
let b64RegImage = null;
let latestPdfPath = null;

// User Management
const userSelect = document.getElementById('user-select');
const refImage = document.getElementById('ref-image');
const refPlaceholder = document.getElementById('ref-preview-box').querySelector('.placeholder-text');

async function loadUsers() {
    try {
        const res = await fetch('/api/users');
        const users = await res.json();
        userSelect.innerHTML = '<option value="">Select a user...</option>';
        users.forEach(user => {
            userSelect.innerHTML += `<option value="${user}">${user}</option>`;
        });
    } catch(e) { console.error('Failed to load users', e); }
}

userSelect.addEventListener('change', async (e) => {
    const name = e.target.value;
    if(!name) {
        refImage.style.display = 'none';
        refPlaceholder.style.display = 'block';
        return;
    }
    const res = await fetch('/api/user/signature', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name})
    });
    const data = await res.json();
    if(data.success) {
        refImage.src = data.image;
        refImage.style.display = 'block';
        refPlaceholder.style.display = 'none';
    }
});

loadUsers();

// File Upload Handlers
function handleFileUpload(inputEl, imgEl, placeholderEl, isTest) {
    inputEl.addEventListener('change', function() {
        if(this.files && this.files[0]){
            const reader = new FileReader();
            reader.onload = function(e){
                imgEl.src = e.target.result;
                imgEl.style.display = 'block';
                placeholderEl.style.display = 'none';
                if(isTest) b64TestImage = e.target.result;
                else b64RegImage = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
}

handleFileUpload(document.getElementById('upload-test'), document.getElementById('test-image'), document.getElementById('test-placeholder'), true);
handleFileUpload(document.getElementById('upload-reg'), document.getElementById('reg-image'), document.getElementById('reg-placeholder'), false);

// Modal Logic for Drawing & Camera
const modalOverlay = document.getElementById('modal-overlay');
const modalTitle = document.getElementById('modal-title');
const btnModalCancel = document.getElementById('btn-modal-cancel');
const btnModalSave = document.getElementById('btn-modal-save');
const btnModalClear = document.getElementById('btn-modal-clear');

const canvas = document.getElementById('signature-canvas');
const ctx = canvas.getContext('2d');
const video = document.getElementById('camera-video');

let currentMode = null; 
let currentTarget = null; 
let stream = null;

function openModal(mode, target) {
    currentMode = mode;
    currentTarget = target;
    modalOverlay.style.display = 'flex';
    
    if(mode === 'draw') {
        modalTitle.innerText = 'Draw Signature';
        canvas.style.display = 'block';
        video.style.display = 'none';
        btnModalClear.style.display = 'inline-block';
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    } else {
        modalTitle.innerText = 'Capture using Camera';
        canvas.style.display = 'none';
        video.style.display = 'block';
        btnModalClear.style.display = 'none';
        startCamera();
    }
}

function closeModal() {
    modalOverlay.style.display = 'none';
    if(stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
}

btnModalCancel.addEventListener('click', closeModal);

let drawing = false;
canvas.addEventListener('mousedown', (e) => { drawing = true; ctx.beginPath(); ctx.moveTo(e.offsetX, e.offsetY); });
canvas.addEventListener('mousemove', (e) => {
    if(drawing){
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 2;
        ctx.stroke();
    }
});
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mouseout', () => drawing = false);

btnModalClear.addEventListener('click', () => {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
});

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({video: true});
        video.srcObject = stream;
    } catch(err) {
        alert("Camera access denied or unavailable.");
        closeModal();
    }
}

btnModalSave.addEventListener('click', () => {
    let resultB64 = null;
    if(currentMode === 'draw') {
        resultB64 = canvas.toDataURL('image/png');
    } else if (currentMode === 'camera') {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = video.videoWidth; tempCanvas.height = video.videoHeight;
        tempCanvas.getContext('2d').drawImage(video, 0, 0);
        resultB64 = tempCanvas.toDataURL('image/png');
    }
    
    if(currentTarget === 'test') {
        b64TestImage = resultB64;
        document.getElementById('test-image').src = resultB64;
        document.getElementById('test-image').style.display = 'block';
        document.getElementById('test-placeholder').style.display = 'none';
    } else {
        b64RegImage = resultB64;
        document.getElementById('reg-image').src = resultB64;
        document.getElementById('reg-image').style.display = 'block';
        document.getElementById('reg-placeholder').style.display = 'none';
    }
    closeModal();
});

document.getElementById('btn-draw-test').addEventListener('click', () => openModal('draw', 'test'));
document.getElementById('btn-capture-test').addEventListener('click', () => openModal('camera', 'test'));
document.getElementById('btn-draw-reg').addEventListener('click', () => openModal('draw', 'reg'));
document.getElementById('btn-capture-reg').addEventListener('click', () => openModal('camera', 'reg'));

// API Interactions
document.getElementById('btn-save-user').addEventListener('click', async () => {
    const name = document.getElementById('reg-name').value;
    if(!name || !b64RegImage) return alert("Please provide a name and a signature.");
    
    const res = await fetch('/api/register', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, image: b64RegImage})
    });
    const data = await res.json();
    alert(data.message);
    if(data.success) {
        document.getElementById('reg-name').value = '';
        b64RegImage = null;
        document.getElementById('reg-image').style.display = 'none';
        document.getElementById('reg-placeholder').style.display = 'block';
        loadUsers();
    }
});

document.getElementById('btn-compare').addEventListener('click', async () => {
    const name = userSelect.value;
    if(!name || !b64TestImage) return alert("Please select a user and provide a test signature.");
    
    const resultBox = document.getElementById('result-box');
    resultBox.className = "result-box hidden";
    
    const res = await fetch('/api/verify', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, image: b64TestImage})
    });
    const data = await res.json();
    
    if(data.success) {
        latestPdfPath = data.pdf_path;
        resultBox.classList.remove('hidden');
        document.getElementById('result-score').innerText = `Similarity: ${data.similarity.toFixed(2)}%`;
        if(data.is_match) {
            resultBox.classList.add('success');
            document.getElementById('result-text').innerText = "✅ SIGNATURE MATCH";
        } else {
            resultBox.classList.add('fail');
            document.getElementById('result-text').innerText = "❌ NO MATCH";
        }
        
        // Show View Report button
        document.getElementById('btn-view-report').style.display = 'inline-flex';
    } else {
        alert(data.message);
    }
});

document.getElementById('btn-view-report').addEventListener('click', () => {
    if (latestPdfPath) {
        window.open('/api/view_report?path=' + encodeURIComponent(latestPdfPath), '_blank');
    }
});
