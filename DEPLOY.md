# 🚀 HƯỚNG DẪN DEPLOY - OMR SYSTEM

## 📋 Tổng Quan

Hướng dẫn deploy ứng dụng Node.js OMR lên các nền tảng phổ biến.

---

## 🔧 Chuẩn Bị

### 1. Kiểm Tra Hệ Thống

```bash
# Node.js version
node --version  # >= 14.0.0

# npm version
npm --version   # >= 6.0.0

# Python version
python --version  # >= 3.7
```

### 2. Test Local

```bash
# Install dependencies
npm install

# Start server
npm start

# Test API
curl http://localhost:3000/api/health
```

---

## 🌐 Deploy lên VPS (Ubuntu/Debian)

### Bước 1: Cài Đặt Môi Trường

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python & pip
sudo apt install -y python3 python3-pip

# Install OpenCV dependencies
sudo apt install -y python3-opencv libopencv-dev
pip3 install opencv-python numpy pillow
```

### Bước 2: Upload Code

```bash
# Option 1: Git clone
cd /var/www
sudo git clone https://github.com/your-repo/omr-system.git
cd omr-system

# Option 2: SCP/SFTP
# Upload files manually
```

### Bước 3: Cài Đặt Dependencies

```bash
# Install Node.js packages
npm install --production

# Set permissions
sudo chown -R $USER:$USER /var/www/omr-system
chmod -R 755 /var/www/omr-system
```

### Bước 4: Cấu Hình Environment

```bash
# Create .env file
nano .env
```

```env
PORT=3000
NODE_ENV=production
```

### Bước 5: Chạy với PM2

```bash
# Install PM2
sudo npm install -g pm2

# Start app
pm2 start server.js --name omr-system

# Auto-start on boot
pm2 startup
pm2 save

# Monitor
pm2 monit
```

### Bước 6: Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/omr-system
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Upload size
        client_max_body_size 10M;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/omr-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Bước 7: SSL với Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## ☁️ Deploy lên Heroku

### Bước 1: Chuẩn Bị

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

### Bước 2: Tạo App

```bash
# Create app
heroku create omr-system-app

# Add buildpacks
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add heroku/python
```

### Bước 3: Cấu Hình

```bash
# Set environment
heroku config:set NODE_ENV=production

# Check config
heroku config
```

### Bước 4: Deploy

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial deploy"

# Add Heroku remote
heroku git:remote -a omr-system-app

# Push to Heroku
git push heroku main

# Open app
heroku open
```

### Bước 5: Monitor

```bash
# View logs
heroku logs --tail

# Check status
heroku ps

# Restart
heroku restart
```

---

## 🚂 Deploy lên Railway

### Bước 1: Tạo Account

1. Truy cập [railway.app](https://railway.app)
2. Login với GitHub

### Bước 2: Deploy

1. Click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Chọn repository của bạn
4. Railway tự động detect và build

### Bước 3: Cấu Hình

1. Vào **Variables** tab
2. Thêm environment variables:
   - `PORT` = 3000
   - `NODE_ENV` = production

### Bước 4: Custom Domain (Optional)

1. Vào **Settings** tab
2. Click **"Generate Domain"**
3. Hoặc add custom domain

---

## 🎨 Deploy lên Render

### Bước 1: Tạo Account

1. Truy cập [render.com](https://render.com)
2. Login với GitHub

### Bước 2: Tạo Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Cấu hình:
   - **Name**: omr-system
   - **Environment**: Node
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`

### Bước 3: Environment Variables

Thêm trong **Environment** tab:
```
NODE_ENV=production
PORT=3000
```

### Bước 4: Deploy

- Click **"Create Web Service"**
- Render tự động deploy

---

## 🐳 Deploy với Docker

### Bước 1: Tạo Dockerfile

```dockerfile
FROM node:18-alpine

# Install Python
RUN apk add --no-cache python3 py3-pip

# Install OpenCV
RUN apk add --no-cache \
    opencv \
    py3-opencv \
    py3-numpy \
    py3-pillow

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install --production

# Copy application files
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

### Bước 2: Tạo docker-compose.yml

```yaml
version: '3.8'

services:
  omr-system:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

### Bước 3: Build & Run

```bash
# Build image
docker build -t omr-system .

# Run container
docker run -d -p 3000:3000 --name omr-system omr-system

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f omr-system
```

---

## 📊 Post-Deploy Checklist

### ✅ Kiểm Tra

- [ ] Server đang chạy
- [ ] API `/api/health` trả về OK
- [ ] Upload file hoạt động
- [ ] Process OMR thành công
- [ ] Kết quả hiển thị đúng

### ✅ Monitoring

```bash
# Check server status
curl https://your-domain.com/api/health

# Monitor with PM2 (VPS)
pm2 monit

# View logs (Heroku)
heroku logs --tail

# View logs (Docker)
docker logs -f omr-system
```

### ✅ Security

- [ ] HTTPS enabled
- [ ] Firewall configured
- [ ] Rate limiting active
- [ ] File validation working
- [ ] Auto cleanup uploads

---

## 🔧 Troubleshooting

### Server Không Start

```bash
# Check logs
pm2 logs omr-system

# Check port
netstat -tulpn | grep 3000

# Check Python
which python3
python3 --version
```

### Upload Lỗi

```bash
# Check permissions
ls -la uploads/

# Fix permissions
chmod 755 uploads/
```

### Python Script Lỗi

```bash
# Test directly
python3 api/process_omr.py path/to/test-image.jpg

# Check libraries
pip3 list | grep opencv
```

---

## 📈 Optimization Tips

### 1. Caching

```javascript
// In server.js
const compression = require('compression');
app.use(compression());
```

### 2. CDN

- Upload static files to CDN
- Update paths in HTML

### 3. Load Balancer

- Use Nginx load balancing
- Multiple PM2 instances

### 4. Database

- Add MongoDB/PostgreSQL
- Store results history

---

## 🎉 Done!

Ứng dụng đã được deploy thành công!

**Test:** https://your-domain.com

---

**Cần hỗ trợ?** Xem [README_NODEJS.md](README_NODEJS.md)

