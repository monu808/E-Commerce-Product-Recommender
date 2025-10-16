# 🤖 AI Prompt Tuning Guide

Master the art of crafting perfect prompts for your recommendation explanations.

---

## 📋 Table of Contents

1. Understanding LLM Integration
2. Basic Prompt Engineering
3. Advanced Prompt Techniques
4. Temperature & Token Settings
5. Multi-Model Support
6. Cost Optimization
7. Testing & Validation

---

## 1. 🧠 Understanding Current LLM Integration

### **Current Implementation** (`backend/llm.py`)

```python
def generate_recommendation_explanation(user, recommended_products, user_behavior):
    prompt = f"""You are a helpful e-commerce shopping assistant. 
    
User: {user.name}
User's Recent Behavior: {user_behavior}

Recommended Products:
{product_list}

Generate a friendly, personalized explanation (2-3 sentences) of why these 
products are recommended to {user.name} based on their browsing and purchase history."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful e-commerce recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
```

---

## 2. ✍️ Basic Prompt Engineering

### **A. Personality & Tone Variations**

#### **Professional & Concise**

```python
system_prompt = """You are a professional e-commerce analyst providing data-driven 
product recommendations. Be concise, factual, and focus on matching criteria."""

user_prompt = f"""Analyze why these products match user {user.name}'s profile:

User Activity:
{user_behavior}

Recommended Products:
{product_list}

Provide a brief, professional explanation of the matching logic."""
```

---

#### **Friendly & Enthusiastic**

```python
system_prompt = """You are an enthusiastic shopping assistant who loves helping 
customers find perfect products! Use emojis, be upbeat, and make shopping fun! 🎉"""

user_prompt = f"""Hey! Our customer {user.name} needs awesome recommendations! 

What they've been into:
{user_behavior}

Perfect matches we found:
{product_list}

Create an exciting, personalized message (2-3 sentences) explaining why 
these are PERFECT for them! Make it fun! 🛍️✨"""
```

---

#### **Luxury & Sophisticated**

```python
system_prompt = """You are a personal shopping consultant for a premium e-commerce 
platform. Use elegant language and emphasize quality and curation."""

user_prompt = f"""Dear {user.name},

Based on your curated selection history:
{user_behavior}

We have carefully selected:
{product_list}

Compose a sophisticated explanation of why these premium selections 
complement their refined taste."""
```

---

### **B. Structured Output Formats**

#### **Bullet Points**

```python
prompt = f"""Create a brief explanation using this format:

🎯 Perfect for {user.name} because:
• [Reason 1 based on their activity]
• [Reason 2 based on their preferences]
• [Reason 3 based on product synergy]

User Activity: {user_behavior}
Recommendations: {product_list}"""
```

---

#### **Story Format**

```python
prompt = f"""Tell a mini-story about {user.name}'s shopping journey:

"Recently, {user.name} has been exploring [category]. They showed particular 
interest in [specific products]. Based on this journey, we believe [recommended 
products] would be the perfect next step because [reasons]."

Fill in the story using:
- User Activity: {user_behavior}
- Recommendations: {product_list}

Keep it warm and personal (2-3 sentences)."""
```

---

## 3. 🎯 Advanced Prompt Techniques

### **A. Chain-of-Thought Prompting**

Better reasoning for complex recommendations:

```python
prompt = f"""Analyze step-by-step why these products are recommended:

Step 1: Examine user behavior
{user_behavior}

Step 2: Identify user preferences
- What categories do they prefer?
- What price range do they shop in?
- What product features matter to them?

Step 3: Match products to preferences
{product_list}

Step 4: Create final explanation
Based on steps 1-3, write a friendly 2-3 sentence explanation for {user.name} 
that connects their behavior to these specific recommendations.

Final Explanation:"""
```

---

### **B. Few-Shot Learning**

Provide examples of good explanations:

```python
prompt = f"""Generate a personalized product recommendation explanation.

Example 1:
User: Alice, recently purchased wireless headphones and viewed speakers
Recommendation: Bluetooth Speaker Pro
Explanation: "Hi Alice! 🎧 Since you recently purchased wireless headphones 
and have been exploring audio equipment, we think you'll love the Bluetooth 
Speaker Pro. It perfectly complements your growing audio setup with premium 
sound quality and wireless convenience you already enjoy!"

Example 2:
User: Bob, viewed mechanical keyboards and bought a gaming mouse
Recommendation: RGB Gaming Keyboard
Explanation: "Hey Bob! Based on your recent purchase of a gaming mouse and 
interest in mechanical keyboards, we're confident the RGB Gaming Keyboard 
is your perfect match. It'll complete your gaming setup with the same 
high-performance features you value!"

Now generate for:
User: {user.name}
Behavior: {user_behavior}
Recommendations: {product_list}

Explanation:"""
```

