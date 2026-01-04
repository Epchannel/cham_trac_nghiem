# 🚀 OMR SHEET EVALUATION SYSTEM - NODE.JS VERSION

## 📋 Tổng Quan

Web application Node.js để chấm phiếu trắc nghiệm OMR tự động với 4 mã đề (101, 102, 103, 104).

### ✨ Tính Năng

- ✅ Upload và xử lý ảnh phiếu OMR
- ✅ Tự động nhận diện mã đề
- ✅ Chấm điểm theo 4 bộ đáp án khác nhau
- ✅ Hiển thị kết quả chi tiết
- ✅ Cảnh báo khi tô nhiều đáp án
- ✅ Giao diện hiện đại, responsive
- ✅ API RESTful
- ✅ Rate limiting & Security

---

## 🛠️ Yêu Cầu Hệ Thống

### Phần Mềm

- **Node.js** >= 14.0.0
- **npm** >= 6.0.0
- **Python** >= 3.7 (cho xử lý OMR)

### Thư Viện Python

Đã cài đặt từ trước (từ Streamlit version):
- opencv-python
- numpy
- Pillow

---

## 📦 Cài Đặt

### Bước 1: Cài đặt Dependencies

```bash
# Cài đặt Node.js packages
npm install

# Hoặc dùng Yarn
yarn install
```

### Bước 2: Cấu Hình (Tùy chọn)

```bash
# Copy file config mẫu
copy config.example.env .env

# Chỉnh sửa .env nếu cần
# Mặc định PORT=3000
```

### Bước 3: Tạo Thư Mục Uploads

```bash
# Tự động tạo khi chạy server
# Hoặc tạo thủ công:
mkdir uploads
```

---

## 🚀 Khởi Động

### Development Mode

```bash
# Chạy với nodemon (auto-reload)
npm run dev

# Hoặc chạy thông thường
npm start
```

### Production Mode

```bash
# Set NODE_ENV=production
set NODE_ENV=production

# Start server
npm start
```

Server sẽ chạy tại: **http://localhost:3000**

---

## 📡 API Endpoints

### 1. Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2026-01-04T...",
  "uptime": 123.456
}
```

### 2. Get Answer Keys

```http
GET /api/answer-keys
```

**Response:**
```json
{
  "101": "D,B,C,B,D,...",
  "102": "B,D,D,A,D,...",
  "103": "C,C,C,C,A,...",
  "104": "C,D,D,B,B,..."
}
```

### 3. Process OMR Sheet

```http
POST /api/process
Content-Type: multipart/form-data
```

**Parameters:**
- `image` (file, required): Ảnh phiếu OMR (JPG, JPEG, PNG)
- `customAnswerKey` (string, optional): Đáp án tùy chỉnh (A,B,C,D,...)

**Success Response:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "ma_de": "101",
    "correct_count": 30,
    "wrong_count": 5,
    "total_questions": 35,
    "marks_obtained": 30,
    "total_marks": 35,
    "percentage": 85.71,
    "grade": "A",
    "multiple_marks_count": 0,
    "multiple_marks": [],
    "details": [...]
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## 📁 Cấu Trúc Thư Mục

```
OMR-Sheet-Evaluation-System/
├── server.js                 # Express server
├── package.json              # Node.js dependencies
├── config.example.env        # Config template
├── api/
│   └── process_omr.py       # Python wrapper for OMR processing
├── public/
│   ├── index.html           # Frontend HTML
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── app.js           # Frontend JavaScript
├── uploads/                  # Temporary upload folder
├── functions.py              # Python OMR processing
├── util.py                   # Python utilities
└── README_NODEJS.md          # This file
```

---

## 🎨 Giao Diện

### Trang Chính

- **Upload Section**: Kéo thả hoặc click để upload ảnh
- **Custom Answer**: Nhập đáp án tùy chỉnh (optional)
- **Results Section**: Hiển thị kết quả chi tiết
- **Info Panel**: Thông tin về mã đề

### Responsive Design

- Desktop: Full layout với sidebar
- Tablet: Adaptive grid
- Mobile: Stacked layout

---

## 🔒 Bảo Mật

### Đã Tích Hợp

- ✅ **Helmet.js** - Security headers
- ✅ **CORS** - Cross-Origin Resource Sharing
- ✅ **Rate Limiting** - 100 requests/15 phút
- ✅ **File Validation** - Chỉ accept ảnh JPG/PNG
- ✅ **File Size Limit** - Max 10MB
- ✅ **Auto Cleanup** - Xóa file sau khi xử lý

### Khuyến Nghị

- Sử dụng HTTPS trong production
- Cấu hình firewall
- Thêm authentication nếu cần
- Logging & monitoring

---

## 🧪 Testing

### Test API Health

```bash
curl http://localhost:3000/api/health
```

### Test với cURL

```bash
curl -X POST http://localhost:3000/api/process \
  -F "image=@path/to/omr-sheet.jpg"
