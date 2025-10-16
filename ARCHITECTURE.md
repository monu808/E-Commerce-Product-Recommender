# 🔄 System Architecture & Workflow

This document explains how the E-Commerce Recommendation System works internally.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                        │
│  (Browser, Mobile App, API Consumer)                    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ HTTP Request (JSON)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER                        │
│                    (main.py)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Endpoints                                    │  │
│  │  - /recommend/{user_id}                          │  │
│  │  - /users, /products, /categories                │  │
│  └───────────────────┬──────────────────────────────┘  │
└────────────────────┬─┴────────────────┬────────────────┘
                     │                  │
        ┌────────────▼──────────┐      │
        │  Recommendation       │      │
        │  Engine               │      │
        │  (recommendation.py)  │      │
        │                       │      │
        │  - User profiling     │      │
        │  - Product scoring    │      │
        │  - Top-N selection    │      │
        └────────────┬──────────┘      │
                     │                  │
        ┌────────────▼──────────┐      │
        │  LLM Integration      │      │
        │  (llm.py)             │      │
        │                       │      │
        │  - OpenAI API         │      │
        │  - Prompt engineering │      │
        │  - Fallback logic     │      │
        └────────────┬──────────┘      │
                     │                  │
                     │         ┌────────▼────────┐
                     │         │  Database Layer │
                     │         │  (database.py)  │
                     └─────────►                 │
                               │  - Users        │
                               │  - Products     │
                               │  - Interactions │
                               └─────────────────┘
```

---

## 🔄 Request Flow: `/recommend/{user_id}`

### Step-by-Step Process

```
1️⃣  CLIENT REQUEST
    │
    │  GET /recommend/1?top_n=5
    │
    ▼
2️⃣  FASTAPI ENDPOINT (main.py)
    │
    │  - Extract user_id from path
    │  - Extract top_n from query params
    │  - Get database session
    │
    ▼
3️⃣  VALIDATE USER
    │
    │  - Query database for user
    │  - If not found → 404 Error
    │  - If found → Continue
    │
    ▼
4️⃣  BUILD USER PROFILE (recommendation.py)
    │
    │  - Get user interactions (views, purchases)
    │  - Extract preferred categories
    │  - Extract interested tags
    │  - Count interaction frequency
    │
    ▼
5️⃣  SCORE PRODUCTS (recommendation.py)
    │
    │  - Get all products from database
    │  - For each product:
    │    • Skip if already interacted
    │    • +10 points for category match
    │    • +3 points per tag match
    │  - Sort by score (descending)
    │
    ▼
6️⃣  SELECT TOP N
    │
    │  - Take top 5 (or requested N) products
    │  - If no recommendations → Return popular items
    │
    ▼
7️⃣  FORMAT USER BEHAVIOR (recommendation.py)
    │
    │  - Create readable summary:
    │    "Recently purchased: X, Y"
    │    "Recently viewed: A, B, C"
    │    "Interested in: Category1, Category2"
    │
    ▼
8️⃣  GENERATE EXPLANATION (llm.py)
    │
    │  ┌─ Has OpenAI API Key? ─┐
    │  │                       │
    │  YES                    NO
    │  │                       │
    │  ├─ Call OpenAI GPT     └─ Use Fallback
    │  │  • Format prompt         • Rule-based
    │  │  • Send API request      • Template fill
    │  │  • Get response          • Return text
    │  │  • Handle errors
    │  │
    │  └─────────┬─────────────────┘
    │            │
    ▼            ▼
9️⃣  BUILD RESPONSE
    │
    │  {
    │    "user_id": 1,
    │    "user_name": "Alice",
    │    "recommended_products": [...],
    │    "llm_explanation": "...",
    │    "user_behavior_summary": "..."
    │  }
    │
    ▼
🔟  RETURN JSON RESPONSE
    │
    │  HTTP 200 OK
    │  Content-Type: application/json
    │
    └──► CLIENT RECEIVES RESPONSE
```

---

## 🧮 Recommendation Algorithm Details

### Content-Based Filtering

```
INPUT: user_id