---

### **C. Role-Based Prompting**

```python
prompt = f"""You are playing the role of a data scientist explaining ML 
recommendations to a non-technical customer.

Task: Explain in simple, friendly terms why your recommendation algorithm 
selected these products for {user.name}.

Available Data:
- User's browsing/purchase history: {user_behavior}
- Algorithm's top picks: {product_list}
- Matching factors: [Extract from context]

Your explanation (avoid technical jargon, use analogies, 2-3 sentences):"""
```

---

### **D. Conditional Logic in Prompts**

```python
def create_dynamic_prompt(user, products, user_profile):
    # Determine user's engagement level
    interaction_count = user_profile.get("interaction_count", 0)
    
    if interaction_count == 0:
        # New user
        context = "This is a new customer with no purchase history yet."
        tone = "welcoming and explanatory"
    elif interaction_count < 5:
        # Light user
        context = f"{user.name} is exploring our store with {interaction_count} interactions."
        tone = "encouraging and helpful"
    else:
        # Regular user
        context = f"{user.name} is a valued customer with {interaction_count} interactions."
        tone = "personalized and appreciative"
    
    # Check if they have purchases
    has_purchases = len(user_profile.get("purchased_products", [])) > 0
    purchase_context = "previous purchases" if has_purchases else "browsing interests"
    
    prompt = f"""Context: {context}
    
Generate a {tone} recommendation explanation for {user.name}.

Based on their {purchase_context}:
{format_user_behavior(user_profile)}

We're recommending:
{format_product_list(products)}

Create a personalized message (2-3 sentences) that acknowledges their 
shopping journey and explains these specific recommendations."""
    
    return prompt
```

---

## 4. ⚙️ Temperature & Token Settings

### **Understanding Parameters**

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,      # Creativity level (0.0 - 2.0)
    max_tokens=150,       # Response length limit
    top_p=1.0,           # Nucleus sampling
    frequency_penalty=0,  # Reduce repetition (0.0 - 2.0)
    presence_penalty=0    # Encourage new topics (0.0 - 2.0)
)
```

---

### **A. Temperature Settings**

#### **Low Temperature (0.0 - 0.3): Consistent & Factual**

```python
# Use for: Formal explanations, consistent tone
temperature=0.2

# Output style: Predictable, professional
# "Based on your purchase of wireless headphones, we recommend..."
# "Based on your purchase of wireless headphones, we recommend..."
# (Nearly identical each time)
```

---

#### **Medium Temperature (0.5 - 0.9): Balanced**

```python
# Use for: Natural, varied explanations (RECOMMENDED)
temperature=0.7

# Output style: Natural variation, personable
# "Since you love wireless headphones, these speakers are perfect!"
# "Your recent headphone purchase inspired these speaker recommendations!"
# (Different but coherent)
```

---

#### **High Temperature (1.0 - 2.0): Creative**

```python
# Use for: Very creative, unpredictable responses
temperature=1.5

# Output style: Highly varied, sometimes unexpected
# "Headphone harmony meets speaker symphony! 🎵"
# "Your audio journey continues with these sonic gems!"
# (Creative but potentially off-brand)
```

---

### **B. Token Optimization**

```python
# Short & sweet (50-80 tokens)
max_tokens=80
# "Perfect for you! These products match your recent purchases and interests."

# Standard (100-150 tokens) - RECOMMENDED
max_tokens=150
# "Hi Alice! Based on your recent purchase of wireless headphones and your 
# interest in audio products, we think you'll love these recommendations..."

# Detailed (200-300 tokens)
max_tokens=250
# Full paragraph with multiple reasons, specific features, and personalization
```

---

## 5. 🔄 Multi-Model Support

### **Implementation**

Update `backend/llm.py`:

```python
import os
from openai import OpenAI

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Add support for other providers
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def generate_explanation_multi_model(
    user,
    recommended_products,
    user_behavior,
    model_provider="openai",  # "openai", "anthropic", "google"
    model_name=None
):
    """
    Generate explanations using different LLM providers
    """
    prompt = create_prompt(user, recommended_products, user_behavior)
    
    if model_provider == "openai":
        return generate_openai(prompt, model_name or "gpt-3.5-turbo")
    
    elif model_provider == "anthropic":
        return generate_anthropic(prompt, model_name or "claude-3-sonnet")
    
    elif model_provider == "google":
        return generate_google(prompt, model_name or "gemini-pro")
    
    else:
        return generate_fallback(user, recommended_products, user_behavior)


