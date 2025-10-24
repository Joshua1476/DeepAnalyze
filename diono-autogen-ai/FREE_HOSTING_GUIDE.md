# Free Hosting Guide for DionoAutogen AI

This guide provides step-by-step instructions for deploying DionoAutogen AI on completely free hosting platforms.

## 🌐 Free Hosting Options

All platforms listed below offer free tiers suitable for DionoAutogen AI:

1. **Railway** - Best for beginners, easiest setup
2. **Render** - Good free tier, automatic deployments
3. **Fly.io** - Generous free tier, Docker-native
4. **Heroku Alternatives** - Various options

---

## 🚂 Railway (Recommended for Beginners)

**Free Tier**: $5 credit/month (enough for small projects)  
**Website**: https://railway.app

### Step 1: Create Account

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)

### Step 2: Fork the Repository

1. Go to https://github.com/Joshua1476/DeepAnalyze
2. Click "Fork" button (top right)
3. This creates your own copy

### Step 3: Deploy on Railway

1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your forked `DeepAnalyze` repository
4. Select the `diono-autogen-ai` directory

### Step 4: Configure Environment Variables

In Railway project settings, add these variables:

```
SECRET_KEY=your-random-secret-key-here
LLM_API_URL=https://api.openai.com/v1
LLM_API_KEY=your-openai-api-key
SANDBOX_NETWORK_ENABLED=true
SANDBOX_MAX_WORKERS=2
```

### Step 5: Deploy

1. Railway automatically detects Docker
2. Click "Deploy"
3. Wait 5-10 minutes for first deployment
4. Railway provides a public URL

### Step 6: Access Your Application

1. Click on your deployment
2. Copy the public URL (e.g., `https://your-app.railway.app`)
3. Open in browser
4. Login with demo/demo

### Railway Tips

- **Free tier limits**: 500 hours/month, $5 credit
- **Automatic deployments**: Pushes to GitHub auto-deploy
- **Custom domains**: Can add your own domain
- **Logs**: View real-time logs in dashboard

---

## 🎨 Render

**Free Tier**: 750 hours/month  
**Website**: https://render.com

### Step 1: Create Account

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select your forked repository
4. Choose `diono-autogen-ai` directory

### Step 3: Configure Service

**Settings:**
- **Name**: diono-autogen-ai
- **Environment**: Docker
- **Region**: Choose closest to you
- **Branch**: main or mentat-1
- **Plan**: Free

### Step 4: Add Environment Variables

Click "Environment" tab and add:

```
SECRET_KEY=your-random-secret-key
LLM_API_URL=https://api.openai.com/v1
LLM_API_KEY=your-api-key
WORKSPACE_DIR=/opt/render/project/workspace
```

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (10-15 minutes first time)
3. Render provides a URL

### Step 6: Access Application

1. Copy the Render URL (e.g., `https://your-app.onrender.com`)
2. Open in browser
3. Login with demo/demo

### Render Tips

- **Free tier**: Spins down after 15 min inactivity
- **First request**: May take 30-60 seconds to wake up
- **Persistent storage**: Not available on free tier
- **Custom domains**: Available on free tier

---

## ✈️ Fly.io

**Free Tier**: 3 shared VMs, 3GB storage  
**Website**: https://fly.io

### Step 1: Install Fly CLI

**macOS:**
```bash
brew install flyctl
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Sign Up and Login

```bash
# Sign up
flyctl auth signup

# Or login if you have account
flyctl auth login
```

### Step 3: Prepare Application

```bash
# Navigate to project
cd DeepAnalyze/diono-autogen-ai

# Initialize Fly app
flyctl launch
```

Answer the prompts:
- **App name**: Choose a unique name
- **Region**: Select closest to you
- **PostgreSQL**: No
- **Redis**: No

### Step 4: Configure fly.toml

Edit `fly.toml`:

```toml
app = "your-app-name"

[build]
  dockerfile = "backend/Dockerfile"

[env]
  PORT = "8000"
  WORKSPACE_DIR = "/workspace"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Step 5: Set Secrets

```bash
flyctl secrets set SECRET_KEY=your-secret-key
flyctl secrets set LLM_API_KEY=your-api-key
flyctl secrets set LLM_API_URL=https://api.openai.com/v1
```

### Step 6: Deploy

```bash
flyctl deploy
```

### Step 7: Access Application

```bash
# Open in browser
flyctl open
```

### Fly.io Tips

- **Free tier**: 3 shared VMs, generous limits
- **Scaling**: Can scale to 0 when not in use
- **Regions**: Deploy to multiple regions
- **Volumes**: Persistent storage available

---

## 🆓 Other Free Options

### Vercel (Frontend Only)

**Best for**: Deploying just the frontend  
**Website**: https://vercel.com

1. Sign up with GitHub
2. Import your repository
3. Select `frontend` directory
4. Deploy automatically

**Note**: Backend needs separate hosting

### Netlify (Frontend Only)

**Best for**: Static frontend hosting  
**Website**: https://netlify.com