STEP 1: Get User History
  ├─ Query all interactions for user
  └─ Separate by action_type:
      ├─ viewed_products[]
      └─ purchased_products[]

STEP 2: Extract Preferences
  ├─ Collect all categories → Count frequency
  ├─ Collect all tags → Count frequency
  └─ Result:
      ├─ Top 3 categories
      └─ Top 5 tags

STEP 3: Score All Products
  FOR EACH product IN database:
    
    IF product.id IN already_interacted:
      score = 0 (skip)
      CONTINUE
    
    score = 0
    
    IF product.category IN top_categories:
      score += 10.0
    
    FOR EACH tag IN product.tags:
      IF tag IN top_tags:
        score += 3.0
    
    product_scores.append((product, score))

STEP 4: Rank and Select
  ├─ Sort product_scores by score (DESC)
  └─ Take top N products

OUTPUT: recommended_products[], user_profile{}
```

### Scoring Example

```
User Profile:
  Categories: [Electronics, Accessories]
  Tags: [audio, wireless, bluetooth, portable]

Product: "Wireless Earbuds"
  Category: Electronics
  Tags: [electronics, audio, earbuds, wireless]

Calculation:
  Category match (Electronics): +10
  Tag matches:
    - audio: +3
    - wireless: +3
  Total: 16 points ✓

Product: "Desk Lamp"
  Category: Home
  Tags: [home, lighting, desk, led]

Calculation:
  Category match: 0 (no match)
  Tag matches: 0 (no matches)
  Total: 0 points ✗
```

---

## 🤖 LLM Explanation Generation

### Process Flow

```
INPUT: user, recommended_products[], user_behavior

STEP 1: Check API Key
  ├─ IF API key exists → Use OpenAI
  └─ ELSE → Use fallback

STEP 2: Format Context (OpenAI path)
  ├─ Extract product names
  ├─ Extract categories
  └─ Format user behavior summary

STEP 3: Build Prompt
  ┌──────────────────────────────────────┐
  │ You are a helpful shopping assistant │
  │                                      │
  │ User: {user_name}                    │
  │ Behavior: {behavior_summary}         │
  │                                      │
  │ Recommended Products:                │
  │ - {product_1}                        │
  │ - {product_2}                        │
  │                                      │
  │ Generate friendly explanation...     │
  └──────────────────────────────────────┘

STEP 4: Call OpenAI API
  ├─ Model: gpt-3.5-turbo
  ├─ Temperature: 0.7 (creative)
  ├─ Max tokens: 150
  └─ Handle errors → Fallback if fails

STEP 5: Process Response
  ├─ Extract explanation text
  ├─ Strip whitespace
  └─ Return to caller

FALLBACK PATH:
  ├─ Use template: "Hi {name}! Based on..."
  ├─ Fill with product names
  └─ Add generic recommendation text

OUTPUT: explanation (string)
```

---

## 🗄️ Database Schema & Relationships

```
┌──────────────────┐
│      users       │
├──────────────────┤
│ id (PK)          │
│ name             │
└────────┬─────────┘
         │
         │ 1:N
         │
         ▼
┌──────────────────┐        N:1         ┌──────────────────┐
│  interactions    │──────────────────►│    products      │
├──────────────────┤                    ├──────────────────┤
│ id (PK)          │                    │ id (PK)          │
│ user_id (FK) ────┘                    │ name             │
│ product_id (FK) ──────────────────────│ category         │
│ action_type      │                    │ price            │
│ (view/click/     │                    │ description      │
│  purchase)       │                    │ tags             │
└──────────────────┘                    └──────────────────┘

Relationships:
  - One user can have many interactions
  - One product can have many interactions
  - Each interaction links one user to one product
```

### Query Patterns

```sql
-- Get user's interaction history
SELECT * FROM interactions
WHERE user_id = ?
ORDER BY id DESC;

-- Get products in a category
SELECT * FROM products
WHERE category = ?;

-- Get user's viewed products
SELECT p.* FROM products p
JOIN interactions i ON p.id = i.product_id
WHERE i.user_id = ? AND i.action_type = 'view';