def generate_openai(prompt, model="gpt-3.5-turbo"):
    """OpenAI GPT models"""
    response = openai_client.chat.completions.create(
        model=model,  # gpt-3.5-turbo, gpt-4, gpt-4-turbo
        messages=[
            {"role": "system", "content": "You are a helpful shopping assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_anthropic(prompt, model="claude-3-sonnet-20240229"):
    """Anthropic Claude models"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        response = client.messages.create(
            model=model,  # claude-3-opus, claude-3-sonnet, claude-3-haiku
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Anthropic error: {e}")
        return generate_fallback_explanation()


def generate_google(prompt, model="gemini-pro"):
    """Google Gemini models"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Google error: {e}")
        return generate_fallback_explanation()
```

---

### **Model Comparison**

| Model | Cost | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **gpt-3.5-turbo** | $ | ⚡⚡⚡ | ⭐⭐⭐ | Production, high volume |
| **gpt-4-turbo** | $$$ | ⚡⚡ | ⭐⭐⭐⭐⭐ | Premium explanations |
| **claude-3-haiku** | $ | ⚡⚡⚡ | ⭐⭐⭐⭐ | Fast, quality responses |
| **claude-3-sonnet** | $$ | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality/cost ratio |
| **gemini-pro** | $ | ⚡⚡⚡ | ⭐⭐⭐⭐ | Google ecosystem |

---

## 6. 💰 Cost Optimization

### **A. Smart Caching**

```python
import hashlib
import json
from functools import lru_cache

# In-memory cache
_explanation_cache = {}

def get_cached_explanation(user_id, product_ids, user_behavior):
    """
    Cache explanations to avoid regenerating identical requests
    """
    # Create cache key from inputs
    cache_data = {
        "user_id": user_id,
        "product_ids": sorted(product_ids),
        "behavior": user_behavior
    }
    cache_key = hashlib.md5(
        json.dumps(cache_data, sort_keys=True).encode()
    ).hexdigest()
    
    # Check cache
    if cache_key in _explanation_cache:
        return _explanation_cache[cache_key]
    
    # Generate new explanation
    explanation = generate_recommendation_explanation(...)
    
    # Store in cache (limit cache size)
    if len(_explanation_cache) > 1000:
        # Remove oldest entries
        _explanation_cache.pop(next(iter(_explanation_cache)))
    
    _explanation_cache[cache_key] = explanation
    return explanation
```

---

### **B. Batch Processing**

```python
def generate_explanations_batch(user_product_pairs):
    """
    Generate multiple explanations in one API call
    """
    batch_prompt = "Generate brief recommendation explanations for multiple users:\n\n"
    
    for i, (user, products, behavior) in enumerate(user_product_pairs):
        batch_prompt += f"""
User {i+1}: {user.name}
Behavior: {behavior}
Products: {[p.name for p in products]}

"""
    
    batch_prompt += "\nProvide one explanation per user (2 sentences each)."
    
    # Single API call for all users
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": batch_prompt}],
        max_tokens=500
    )
    
    # Parse individual explanations
    explanations = parse_batch_response(response.choices[0].message.content)
    return explanations
```

---

### **C. Fallback Tiers**

```python
def generate_with_fallback_tiers(user, products, behavior):
    """
    Try cheaper/faster models first, fall back to better models if needed
    """
    # Tier 1: Template-based (free, instant)
    if len(products) <= 2:
        return generate_template_explanation(user, products, behavior)
    
    # Tier 2: GPT-3.5-turbo (cheap, fast)
    try:
        return generate_openai(prompt, "gpt-3.5-turbo")
    except Exception as e:
        print(f"GPT-3.5 failed: {e}")
    
    # Tier 3: Claude Haiku (moderate cost)
    try:
        return generate_anthropic(prompt, "claude-3-haiku")
    except Exception as e:
        print(f"Claude Haiku failed: {e}")
    
    # Tier 4: Rule-based fallback (free)
    return generate_fallback_explanation(user, products, behavior)
```

---

## 7. 🧪 Testing & Validation

### **A. Prompt Testing Framework**

Create `backend/test_prompts.py`:

```python
"""
Test different prompts and compare outputs
"""
import asyncio
from llm import generate_recommendation_explanation
from database import SessionLocal, User, Product

# Test cases
test_cases = [
    {
        "user_name": "Alice",
        "behavior": "Recently purchased: Wireless Headphones. Viewed: Speakers, Earbuds",
        "products": ["Bluetooth Speaker", "Wireless Earbuds"],
        "expected_keywords": ["audio", "wireless", "headphones", "complement"]
    },
    {
        "user_name": "Bob",
        "behavior": "Recently viewed: Mechanical Keyboard, Gaming Mouse",
        "products": ["RGB Gaming Keyboard", "Mouse Pad"],
        "expected_keywords": ["gaming", "setup", "complement", "keyboard"]
    }
]

def test_prompt_variations():
    """
    Test multiple prompt variations
    """
    results = []
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test['user_name']}")
        print(f"{'='*60}")
        
        # Test different temperatures
        for temp in [0.3, 0.7, 1.0]:
            explanation = generate_explanation_with_temp(
                test["user_name"],
                test["products"],
                test["behavior"],
                temperature=temp
            )
            
            print(f"\nTemperature {temp}:")
            print(explanation)
            
            # Check for expected keywords
            keywords_found = [
                kw for kw in test["expected_keywords"]
                if kw.lower() in explanation.lower()
            ]
            
            results.append({
                "test": test["user_name"],
                "temperature": temp,
                "explanation": explanation,
                "keywords_matched": len(keywords_found),
                "total_keywords": len(test["expected_keywords"])
            })
    
    return results