```

### Test với Python

```python
import requests

url = 'http://localhost:3000/api/process'
files = {'image': open('omr-sheet.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

---

## 🐛 Troubleshooting

### Server không khởi động

```bash
# Kiểm tra port đã bị chiếm chưa
netstat -ano | findstr :3000

# Thay đổi port trong .env
PORT=3001
```

### Lỗi Python

```bash
# Kiểm tra Python có trong PATH
python --version

# Kiểm tra thư viện
pip list | findstr opencv
```

### Lỗi Upload

- Kiểm tra thư mục `uploads/` có quyền ghi
- Kiểm tra file size < 10MB
- Kiểm tra định dạng file (JPG, PNG)

---

## 🚀 Deploy

### Deploy lên VPS/Cloud

```bash
# 1. Clone repo
git clone <repo-url>
cd OMR-Sheet-Evaluation-System

# 2. Install dependencies
npm install

# 3. Set environment
export NODE_ENV=production
export PORT=80

# 4. Start with PM2 (recommended)
npm install -g pm2
pm2 start server.js --name omr-system
pm2 save
pm2 startup
```

### Deploy lên Heroku

```bash
# 1. Login
heroku login

# 2. Create app
heroku create omr-system

# 3. Add buildpacks
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add heroku/python

# 4. Deploy
git push heroku main

# 5. Open
heroku open
```

### Deploy lên Railway/Render

1. Connect GitHub repo
2. Set build command: `npm install`
3. Set start command: `npm start`
4. Add environment variables
5. Deploy!

---

## 📊 Performance

### Optimization Tips

1. **Enable gzip compression**
```javascript
app.use(compression());
```

2. **Add caching**
```javascript
app.use(express.static('public', { maxAge: '1d' }));
```

3. **Use CDN** cho static files

4. **Database** cho lưu kết quả (optional)

---

## 🔄 Roadmap

### Planned Features

- [ ] User authentication
- [ ] Result history & database
- [ ] Batch processing (nhiều phiếu)
- [ ] Export to Excel/PDF
- [ ] Email notification
- [ ] Admin dashboard
- [ ] Multi-language support
- [ ] Dark mode

---

## 📝 License

MIT License - Xem file LICENSE

---

## 👥 Contributing

Contributions welcome! Please:

1. Fork repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📞 Support

- **Email**: support@omr-system.com
- **GitHub Issues**: [Create Issue](https://github.com/...)
- **Documentation**: [Wiki](https://github.com/.../wiki)

---

## 🎉 Credits

- **OpenCV** - Image processing
- **Express.js** - Web framework
- **Node.js** - Runtime
- **Python** - OMR algorithm

---

**Version**: 2.0.0  
**Last Updated**: 04/01/2026  
**Status**: ✅ Ready for Production

---

## 🚀 Quick Start Summary

```bash
# 1. Install
npm install

# 2. Run
npm start

# 3. Open
http://localhost:3000

# 4. Upload OMR sheet and see results!
```

**Enjoy! 🎉📝**

