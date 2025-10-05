from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import pickle
import os

class DelayPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.is_trained = False
        
    def train(self, X, y):
        """Train the delay prediction model"""
        self.model.fit(X, y)
        self.is_trained = True
        
    def predict_delay_probability(self, features):
        """Predict delay probability"""
        if not self.is_trained:
            # Use rule-based system if not trained
            return self._rule_based_prediction(features)
        
        prob = self.model.predict_proba([features])[0]
        return prob[1] if len(prob) > 1 else prob[0]
    
    def _rule_based_prediction(self, features):
        """Rule-based delay prediction fallback"""
        # features: [hour, day_of_week, weather_encoded, station_encoded]
        base_prob = 0.15  # 15% base delay probability
        
        # Peak hours (7-10 AM, 5-8 PM)
        hour = features[0] if len(features) > 0 else 12
        if 7 <= hour <= 10 or 17 <= hour <= 20:
            base_prob += 0.25
        
        # Weekend factor
        day = features[1] if len(features) > 1 else 1
        if day >= 5:  # Weekend
            base_prob -= 0.05
        
        # Weather factor
        weather = features[2] if len(features) > 2 else 0
        if weather > 1:  # Bad weather
            base_prob += 0.30
        
        return min(base_prob, 0.95)

class ReroutingEngine:
    def __init__(self):
        self.route_graph = self._build_route_network()
        
    def _build_route_network(self):
        """Build a simple railway network graph"""
        # Simplified Indian railway network
        network = {
            "Mumbai": ["Pune", "Surat", "Vadodara"],
            "Pune": ["Mumbai", "Solapur", "Kolhapur"],
            "Delhi": ["Jaipur", "Agra", "Chandigarh", "Lucknow"],
            "Bangalore": ["Chennai", "Mysore", "Hubli"],
            "Chennai": ["Bangalore", "Hyderabad", "Coimbatore"],
            "Kolkata": ["Patna", "Bhubaneswar", "Guwahati"],
            "Hyderabad": ["Bangalore", "Chennai", "Vijayawada"],
            "Ahmedabad": ["Surat", "Vadodara", "Rajkot"],
            "Jaipur": ["Delhi", "Jodhpur", "Udaipur"],
            "Lucknow": ["Delhi", "Kanpur", "Varanasi"]
        }
        return network
    
    def find_alternative_route(self, start, destination, blocked_stations=[]):
        """Find alternative routes using simple BFS"""
        from collections import deque
        
        if start not in self.route_graph or destination not in self.route_graph:
            return []
        
        queue = deque([(start, [start])])
        visited = set(blocked_stations)
        
        while queue:
            current, path = queue.popleft()
            
            if current == destination:
                return path
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor in self.route_graph.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return []

# Global model instances
delay_predictor = DelayPredictor()
rerouting_engine = ReroutingEngine()

def get_delay_predictor():
    return delay_predictor

def get_rerouting_engine():
    return rerouting_engine
