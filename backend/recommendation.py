"""
Product recommendation logic using content-based filtering
"""
from sqlalchemy.orm import Session
from database import Product, Interaction, User
from typing import List, Dict, Tuple
from collections import Counter


def get_user_interactions(db: Session, user_id: int) -> List[Interaction]:
    """Get all interactions for a specific user"""
    return db.query(Interaction).filter(Interaction.user_id == user_id).all()


def get_user_profile(db: Session, user_id: int) -> Dict:
    """Build a user profile based on their interaction history"""
    interactions = get_user_interactions(db, user_id)
    
    if not interactions:
        return {
            "viewed_products": [],
            "purchased_products": [],
            "interested_categories": [],
            "interested_tags": []
        }
    
    viewed_products = []
    purchased_products = []
    all_tags = []
    all_categories = []
    
    for interaction in interactions:
        product = db.query(Product).filter(Product.id == interaction.product_id).first()
        if product:
            if interaction.action_type == "view":
                viewed_products.append(product)
            elif interaction.action_type == "purchase":
                purchased_products.append(product)
            
            # Collect tags and categories
            all_categories.append(product.category)
            if product.tags:
                all_tags.extend([tag.strip() for tag in product.tags.split(",")])
    
    # Count most common categories and tags
    category_counter = Counter(all_categories)
    tag_counter = Counter(all_tags)
    
    return {
        "viewed_products": viewed_products,
        "purchased_products": purchased_products,
        "interested_categories": [cat for cat, _ in category_counter.most_common(3)],
        "interested_tags": [tag for tag, _ in tag_counter.most_common(5)],
        "interaction_count": len(interactions)
    }


def calculate_product_score(product: Product, user_profile: Dict, already_interacted: List[int]) -> float:
    """
    Calculate a relevance score for a product based on user profile
    Higher score = more relevant
    """
    # Skip products user already interacted with
    if product.id in already_interacted:
        return 0.0
    
    score = 0.0
    
    # Category match (highest weight)
    if product.category in user_profile["interested_categories"]:
        score += 10.0
    
    # Tag matches
    if product.tags:
        product_tags = [tag.strip() for tag in product.tags.split(",")]
        matching_tags = set(product_tags) & set(user_profile["interested_tags"])
        score += len(matching_tags) * 3.0
    
    return score


def get_recommendations(db: Session, user_id: int, top_n: int = 5) -> Tuple[List[Product], Dict]:
    """
    Generate product recommendations for a user
    Returns: (recommended_products, user_profile)
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return [], {}
    
    # Build user profile
    user_profile = get_user_profile(db, user_id)
    
    # If user has no interactions, return popular products
    if user_profile["interaction_count"] == 0:
        popular_products = db.query(Product).limit(top_n).all()
        return popular_products, user_profile
    
    # Get all products user already interacted with
    already_interacted = [p.id for p in user_profile["viewed_products"]] + \
                         [p.id for p in user_profile["purchased_products"]]
    
    # Get all products
    all_products = db.query(Product).all()
    
    # Calculate scores for each product
    product_scores = []
    for product in all_products:
        score = calculate_product_score(product, user_profile, already_interacted)
        if score > 0:
            product_scores.append((product, score))
    
    # Sort by score (descending) and get top N
    product_scores.sort(key=lambda x: x[1], reverse=True)
    recommended_products = [prod for prod, score in product_scores[:top_n]]
    
    return recommended_products, user_profile


def format_user_behavior(user_profile: Dict) -> str:
    """Format user behavior into a readable string for LLM context"""
    behavior_parts = []
    
    if user_profile.get("purchased_products"):
        purchased_names = [p.name for p in user_profile["purchased_products"]]
        behavior_parts.append(f"Recently purchased: {', '.join(purchased_names)}")
    
    if user_profile.get("viewed_products"):
        viewed_names = [p.name for p in user_profile["viewed_products"][:3]]
        behavior_parts.append(f"Recently viewed: {', '.join(viewed_names)}")
    
    if user_profile.get("interested_categories"):
        behavior_parts.append(f"Interested in categories: {', '.join(user_profile['interested_categories'])}")
    
    return ". ".join(behavior_parts) if behavior_parts else "No previous activity"
