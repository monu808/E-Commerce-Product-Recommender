# 🎯 Customizing Recommendations Guide

Advanced techniques to tune and improve your recommendation algorithm.

---

## 📋 Table of Contents

1. Understanding the Algorithm
2. Scoring System Tuning
3. Advanced Filtering Techniques
4. Collaborative Filtering
5. Hybrid Approaches
6. Performance Optimization

---

## 1. 🧠 Understanding the Current Algorithm

### **Current Implementation: Content-Based Filtering**

The system recommends products based on:
- **User's browsing history** (viewed products)
- **Purchase history** (bought products)
- **Category preferences** (Electronics, Accessories, etc.)
- **Tag matching** (audio, wireless, bluetooth, etc.)

### **How Scoring Works:**

```python
# Current scoring in recommendation.py

score = 0

# Category match (highest weight)
if product.category in user_preferences:
    score += 10.0  # ⚡ Primary signal

# Tag matches (secondary weight)
for tag in product_tags:
    if tag in user_interested_tags:
        score += 3.0  # 🎯 Secondary signal

# Products already viewed/purchased = score 0 (excluded)
```

---

## 2. ⚙️ Scoring System Tuning

### **A. Adjust Basic Weights**

Edit `backend/recommendation.py`:

```python
def calculate_product_score(product: Product, user_profile: Dict, already_interacted: List[int]) -> float:
    """
    Calculate relevance score with custom weights
    """
    if product.id in already_interacted:
        return 0.0
    
    score = 0.0
    
    # ===== TUNE THESE VALUES =====
    
    # 1. Category Match Weight
    CATEGORY_WEIGHT = 15.0  # Increase from 10.0 for stronger category preference
    
    # 2. Tag Match Weight  
    TAG_WEIGHT = 4.0  # Increase from 3.0 for stronger tag influence
    
    # 3. Price Preference Weight (NEW)
    PRICE_WEIGHT = 2.0
    
    # ===== SCORING LOGIC =====
    
    # Category scoring
    if product.category in user_profile["interested_categories"]:
        category_rank = user_profile["interested_categories"].index(product.category)
        # First category gets full weight, others get diminishing weight
        score += CATEGORY_WEIGHT * (1.0 / (category_rank + 1))
    
    # Tag scoring
    if product.tags:
        product_tags = [tag.strip() for tag in product.tags.split(",")]
        matching_tags = set(product_tags) & set(user_profile["interested_tags"])
        
        # Award points for each matching tag
        score += len(matching_tags) * TAG_WEIGHT
    
    # Price scoring (prefer similar price range)
    if user_profile.get("avg_price"):
        price_diff = abs(product.price - user_profile["avg_price"])
        # Lower score for products far from user's typical price range
        if price_diff < 50:
            score += PRICE_WEIGHT * (1 - price_diff / 50)
    
    return score
```

---

### **B. Add Purchase History Weight**

Purchases are stronger signals than views:

```python
def get_user_profile(db: Session, user_id: int) -> Dict:
    """Enhanced user profiling with purchase weighting"""
    
    interactions = get_user_interactions(db, user_id)
    
    if not interactions:
        return {"viewed_products": [], "purchased_products": [], 
                "interested_categories": [], "interested_tags": []}
    
    viewed_products = []
    purchased_products = []
    all_tags = []
    all_categories = []
    category_weights = {}  # NEW: Track category importance
    tag_weights = {}       # NEW: Track tag importance
    
    for interaction in interactions:
        product = db.query(Product).filter(Product.id == interaction.product_id).first()
        if not product:
            continue
        
        # Assign different weights based on action type
        if interaction.action_type == "purchase":
            weight = 5.0  # Purchases are 5x more important
            purchased_products.append(product)
        elif interaction.action_type == "click":
            weight = 2.0  # Clicks are 2x more important than views
        else:  # view
            weight = 1.0
            viewed_products.append(product)
        
        # Weight the categories
        category_weights[product.category] = category_weights.get(product.category, 0) + weight
        
        # Weight the tags
        if product.tags:
            for tag in product.tags.split(","):
                tag = tag.strip()
                tag_weights[tag] = tag_weights.get(tag, 0) + weight
    
    # Sort by weighted importance
    sorted_categories = sorted(category_weights.items(), key=lambda x: x[1], reverse=True)
    sorted_tags = sorted(tag_weights.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate average price from purchases
    avg_price = sum(p.price for p in purchased_products) / len(purchased_products) if purchased_products else None
    
    return {
        "viewed_products": viewed_products,
        "purchased_products": purchased_products,
        "interested_categories": [cat for cat, _ in sorted_categories[:3]],
        "interested_tags": [tag for tag, _ in sorted_tags[:5]],
        "category_weights": category_weights,
        "tag_weights": tag_weights,
        "avg_price": avg_price,
        "interaction_count": len(interactions)
    }
```

