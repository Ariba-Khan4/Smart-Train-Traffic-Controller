from app.models import get_delay_predictor, get_rerouting_engine
from datetime import datetime, timedelta
import random

def predict_train_delay(train_id: str, current_time: str, station: str, 
                       weather: str = "clear", day_of_week: int = 1):
    """
    Predict delay probability for a train
    """
    predictor = get_delay_predictor()
    
    # Parse time
    try:
        time_obj = datetime.strptime(current_time, "%H:%M")
        hour = time_obj.hour
    except:
        hour = 12
    
    # Encode weather
    weather_map = {"clear": 0, "cloudy": 1, "rain": 2, "storm": 3, "fog": 2}
    weather_encoded = weather_map.get(weather.lower(), 0)
    
    # Encode station (simplified hash)
    station_encoded = hash(station) % 10
    
    # Create feature vector
    features = [hour, day_of_week, weather_encoded, station_encoded]
    
    # Get prediction
    delay_prob = predictor.predict_delay_probability(features)
    
    # Calculate predicted delay minutes
    if delay_prob < 0.3:
        delay_minutes = random.randint(0, 10)
        risk_level = "LOW"
    elif delay_prob < 0.6:
        delay_minutes = random.randint(10, 30)
        risk_level = "MEDIUM"
    else:
        delay_minutes = random.randint(30, 90)
        risk_level = "HIGH"
    
    # Identify factors
    factors = []
    if 7 <= hour <= 10 or 17 <= hour <= 20:
        factors.append("Peak hours")
    if weather_encoded >= 2:
        factors.append("Adverse weather")
    if day_of_week >= 5:
        factors.append("Weekend traffic")
    if not factors:
        factors.append("Normal conditions")
    
    return {
        "train_id": train_id,
        "delay_probability": round(delay_prob, 3),
        "predicted_delay_minutes": delay_minutes,
        "risk_level": risk_level,
        "factors": factors
    }

def suggest_reroute(delayed_train_id: str, current_station: str, 
                   destination_station: str, delay_minutes: int, 
                   available_routes: list = []):
    """
    Suggest optimal rerouting strategy
    """
    engine = get_rerouting_engine()
    
    # Find alternative route
    alt_route = engine.find_alternative_route(current_station, destination_station)
    
    # Determine action based on delay severity
    if delay_minutes < 15:
        action = "MONITOR - Continue on current route"
        recovery_time = delay_minutes // 2
    elif delay_minutes < 45:
        action = "REROUTE - Take alternative path"
        recovery_time = delay_minutes // 3
    else:
        action = "HOLD - Wait for track clearance"
        recovery_time = delay_minutes // 4
    
    # Generate alternative trains
    alternative_trains = []
    for i in range(1, 4):
        alt_train_id = f"ALT{random.randint(1000, 9999)}"
        departure_time = datetime.now() + timedelta(minutes=random.randint(15, 60))
        alternative_trains.append({
            "train_id": alt_train_id,
            "departure_time": departure_time.strftime("%H:%M"),
            "available_seats": random.randint(50, 200),
            "route": " → ".join(alt_route[:3]) if len(alt_route) >= 3 else "Direct"
        })
    
    # Calculate confidence score
    confidence = 0.85 if alt_route else 0.60
    if delay_minutes > 60:
        confidence -= 0.15
    
    return {
        "delayed_train_id": delayed_train_id,
        "recommended_action": action,
        "alternative_trains": alternative_trains,
        "reroute_path": alt_route if alt_route else [current_station, destination_station],
        "estimated_recovery_time": recovery_time,
        "confidence_score": round(confidence, 2)
    }
