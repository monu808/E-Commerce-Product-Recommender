# E-Commerce Product Recommender System 🛍️

An AI-powered product recommendation system built with **FastAPI**, **SQLite**, and **OpenAI GPT** that provides personalized product recommendations with natural language explanations.

## 🌟 Features

- **Content-Based Recommendation Engine**: Recommends products based on user browsing and purchase history
- **AI-Powered Explanations**: Uses OpenAI GPT to generate natural, personalized explanations for recommendations
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **SQLite Database**: Lightweight database with SQLAlchemy ORM
- **Mock Data**: Pre-seeded with realistic user and product data for testing
- **CORS Enabled**: Ready for frontend integration

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application and API endpoints
├── database.py          # SQLAlchemy models and database initialization
├── recommendation.py    # Recommendation algorithm logic
├── llm.py              # OpenAI integration for explanations
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- OpenAI API key (optional, but recommended for LLM explanations)

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note**: The system will work without an OpenAI API key, but will use fallback explanations instead of AI-generated ones.

### 4. Initialize Database

```bash
# Run the database initialization script
python database.py
```

This will create the SQLite database and seed it with mock data:
- 4 users (Alice, Bob, Charlie, Diana)
- 15 products across Electronics, Accessories, and Home categories
- ~20 user interactions (views, clicks, purchases)

### 5. Run the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload

# Or run directly
python main.py
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Main Endpoints

#### 🎯 Get Recommendations
```http
GET /recommend/{user_id}?top_n=5
```

**Example Request:**
```bash
curl http://localhost:8000/recommend/1
```

**Example Response:**
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
      "description": "Premium over-ear headphones with active noise cancellation",
      "tags": "electronics,audio,headphones,noise-cancelling"
    },
    {
      "id": 15,
      "name": "Wireless Earbuds",
      "category": "Electronics",
      "price": 79.99,
      "description": "True wireless earbuds with charging case",
      "tags": "electronics,audio,earbuds,wireless"
    }
  ],
  "llm_explanation": "Hi Alice! Based on your recent purchase of a Bluetooth Speaker and your interest in audio products, we think you'd love these Noise Cancelling Headphones and Wireless Earbuds. These recommendations perfectly match your passion for high-quality audio equipment. Happy shopping!",
  "user_behavior_summary": "Recently purchased: Bluetooth Speaker. Recently viewed: Bluetooth Speaker, Noise Cancelling Headphones, Wireless Earbuds. Interested in categories: Electronics"
}
```

#### 👥 Get All Users
```http
GET /users
```

#### 🛒 Get All Products
```http
GET /products
GET /products?category=Electronics
```

#### 📊 Get Categories
```http
GET /categories
```

## 🧠 How It Works

### 1. Recommendation Algorithm

The system uses **content-based filtering**:

1. **User Profile Building**: Analyzes user's interaction history (views, purchases)
2. **Interest Extraction**: Identifies preferred categories and tags
3. **Product Scoring**: Calculates relevance scores based on:
   - Category matches (weight: 10.0)
   - Tag matches (weight: 3.0 per tag)
4. **Ranking**: Sorts products by score and returns top N

### 2. LLM Explanation Generation

For each recommendation set:

1. **Context Gathering**: Formats user behavior and recommended products
2. **Prompt Engineering**: Creates a natural prompt for the LLM
3. **API Call**: Sends request to OpenAI GPT-3.5-turbo
4. **Fallback**: Uses rule-based explanations if API fails

### 3. Database Schema

```
users
├── id (PK)
└── name

products
├── id (PK)
├── name
├── category
├── price
├── description
└── tags

interactions
├── id (PK)
├── user_id (FK)
├── product_id (FK)
└── action_type (view/click/purchase)
```

## 🧪 Testing

### Test with different users:

```bash
# User 1 (Alice) - Likes audio products
curl http://localhost:8000/recommend/1

# User 2 (Bob) - Computer accessories enthusiast  
curl http://localhost:8000/recommend/2

# User 3 (Charlie) - Setting up home office
curl http://localhost:8000/recommend/3

# User 4 (Diana) - Mobile accessories
curl http://localhost:8000/recommend/4
```

### Using PowerShell:

```powershell
# Test the API
Invoke-RestMethod -Uri http://localhost:8000/recommend/1 -Method Get | ConvertTo-Json -Depth 5
```

## 🔧 Configuration Options

### Environment Variables (.env)

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./ecommerce.db
```

### Recommendation Parameters

In `recommendation.py`, adjust scoring weights:

```python
# Category match weight
if product.category in user_profile["interested_categories"]:
    score += 10.0  # Adjust this value

# Tag match weight
score += len(matching_tags) * 3.0  # Adjust multiplier
```

## 📈 Future Enhancements

- [ ] Add collaborative filtering (user-user similarity)
- [ ] Implement real-time interaction tracking
- [ ] Add popularity-based boosting
- [ ] Create user preference learning system
- [ ] Build React/Tailwind frontend dashboard
- [ ] Add product image support
- [ ] Implement A/B testing framework
- [ ] Add caching layer for performance
- [ ] Support for multiple LLM providers
- [ ] Add recommendation diversity controls

## 🐛 Troubleshooting

### Database Issues

```bash
# Delete and recreate database
rm ecommerce.db
python database.py
```

### Port Already in Use

```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### OpenAI API Errors

- Check your API key is valid
- Ensure you have credits in your OpenAI account
- System will automatically use fallback explanations if API fails

## 📄 License

MIT License - Feel free to use this project for learning and development!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, SQLAlchemy, and OpenAI**
