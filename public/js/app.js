// Global state
let selectedFile = null;
let cameraStream = null;
let currentMode = 'upload'; // 'upload' or 'camera'

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const btnRemove = document.getElementById('btnRemove');
const btnProcess = document.getElementById('btnProcess');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const customAnswerKey = document.getElementById('customAnswerKey');

// Camera Elements
const btnUploadMode = document.getElementById('btnUploadMode');
const btnCameraMode = document.getElementById('btnCameraMode');
const uploadMode = document.getElementById('uploadMode');
const cameraMode = document.getElementById('cameraMode');
const cameraVideo = document.getElementById('cameraVideo');
const cameraCanvas = document.getElementById('cameraCanvas');
const btnStartCamera = document.getElementById('btnStartCamera');
const btnCapture = document.getElementById('btnCapture');
const btnStopCamera = document.getElementById('btnStopCamera');
const capturedPreview = document.getElementById('capturedPreview');
const capturedImg = document.getElementById('capturedImg');
const btnRemoveCaptured = document.getElementById('btnRemoveCaptured');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    console.log('OMR System initialized');
});

// Setup Event Listeners
function setupEventListeners() {
    // Mode toggle
    btnUploadMode.addEventListener('click', () => switchMode('upload'));
    btnCameraMode.addEventListener('click', () => switchMode('camera'));
    
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag & Drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Remove image
    btnRemove.addEventListener('click', removeImage);
    
    // Camera controls
    btnStartCamera.addEventListener('click', startCamera);
    btnCapture.addEventListener('click', captureImage);
    btnStopCamera.addEventListener('click', stopCamera);
    btnRemoveCaptured.addEventListener('click', removeCaptured);
    
    // Process button
    btnProcess.addEventListener('click', processOMR);
    
    // New scan button
    document.getElementById('btnNew')?.addEventListener('click', resetForm);
    
    // Retry button
    document.getElementById('btnRetry')?.addEventListener('click', resetForm);
    
    // Print button
    document.getElementById('btnPrint')?.addEventListener('click', () => window.print());
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

// Handle drag over
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

// Handle drop
function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        processFile(file);
    }
}

// Process file
function processFile(file) {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
        showError('Chỉ chấp nhận file ảnh (JPG, JPEG, PNG)!');
        return;
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File quá lớn! Kích thước tối đa là 10MB.');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadArea.style.display = 'none';
        imagePreview.style.display = 'block';
        btnProcess.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Remove image
function removeImage() {
    selectedFile = null;
    fileInput.value = '';
    previewImg.src = '';
    uploadArea.style.display = 'block';
    imagePreview.style.display = 'none';
    btnProcess.disabled = true;
}

// ==================== CAMERA FUNCTIONS ====================

// Switch mode between upload and camera
function switchMode(mode) {
    currentMode = mode;
    
    if (mode === 'upload') {
        btnUploadMode.classList.add('active');
        btnCameraMode.classList.remove('active');
        uploadMode.style.display = 'block';
        cameraMode.style.display = 'none';
        stopCamera();
    } else {
        btnCameraMode.classList.add('active');
        btnUploadMode.classList.remove('active');
        cameraMode.style.display = 'block';
        uploadMode.style.display = 'none';
        removeImage();
    }
    
    // Reset results
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Start camera
async function startCamera() {
    try {
        // Request camera access with high resolution
        const constraints = {
            video: {
                width: { ideal: 1920 },
                height: { ideal: 1080 },
                facingMode: 'environment' // Use back camera on mobile
            }
        };
        
        cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
        cameraVideo.srcObject = cameraStream;
        
        // Show/hide buttons
        btnStartCamera.style.display = 'none';
        btnCapture.style.display = 'inline-block';
        btnStopCamera.style.display = 'inline-block';
        
        console.log('Camera started successfully');
    } catch (error) {
        console.error('Camera error:', error);
        showError('Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập camera.');
    }
}

// Stop camera
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraVideo.srcObject = null;
        cameraStream = null;
        
        // Show/hide buttons
        btnStartCamera.style.display = 'inline-block';
        btnCapture.style.display = 'none';
        btnStopCamera.style.display = 'none';
        
        console.log('Camera stopped');
    }
}

// Capture image from camera
function captureImage() {
    if (!cameraStream) {
        showError('Camera chưa được bật!');
        return;
    }
    
    // Set canvas size to match video
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;
    
    // Draw video frame to canvas
    const ctx = cameraCanvas.getContext('2d');
    ctx.drawImage(cameraVideo, 0, 0);
    
    // Convert to blob
    cameraCanvas.toBlob((blob) => {
        if (blob) {
            // Create file from blob
            const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
            selectedFile = file;
            
            // Show preview
            const url = URL.createObjectURL(blob);
            capturedImg.src = url;
            capturedPreview.style.display = 'block';
            
            // Stop camera
            stopCamera();
            
            // Enable process button
            btnProcess.disabled = false;
            
            console.log('Image captured successfully');
        }
    }, 'image/jpeg', 0.95);
}