if __name__ == "__main__":
    results = test_prompt_variations()
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for r in results:
        match_rate = r["keywords_matched"] / r["total_keywords"] * 100
        print(f"{r['test']} (T={r['temperature']}): {match_rate:.0f}% keyword match")
```

Run with:
```bash
python backend/test_prompts.py
```

---

### **B. Quality Metrics**

```python
def evaluate_explanation_quality(explanation, expected_criteria):
    """
    Score explanation quality on multiple dimensions
    """
    scores = {}
    
    # Length check (too short or too long)
    word_count = len(explanation.split())
    scores["length"] = 1.0 if 20 <= word_count <= 60 else 0.5
    
    # Personalization (mentions user name)
    scores["personalization"] = 1.0 if "alice" in explanation.lower() else 0.0
    
    # Specificity (mentions actual product names)
    product_mentions = sum(
        1 for p in expected_criteria["products"]
        if p.lower() in explanation.lower()
    )
    scores["specificity"] = product_mentions / len(expected_criteria["products"])
    
    # Tone (friendly indicators)
    friendly_words = ["perfect", "love", "great", "ideal", "enjoy"]
    scores["friendliness"] = min(
        sum(1 for w in friendly_words if w in explanation.lower()) / 2,
        1.0
    )
    
    # Overall score
    overall = sum(scores.values()) / len(scores)
    
    return {
        "overall_score": overall,
        "dimensions": scores
    }
```

---

## 8. 📊 Monitoring & Analytics

### **Track LLM Performance**

```python
import time
import logging

class LLMMetrics:
    def __init__(self):
        self.calls = []
    
    def log_call(self, model, prompt_tokens, completion_tokens, latency, cost):
        self.calls.append({
            "timestamp": time.time(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "latency_ms": latency * 1000,
            "cost_usd": cost
        })
    
    def get_summary(self):
        if not self.calls:
            return None
        
        return {
            "total_calls": len(self.calls),
            "total_tokens": sum(c["total_tokens"] for c in self.calls),
            "total_cost": sum(c["cost_usd"] for c in self.calls),
            "avg_latency_ms": sum(c["latency_ms"] for c in self.calls) / len(self.calls),
            "models_used": list(set(c["model"] for c in self.calls))
        }

# Global metrics tracker
llm_metrics = LLMMetrics()

# Use in generation function
def generate_with_metrics(prompt, model="gpt-3.5-turbo"):
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    latency = time.time() - start_time
    
    # Calculate cost (example rates)
    cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens for GPT-3.5
    cost = (response.usage.total_tokens / 1000) * cost_per_1k_tokens
    
    llm_metrics.log_call(
        model=model,
        prompt_tokens=response.usage.prompt_tokens,
        completion_tokens=response.usage.completion_tokens,
        latency=latency,
        cost=cost
    )
    
    return response.choices[0].message.content
```

---

## 📚 Quick Reference

### **Best Practices Checklist**

- ✅ Use temperature 0.7 for natural variation
- ✅ Limit max_tokens to 150 for concise explanations
- ✅ Include user name for personalization
- ✅ Mention specific products by name
- ✅ Test multiple prompt variations
- ✅ Implement caching for identical requests
- ✅ Use fallback for API failures
- ✅ Monitor costs and token usage
- ✅ A/B test different prompts
- ✅ Validate output quality regularly

---

**🎉 You're now an LLM prompt engineering expert!**

Next: See `DEPLOYMENT_GUIDE.md` for production deployment.
