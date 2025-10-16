# 🔧 Troubleshooting Guide

Common issues and their solutions when setting up and running the E-Commerce Product Recommender.

---

## 🚨 Setup Issues

### Issue: "Scripts are disabled on this system"

**Error Message:**
```
.\setup.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

**Solution:**
```powershell
# Run this in PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\setup.ps1
```

**Why:** Windows blocks script execution by default for security.

---

### Issue: "Python not found" or "python is not recognized"

**Error Message:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Option 1: Install Python**
1. Download from https://www.python.org/downloads/
2. ✅ CHECK "Add Python to PATH" during installation
3. Restart terminal

**Option 2: Use py launcher**
```powershell
# Instead of 'python', use 'py'
py --version
py -m venv venv
py database.py
```

**Verify Installation:**
```powershell
python --version  # Should show Python 3.8+
```

---

### Issue: "pip is not recognized"

**Error Message:**
```
'pip' is not recognized as an internal or external command
```

**Solution:**
```powershell
# Use python -m pip instead
python -m pip install -r requirements.txt

# Or update pip
python -m ensurepip --upgrade
```

---

### Issue: "Virtual environment won't activate"

**Error Messages:**
- `Activate.ps1 cannot be loaded`
- `venv not recognized`

**Solution 1: Check PowerShell execution policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solution 2: Use full path**
```powershell
# Instead of:
.\venv\Scripts\Activate.ps1

# Try:
& "C:\Users\ASUS\Desktop\E_Commerce\E-Commerce-Product-Recommender\backend\venv\Scripts\Activate.ps1"
```

**Solution 3: Use Command Prompt instead**
```cmd
venv\Scripts\activate.bat
```

**Verify Activation:**
```powershell
# You should see (venv) at the start of your prompt
(venv) PS C:\...\backend>
```

---

## 📦 Dependency Issues

### Issue: "No module named 'fastapi'" (or other modules)

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Or install specific package
pip install fastapi
```

**Verify Installation:**
```powershell
pip list | Select-String "fastapi"
```

---

### Issue: Dependencies fail to install

**Error Message:**
```
ERROR: Could not install packages due to an OSError
```

**Solutions:**

**Option 1: Update pip**
```powershell
python -m pip install --upgrade pip
```

**Option 2: Install with --user flag**
```powershell
pip install --user -r requirements.txt
```

**Option 3: Check Python version**
```powershell
python --version  # Must be 3.8 or higher
```

**Option 4: Use virtual environment**
```powershell
# Delete old venv
Remove-Item -Recurse -Force venv

# Create new one
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🗄️ Database Issues

### Issue: "Database is locked"

**Error Message:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**

**Option 1: Close other connections**
- Close any database browser tools (DB Browser for SQLite, etc.)
- Stop any running uvicorn servers
- Restart your terminal

**Option 2: Delete and recreate database**
```powershell
# Stop the server (Ctrl+C)
# Delete database
Remove-Item ecommerce.db -ErrorAction SilentlyContinue
# Recreate
python database.py
```

**Option 3: Check for orphaned processes**
```powershell
# Find python processes
Get-Process python

# Kill if needed (replace PID)
Stop-Process -Id <PID>
```

---

### Issue: "No such table: users" or similar

**Error Message:**
```
sqlite3.OperationalError: no such table: users
```

**Solution:**
```powershell
# Initialize database
python database.py
```

**Verify:**
```powershell
# Check if ecommerce.db exists
Test-Path ecommerce.db  # Should return True

# Check file size
(Get-Item ecommerce.db).Length  # Should be > 0
```

---

### Issue: "Database already contains data"

**Message:**
```
Database already contains data. Skipping seed.
```

**This is normal!** The database keeps data between runs.

**To reseed:**
```powershell
# Delete database
Remove-Item ecommerce.db
# Run again
python database.py
```

---

## 🚀 Server Issues

### Issue: "Address already in use" or "Port 8000 already in use"

**Error Message:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solutions:**

**Option 1: Use different port**
```powershell
uvicorn main:app --reload --port 8001
```

**Option 2: Kill process using port 8000**
```powershell
# Find process
netstat -ano | Select-String ":8000"

# Kill it (replace PID)
Stop-Process -Id <PID> -Force
```

**Option 3: Restart computer**
(Last resort, but always works!)

---

### Issue: "Cannot start uvicorn"

**Error Message:**
```
'uvicorn' is not recognized as an internal or external command
```

**Solutions:**

**Option 1: Ensure venv is activated**
```powershell
.\venv\Scripts\Activate.ps1
```

**Option 2: Run as module**
```powershell
python -m uvicorn main:app --reload
```

**Option 3: Reinstall uvicorn**
```powershell
pip install --force-reinstall uvicorn
```

---

### Issue: "Application startup failed"

**Check these:**

1. **Working directory**
   ```powershell
   # Must be in backend folder
   cd backend
   pwd  # Should show .../backend
   ```

2. **main.py exists**
   ```powershell
   Test-Path main.py  # Should return True
   ```

3. **No syntax errors**
   ```powershell
   python -c "import main"
   # Should not show errors
   ```

4. **Check logs**
   - Look at the error message in terminal
   - Often shows which module or import failed

---

## 🤖 OpenAI API Issues

### Issue: "Incorrect API key provided"

**Error Message:**
```
openai.error.AuthenticationError: Incorrect API key provided
```

**Solutions:**

1. **Check .env file exists**
   ```powershell
   Test-Path .env  # Should return True
   ```

2. **Check API key format**
   - Should start with `sk-`
   - No spaces before/after
   - No quotes needed

   **Correct:**
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   ```

   **Wrong:**
   ```
   OPENAI_API_KEY = "sk-proj-xxx"  # No spaces, no quotes
   ```