-- Get popular products (most interactions)
SELECT p.*, COUNT(i.id) as interaction_count
FROM products p
LEFT JOIN interactions i ON p.id = i.product_id
GROUP BY p.id
ORDER BY interaction_count DESC
LIMIT ?;
```

---

## 🔌 API Endpoint Flows

### 1. Health Check: `GET /`

```
Request → Endpoint → Return static info
          (No DB query needed)
```

### 2. List Users: `GET /users`

```
Request → Query DB → Format response
          ├─ SELECT * FROM users
          └─ Return {count, users[]}
```

### 3. Get Product: `GET /products/{id}`

```
Request → Validate ID → Query DB → Return product
          ├─ Check if ID is integer
          ├─ SELECT * FROM products WHERE id = ?
          ├─ If not found → 404
          └─ Return product details
```

### 4. Recommend: `GET /recommend/{user_id}`

```
Request → Validate → Profile → Score → LLM → Response
          ├─ Check user exists
          ├─ Build user profile
          ├─ Score all products
          ├─ Generate explanation
          └─ Return full recommendation
```

---

## ⚡ Performance Considerations

### Current Implementation

- **Database**: SQLite (single file, no network overhead)
- **Queries**: Simple SELECT statements (fast)
- **Caching**: None (every request queries DB)
- **LLM Calls**: Synchronous (blocks during API call)

### Optimization Opportunities

```
🔄 Add Caching
  ├─ User profiles (Redis/in-memory)
  ├─ Product catalog
  └─ Recommendation results (TTL: 5 min)

⚡ Async Processing
  ├─ LLM calls (already has async function)
  ├─ Database queries (use async SQLAlchemy)
  └─ Parallel product scoring

📊 Database Optimization
  ├─ Add indexes on foreign keys
  ├─ Migrate to PostgreSQL for production
  └─ Connection pooling

🧠 Algorithm Enhancement
  ├─ Pre-compute user profiles
  ├─ Batch process recommendations
  └─ Add collaborative filtering
```

---

## 🔒 Security & Best Practices

### Current Implementation

```
✅ IMPLEMENTED:
  ├─ Environment variables for secrets
  ├─ CORS middleware
  ├─ Input validation (FastAPI Pydantic)
  ├─ Database ORM (SQLAlchemy)
  └─ Error handling

⚠️  FOR PRODUCTION:
  ├─ Add authentication (JWT tokens)
  ├─ Rate limiting (API calls)
  ├─ Input sanitization (SQL injection protection)
  ├─ HTTPS only
  ├─ API key rotation
  └─ Logging and monitoring
```

---

## 📈 Scalability Path

### Phase 1: Current (Single Server)
```
Client → FastAPI → SQLite
         (1 server)
```

### Phase 2: Add Caching
```
Client → FastAPI → Redis Cache → SQLite
         (1 server)     (1 Redis)
```

### Phase 3: Load Balancing
```
         ┌─ FastAPI 1 ─┐
Client → Load Balancer  ├─→ Redis → PostgreSQL
         └─ FastAPI 2 ─┘
```

### Phase 4: Microservices
```
         ┌─ API Gateway ─┐
         │               │
Client → ├─ Rec Service  ├─→ Redis → PostgreSQL
         │               │
         └─ LLM Service ─┘
```

---

## 🧪 Testing Strategy

### Unit Tests
```
✓ Database models
✓ Recommendation algorithm
✓ Scoring logic
✓ LLM prompt generation
```

### Integration Tests
```
✓ API endpoints
✓ Database queries
✓ OpenAI API calls
✓ Error handling
```

### End-to-End Tests
```
✓ Complete user flow
✓ Multiple user scenarios
✓ Edge cases (no history, etc.)
```

---

## 📚 Further Reading

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Content-Based Filtering**: https://en.wikipedia.org/wiki/Recommender_system
- **OpenAI API**: https://platform.openai.com/docs/

---

**System Architecture Complete! 🎉**

*This document explains the inner workings of your recommendation system.*
