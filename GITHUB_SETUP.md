# GitHub Repository Setup Instructions

Your local git repository is ready! Follow these steps to create the GitHub repo and push your code:

## Step 1: Create Repository on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in:
   - **Repository name**: `podman-bluesky-feed` (or any name you prefer)
   - **Description**: "Bluesky feed generator for Podman community"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Connect and Push

After creating the repo, GitHub will show you commands. Use these:

```bash
cd "/Users/nesmith/Documents/cursor junk"

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/podman-bluesky-feed.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/podman-bluesky-feed.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify

Check your GitHub repository - you should see all your files there!

## Step 4: Deploy to Render

Once your code is on GitHub:

1. Go to [render.com](https://render.com)
2. Sign up/login
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub account
5. Select the `podman-bluesky-feed` repository
6. Configure:
   - **Name**: `podman-feed` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python feed_generator.py`
7. Add **Environment Variables**:
   - `BLUESKY_HANDLE` = `actionmancan.bsky.social`
   - `BLUESKY_PASSWORD` = `your-app-password`
   - `FEED_GENERATOR_DID` = `did:plc:oe2nzi6rjpijm5o2w2gp7jzo`
   - `PORT` = `8000`
8. Click **"Create Web Service"**
9. Wait for deployment (takes a few minutes)
10. Copy your Render URL (e.g., `podman-feed.onrender.com`)

## Step 5: Connect to Your Domain

1. In GoDaddy DNS, add CNAME record:
   - **Name**: `feed`
   - **Value**: `podman-feed.onrender.com` (your Render URL)
2. Wait 5-60 minutes for DNS propagation
3. Your feed will be live at `https://feed.laswaan.com`!

## Troubleshooting

### If you get authentication errors:
- Make sure you're logged into GitHub
- Try using a Personal Access Token instead of password
- Or use SSH keys instead

### If Render deployment fails:
- Check the logs in Render dashboard
- Make sure all environment variables are set
- Verify `requirements.txt` is correct

## Next Steps

Once deployed:
- Test: `curl https://feed.laswaan.com/health`
- Test: `curl https://feed.laswaan.com/.well-known/atproto-did`
- Share your feed URI in Bluesky: `at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community`

