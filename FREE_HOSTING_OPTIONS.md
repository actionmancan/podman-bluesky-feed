# Free Hosting Options for Bluesky Feed Generator (2024)

Since Railway no longer has a free tier, here are the best **actually free** options:

## 1. Render (Recommended - Easiest)

**Free Tier**: ✅ Yes
**Stays Running**: ❌ Spins down after 15 min inactivity (wakes on request)
**Custom Domain**: ✅ Yes (free)
**Setup Difficulty**: ⭐ Easy

### Pros:
- Very easy to set up
- Free custom domain support
- Automatic SSL
- Good documentation

### Cons:
- Spins down after inactivity (first request takes ~30 seconds)
- Limited to 750 hours/month on free tier

### Setup:
1. Sign up at [render.com](https://render.com)
2. Connect GitHub repo
3. Create Web Service
4. Add environment variables
5. Deploy!

---

## 2. Fly.io (Best for Always-On)

**Free Tier**: ✅ Yes (3 shared VMs)
**Stays Running**: ✅ Yes (doesn't spin down)
**Custom Domain**: ✅ Yes (free)
**Setup Difficulty**: ⭐⭐ Medium (requires CLI)

### Pros:
- Stays running 24/7
- No spin-down delays
- Free custom domain
- Good performance

### Cons:
- Requires CLI setup
- Slightly more complex than Render

### Setup:
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth signup

# Deploy
fly launch

# Add custom domain
fly domains add feed.laswaan.com
```

---

## 3. PythonAnywhere

**Free Tier**: ✅ Yes
**Stays Running**: ✅ Yes (but limited)
**Custom Domain**: ❌ No (only subdomain)
**Setup Difficulty**: ⭐⭐ Medium

### Pros:
- Always running
- Good for Python apps
- Web-based console

### Cons:
- Limited free tier
- No custom domain on free tier
- URL will be `yourusername.pythonanywhere.com`

---

## 4. Replit

**Free Tier**: ✅ Yes
**Stays Running**: ❌ Spins down after inactivity
**Custom Domain**: ✅ Yes (with paid plan)
**Setup Difficulty**: ⭐ Easy

### Pros:
- Very easy to use
- Built-in editor
- Good for testing

### Cons:
- Spins down after inactivity
- Custom domain requires paid plan

---

## Recommendation for Your Use Case

**For laswaan.com subdomain:**

1. **Render** - Best balance of ease and functionality
   - Free custom domain support
   - Easy setup
   - Only downside: 30-second wake-up delay

2. **Fly.io** - Best if you need always-on
   - No spin-down delays
   - Free custom domain
   - Requires CLI setup

---

## Quick Comparison

| Service | Free? | Always On? | Custom Domain? | Ease |
|---------|-------|------------|----------------|------|
| Render | ✅ | ❌ (spins down) | ✅ | ⭐⭐⭐ |
| Fly.io | ✅ | ✅ | ✅ | ⭐⭐ |
| PythonAnywhere | ✅ | ✅ | ❌ | ⭐⭐ |
| Replit | ✅ | ❌ | ❌ | ⭐⭐⭐ |

---

## My Recommendation: Use Render

For your GoDaddy domain setup, Render is the easiest:
1. Sign up (free)
2. Connect GitHub
3. Deploy
4. Add CNAME in GoDaddy: `feed` → `your-app.onrender.com`
5. Done!

The 30-second wake-up delay is usually fine for a feed generator since Bluesky will retry if needed.

