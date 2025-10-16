"""
FastAPI application for E-commerce Product Recommender System
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import uvicorn

from database import get_db, init_db, seed_mock_data, User, Product
from recommendation import get_recommendations, format_user_behavior
from llm import generate_recommendation_explanation_async

# Initialize FastAPI app
app = FastAPI(
    title="E-Commerce Product Recommender API",
    description="AI-powered product recommendation system with natural language explanations",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class ProductResponse:
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.category = product.category
        self.price = product.price
        self.description = product.description
        self.tags = product.tags


class RecommendationResponse:
    def __init__(self, user_id: int, recommended_products: List[ProductResponse], llm_explanation: str):
        self.user_id = user_id
        self.recommended_products = recommended_products
        self.llm_explanation = llm_explanation


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting E-Commerce Recommender API...")
    init_db()
    seed_mock_data()
    print("✅ Database initialized and seeded!")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "E-Commerce Product Recommender API is running!",
        "version": "1.0.0",
        "endpoints": {
            "recommend": "/recommend/{user_id}",
            "users": "/users",
            "products": "/products"
        }
    }


@app.get("/recommend/{user_id}")
async def recommend_products(
    user_id: int,
    top_n: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get product recommendations for a specific user with LLM explanation
    
    Args:
        user_id: The ID of the user to get recommendations for
        top_n: Number of recommendations to return (default: 5)
    
    Returns:
        JSON with recommended products and explanation
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Get recommendations
    recommended_products, user_profile = get_recommendations(db, user_id, top_n)
    
    if not recommended_products:
        return {
            "user_id": user_id,
            "user_name": user.name,
            "recommended_products": [],
            "llm_explanation": f"Hello {user.name}! We don't have enough products to recommend right now. Please check back later!"
        }
    
    # Format user behavior for LLM
    user_behavior = format_user_behavior(user_profile)
    
    # Generate LLM explanation
    explanation = await generate_recommendation_explanation_async(
        user, recommended_products, user_behavior
    )
    
    # Format response
    product_responses = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "description": p.description,
            "tags": p.tags.split(",") if p.tags else []
        }
        for p in recommended_products
    ]
    
    return {
        "user_id": user_id,
        "user_name": user.name,
        "recommended_products": product_responses,
        "llm_explanation": explanation,
        "user_behavior_summary": user_behavior
    }


@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users in the system"""
    users = db.query(User).all()
    return {
        "count": len(users),
        "users": [{"id": u.id, "name": u.name} for u in users]
    }


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get details of a specific user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "interaction_count": len(user.interactions)
    }


@app.get("/products")
async def get_all_products(
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get all products, optionally filtered by category"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.all()
    
    return {
        "count": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "description": p.description,
                "tags": p.tags.split(",") if p.tags else []
            }
            for p in products
        ]
    }


@app.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get details of a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": product.price,
        "description": product.description,
        "tags": product.tags.split(",") if product.tags else []
    }


@app.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique product categories"""
    categories = db.query(Product.category).distinct().all()
    return {
        "categories": [cat[0] for cat in categories]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
