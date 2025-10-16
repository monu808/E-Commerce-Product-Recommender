# 🛍️ E-Commerce Product Recommender System

An intelligent product recommendation system that combines **machine learning algorithms** with **AI-powered explanations** to deliver personalized shopping experiences.

## 🎯 Overview

This project demonstrates how to build a modern recommendation system that:
- Analyzes user behavior (views, clicks, purchases)
- Recommends relevant products using content-based filtering
- Explains recommendations in natural language using LLM (OpenAI GPT)
- Provides a RESTful API for easy integration

## ✨ Key Features

- **Smart Recommendations**: Content-based filtering algorithm that learns from user interactions
- **AI Explanations**: Natural language explanations powered by OpenAI GPT
- **RESTful API**: Built with FastAPI for high performance and easy integration
- **SQLite Database**: Lightweight and portable database with SQLAlchemy ORM
- **Mock Data**: Pre-populated with realistic e-commerce data for immediate testing
- **Production Ready**: Includes error handling, CORS support, and API documentation

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
│  (Browser/  │
│    App)     │
└──────┬──────┘
       │
       │ HTTP Request
       ▼
┌─────────────────────────────────┐
│      FastAPI Backend            │
│  ┌──────────────────────────┐  │
│  │  Recommendation Engine   │  │
│  │  (Content-Based Filter)  │  │
│  └──────────────────────────┘  │
│              ▼                  │
│  ┌──────────────────────────┐  │
│  │   OpenAI LLM Integration │  │
│  │  (Explanation Generator) │  │
│  └──────────────────────────┘  │
│              ▼                  │
│  ┌──────────────────────────┐  │
│  │   SQLite Database        │  │
│  │   (Users, Products,      │  │
│  │    Interactions)         │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key (optional, but recommended)

### Installation

1. **Clone the repository**
   ```bash
   cd E-Commerce-Product-Recommender
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy environment template
   copy .env.example .env
   
   # Edit .env and add your OpenAI API key (optional)
   # OPENAI_API_KEY=sk-your-key-here
   ```

4. **Initialize database**
   ```bash
   python database.py
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Test the API**
   - Open your browser: http://localhost:8000
   - View API docs: http://localhost:8000/docs
   - Try a recommendation: http://localhost:8000/recommend/1

## 📖 Usage Examples

### Get Recommendations for a User

**Request:**
```bash
curl http://localhost:8000/recommend/1
```

**Response:**
```json
{
  "user_id": 1,
  "user_name": "Alice Johnson",
  "recommended_products": [
    {
      "id": 6,
      "name": "Noise Cancelling Headphones",
      "category": "Electronics",
      "price": 199.99
    }
  ],
  "llm_explanation": "These headphones are perfect for you, Alice! Since you recently bought a Bluetooth Speaker and have been browsing audio equipment, we think you'll love the premium sound quality and noise cancellation features."
}
```

### List All Users

```bash
curl http://localhost:8000/users
```

### Browse Products

```bash
curl http://localhost:8000/products
curl http://localhost:8000/products?category=Electronics
```

## 🧪 Demo Users

The system comes with 4 pre-configured users:

1. **Alice Johnson** (ID: 1) - Audio enthusiast
2. **Bob Smith** (ID: 2) - Computer accessories fan
3. **Charlie Brown** (ID: 3) - Home office setup
4. **Diana Prince** (ID: 4) - Mobile accessories lover

Try recommendations for each user to see different results!

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | FastAPI |
| Database | SQLite + SQLAlchemy ORM |
| AI/LLM | OpenAI GPT-3.5-turbo |
| Language | Python 3.8+ |
| API Documentation | Swagger/OpenAPI |

## 📊 Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Products Table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    tags TEXT
);

-- Interactions Table
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    action_type TEXT NOT NULL  -- 'view', 'click', 'purchase'
);
```

## 🎓 How It Works

### 1. Content-Based Filtering

The recommendation engine:
1. Analyzes user's past interactions (views, purchases)
2. Extracts preferred categories and tags
3. Scores all products based on similarity to user preferences
4. Returns top-ranked products

### 2. LLM-Powered Explanations

For each recommendation:
1. System gathers user behavior context
2. Formats a natural language prompt
3. Sends to OpenAI GPT-3.5-turbo
4. Receives personalized explanation
5. Falls back to rule-based explanation if API unavailable

## 📁 Project Structure

```
E-Commerce-Product-Recommender/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── database.py          # Database models & setup
│   ├── recommendation.py    # Recommendation logic
│   ├── llm.py              # OpenAI integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment template
│   └── README.md           # Backend documentation
├── .gitignore
└── README.md               # This file
```

## 🔮 Future Enhancements

- [ ] React/Tailwind frontend dashboard
- [ ] Collaborative filtering (user-user similarity)
- [ ] Real-time interaction tracking
- [ ] Product images and ratings
- [ ] User authentication system
- [ ] Advanced analytics dashboard
- [ ] A/B testing framework
- [ ] Redis caching layer
- [ ] Docker containerization
- [ ] PostgreSQL support for production

## 📚 API Documentation

Once the server is running, comprehensive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI for GPT API
- SQLAlchemy for database ORM

## 📞 Support

If you encounter any issues or have questions:
1. Check the [backend README](backend/README.md) for detailed setup instructions
2. Review the API documentation at `/docs`
3. Open an issue on GitHub

---

**Happy Coding! 🚀**

Built with ❤️ for learning and demonstrating modern AI-powered e-commerce solutions.
