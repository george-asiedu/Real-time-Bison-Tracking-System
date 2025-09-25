messages = {
    "db_connection": "Database connection initialized...",
    "shutdown": "Application shutting down...",
    "app_title": "Real-time-Bison-Tracking-System API",
    "app_description": "A real time bison tracking system using FastAPI, beanie ODM, and MongoDB",
    "app_version": "1.0.0",
    "welcome": "Welcome to the Real-time-Bison-Tracking-System API",
    "db_connection_error": "DATABASE_URI is not set in environment variables",
    "db_name_error": "DB_NAME is not set in environment variables",
    "server_running": "Tracker service is already running",
    "start_server": "Starting Bison Tracker Service",
    "stop_server": "Stopping Bison Tracking Service",
    "rtsp_error": "Cannot start stream at",
    "stream_success": "Successfully connected to RTSP stream",
    "stream_ended": "Stream ended or failed to read frame. Stopping.",
    "docs_success": "Successfully ingested bison frame with",
    "docs_failed": "An error occurred during frame processing:",
    "model_failed": "Failed to load YOLO model:",
    "model_not_loaded": "Cannot start tracker service: Model is not loaded."
}

state = {
    "tracker_service": None,
    "tracker_task": None
}