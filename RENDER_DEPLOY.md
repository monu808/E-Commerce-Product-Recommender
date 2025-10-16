# 🚀 Render Deployment Instructions

Follow these steps to deploy your E-commerce Recommender to Render.

## 📋 Prerequisites

- ✅ GitHub repository with your code
- ✅ PostgreSQL database URL (you have this!)
- ✅ OpenAI API key
- ✅ Render account (free)

---

## Step 1: Prepare for Deployment

### A. Update Environment Variables

Your PostgreSQL URL from `.env`:
```
Postgres_SQL_URL=postgresql://user:password@host:port/database
```

**Note**: Use your actual PostgreSQL URL from your `.env` file.

---

## Step 2: Migrate Data to PostgreSQL

Run this locally to migrate your data:

```powershell
cd backend

# Set the PostgreSQL URL (use your actual URL from .env)
$env:DATABASE_URL="postgresql://user:password@host:port/database"

# Run migration
python migrate_to_postgres.py
```

This will:
- Create all tables in PostgreSQL
- Copy 4 users from SQLite to PostgreSQL
- Copy 15 products from SQLite to PostgreSQL
- Copy 20+ interactions from SQLite to PostgreSQL

---

## Step 3: Push Changes to GitHub

```powershell
git add .
git commit -m "Add PostgreSQL support and Render deployment config"
git push origin main
```

---

## Step 4: Deploy to Render

### Option A: Using Blueprint (render.yaml) - Recommended

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Click "New +"** → **"Blueprint"**

3. **Connect Repository**:
   - Select your GitHub repository: `monu808/E-Commerce-Product-Recommender`
   - Render will detect `render.yaml`

4. **Configure Environment Variables**:
   - `OPENAI_API_KEY`: `<your-openai-api-key-here>`
   - `DATABASE_URL`: `<your-postgresql-url-here>`

5. **Click "Apply"** to deploy!

### Option B: Manual Setup

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select: `monu808/E-Commerce-Product-Recommender`

3. **Configure Service**:
   ```
   Name: ecommerce-recommender-api
   Region: Singapore (closest to your DB)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

4. **Add Environment Variables**:
   - Click "Environment" tab
   - Add variables:
     ```
     OPENAI_API_KEY = <your-openai-api-key>
     
     DATABASE_URL = <your-postgresql-database-url>
     
     PYTHON_VERSION = 3.11.1
     ```

5. **Create Web Service**: Click "Create Web Service"

---

## Step 5: Wait for Deployment

Render will:
1. ✅ Clone your repository
2. ✅ Install Python dependencies (takes ~2-3 minutes)
3. ✅ Start your FastAPI server
4. ✅ Assign a public URL

Watch the logs in real-time!

---

## Step 6: Test Your Deployment

Once deployed, you'll get a URL like:
```
https://ecommerce-recommender-api.onrender.com
```

### Test the API:

1. **Health Check**:
   ```
   https://ecommerce-recommender-api.onrender.com/health
   ```

2. **Get Users**:
   ```
   https://ecommerce-recommender-api.onrender.com/users
   ```

3. **Get Recommendations**:
   ```
   https://ecommerce-recommender-api.onrender.com/recommend/1
   ```

4. **API Docs**:
   ```
   https://ecommerce-recommender-api.onrender.com/docs
   ```

---

## Step 7: Update Frontend to Use Production API

Update `ecommerce-recommender-frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=https://ecommerce-recommender-api.onrender.com
```

Then redeploy or test locally!

---

## 🎉 Deployment Complete!

Your backend is now live on Render with PostgreSQL! 

### What's Next?

1. **Deploy Frontend to Vercel**:
   - Go to https://vercel.com
   - Import your GitHub repo
   - Deploy `ecommerce-recommender-frontend` folder
   - Add environment variable: `NEXT_PUBLIC_API_URL`

2. **Monitor Your App**:
   - Check Render dashboard for logs
   - Monitor API performance
   - Check database connections

3. **Scale as Needed**:
   - Free tier includes 750 hours/month
   - Upgrade to paid plan for more resources

---

## 🐛 Troubleshooting

### Build Fails?
- Check that `requirements.txt` includes `psycopg2-binary`
- Verify Python version is 3.11.1
- Check build logs for specific errors

### Database Connection Fails?
- Verify DATABASE_URL is correct
- Check PostgreSQL database is running
- Ensure database has tables (run migration)

### App Crashes?
- Check logs in Render dashboard
- Verify OPENAI_API_KEY is valid
- Check for any missing environment variables

### Slow Response?
- Free tier has cold starts (first request takes 30s)
- Consider upgrading to paid plan for always-on service

---

## 📚 Useful Commands

```bash
# View live logs (in Render dashboard)
# Or use Render CLI:
render logs -f

# Restart service
render restart

# Open deployed app
render open
```

---

**🚀 Your app is now live and accessible worldwide!**

Share your deployed API URL and celebrate! 🎉
