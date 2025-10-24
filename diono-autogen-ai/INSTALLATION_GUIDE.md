# Complete Installation Guide for All Platforms

This guide will help you install and run DionoAutogen AI on your computer, regardless of your operating system or technical experience.

## 📋 System Requirements

### Minimum Requirements
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space (500GB SSD recommended)
- **Internet**: Required for initial setup and LLM usage

### Supported Operating Systems
- ✅ macOS (Intel & Apple Silicon M1/M2/M3)
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

---

## 🍎 macOS Installation

### Step 1: Install Homebrew (Package Manager)

Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter) and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions. This may take 5-10 minutes.

### Step 2: Install Required Software

In Terminal, run these commands one by one:

```bash
# Install Docker Desktop
brew install --cask docker

# Install jq (JSON processor)
brew install jq

# Install Tesseract (for image text extraction)
brew install tesseract

# Install FFmpeg (for video processing)
brew install ffmpeg

# Install Git (if not already installed)
brew install git
```

### Step 3: Start Docker Desktop

1. Open **Spotlight** (Cmd + Space)
2. Type "Docker" and press Enter
3. Wait for Docker to start (whale icon in menu bar)
4. Click the whale icon and ensure it says "Docker Desktop is running"

### Step 4: Download DionoAutogen AI

In Terminal:

```bash
# Navigate to your home directory
cd ~

# Clone the repository
git clone https://github.com/Joshua1476/DeepAnalyze.git

# Enter the project directory
cd DeepAnalyze/diono-autogen-ai
```

### Step 5: Configure the Application

```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Make scripts executable
chmod +x scripts/*.sh
chmod +x start.sh stop.sh
```

### Step 6: Start the Application

```bash
# Start all services
./start.sh
```

**First-time startup takes 5-10 minutes** as it downloads required images.

### Step 7: Access the Application

Open your web browser and go to:
- **Application**: http://localhost:3000
- **Login**: username: `demo`, password: `demo`

### Troubleshooting macOS

**Docker won't start:**
- Make sure you have at least 4GB RAM allocated to Docker
- Go to Docker Desktop → Settings → Resources → Memory
- Set to at least 4GB (8GB recommended)

**Port already in use:**
```bash
# Find what's using port 3000
lsof -i :3000
# Kill the process (replace PID with actual number)
kill -9 PID
```

**Apple Silicon (M1/M2/M3) specific:**
- Docker Desktop for Mac automatically handles ARM architecture
- All images will run correctly on Apple Silicon

---

## 🪟 Windows Installation

### Step 1: Enable WSL2 (Windows Subsystem for Linux)

1. Open **PowerShell as Administrator**:
   - Press `Win + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. Run this command:
```powershell
wsl --install
```

3. **Restart your computer** when prompted

4. After restart, open PowerShell again and run:
```powershell
wsl --set-default-version 2
```

### Step 2: Install Docker Desktop

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Run the installer
3. During installation, ensure "Use WSL 2 instead of Hyper-V" is checked
4. Restart your computer when installation completes
5. Start Docker Desktop from Start Menu
6. Wait for Docker to start (whale icon in system tray)

### Step 3: Install Git

1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (just click "Next" through all options)

### Step 4: Install Additional Tools

Open **PowerShell** (not as admin) and run:

```powershell
# Install Chocolatey (package manager)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Close and reopen PowerShell, then install tools
choco install jq tesseract ffmpeg -y
```

### Step 5: Download DionoAutogen AI

In PowerShell:

```powershell
# Navigate to your Documents folder
cd $HOME\Documents

# Clone the repository
git clone https://github.com/Joshua1476/DeepAnalyze.git

# Enter the project directory
cd DeepAnalyze\diono-autogen-ai
```

### Step 6: Configure the Application

```powershell
# Copy environment files
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

### Step 7: Start the Application

```powershell
# Start all services (PowerShell script)
.\start.ps1
```

**Note**: If you get an error about execution policy, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative**: If you prefer using bash, you can use Git Bash or WSL:
```bash
# In Git Bash or WSL
./start.sh
```

### Step 8: Access the Application

Open your web browser and go to:
- **Application**: http://localhost:3000
- **Login**: username: `demo`, password: `demo`

### Troubleshooting Windows

**WSL2 not working:**
- Ensure virtualization is enabled in BIOS
- Run: `wsl --status` to check WSL version
- Update WSL: `wsl --update`

**Docker Desktop won't start:**
- Ensure WSL2 is running: `wsl --list --verbose`
- Restart Docker Desktop
- Check Docker Desktop → Settings → Resources

**Firewall blocking:**
- Windows Defender may ask for permission
- Click "Allow access" when prompted

---

## 🐧 Linux Installation