---

### **C. Add Recency Scoring**

Recent interactions matter more:

```python
from datetime import datetime, timedelta

def calculate_recency_score(interaction_date: datetime) -> float:
    """
    Recent interactions get higher scores
    """
    days_ago = (datetime.now() - interaction_date).days
    
    if days_ago <= 7:
        return 1.0  # Last week: full weight
    elif days_ago <= 30:
        return 0.7  # Last month: 70% weight
    elif days_ago <= 90:
        return 0.4  # Last 3 months: 40% weight
    else:
        return 0.1  # Older: 10% weight
```

Then add a `created_at` column to the Interaction model:

```python
# In database.py

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    action_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # NEW
    
    user = relationship("User", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")
```

---

## 3. 🎯 Advanced Filtering Techniques

### **A. Diversity Boost**

Avoid recommending only one category:

```python
def apply_diversity_boost(recommendations: List[Tuple[Product, float]]) -> List[Product]:
    """
    Ensure category diversity in recommendations
    """
    diverse_recs = []
    used_categories = set()
    remaining_recs = []
    
    # First pass: one product per category
    for product, score in recommendations:
        if product.category not in used_categories:
            diverse_recs.append(product)
            used_categories.add(product.category)
        else:
            remaining_recs.append(product)
        
        if len(diverse_recs) >= 3:  # At least 3 different categories
            break
    
    # Second pass: fill remaining slots
    diverse_recs.extend(remaining_recs[:10 - len(diverse_recs)])
    
    return diverse_recs
```

---

### **B. Price Range Filtering**

```python
def filter_by_price_range(
    products: List[Product],
    user_profile: Dict,
    tolerance: float = 0.5
) -> List[Product]:
    """
    Filter products within user's typical price range
    tolerance: 0.5 = ±50% of average price
    """
    if not user_profile.get("avg_price"):
        return products
    
    avg_price = user_profile["avg_price"]
    min_price = avg_price * (1 - tolerance)
    max_price = avg_price * (1 + tolerance)
    
    return [p for p in products if min_price <= p.price <= max_price]
```

---

### **C. Popularity Boost**

Popular products get a small boost:

```python
def add_popularity_score(db: Session, product: Product) -> float:
    """
    Add popularity score based on total interactions
    """
    interaction_count = db.query(Interaction).filter(
        Interaction.product_id == product.id
    ).count()
    
    # Log scale to prevent popular items from dominating
    import math
    popularity_score = math.log(interaction_count + 1) * 0.5
    
    return popularity_score
```

---

## 4. 🤝 Collaborative Filtering

Add user-to-user similarity:

### **Implementation**

Create `backend/collaborative_filtering.py`:

