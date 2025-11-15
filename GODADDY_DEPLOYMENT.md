# Deploying to GoDaddy Domain (laswaan.com)

Since GoDaddy's free hosting doesn't support Python applications, here are your best options:

## Option 1: Use a Subdomain with Free PaaS (Recommended & Free)

Deploy the feed generator to a free hosting service and use a subdomain like `feed.laswaan.com`:

### Step-by-Step:

1. **Deploy to Render (Free Tier) - RECOMMENDED**
   - Go to [render.com](https://render.com)
   - Sign up (free)
   - Create new Web Service
   - Connect your GitHub repo
   - Set environment variables
   - Render gives you a URL like `your-app.onrender.com`
   - **Note**: Free tier spins down after 15 min inactivity, but wakes up on first request

2. **Or Deploy to Fly.io (Free Tier)**
   - Go to [fly.io](https://fly.io)
   - Sign up (free tier: 3 shared VMs)
   - Install Fly CLI and deploy
   - Can add custom domain easily

3. **Set up Subdomain in GoDaddy**
   - Log into GoDaddy
   - Go to DNS Management for laswaan.com
   - Add a CNAME record:
     - **Name**: `feed` (or `bluesky`, `podman`, etc.)
     - **Value**: `your-app.up.railway.app` (or your Render URL)
     - **TTL**: 3600 (or default)

4. **Configure SSL on Railway/Render**
   - Both services automatically provide SSL
   - Your subdomain will be accessible at `https://feed.laswaan.com`

5. **Update Feed Generator Configuration**
   - The feed will be accessible via your subdomain
   - Update your DID if needed (or keep using did:plc)

### Cost: FREE (both Railway and Render have free tiers)

---

## Option 2: Upgrade GoDaddy Hosting (If Available)

If GoDaddy offers Python hosting for your domain:

1. **Check GoDaddy Hosting Options**
   - Log into GoDaddy
   - Look for "Hosting" → "Upgrade" or "Add Hosting"
   - Check if they offer Python/cPanel hosting

2. **If Python Hosting Available:**
   - Upload your code via FTP/SFTP
   - Set up Python environment
   - Configure `.env` file
   - Set up process management (may require SSH access)

**Note**: GoDaddy's basic hosting often doesn't support long-running Python processes well.

---

## Option 3: Use Fly.io (Free Tier + Custom Domain)

Fly.io offers free tier and easy custom domain setup:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create Fly.io Account:**
   ```bash
   fly auth signup
   ```

3. **Deploy:**
   ```bash
   fly launch
   ```

4. **Add Custom Domain:**
   ```bash
   fly domains add feed.laswaan.com
   ```

5. **Update DNS in GoDaddy:**
   - Add A record pointing to Fly.io's IP (they'll provide it)
   - Or use CNAME if they provide a hostname

---

## Recommended: Option 1 (Render + Subdomain)

This is the easiest and free option:

### Quick Setup:

1. **Create Render Account** (free at render.com)
2. **Deploy your feed generator** from GitHub
3. **Add environment variables** in Render:
   - `BLUESKY_HANDLE=actionmancan.bsky.social`
   - `BLUESKY_PASSWORD=your-password`
   - `FEED_GENERATOR_DID=did:plc:oe2nzi6rjpijm5o2w2gp7jzo`
   - `PORT=8000`

4. **Get Render URL** (e.g., `podman-feed.onrender.com`)

5. **In GoDaddy DNS:**
   - Add CNAME: `feed` → `podman-feed.onrender.com`

6. **Wait for DNS propagation** (5-60 minutes)

7. **Your feed will be at:** `https://feed.laswaan.com`

**Note**: Render free tier spins down after 15 minutes of inactivity, but automatically wakes up when someone requests it (takes ~30 seconds to wake up).

---

## DNS Configuration in GoDaddy

Here's exactly what to do:

1. Log into GoDaddy
2. Go to **My Products** → **DNS** (or **Domain Manager**)
3. Find `laswaan.com` and click **DNS** or **Manage DNS**
4. Click **Add** or **+** to add a new record
5. Select **CNAME** record type
6. Fill in:
   - **Name**: `feed` (or `bluesky`, `podman`)
   - **Value**: Your Railway/Render URL (e.g., `your-app.up.railway.app`)
   - **TTL**: 3600 (or leave default)
7. Save

**Note**: Remove the `@` or `www` prefix - just use `feed` as the name.

---

## Testing After Deployment

Once DNS propagates:

1. Test: `curl https://feed.laswaan.com/health`
2. Test: `curl https://feed.laswaan.com/.well-known/atproto-did`
3. Test: `curl https://feed.laswaan.com/xrpc/app.bsky.feed.describeFeedGenerator`

---

## Your Feed URI

Once deployed, your feed will be accessible at:
```
at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community
```

Users can subscribe to it in Bluesky!

---

## Cost Summary

- **Render Free Tier**: Free but spins down after 15 min inactivity (wakes on request, ~30 sec delay)
- **Fly.io Free Tier**: 3 shared VMs free (more reliable, stays running)
- **PythonAnywhere Free Tier**: Free but limited (good for testing)
- **GoDaddy DNS**: Free (part of domain)
- **Total Cost**: $0/month

## Best Free Options (2024)

1. **Render** - Easiest setup, free tier available
2. **Fly.io** - More reliable (stays running), free tier available
3. **PythonAnywhere** - Free tier for testing (limited)

---

## Need Help?

If you want, I can help you:
1. Set up a GitHub repo for easy deployment
2. Create deployment configuration files
3. Walk through the Railway/Render setup

Let me know which option you prefer!