// Remove captured image
function removeCaptured() {
    selectedFile = null;
    capturedImg.src = '';
    capturedPreview.style.display = 'none';
    btnProcess.disabled = true;
    startCamera();
}

// ==================== END CAMERA FUNCTIONS ====================

// Process OMR
async function processOMR() {
    if (!selectedFile) {
        showError('Vui lòng chọn ảnh phiếu trắc nghiệm!');
        return;
    }
    
    // Hide results/errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Show loading
    loading.style.display = 'block';
    btnProcess.disabled = true;
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        // Add custom answer key if provided
        const customKey = customAnswerKey.value.trim();
        if (customKey) {
            formData.append('customAnswerKey', customKey);
        }
        
        // Send request
        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        // Hide loading
        loading.style.display = 'none';
        
        if (result.success && result.data.success) {
            displayResults(result.data);
        } else {
            showError(result.data?.error || result.error || 'Lỗi khi xử lý phiếu');
        }
        
    } catch (error) {
        console.error('Error:', error);
        loading.style.display = 'none';
        showError('Lỗi kết nối server. Vui lòng thử lại!');
    }
}

// Display results
function displayResults(data) {
    // Display images
    if (data.warped_image) {
        document.getElementById('originalImage').src = data.warped_image;
    }
    if (data.result_image) {
        document.getElementById('resultImage').src = data.result_image;
    }
    
    // Update stats
    document.getElementById('statMaDe').textContent = data.ma_de;
    document.getElementById('statCorrect').textContent = `${data.correct_count}/${data.total_questions}`;
    document.getElementById('statScore').textContent = `${data.marks_obtained}/${data.total_marks}`;
    document.getElementById('statGrade').textContent = data.grade;
    
    // Update progress bar
    const percentage = data.percentage;
    document.getElementById('progressFill').style.width = `${percentage}%`;
    document.getElementById('progressText').textContent = `${percentage.toFixed(1)}%`;
    
    // Update progress bar color based on percentage
    const progressFill = document.getElementById('progressFill');
    if (percentage >= 80) {
        progressFill.style.background = 'linear-gradient(90deg, #10B981, #34D399)';
    } else if (percentage >= 50) {
        progressFill.style.background = 'linear-gradient(90deg, #F59E0B, #FBBF24)';
    } else {
        progressFill.style.background = 'linear-gradient(90deg, #EF4444, #F87171)';
    }
    
    // Show warning if multiple marks
    const warningMultiple = document.getElementById('warningMultiple');
    if (data.multiple_marks_count > 0) {
        document.getElementById('multipleCount').textContent = data.multiple_marks_count;
        document.getElementById('multipleList').textContent = data.multiple_marks.map(q => `Câu ${q}`).join(', ');
        warningMultiple.style.display = 'block';
    } else {
        warningMultiple.style.display = 'none';
    }
    
    // Display details
    displayDetails(data.details);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display question details
function displayDetails(details) {
    const detailsGrid = document.getElementById('detailsGrid');
    detailsGrid.innerHTML = '';
    
    details.forEach(item => {
        const div = document.createElement('div');
        div.className = 'detail-item';
        
        // Add appropriate class
        if (item.is_multiple) {
            div.classList.add('multiple');
        } else if (item.is_correct) {
            div.classList.add('correct');
        } else {
            div.classList.add('wrong');
        }
        
        // Status icon
        let statusIcon = '';
        if (item.is_multiple) {
            statusIcon = '⚠️';
        } else if (item.is_correct) {
            statusIcon = '✅';
        } else if (item.is_empty) {
            statusIcon = '⭕';
        } else {
            statusIcon = '❌';
        }
        
        // Display student answer
        let studentAns = item.student_answer || '(Trống)';
        if (item.is_multiple) {
            studentAns = '(Nhiều)';
        }
        
        div.innerHTML = `
            <div class="detail-question">Câu ${item.question}</div>
            <div class="detail-answer">
                <strong>${studentAns}</strong> → ${item.correct_answer}
            </div>
            <div class="detail-status">${statusIcon}</div>
        `;
        
        detailsGrid.appendChild(div);
    });
}

// Show error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.style.display = 'block';
    btnProcess.disabled = false;
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Reset form
function resetForm() {
    removeImage();
    
    // Also clear captured image if in camera mode
    if (currentMode === 'camera') {
        selectedFile = null;
        capturedImg.src = '';
        capturedPreview.style.display = 'none';
        btnProcess.disabled = true;
    }
    
    customAnswerKey.value = '';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Utility: Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Check API health on load
fetch('/api/health')
    .then(res => res.json())
    .then(data => console.log('API Health:', data))
    .catch(err => console.error('API Health Check Failed:', err));