```python
"""
Collaborative filtering: Find similar users and recommend what they liked
"""
from sqlalchemy.orm import Session
from database import User, Product, Interaction
from typing import List, Dict, Tuple
from collections import Counter
import math


def calculate_user_similarity(user1_interactions: List[int], user2_interactions: List[int]) -> float:
    """
    Calculate Jaccard similarity between two users based on their interactions
    """
    set1 = set(user1_interactions)
    set2 = set(user2_interactions)
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def find_similar_users(db: Session, user_id: int, top_n: int = 5) -> List[Tuple[int, float]]:
    """
    Find users with similar interaction patterns
    Returns: [(user_id, similarity_score), ...]
    """
    # Get target user's interactions
    target_interactions = db.query(Interaction.product_id).filter(
        Interaction.user_id == user_id
    ).all()
    target_product_ids = [i.product_id for i in target_interactions]
    
    # Get all other users
    all_users = db.query(User).filter(User.id != user_id).all()
    
    similarities = []
    
    for user in all_users:
        # Get this user's interactions
        user_interactions = db.query(Interaction.product_id).filter(
            Interaction.user_id == user.id
        ).all()
        user_product_ids = [i.product_id for i in user_interactions]
        
        # Calculate similarity
        similarity = calculate_user_similarity(target_product_ids, user_product_ids)
        
        if similarity > 0:
            similarities.append((user.id, similarity))
    
    # Sort by similarity and return top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]


def get_collaborative_recommendations(
    db: Session,
    user_id: int,
    top_n: int = 10
) -> List[Product]:
    """
    Recommend products that similar users interacted with
    """
    # Find similar users
    similar_users = find_similar_users(db, user_id)
    
    if not similar_users:
        return []
    
    # Get products that user hasn't interacted with
    user_product_ids = {
        i.product_id for i in db.query(Interaction.product_id).filter(
            Interaction.user_id == user_id
        ).all()
    }
    
    # Collect products from similar users, weighted by similarity
    product_scores = Counter()
    
    for similar_user_id, similarity in similar_users:
        # Get products this similar user liked (purchased)
        liked_products = db.query(Interaction).filter(
            Interaction.user_id == similar_user_id,
            Interaction.action_type.in_(["purchase", "click"])
        ).all()
        
        for interaction in liked_products:
            if interaction.product_id not in user_product_ids:
                # Weight by similarity and action type
                weight = similarity
                if interaction.action_type == "purchase":
                    weight *= 2.0
                
                product_scores[interaction.product_id] += weight
    
    # Get top products
    top_product_ids = [pid for pid, _ in product_scores.most_common(top_n)]
    
    # Fetch product objects
    products = db.query(Product).filter(Product.id.in_(top_product_ids)).all()
    
    # Sort by score
    products_with_scores = [(p, product_scores[p.id]) for p in products]
    products_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [p for p, _ in products_with_scores]
```

---

## 5. 🔀 Hybrid Approach

Combine content-based and collaborative filtering:

Update `backend/recommendation.py`:

```python
from collaborative_filtering import get_collaborative_recommendations

def get_hybrid_recommendations(
    db: Session,
    user_id: int,
    top_n: int = 10,
    content_weight: float = 0.7,
    collab_weight: float = 0.3
) -> List[Product]:
    """
    Combine content-based and collaborative filtering
    
    Args:
        content_weight: Weight for content-based (0.0 to 1.0)
        collab_weight: Weight for collaborative (0.0 to 1.0)
    """
    # Get content-based recommendations
    content_recs, user_profile = get_recommendations(db, user_id, top_n * 2)
    
    # Get collaborative recommendations
    collab_recs = get_collaborative_recommendations(db, user_id, top_n * 2)
    
    # Combine scores
    combined_scores = {}
    
    # Score content-based recs
    for i, product in enumerate(content_recs):
        score = (len(content_recs) - i) * content_weight
        combined_scores[product.id] = combined_scores.get(product.id, 0) + score
    
    # Score collaborative recs
    for i, product in enumerate(collab_recs):
        score = (len(collab_recs) - i) * collab_weight
        combined_scores[product.id] = combined_scores.get(product.id, 0) + score
    
    # Sort by combined score
    sorted_products = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]
    
    # Fetch products
    product_ids = [pid for pid, _ in sorted_products]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    
    # Sort products by combined score
    product_map = {p.id: p for p in products}
    sorted_product_list = [product_map[pid] for pid, _ in sorted_products if pid in product_map]
    
    return sorted_product_list, user_profile
```

