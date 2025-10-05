# 🏗️ System Architecture

## Overview

The Smart Train Traffic Controller follows a microservices architecture with containerized components communicating over a Docker network.

## Architecture Diagram

┌──────────────────────────────────────────────────────────┐
│ Docker Network │
│ │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Frontend │ │ Backend │ │
│ │ (Streamlit) │─────HTTP────▶│ (FastAPI) │ │
│ │ Port: 8501 │ │ Port: 8000 │ │
│ └─────────────────┘ └─────────────────┘ │
│ │ │ │
│ │ │ │
│ ▼ ▼ │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │ User Interface │ │ ML Models │ │
│ │ - Dashboard │ │ - Predictor │ │
│ │ - Forms │ │ - Rerouting │ │
│ └─────────────────┘ └─────────────────┘ │
│ │
└──────────────────────────────────────────────────────────┘


## Component Details

### 1. Frontend Service (Streamlit)

**Technology**: Streamlit 1.28.1

**Responsibilities**:
- Render user interface
- Handle user interactions
- Make HTTP requests to backend
- Display real-time data
- Manage dispatcher controls

**Endpoints Used**:
- GET /health - Check backend status
- GET /trains - Fetch train list
- POST /predict_delay - Request delay prediction
- POST /reroute - Request rerouting plan

### 2. Backend Service (FastAPI)

**Technology**: FastAPI 0.104.1 + Uvicorn

**Responsibilities**:
- Handle API requests
- Execute business logic
- Interface with ML models
- Data validation and processing
- Logging and monitoring

**API Routes**:
- `/` - Root endpoint
- `/health` - Health check
- `/trains` - Get all trains
- `/predict_delay` - Delay prediction
- `/reroute` - Rerouting suggestions

### 3. ML Models Layer

**Components**:

**a) Delay Predictor**
- Model: Random Forest Classifier (sklearn)
- Input: Time, weather, station, day
- Output: Delay probability, minutes, risk level
- Fallback: Rule-based system

**b) Rerouting Engine**
- Algorithm: Breadth-First Search (BFS)
- Input: Source, destination, blocked routes
- Output: Alternative paths, trains
- Network: Graph-based railway network

### 4. Data Layer

**Storage**:
- CSV files for train schedules
- In-memory data structures
- Sample dataset included

**Format**:
train_id,train_name,source,destination,scheduled_departure,scheduled_arrival,platform,status
TR0001,Express 1,Mumbai,Pune,07:00,10:00,1,On Time


## Communication Flow

### Delay Prediction Flow


User Input (Frontend)
↓
HTTP POST /predict_delay
↓
FastAPI Route Handler
↓
Service Layer Processing
↓
ML Model Inference
↓
Response JSON
↓
Frontend Display


### Rerouting Flow

Delay Event (Frontend)
↓
HTTP POST /reroute
↓
FastAPI Route Handler
↓
Rerouting Engine
↓
Graph Traversal (BFS)
↓
Alternative Trains Lookup
↓
Response JSON
↓
Frontend Dashboard Update
↓
Dispatcher Decision



## Docker Configuration

### Network

- Type: Bridge network
- Name: `train_network`
- Isolation: Container-level
- DNS: Automatic service discovery

### Volumes

- Backend: `./backend/app:/app/app`
- Frontend: `./frontend:/app`
- Purpose: Hot-reload during development

### Health Checks

**Backend**:
- Endpoint: http://localhost:8000/health
- Interval: 30s
- Retries: 3

## Scalability Considerations

### Horizontal Scaling
- Add multiple backend replicas
- Load balancer (nginx) for distribution
- Redis for session management

### Vertical Scaling
- Increase container CPU/memory limits
- Optimize ML model size
- Database for persistent storage

### Future Architecture

┌─────────────┐
│Load Balancer│
└──────┬──────┘
│
┌───┴───┬───────┬───────┐
▼ ▼ ▼ ▼
Backend1 Backend2 Backend3 ...
│ │ │ │
└───────┴───┬───┴───────┘
│
┌────▼────┐
│ Redis │
│ Cache │
└─────────┘


## Security

- No authentication (hackathon demo)
- CORS enabled for development
- Input validation via Pydantic
- Future: JWT tokens, API keys

## Performance

- FastAPI async capabilities
- Lightweight models (CPU-friendly)
- Docker resource limits
- Response time: <200ms avg

## Monitoring

- Logging: Python logging module
- Metrics: Request/response logs
- Health checks: Docker healthcheck
- Future: Prometheus + Grafana

## Data Flow

CSV Upload → Pandas DataFrame → Validation → Processing → Storage
↓
User Request → API → Service → Model → Prediction → Response


## Deployment

### Development

docker-compose up --build


### Production (Future)
- Kubernetes deployment
- CI/CD pipeline
- Multi-region support
- Database replication

---

**Architecture designed for hackathon demo, production-ready with minimal modifications**

