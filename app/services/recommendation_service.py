"""
AI Car Recommendation Engine.

This provides a lightweight, heuristic-based recommendation system that simulates
an AI assistant finding the best car based on the user's intent.

It scores available cars based on:
- Passenger count
- Budget per day
- Purpose (city, off-road, luxury, family, eco)
- Rental duration
"""

from typing import Dict, List

from app.models.car import Car
from database import db


def recommend_cars(passengers: int, budget: float, purpose: str, days: int) -> List[Dict[str, object]]:
    """
    Score and recommend cars based on user inputs.

    Args:
        passengers: Number of people (affects category needed)
        budget: Max daily budget ($)
        purpose: General use case (e.g., 'city', 'family', 'luxury', 'offroad', 'eco')
        days: Intended rental duration (filters out cars with incompatible min/max days)

    Returns:
        List of dictionaries containing the recommended cars and their match score.
    """
    # Only consider cars currently available
    available_cars = db.session.query(Car).filter_by(available_now=True).all()
    
    recommendations = []
    
    purpose = purpose.lower()
    
    for car in available_cars:
        score = 0
        reasons = []
        
        # 1. Budget check (strict filter, but we allow up to 10% over for a 'good fit')
        if car.daily_rate <= budget:
            score += 30
            reasons.append("Under budget")
        elif car.daily_rate <= (budget * 1.1):
            score += 10
            reasons.append("Slightly over budget but great fit")
        else:
            # Too expensive, skip
            continue
            
        # 2. Duration check (strict filter)
        if days < car.min_rent_period or days > car.max_rent_period:
            continue
            
        # 3. Passenger capacity matching (heuristic based on category)
        # Assuming Sedans/SUVs hold 5, Minivans hold 7-8, Economy holds 4.
        capacity = 4
        if car.category.lower() in ['suv', 'sedan', 'luxury']:
            capacity = 5
        elif car.category.lower() in ['minivan', 'van']:
            capacity = 7
            
        if capacity >= passengers:
            score += 20
            reasons.append(f"Fits {passengers} passengers comfortably")
        else:
            # Too small, skip
            continue
            
        # 4. Purpose matching
        if 'city' in purpose and car.category.lower() in ['economy', 'compact', 'hatchback']:
            score += 40
            reasons.append("Perfect for city parking and agility")
            
        if 'family' in purpose and car.category.lower() in ['suv', 'minivan', 'sedan']:
            score += 40
            reasons.append("Spacious and safe for families")
            
        if 'luxury' in purpose and car.category.lower() in ['luxury', 'premium']:
            score += 40
            reasons.append("Premium features and comfort")
            
        if 'offroad' in purpose or 'mountain' in purpose:
            if car.category.lower() == 'suv':
                score += 40
                reasons.append("High clearance for adventure")
                
        if 'eco' in purpose or 'green' in purpose or 'electric' in purpose:
            if 'hybrid' in car.model.lower() or 'ev' in car.model.lower() or car.category.lower() == 'electric':
                score += 50
                reasons.append("Zero emissions / Eco-friendly")
                
        # Base appeal (newer cars score slightly higher)
        score += (car.year - 2015) * 2
        
        if score > 0:
            recommendations.append({
                'car': car,
                'score': score,
                'reasons': reasons
            })
            
    # Sort by score descending
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top 3
    return recommendations[:3]