Add endpoint in `main.py`:

```python
@app.get("/recommend-hybrid/{user_id}")
async def recommend_hybrid(
    user_id: int,
    top_n: int = 5,
    content_weight: float = 0.7,
    db: Session = Depends(get_db)
):
    """
    Get hybrid recommendations (content-based + collaborative)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    recommended_products, user_profile = get_hybrid_recommendations(
        db, user_id, top_n, content_weight, 1.0 - content_weight
    )
    
    user_behavior = format_user_behavior(user_profile)
    explanation = await generate_recommendation_explanation_async(
        user, recommended_products, user_behavior
    )
    
    return {
        "user_id": user_id,
        "user_name": user.name,
        "method": "hybrid",
        "content_weight": content_weight,
        "collaborative_weight": 1.0 - content_weight,
        "recommended_products": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "description": p.description,
                "tags": p.tags
            }
            for p in recommended_products
        ],
        "llm_explanation": explanation
    }
```

Test it:
```
http://127.0.0.1:8000/recommend-hybrid/1?content_weight=0.6
```

---

## 6. 🚀 Performance Optimization

### **A. Add Caching**

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache user profiles for 5 minutes
_profile_cache = {}
_cache_timeout = timedelta(minutes=5)

def get_user_profile_cached(db: Session, user_id: int) -> Dict:
    """
    Cached version of get_user_profile
    """
    cache_key = user_id
    current_time = datetime.now()
    
    # Check cache
    if cache_key in _profile_cache:
        profile, timestamp = _profile_cache[cache_key]
        if current_time - timestamp < _cache_timeout:
            return profile
    
    # Generate new profile
    profile = get_user_profile(db, user_id)
    _profile_cache[cache_key] = (profile, current_time)
    
    return profile
```

---

### **B. Batch Processing**

```python
def get_recommendations_batch(
    db: Session,
    user_ids: List[int],
    top_n: int = 5
) -> Dict[int, List[Product]]:
    """
    Generate recommendations for multiple users at once
    """
    results = {}
    
    # Fetch all user profiles at once
    profiles = {
        user_id: get_user_profile(db, user_id)
        for user_id in user_ids
    }
    
    # Fetch all products once
    all_products = db.query(Product).all()
    
    # Score for each user
    for user_id, profile in profiles.items():
        already_interacted = [
            p.id for p in profile["viewed_products"] + profile["purchased_products"]
        ]
        
        product_scores = [
            (product, calculate_product_score(product, profile, already_interacted))
            for product in all_products
        ]
        
        product_scores = [(p, s) for p, s in product_scores if s > 0]
        product_scores.sort(key=lambda x: x[1], reverse=True)
        
        results[user_id] = [p for p, _ in product_scores[:top_n]]
    
    return results
```

---

## 7. 📊 A/B Testing Setup

Test different algorithms:

```python
import random

@app.get("/recommend-ab/{user_id}")
async def recommend_ab_test(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    A/B test different recommendation strategies
    """
    # Randomly assign strategy
    strategy = random.choice(["content", "collaborative", "hybrid"])
    
    if strategy == "content":
        recs, profile = get_recommendations(db, user_id)
    elif strategy == "collaborative":
        recs = get_collaborative_recommendations(db, user_id)
        profile = get_user_profile(db, user_id)
    else:  # hybrid
        recs, profile = get_hybrid_recommendations(db, user_id)
    
    # Log for analytics (implement your logging)
    # log_ab_test(user_id, strategy, recs)
    
    return {
        "strategy": strategy,
        "recommendations": recs
    }
```

---

**🎉 You now have advanced recommendation capabilities!**

Next: See `TUNE_AI_PROMPTS.md` for LLM optimization.
