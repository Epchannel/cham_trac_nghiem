const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet({
    contentSecurityPolicy: false, // Disable for easier development
}));
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('combined'));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Serve static files
app.use(express.static('public'));

// Create uploads directory if not exists
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadsDir);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, 'omr-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB
    },
    fileFilter: (req, file, cb) => {
        const allowedTypes = /jpeg|jpg|png/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);
        
        if (extname && mimetype) {
            return cb(null, true);
        } else {
            cb(new Error('Chỉ chấp nhận file ảnh (JPEG, JPG, PNG)!'));
        }
    }
});

// API Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Get answer keys
app.get('/api/answer-keys', (req, res) => {
    const answerKeys = {
        "101": "D,B,C,B,D,C,B,A,B,D,D,C,B,D,D,A,D,A,D,A,D,B,C,D,B,A,A,A,B,D,C,A,A,B,D",
        "102": "B,D,D,A,D,D,C,A,A,A,B,A,B,B,C,B,C,B,C,D,D,B,D,B,A,D,D,A,A,A,D,C,C,B,A",
        "103": "C,C,C,C,A,A,A,C,D,D,A,B,A,D,A,C,C,C,D,C,D,D,B,A,A,C,C,D,D,B,C,A,B,A,D",
        "104": "C,D,D,B,B,A,A,D,B,C,C,A,D,D,A,A,C,B,C,A,D,C,A,A,A,D,A,D,D,A,D,B,B,B,C"
    };
    res.json(answerKeys);
});

// Process OMR sheet
app.post('/api/process', upload.single('image'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({
            success: false,
            error: 'Không có file ảnh được upload!'
        });
    }

    const imagePath = req.file.path;
    const customAnswerKey = req.body.customAnswerKey || null;
    
    console.log(`Processing OMR sheet: ${imagePath}`);
    
    try {
        // Call Python script to process OMR
        const pythonProcess = spawn('python', [
            path.join(__dirname, 'api', 'process_omr.py'),
            imagePath,
            customAnswerKey || ''
        ]);

        let resultData = '';
        let errorData = '';

        pythonProcess.stdout.on('data', (data) => {
            resultData += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
            console.error('Python Error:', data.toString());
        });

        pythonProcess.on('close', (code) => {
            // Clean up uploaded file
            fs.unlink(imagePath, (err) => {
                if (err) console.error('Error deleting file:', err);
            });

            if (code !== 0) {
                console.error('Python process failed:', errorData);
                return res.status(500).json({
                    success: false,
                    error: 'Không thể xử lý phiếu. Vui lòng kiểm tra lại ảnh.',
                    details: errorData
                });
            }

            try {
                const result = JSON.parse(resultData);
                res.json({
                    success: true,
                    data: result
                });
            } catch (e) {
                console.error('JSON parse error:', e);
                console.error('Result data:', resultData);
                res.status(500).json({
                    success: false,
                    error: 'Lỗi khi xử lý kết quả',
                    details: resultData
                });
            }
        });

    } catch (error) {
        console.error('Error processing OMR:', error);
        
        // Clean up uploaded file
        fs.unlink(imagePath, (err) => {
            if (err) console.error('Error deleting file:', err);
        });
        
        res.status(500).json({
            success: false,
            error: 'Lỗi server khi xử lý phiếu',
            details: error.message
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Error:', err);
    
    if (err instanceof multer.MulterError) {
        if (err.code === 'LIMIT_FILE_SIZE') {
            return res.status(400).json({
                success: false,
                error: 'File quá lớn! Kích thước tối đa là 10MB.'
            });
        }
    }
    
    res.status(500).json({
        success: false,
        error: err.message || 'Lỗi server'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint không tồn tại'
    });
});

// Start server
app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('  🚀 OMR SHEET EVALUATION SYSTEM - NODE.JS');
    console.log('='.repeat(60));
    console.log(`  Server running on: http://localhost:${PORT}`);
    console.log(`  Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`  Uploads directory: ${uploadsDir}`);
    console.log('='.repeat(60));
    console.log('  API Endpoints:');
    console.log(`    GET  /api/health        - Health check`);
    console.log(`    GET  /api/answer-keys   - Get answer keys`);
    console.log(`    POST /api/process       - Process OMR sheet`);
    console.log('='.repeat(60));
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    server.close(() => {
        console.log('HTTP server closed');
    });
});

