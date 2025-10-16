# 🚀 Quick Start Guide

## Complete Setup Instructions (Windows)

### Step 1: Navigate to Backend Directory
```powershell
cd backend
```

### Step 2: Run the Automated Setup Script
```powershell
.\setup.ps1
```

This script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env configuration file
- ✅ Initialize SQLite database
- ✅ Seed mock data (users, products, interactions)

---

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Create Virtual Environment
```powershell
python -m venv venv
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment
```powershell
# Copy template
copy .env.example .env

# Edit .env and add your OpenAI API key
notepad .env
```

### 5. Initialize Database
```powershell
python database.py
```

---

## 🎯 Running the Application

### Start the Server
```powershell
uvicorn main:app --reload
```

The server will start at: **http://localhost:8000**

### Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Testing the API

### Method 1: Using Browser
Simply visit these URLs in your browser:

1. **Health Check**: http://localhost:8000/
2. **Get Recommendations**: http://localhost:8000/recommend/1
3. **List Users**: http://localhost:8000/users
4. **List Products**: http://localhost:8000/products

### Method 2: Using PowerShell
```powershell
# Get recommendations for User 1 (Alice)
Invoke-RestMethod -Uri "http://localhost:8000/recommend/1" | ConvertTo-Json -Depth 5

# Get all users
Invoke-RestMethod -Uri "http://localhost:8000/users" | ConvertTo-Json

# Get all products
Invoke-RestMethod -Uri "http://localhost:8000/products" | ConvertTo-Json

# Get products by category
Invoke-RestMethod -Uri "http://localhost:8000/products?category=Electronics" | ConvertTo-Json
```

### Method 3: Using the Test Script
```powershell
python test_system.py
```

---

## 👥 Demo Users

The system comes pre-loaded with 4 users:

| ID | Name | Interests |
|----|------|-----------|
| 1 | Alice Johnson | Audio products (speakers, headphones) |
| 2 | Bob Smith | Computer accessories (mouse, keyboard) |
| 3 | Charlie Brown | Home office setup (desk lamp, monitor arm) |
| 4 | Diana Prince | Mobile accessories (phone stand, wireless charger) |

### Try Different Recommendations
```powershell
# Alice - Audio enthusiast
Invoke-RestMethod -Uri "http://localhost:8000/recommend/1"

# Bob - Computer accessories fan
Invoke-RestMethod -Uri "http://localhost:8000/recommend/2"

# Charlie - Home office setup
Invoke-RestMethod -Uri "http://localhost:8000/recommend/3"

# Diana - Mobile accessories lover
Invoke-RestMethod -Uri "http://localhost:8000/recommend/4"
```

---

## 🔑 OpenAI API Configuration

### Get Your API Key
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key

### Add to Your Project
1. Open `.env` file
2. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Restart the server

### Without OpenAI API Key
The system will work with **fallback explanations** (rule-based) if you don't provide an API key. The recommendations will still work perfectly!

---

## 📊 Understanding the Response

When you call `/recommend/1`, you'll get:

```json
{
  "user_id": 1,
  "user_name": "Alice Johnson",
  "recommended_products": [
    {
      "id": 6,
      "name": "Noise Cancelling Headphones",
      "category": "Electronics",
      "price": 199.99,
      "description": "Premium over-ear headphones...",
      "tags": "electronics,audio,headphones,noise-cancelling"
    }
  ],
  "llm_explanation": "Hi Alice! Based on your recent purchase...",
  "user_behavior_summary": "Recently purchased: Bluetooth Speaker..."
}
```

**Key Fields:**
- `recommended_products`: Array of recommended items
- `llm_explanation`: AI-generated natural language explanation
- `user_behavior_summary`: What the recommendation is based on

---

## 🛠️ Troubleshooting

### Issue: "Cannot activate virtual environment"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Port 8000 already in use"
**Solution:** Use a different port:
```powershell
uvicorn main:app --reload --port 8001
```

### Issue: "Module not found" errors
**Solution:** Reinstall dependencies:
```powershell
pip install -r requirements.txt --force-reinstall
```

### Issue: "Database is locked"
**Solution:** Delete and recreate database:
```powershell
rm ecommerce.db
python database.py
```

### Issue: OpenAI API errors
**Solution:** 
- Check your API key is correct in `.env`
- Ensure you have credits in your OpenAI account
- The system will use fallback explanations if API fails

---

## 📝 Next Steps

1. ✅ Explore the API documentation at `/docs`
2. ✅ Try recommendations for different users
3. ✅ Experiment with the recommendation logic in `recommendation.py`
4. ✅ Customize the LLM prompts in `llm.py`
5. ✅ Add your own products and users to the database
6. ✅ Build a frontend dashboard (React/Tailwind)

---

## 🎓 Learn More

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **OpenAI API**: https://platform.openai.com/docs/

---

## 💡 Tips

- Use `/docs` endpoint for interactive API testing
- Check `database.py` to see how mock data is structured
- Modify scoring weights in `recommendation.py` to tune recommendations
- The system supports both sync and async operations
- All endpoints support CORS for frontend integration

---

**Happy Coding! 🎉**

Need help? Check the main README.md or backend/README.md for more details.
