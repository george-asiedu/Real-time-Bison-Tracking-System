# Real-time-Bison-Tracking-System
The **Real-time Bison Tracking System** is a Python-based application that leverages **YOLO object detection**, **RTSP video streaming**, and **FastAPI** to monitor, detect, and track bison in real-time.

It supports:
- AI-powered detection with YOLO models (`best.pt` or any YOLOv8 weight file).  
- RTSP video ingestion and HLS/MJPEG web streaming.  
- REST API endpoints to start/stop the tracker, fetch status, and query detection data.  
- MongoDB integration for persisting detection frames and statistics.

## Project Structure
Real-time-Bison-Tracking-System/
│── app/
│ ├── bison_tracker/ # Tracker logic & routes
│ │ ├── tracker_router.py
│ │ ├── tracker_service.py
│ ├── core/ # config, constants, logger
│ ├── database/ # Beanie document, db connection
│ ├── yolo_utils.py # YOLO model loading utility
│ ├── main.py # FastAPI entry point
│
│── best.pt # YOLO weights (replace with your trained model)
│── args.yaml # Tracker config
│── .env
│── requirements.txt
│── README.md

## 🌐 Deployed Server

* **Base URL**: [https://real-time-bison-tracking-system.onrender.com](https://real-time-bison-tracking-system.onrender.com
* **Swagger Docs**: [https://real-time-bison-tracking-system.onrender.com/docs](https://real-time-bison-tracking-system.onrender.com/docs)

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas) (Cloud)
- **ODM**: [Beanie](https://beanie-odm.dev/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/)
- **Deployment**: [Render](https://render.com)
- **Ultralytics**: [Ultralytics](https://www.ultralytics.com/)

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/george-asiedu/Real-time-Bison-Tracking-System.git
cd Real-time-Bison-Tracking-System
```

### 2. Create & activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

#### Create a .env file in the root directory

```bash
MONGO_URI=your_mongodb_url
DB_NAME=your_db_name
MODEL_WEIGHTS_PATH=yolo_model_path
TRACKER_CFG_PATH=your_args.yaml_file
RTSP_URL=your_bison_url
```

### 5. Run the server

```bash
fastapi dev app/main.py
```

Server will run at: <http://127.0.0.1:8000>

## API Documentation

* **Swagger UI**: /docs

### API Endpoints

| Method | Endpoint              | Description                     |
|:-------|:----------------------|:--------------------------------|
| `POST` | `/api/tracker/start`  | Start the tracker service       |
| `POST` | `/api/tracker/stop`   | Stop the tracker service        |
| `GET`  | `/api/tracker/status` | Get tracker running status      |
| `GET`  | `/api/data/latest` | Get the latest detection frame  |
| `GET`  | `/api/data/timeseries?minutes=5` | Get time-series detection data |

### Stopping the server
Few minutes after starting the service, shutdown the service gracefully by hitting the stop endpoint