3. **Restart server after changing .env**
   ```powershell
   # Stop server (Ctrl+C)
   # Start again
   uvicorn main:app --reload
   ```

---

### Issue: "You exceeded your current quota"

**Error Message:**
```
openai.error.RateLimitError: You exceeded your current quota
```

**What it means:** No credits left in OpenAI account

**Solutions:**

1. **Add credits to OpenAI account**
   - Visit https://platform.openai.com/account/billing
   - Add payment method

2. **Use fallback mode**
   - The system automatically uses rule-based explanations
   - Works without OpenAI API!
   - Just remove or comment out API key in .env

---

### Issue: "Connection timeout" or "Network error"

**Error Message:**
```
openai.error.APIConnectionError: Error communicating with OpenAI
```

**Solutions:**

1. **Check internet connection**
2. **Check firewall/proxy settings**
3. **Try again** - Sometimes OpenAI API is temporarily down
4. **Use fallback mode** - System will automatically fall back

---

## 🌐 API / Browser Issues

### Issue: "Cannot connect to localhost:8000"

**Browser shows:** "This site can't be reached"

**Solutions:**

1. **Verify server is running**
   ```powershell
   # Should see:
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

2. **Try different URL formats**
   - http://localhost:8000
   - http://127.0.0.1:8000
   - http://0.0.0.0:8000

3. **Check firewall**
   - Windows Firewall might block
   - Allow Python through firewall

4. **Restart server**
   - Stop (Ctrl+C)
   - Start again

---

### Issue: "404 Not Found" on API endpoints

**Browser/Request shows:** 404 error

**Solutions:**

1. **Check URL spelling**
   - ✅ `/recommend/1`
   - ❌ `/recommendations/1`
   - ❌ `/Recommend/1` (case-sensitive)

2. **Check server logs**
   - Look for error messages
   - Shows which endpoints are registered

3. **Verify in docs**
   - Visit http://localhost:8000/docs
   - See all available endpoints

---

### Issue: "CORS errors" in browser console

**Error Message:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**This shouldn't happen** - CORS is enabled for all origins

**If it does:**

Check `main.py` has this:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be present
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing Issues

### Issue: test_system.py fails

**Solutions based on which test fails:**

**"Package Imports" fails:**
```powershell
pip install -r requirements.txt
```

**"Database Setup" fails:**
```powershell
python database.py
```

**"Recommendation Logic" fails:**
- Check database has data
- Check no code errors in recommendation.py

**"API Endpoints" fails:**
- Make sure server is running
- `uvicorn main:app --reload` in another terminal

---

## 💻 IDE / Editor Issues

### Issue: "Import could not be resolved" in VS Code

**Red squiggly lines under imports**

**Solutions:**

1. **Select Python interpreter**
   - Ctrl+Shift+P
   - "Python: Select Interpreter"
   - Choose venv interpreter

2. **Restart VS Code**

3. **Install Python extension**
   - Search for "Python" in extensions
   - Install official Microsoft extension

---

### Issue: "Pylance reports import errors"

**Solutions:**

1. **Set Python path**
   - File → Preferences → Settings
   - Search "python.defaultInterpreterPath"
   - Set to venv python.exe

2. **Add to workspace settings**
   Create `.vscode/settings.json`:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/Scripts/python.exe"
   }
   ```

---

## 🎯 Common Workflow Issues

### Issue: "Recommendations are all the same"

**Why:** Not enough diverse interaction data

**Solutions:**

1. **Add more interactions**
   Edit `database.py` seed_mock_data() function

2. **Add more products**
   Add products with different categories/tags

3. **Adjust scoring weights**
   Edit `recommendation.py` scoring function

---

### Issue: "Explanations are generic"

**Why:** Either fallback mode OR prompt needs tuning

**Solutions:**

1. **Check OpenAI API is working**
   - Verify API key in .env
   - Check for errors in terminal

2. **Customize prompts**
   - Edit `llm.py`
   - Modify prompt template
   - Adjust temperature/tokens

---

### Issue: "No recommendations returned"

**Response shows:** `"recommended_products": []`

**Solutions:**

1. **Check user has interactions**
   ```powershell
   # Test with user 1 (Alice) - has interactions
   Invoke-RestMethod http://localhost:8000/recommend/1
   ```

2. **Check products exist**
   ```powershell
   Invoke-RestMethod http://localhost:8000/products
   ```

3. **Reseed database**
   ```powershell
   Remove-Item ecommerce.db
   python database.py
   ```

---

## 🆘 Emergency Reset

### When nothing works, do this:

```powershell
# 1. Stop all servers (Ctrl+C)

# 2. Delete everything generated
Remove-Item -Recurse -Force venv
Remove-Item ecommerce.db -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue

# 3. Start fresh
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python database.py
uvicorn main:app --reload

# 4. Test
Invoke-RestMethod http://localhost:8000
```

---

## 📞 Still Stuck?

### Before asking for help, gather this info:

1. **System Info**
   ```powershell
   python --version
   pip --version
   $PSVersionTable.PSVersion
   ```

2. **Error Message**
   - Full error text
   - Stack trace if available

3. **What you tried**
   - List of solutions attempted

4. **Screenshots**
   - Terminal output
   - Error messages

### Where to get help:

- Check GitHub issues
- Read documentation files
- Review code comments
- Use `/docs` endpoint

---

## ✅ Verification Checklist

After fixing issues, verify everything works:

- [ ] Virtual environment activates
- [ ] Dependencies install successfully
- [ ] Database initializes and seeds
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] `/docs` endpoint loads
- [ ] `/recommend/1` returns recommendations
- [ ] test_system.py passes all tests

---

**Happy Troubleshooting! 🔧**

*Most issues are solved by: restarting terminal, recreating venv, or reseeding database.*