### Ubuntu/Debian

Open **Terminal** (Ctrl + Alt + T) and run:

```bash
# Update package list
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional tools
sudo apt-get install -y git jq tesseract-ocr ffmpeg

# Log out and log back in for Docker permissions to take effect
```

### Fedora/RHEL

```bash
# Install Docker
sudo dnf install -y docker docker-compose

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install additional tools
sudo dnf install -y git jq tesseract ffmpeg

# Log out and log back in
```

### Download and Start

```bash
# Navigate to home directory
cd ~

# Clone repository
git clone https://github.com/Joshua1476/DeepAnalyze.git
cd DeepAnalyze/diono-autogen-ai

# Configure
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
chmod +x scripts/*.sh start.sh stop.sh

# Start application
./start.sh
```

### Access the Application

Open browser: http://localhost:3000  
Login: `demo` / `demo`

### Troubleshooting Linux

**Permission denied:**
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

**Port conflicts:**
```bash
# Check what's using port
sudo lsof -i :3000
# Stop the service or change port in docker-compose.yml
```

---

## 🎯 Quick Start Guide (All Platforms)

Once installed, here's how to use DionoAutogen AI:

### Starting the Application

```bash
cd DeepAnalyze/diono-autogen-ai
./start.sh
```

Wait 2-3 minutes for all services to start.

### Stopping the Application

```bash
./stop.sh
```

### Using the Application

1. **Open browser**: http://localhost:3000
2. **Login**: demo / demo
3. **Create a project**: Click "New Project"
4. **Describe what you want**: Type in plain English
5. **Let AI build it**: Watch as code is generated
6. **Upload media**: Drag and drop images/videos for processing

### Example Tasks

**Create a web app:**
```
Create a simple todo list web application with React
```

**Process an image:**
1. Upload an image with text
2. System automatically extracts text
3. View results in the interface

**Process a video:**
1. Upload a video with speech
2. System automatically transcribes audio
3. View transcript

---

## 💾 System Optimization for 16GB RAM

### Recommended Docker Settings

**macOS/Windows:**
1. Open Docker Desktop
2. Go to Settings → Resources
3. Set:
   - **Memory**: 8GB (half of your RAM)
   - **CPUs**: 4 cores
   - **Disk**: 50GB

**Linux:**
Docker uses system resources directly, no configuration needed.

### Reducing Memory Usage

Edit `docker-compose.yml` and adjust:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2g  # Reduce if needed
```

### Freeing Up Space

```bash
# Remove unused Docker images
docker system prune -a

# Remove old containers
docker container prune

# Check disk usage
docker system df
```

---

## 🆘 Common Issues and Solutions

### "Cannot connect to Docker daemon"

**Solution:**
- Ensure Docker Desktop is running
- Check system tray/menu bar for Docker icon
- Restart Docker Desktop

### "Port 3000 already in use"

**Solution:**
```bash
# Find and kill the process
# macOS/Linux:
lsof -i :3000
kill -9 <PID>

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### "Out of memory" errors

**Solution:**
1. Close other applications
2. Increase Docker memory allocation
3. Restart Docker Desktop

### Application won't start

**Solution:**
```bash
# Stop everything
./stop.sh

# Remove old containers
docker-compose down -v

# Start fresh
./start.sh
```

### Slow performance

**Solution:**
1. Ensure you have at least 8GB RAM allocated to Docker
2. Close unnecessary applications
3. Use SSD instead of HDD
4. Reduce `SANDBOX_MAX_WORKERS` in backend/.env to 2

---

## 📱 Accessing from Other Devices

### On Same Network

1. Find your computer's IP address:

**macOS/Linux:**
```bash
ifconfig | grep "inet "
```

**Windows:**
```powershell
ipconfig
```

2. On other device, open browser to:
```
http://YOUR_IP_ADDRESS:3000
```

Example: `http://192.168.1.100:3000`

---

## 🔄 Updating DionoAutogen AI

```bash
cd DeepAnalyze/diono-autogen-ai

# Stop application
./stop.sh

# Get latest updates
git pull

# Rebuild and restart
docker-compose build
./start.sh
```

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

2. **Restart services:**
   ```bash
   ./stop.sh
   ./start.sh
   ```

3. **Check system requirements:**
   - Ensure you have enough RAM
   - Ensure you have enough disk space
   - Ensure Docker is running

4. **Search for error messages** in the logs

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Docker Desktop is running
- [ ] Can access http://localhost:3000
- [ ] Can login with demo/demo
- [ ] Can create a new project
- [ ] Can upload an image (OCR works)
- [ ] Can upload a video (transcription works)
- [ ] Can execute code in sandbox

If all checks pass, you're ready to use DionoAutogen AI! 🎉