Similar to Vercel, frontend only.

### Google Cloud Run

**Free Tier**: 2 million requests/month  
**Website**: https://cloud.google.com/run

1. Create Google Cloud account
2. Enable Cloud Run API
3. Deploy Docker container
4. Configure environment variables

### AWS Free Tier

**Free Tier**: 12 months free  
**Website**: https://aws.amazon.com/free

Options:
- **EC2**: Virtual machine
- **ECS**: Container service
- **Elastic Beanstalk**: Platform as a service

---

## 🔧 Configuration for Free Hosting

### Optimize for Free Tiers

Edit `backend/.env`:

```bash
# Reduce resource usage
SANDBOX_MAX_WORKERS=1
SANDBOX_MEMORY_LIMIT=512m
SANDBOX_CPU_LIMIT=0.5

# Use external LLM (no local Ollama)
LLM_API_URL=https://api.openai.com/v1
LLM_API_KEY=your-key
```

### Use External Services

**For LLM:**
- OpenAI (pay-as-you-go)
- Anthropic Claude
- Google Gemini (free tier)

**For Storage:**
- Google Drive API (free)
- Dropbox API (free)

---

## 💡 Cost Optimization Tips

### 1. Use Free LLM APIs

**Google Gemini** (Free tier):
```bash
LLM_API_URL=https://generativelanguage.googleapis.com/v1
LLM_API_KEY=your-gemini-key
```

**Hugging Face** (Free):
```bash
LLM_API_URL=https://api-inference.huggingface.co
LLM_API_KEY=your-hf-token
```

### 2. Reduce Resource Usage

- Set `SANDBOX_MAX_WORKERS=1`
- Disable features you don't need
- Use smaller Docker images

### 3. Auto-Sleep Configuration

Most free tiers sleep after inactivity. This is fine for:
- Personal projects
- Development
- Low-traffic applications

### 4. Monitor Usage

- Check platform dashboards regularly
- Set up usage alerts
- Stay within free tier limits

---

## 🌍 Choosing the Right Platform

### Railway
 Easiest setup  
 Good for beginners  
 Automatic deployments  
 Limited free tier ($5/month)

### Render
 Generous free tier  
 Easy to use  
 Good documentation  
 Spins down after inactivity

### Fly.io
 Most generous free tier  
 Docker-native  
 Multiple regions  
 Requires CLI knowledge

### Recommendation

**For beginners**: Start with Railway  
**For developers**: Use Fly.io  
**For frontend only**: Use Vercel/Netlify

---

## 🔒 Security for Public Hosting

### 1. Change Default Credentials

Edit `backend/app/auth.py` and change:
- Default username
- Default password
- Add proper user management

### 2. Use Strong Secrets

```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Enable HTTPS

All platforms provide free HTTPS automatically.

### 4. Set CORS Properly

Edit `backend/app/config.py`:

```python
CORS_ORIGINS = [
    "https://your-frontend-domain.com",
    "https://your-backend-domain.com"
]
```

### 5. Rate Limiting

Add rate limiting to prevent abuse:

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

---

## 📊 Monitoring Your Deployment

### Check Application Health

```bash
# Railway
railway logs

# Render
# View logs in dashboard

# Fly.io
flyctl logs
```

### Monitor Resource Usage

All platforms provide dashboards showing:
- CPU usage
- Memory usage
- Request count
- Error rates

---

## 🆘 Troubleshooting Free Hosting

### Application Won't Start

1. Check logs for errors
2. Verify environment variables
3. Ensure Docker builds successfully
4. Check resource limits

### Out of Memory

1. Reduce `SANDBOX_MAX_WORKERS`
2. Decrease `SANDBOX_MEMORY_LIMIT`
3. Upgrade to paid tier if needed

### Slow Performance

1. Free tiers have limited resources
2. Consider upgrading for production
3. Optimize Docker image size
4. Use CDN for static files

### Deployment Fails

1. Check Dockerfile syntax
2. Verify all dependencies
3. Test locally first
4. Check platform-specific requirements

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Fork repository to your GitHub
- [ ] Choose hosting platform
- [ ] Create account on platform
- [ ] Configure environment variables
- [ ] Change default credentials
- [ ] Test locally first
- [ ] Deploy to platform
- [ ] Verify deployment works
- [ ] Set up monitoring
- [ ] Configure custom domain (optional)

---

## 🎓 Next Steps

After successful deployment:

1. **Test all features** thoroughly
2. **Monitor usage** to stay within limits
3. **Set up backups** if needed
4. **Configure custom domain** (optional)
5. **Add authentication** for production use
6. **Set up CI/CD** for automatic deployments

---

## 📞 Getting Help

If you encounter issues:

1. Check platform documentation
2. Review deployment logs
3. Search platform community forums
4. Contact platform support
5. Check GitHub issues

---

## 🎉 Success!

Once deployed, your DionoAutogen AI is accessible worldwide at your public URL!

Share it with:
- Team members
- Clients
- Portfolio
- Community

Remember to monitor usage and stay within free tier limits! 🚀
