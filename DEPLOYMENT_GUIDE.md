# 🚀 Deployment Guide

Deploy your E-commerce Product Recommender to production.

---

## 📋 Table of Contents

1. Pre-Deployment Checklist
2. Environment Configuration
3. Database Migration (SQLite → PostgreSQL)
4. Deploy to Render (Recommended)
5. Deploy to Railway
6. Deploy to Heroku
7. Deploy to AWS
8. Deploy to Azure
9. Docker Deployment
10. CI/CD Setup
11. Monitoring & Logging
12. Troubleshooting

---

## 1. ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Working local environment
- ✅ OpenAI API key with sufficient credits
- ✅ Git repository (GitHub/GitLab/Bitbucket)
- ✅ Production database plan (PostgreSQL recommended)
- ✅ Domain name (optional but recommended)
- ✅ SSL certificate plan (Let's Encrypt or managed)

### **Test Locally First**

```bash
# Activate virtual environment
cd backend
.\.venv\Scripts\activate

# Test server
uvicorn main:app --reload

# Test all endpoints
# Visit: http://127.0.0.1:8000/docs
```

---

## 2. 🔐 Environment Configuration

### **A. Production Environment Variables**

Create `backend/.env.production`:

```env
# Production Configuration
OPENAI_API_KEY=sk-proj-your-production-key
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Performance
MAX_WORKERS=4
TIMEOUT=60

# Monitoring (optional)
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

### **B. Update `main.py` for Production**

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
env_file = ".env.production" if os.getenv("ENV") == "production" else ".env"
load_dotenv(env_file)

app = FastAPI(
    title="E-commerce Recommender API",
    docs_url="/docs" if os.getenv("ENV") != "production" else None,  # Disable in prod
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None
)

# CORS - Restrict to your frontend domain in production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of your code
```

---

## 3. 🗄️ Database Migration (SQLite → PostgreSQL)

### **Why PostgreSQL?**

- ✅ Better performance for concurrent users
- ✅ Required by most cloud platforms
- ✅ More robust for production workloads

### **A. Install PostgreSQL Driver**

Update `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
openai>=1.12.0
python-dotenv==1.0.0
pydantic==2.5.0

# PostgreSQL support
psycopg2-binary==2.9.9
```

### **B. Update Database Configuration**

Modify `backend/database.py`:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle SQLite vs PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
elif DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Default to SQLite for local development
    DATABASE_URL = "sqlite:///./ecommerce.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### **C. Migration Script**

Create `backend/migrate_to_postgres.py`:

```python
"""
Migrate data from SQLite to PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Product, Interaction, Base

# Source (SQLite)
sqlite_engine = create_engine("sqlite:///./ecommerce.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)

# Destination (PostgreSQL)
postgres_url = os.getenv("DATABASE_URL")  # Set this to your PostgreSQL URL
postgres_engine = create_engine(postgres_url)
PostgresSession = sessionmaker(bind=postgres_engine)

def migrate_data():
    """Copy all data from SQLite to PostgreSQL"""
    
    # Create tables in PostgreSQL
    Base.metadata.create_all(postgres_engine)
    
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()
    
    try:
        # Migrate Users
        print("Migrating users...")
        users = sqlite_session.query(User).all()
        for user in users:
            postgres_session.merge(user)
        postgres_session.commit()
        print(f"✓ Migrated {len(users)} users")
        
        # Migrate Products
        print("Migrating products...")
        products = sqlite_session.query(Product).all()
        for product in products:
            postgres_session.merge(product)
        postgres_session.commit()
        print(f"✓ Migrated {len(products)} products")
        
        # Migrate Interactions
        print("Migrating interactions...")
        interactions = sqlite_session.query(Interaction).all()
        for interaction in interactions:
            postgres_session.merge(interaction)
        postgres_session.commit()
        print(f"✓ Migrated {len(interactions)} interactions")
        
        print("\n✅ Migration complete!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        postgres_session.rollback()
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()
```

Run migration:

```bash
# Set PostgreSQL URL
$env:DATABASE_URL="postgresql://user:password@host:5432/dbname"

# Run migration
python backend/migrate_to_postgres.py
```

---

## 4. 🟢 Deploy to Render (Recommended)

**Why Render?** Free tier, automatic HTTPS, easy PostgreSQL setup.

### **Step 1: Prepare Files**

Create `render.yaml` in project root:

```yaml
services:
  # Web Service
  - type: web
    name: ecommerce-recommender-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: ecommerce-db
          property: connectionString
      - key: ENV
        value: production

databases:
  # PostgreSQL Database
  - name: ecommerce-db
    plan: free
    databaseName: ecommerce_db
    user: ecommerce_user
```

### **Step 2: Deploy**

1. **Sign up**: Go to [render.com](https://render.com)
2. **New Web Service**: Click "New" → "Web Service"
3. **Connect Repo**: Link your GitHub repository
4. **Configure**:
   - Name: `ecommerce-recommender`
   - Region: Choose closest to users
   - Branch: `main`
   - Root Directory: Leave empty
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**:
   - `OPENAI_API_KEY`: Your API key
   - `ENV`: `production`

6. **Create PostgreSQL Database**:
   - Click "New" → "PostgreSQL"
   - Name: `ecommerce-db`
   - Plan: Free
   - Copy the "Internal Database URL"

7. **Link Database**:
   - Go back to your web service
   - Add environment variable: `DATABASE_URL` = (paste database URL)

8. **Deploy**: Click "Create Web Service"

### **Step 3: Initialize Database**

After deployment:

```bash
# SSH into Render (or use dashboard shell)
# Run database initialization
python backend/database.py
```

Your API will be live at: `https://your-service-name.onrender.com`

---

## 5. 🚂 Deploy to Railway

**Why Railway?** Simple deployment, generous free tier.

### **Step 1: Install Railway CLI**

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Or use npm
npm install -g @railway/cli
```

### **Step 2: Deploy**

```bash
# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up

# Set environment variables
railway variables set OPENAI_API_KEY=sk-proj-your-key
railway variables set ENV=production

# Get deployment URL
railway domain
```

### **Step 3: Configure Start Command**

In Railway dashboard:
- Go to Settings → Deploy
- Set Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 6. 🟣 Deploy to Heroku

### **Step 1: Prepare Files**

Create `Procfile` in project root:

```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:

```
python-3.11.1
```

### **Step 2: Deploy**

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-proj-your-key
heroku config:set ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run python backend/database.py

# Open app
heroku open
```

---

## 7. ☁️ Deploy to AWS (EC2 + RDS)

### **Architecture**

- EC2 instance for FastAPI
- RDS PostgreSQL for database
- Application Load Balancer for HTTPS
- Route 53 for DNS

### **Step 1: Launch EC2 Instance**

```bash
# 1. Launch EC2 (t2.micro for free tier)
# 2. Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
# 3. Create key pair and download .pem file

# Connect to EC2
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### **Step 2: Setup Server**

```bash
# Update system
sudo yum update -y

# Install Python 3.11
sudo yum install python3.11 -y

# Install git
sudo yum install git -y

# Clone repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install gunicorn (production server)
pip install gunicorn
```

### **Step 3: Configure Environment**

```bash
# Create .env file
nano backend/.env

# Add:
OPENAI_API_KEY=sk-proj-your-key
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/dbname
ENV=production
```

### **Step 4: Setup Systemd Service**

Create `/etc/systemd/system/recommender.service`:

```ini
[Unit]
Description=E-commerce Recommender API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/your-repo/backend
Environment="PATH=/home/ec2-user/your-repo/venv/bin"
ExecStart=/home/ec2-user/your-repo/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl start recommender
sudo systemctl enable recommender
sudo systemctl status recommender
```

### **Step 5: Setup Nginx (Reverse Proxy)**

```bash
# Install Nginx
sudo yum install nginx -y

# Configure
sudo nano /etc/nginx/conf.d/recommender.conf
```

Add:

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

Start Nginx:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### **Step 6: Setup HTTPS with Let's Encrypt**

```bash
# Install certbot
sudo yum install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com
```

---

## 8. 🔷 Deploy to Azure (App Service)

### **Step 1: Install Azure CLI**

```bash
# Windows
winget install Microsoft.AzureCLI

# Or download from: https://aka.ms/installazurecliwindows
```

### **Step 2: Deploy**

```bash
# Login
az login

# Create resource group
az group create --name ecommerce-rg --location eastus

# Create App Service plan
az appservice plan create `
  --name ecommerce-plan `
  --resource-group ecommerce-rg `
  --sku B1 `
  --is-linux

# Create web app
az webapp create `
  --resource-group ecommerce-rg `
  --plan ecommerce-plan `
  --name your-app-name `
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set `
  --resource-group ecommerce-rg `
  --name your-app-name `
  --startup-file "cd backend && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000"

# Set environment variables
az webapp config appsettings set `
  --resource-group ecommerce-rg `
  --name your-app-name `
  --settings OPENAI_API_KEY=sk-proj-your-key ENV=production

# Create PostgreSQL
az postgres flexible-server create `
  --resource-group ecommerce-rg `
  --name ecommerce-db `
  --location eastus `
  --admin-user adminuser `
  --admin-password YourPassword123! `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --storage-size 32

# Get connection string
az postgres flexible-server show-connection-string `
  --server-name ecommerce-db

# Set DATABASE_URL
az webapp config appsettings set `
  --resource-group ecommerce-rg `
  --name your-app-name `
  --settings DATABASE_URL="postgresql://..."

# Deploy code
az webapp up `
  --resource-group ecommerce-rg `
  --name your-app-name
```

---

## 9. 🐳 Docker Deployment

### **Step 1: Create Dockerfile**

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Step 2: Create Docker Compose**

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://user:password@db:5432/ecommerce
      - ENV=production
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ecommerce
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### **Step 3: Deploy**

```bash
# Build and run
docker-compose up -d

# Initialize database
docker-compose exec api python database.py

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### **Deploy to Docker Hub**

```bash
# Build image
docker build -t yourusername/ecommerce-recommender ./backend

# Push to Docker Hub
docker push yourusername/ecommerce-recommender

# Pull and run on any server
docker pull yourusername/ecommerce-recommender
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=sk-proj-your-key \
  -e DATABASE_URL=postgresql://... \
  yourusername/ecommerce-recommender
```

---

## 10. 🔄 CI/CD Setup

### **GitHub Actions**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          python test_system.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST https://api.render.com/deploy/srv-xxx?key=$RENDER_API_KEY
```

---

## 11. 📊 Monitoring & Logging

### **A. Setup Sentry (Error Tracking)**

```bash
pip install sentry-sdk[fastapi]
```

Update `backend/main.py`:

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENV", "development"),
    traces_sample_rate=1.0
)
```

### **B. Setup Logging**

Create `backend/logger.py`:

```python
import logging
import sys

def setup_logger():
    logger = logging.getLogger("recommender")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()
```

Use in code:

```python
from logger import logger

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: int):
    logger.info(f"Recommendation request for user {user_id}")
    # ...
```

---

## 12. 🔧 Troubleshooting

### **Common Issues**

#### **1. Database Connection Failed**

```
Solution: Check DATABASE_URL format
PostgreSQL: postgresql://user:password@host:5432/dbname
SQLite: sqlite:///./ecommerce.db
```

#### **2. OpenAI API Rate Limit**

```python
# Add retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_explanation_with_retry(...):
    return generate_recommendation_explanation(...)
```

#### **3. Port Already in Use**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

#### **4. CORS Errors**

```python
# Update allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎉 Deployment Complete!

Your E-commerce Product Recommender is now live!

### **Post-Deployment Checklist**

- ✅ API responding at production URL
- ✅ Database populated with data
- ✅ HTTPS enabled
- ✅ Environment variables configured
- ✅ Monitoring setup (Sentry)
- ✅ Logs accessible
- ✅ Backup strategy in place

### **Next Steps**

1. **Monitor Performance**: Check logs and metrics daily
2. **Scale as Needed**: Upgrade plan when traffic grows
3. **Add Caching**: Use Redis for faster responses
4. **Setup Backups**: Automate database backups
5. **CDN**: Use Cloudflare for static assets

---

**🚀 Happy Deploying!**

For questions, see other documentation files or open an issue.
