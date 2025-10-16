"""
LLM integration for generating natural language explanations
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from database import Product, User

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_recommendation_explanation(
    user: User,
    recommended_products: List[Product],
    user_behavior: str
) -> str:
    """
    Use LLM to generate a natural explanation for why products are recommended
    """
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        # Fallback explanation if no API key
        return generate_fallback_explanation(user, recommended_products, user_behavior)
    
    try:
        # Format product list for the prompt
        product_list = "\n".join([
            f"- {p.name} (Category: {p.category}, Price: ${p.price})"
            for p in recommended_products[:3]  # Limit to top 3 for concise explanation
        ])
        
        # Create the prompt
        prompt = f"""You are a helpful e-commerce shopping assistant. 
        
User: {user.name}
User's Recent Behavior: {user_behavior}

Recommended Products:
{product_list}

Generate a friendly, personalized explanation (2-3 sentences) of why these products are recommended to {user.name} based on their browsing and purchase history. Make it sound natural and conversational."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful e-commerce recommendation assistant that explains product suggestions in a friendly, natural way."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        explanation = response.choices[0].message.content.strip()
        return explanation
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return generate_fallback_explanation(user, recommended_products, user_behavior)


def generate_fallback_explanation(
    user: User,
    recommended_products: List[Product],
    user_behavior: str
) -> str:
    """
    Generate a simple rule-based explanation if LLM is not available
    """
    if not recommended_products:
        return f"Hello {user.name}! We don't have enough information about your preferences yet. Check out our popular products!"
    
    product_names = ", ".join([p.name for p in recommended_products[:3]])
    categories = list(set([p.category for p in recommended_products]))
    
    explanation = f"Hi {user.name}! Based on your recent activity, we think you'd love these products: {product_names}. "
    
    if user_behavior and user_behavior != "No previous activity":
        explanation += f"These recommendations match your interest in {categories[0] if categories else 'similar'} products. "
    else:
        explanation += "These are some of our most popular items that we think you'll enjoy. "
    
    explanation += "Happy shopping!"
    
    return explanation


async def generate_recommendation_explanation_async(
    user: User,
    recommended_products: List[Product],
    user_behavior: str
) -> str:
    """
    Async version of the explanation generator (for better FastAPI performance)
    """
    # For now, just call the sync version
    # In production, you'd use an async OpenAI client
    return generate_recommendation_explanation(user, recommended_products, user_behavior)
