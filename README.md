# 🚂 Smart Train Traffic Controller

**Railway Automation System for Delay Prediction & Intelligent Rerouting**

## 🎯 Problem Statement

Railway networks face significant challenges with train delays, causing disruptions that affect millions of passengers daily. Traditional traffic control systems lack predictive capabilities and real-time optimization, leading to cascading delays and inefficient resource utilization.

## 💡 Solution

Smart Train Traffic Controller is an AI-powered microservices-based system that:

- **Predicts train delays** using machine learning models trained on historical data and real-time conditions
- **Suggests optimal rerouting** strategies to minimize disruption
- **Provides a live dispatcher dashboard** for real-time decision making
- **Automates traffic control** with intelligent algorithms

## 🏗️ Architecture

┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│ Streamlit │────────▶│ FastAPI │────────▶│ ML Models │
│ Frontend │ │ Backend │ │ (sklearn) │
│ (Port 8501)│◀────────│ (Port 8000) │◀────────│ │
└─────────────┘ └──────────────┘ └─────────────┘
│ │
└────────Docker Network──┘


## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- 4GB RAM minimum
- Port 8000 and 8501 available

### Installation

1. **Clone the repository**
git clone https://github.com/yourusername/smart-train-traffic-controller.git
cd smart-train-traffic-controller


2. **Build and run with Docker Compose**
docker-compose up --build


3. **Access the application**
- Frontend Dashboard: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Stopping the Application

docker-compose down


## 📊 Features

### 1. Live Dashboard
- Real-time train status monitoring
- Visual indicators for delayed/on-time trains
- Filter and search capabilities
- Platform and schedule information

### 2. Delay Predictor
- Input: Train ID, station, weather, time
- Output: Delay probability, predicted delay minutes, risk level
- Contributing factors analysis

### 3. Rerouting Engine
- Intelligent route optimization
- Alternative train suggestions
- Recovery time estimation
- Dispatcher approval workflow

### 4. Schedule Management
- CSV upload for train schedules
- Bulk data processing
- Schedule analysis tools

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python)
- **ML**: Scikit-learn, Pandas, NumPy
- **Deployment**: Docker, Docker Compose
- **Data**: CSV (Indian Railways dataset compatible)

## 📁 Project Structure


smart-train-traffic-controller/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── routes.py # API endpoints
│ │ ├── models.py # ML models
│ │ ├── services.py # Business logic
│ │ ├── utils.py # Helper functions
│ │ └── sample_data.csv # Demo dataset
│ ├── requirements.txt
│ └── Dockerfile
├── frontend/
│ ├── app.py # Streamlit dashboard
│ ├── requirements.txt
│ └── Dockerfile
├── docker-compose.yml
├── README.md
├── ARCHITECTURE.md
└── DEMO_FLOW.md


## 🧪 API Endpoints

### POST /predict_delay
Predict train delay probability

**Request:**
{
"train_id": "TR0001",
"current_time": "14:30",
"station": "Mumbai",
"weather_condition": "rain",
"day_of_week": 1
}


**Response:**
{
"train_id": "TR0001",
"delay_probability": 0.65,
"predicted_delay_minutes": 35,
"risk_level": "MEDIUM",
"factors": ["Peak hours", "Adverse weather"]
}


### POST /reroute
Generate optimal rerouting plan

**Request:**

{
"delayed_train_id": "TR0041",
"current_station": "Mumbai",
"destination_station": "Pune",
"delay_minutes": 45
}


**Response:**
{
"delayed_train_id": "TR0041",
"recommended_action": "REROUTE - Take alternative path",
"alternative_trains": [...],
"reroute_path": ["Mumbai", "Panvel", "Pune"],
"estimated_recovery_time": 15,
"confidence_score": 0.85
}


## 🎬 Demo Flow

See [DEMO_FLOW.md](DEMO_FLOW.md) for step-by-step demo instructions.

## 📈 Future Enhancements

- Integration with real-time GPS tracking
- Advanced ML models (LSTM, transformers)
- Multi-language support
- Mobile app for passengers
- Integration with IRCTC API
- Weather API integration
- Push notifications

## 🤝 Contributing

Contributions welcome! Please submit pull requests.

## 📄 License

MIT License - free for hackathons and personal use

---

**Built with ❤️ using FastAPI, Streamlit & Docker**
