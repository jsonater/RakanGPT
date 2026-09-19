# Deployment Guide - Make RakanGPT Public

This guide covers deploying RakanGPT as a public web application on various platforms.

## 📋 Table of Contents

1. [Heroku (Easiest)](#heroku)
2. [Railway](#railway)
3. [Render](#render)
4. [PythonAnywhere](#pythonanywhere)
5. [AWS](#aws)
6. [Local Server](#local)

---

## Heroku Deployment

**Best for:** Free/paid hosting, very beginner-friendly

### Prerequisites
- Heroku account (https://www.heroku.com)
- Heroku CLI installed
- Git initialized in your project

### Steps

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create a Heroku app:**
```bash
heroku create your-app-name
```

3. **Create `Procfile`** (tells Heroku how to run your app):
```
web: gunicorn app:app
```

4. **Create `runtime.txt`** (specify Python version):
```
python-3.11.7
```

5. **Update requirements.txt** (add gunicorn):
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

6. **Set environment variable:**
```bash
heroku config:set ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"
```

7. **Deploy:**
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

8. **View your app:**
```bash
heroku open
```

Your app is now live at: `https://your-app-name.herokuapp.com`

**Cost:** Free tier available (limited), paid plans start at $7/month

---

## Railway Deployment

**Best for:** Simple deployment, pay-as-you-go pricing

### Prerequisites
- Railway account (https://railway.app)
- GitHub account (to connect your repo)

### Steps

1. **Push your code to GitHub:**
```bash
git remote add origin https://github.com/yourusername/RakanGPT.git
git push -u origin main
```

2. **Go to Railway.app and login**

3. **Create new project → Deploy from GitHub**

4. **Select your RakanGPT repository**

5. **Add environment variables:**
   - Click "Add Variable"
   - Name: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-YOUR-KEY-HERE`

6. **Railway auto-deploys** - your app is live!

**Cost:** $5/month free credit, then pay for usage

---

## Render Deployment

**Best for:** Free tier with good features

### Prerequisites
- Render account (https://render.com)
- GitHub account

### Steps

1. **Push to GitHub** (if not already done):
```bash
git remote add origin https://github.com/yourusername/RakanGPT.git
git push -u origin main
```

2. **On Render.com, click "New" → "Web Service"**

3. **Connect your GitHub repository**

4. **Fill in settings:**
   - **Name:** rakangpt
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. **Add environment variables:**
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** `sk-ant-YOUR-KEY-HERE`

6. **Click Deploy**

**Cost:** Free tier available ($0-$7/month)

---

## PythonAnywhere Deployment

**Best for:** Hosted Python environment, very easy

### Prerequisites
- PythonAnywhere account (https://www.pythonanywhere.com)

### Steps

1. **Upload your files:**
   - Go to Files tab
   - Create folder `/rakangpt`
   - Upload all project files

2. **Create Web App:**
   - Click "Web" → "Add New Web App"
   - Choose "Python 3.11" + Flask

3. **Configure WSGI file:**
   - PythonAnywhere creates `flask_app.py`
   - Edit to point to your `app.py`

4. **Install packages:**
   - Go to "Web" tab
   - Click "Virtualenv"
   - Upload `requirements.txt` and run:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables:**
   - Edit WSGI file to include:
   ```python
   import os
   os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-YOUR-KEY-HERE'
   ```

6. **Reload web app**

Your app is live at: `https://yourusername.pythonanywhere.com`

**Cost:** Free tier available, paid plans from $5/month

---

## AWS Deployment (EC2)

**Best for:** Scalable, professional deployment

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04)
- SSH access to instance

### Steps

1. **Connect to your instance via SSH**

2. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git
```

3. **Clone your repository:**
```bash
git clone https://github.com/yourusername/RakanGPT.git
cd RakanGPT
```

4. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

5. **Set environment variable:**
```bash
export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"
```

6. **Test run:**
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

7. **Install Nginx (reverse proxy):**
```bash
sudo apt install nginx
```

8. **Configure Nginx:**
Create `/etc/nginx/sites-available/rakangpt`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable it:
```bash
sudo ln -s /etc/nginx/sites-available/rakangpt /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

9. **Run app with systemd:**
Create `/etc/systemd/system/rakangpt.service`:
```ini
[Unit]
Description=RakanGPT Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/RakanGPT
Environment="ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE"
ExecStart=/home/ubuntu/RakanGPT/venv/bin/gunicorn app:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rakangpt
sudo systemctl start rakangpt
```

Your app is live at: `http://your-ec2-ip` or your domain

**Cost:** $3-30/month depending on instance size

---

## Local Server Deployment

**Best for:** Testing, or hosting on your own machine

### Prerequisites
- Static IP or dynamic DNS service

### Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install gunicorn
```

2. **Set environment variable:**
```bash
export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"
```

3. **Run production server:**
```bash
gunicorn app:app --bind 0.0.0.0:8000
```

4. **Set up port forwarding:**
   - Log into your router
   - Forward port 80 (or 8000) to your computer's local IP

5. **Get a domain (optional):**
   - Use DuckDNS (free): https://www.duckdns.org
   - Get HTTPS certificate with Let's Encrypt

**Cost:** Only internet bill + electricity

---

## Comparison Table

| Platform | Cost | Setup Time | Ease | Uptime |
|----------|------|-----------|------|--------|
| **Heroku** | $7+/month | 10 min | ⭐⭐⭐⭐⭐ | Excellent |
| **Railway** | Pay-as-you-go | 5 min | ⭐⭐⭐⭐⭐ | Excellent |
| **Render** | Free/$7+ | 10 min | ⭐⭐⭐⭐⭐ | Excellent |
| **PythonAnywhere** | Free/$5+ | 15 min | ⭐⭐⭐⭐ | Good |
| **AWS** | $3-30/month | 30 min | ⭐⭐⭐ | Excellent |
| **Local** | Free | 20 min | ⭐⭐ | Depends |

---

## Important Security Notes

⚠️ **Never commit your API key!**

1. Always use `.env` file (included in `.gitignore`)
2. Set environment variables on the hosting platform
3. Use different API keys for testing vs production
4. Rotate keys periodically

---

## Post-Deployment

### 1. Test your app:
- Visit your deployed URL
- Try generating an essay
- Try generating an email
- Check grammar function

### 2. Set up custom domain:
Most platforms allow custom domains. Check their docs.

### 3. Monitor usage:
- Watch API costs
- Monitor server performance
- Check error logs regularly

### 4. Keep it updated:
```bash
git pull
# Push changes to hosting
```

---

## Troubleshooting

### "ModuleNotFoundError"
→ Install dependencies: `pip install -r requirements.txt`

### "ANTHROPIC_API_KEY not found"
→ Set environment variable on the hosting platform

### "Connection timeout"
→ Check firewall/security group settings (especially AWS)

### "404 Not Found"
→ Make sure `app.py` is in the root directory

### "502 Bad Gateway"
→ Check app logs on the hosting platform

---

## Quick Deploy Commands

### Heroku:
```bash
heroku login
heroku create your-app
heroku config:set ANTHROPIC_API_KEY=your-key
git push heroku main
heroku open
```

### Railway:
1. Push to GitHub
2. Go to Railway.app → New Project → GitHub
3. Add environment variable
4. Done!

### Local:
```bash
gunicorn app:app --bind 0.0.0.0:8000
# Visit http://localhost:8000
```

---

## Next Steps

1. **Choose a platform** based on your needs
2. **Follow deployment steps**
3. **Test your application**
4. **Share your URL** with others!

For more help: Check specific platform documentation in links above.

