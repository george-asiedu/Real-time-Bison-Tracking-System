from .tracker_service import bison_service
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from app.core.constants import state, messages
from app.database.bison_model import BisonFrame
from typing import List
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/tracker", tags=["Tracker"])

@router.post('/start', status_code=202)
async def start_tracker(background_task: BackgroundTasks):
    if state.get('tracker_task') and not state['tracker_task'].done():
        raise HTTPException(status_code=400, detail=messages['server_running'])

    state['tracker_service'] = bison_service
    state['tracker_task'] = background_task.add_task(state['tracker_service'].start)
    return {"message": "Bison tracker service started."}


@router.post('/stop', status_code=200)
async def stop_tracker():
    if not state.get('tracker_service') or not state['tracker_service'].is_running:
        raise HTTPException(status_code=404, detail="Tracker is not running.")

    state['tracker_service'].stop()
    state['tracker_task'] = None

    return {"message": "Bison tracker service stopped."}


@router.get('/status', status_code=200)
async def get_tracker_status():
    is_running = state.get('tracker_service') and state['tracker_service'].is_running
    return {"status": "running" if is_running else "stopped"}


@router.get('/data/latest', status_code=200, response_model=BisonFrame)
async def get_latest_data():
    latest_analysis = await BisonFrame.find_one(sort=[("-timestamp", 1)])
    if not latest_analysis:
        raise HTTPException(status_code=404, detail="No data found.")
    return latest_analysis


@router.get("/data/timeseries", response_model=List[BisonFrame])
async def get_data_timeseries(minutes: int = Query(5, ge=1, le=1440)):
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    analyses = await BisonFrame.find(
        BisonFrame.timestamp >= time_threshold
    ).sort("-timestamp").to_list()

    if not analyses:
        raise HTTPException(status_code=404, detail=f"No data found in the last {minutes} minutes.")
    return analyses