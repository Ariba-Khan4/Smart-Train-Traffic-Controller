import pandas as pd
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_request(endpoint: str, data: dict):
    """Log incoming API requests"""
    logger.info(f"Endpoint: {endpoint} | Data: {data}")

def load_sample_data():
    """Load sample train schedule data"""
    data_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    
    # Generate sample data if file doesn't exist
    sample_data = pd.DataFrame({
        "train_id": [f"TR{i:04d}" for i in range(1, 51)],
        "train_name": [f"Express {i}" for i in range(1, 51)],
        "source": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"] * 10,
        "destination": ["Pune", "Jaipur", "Mysore", "Hyderabad", "Patna"] * 10,
        "scheduled_departure": [f"{7+i%12:02d}:{i%60:02d}" for i in range(50)],
        "scheduled_arrival": [f"{10+i%12:02d}:{i%60:02d}" for i in range(50)],
        "platform": [i % 10 + 1 for i in range(50)],
        "status": ["On Time"] * 40 + ["Delayed"] * 10
    })
    
    sample_data.to_csv(data_path, index=False)
    return sample_data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess train data"""
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def get_current_ist_time():
    """Get current IST time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
