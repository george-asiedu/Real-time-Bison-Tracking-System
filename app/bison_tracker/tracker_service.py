import cv2
import asyncio
from datetime import datetime, timezone
from app.core.config import get_settings
from app.core.logger import logger
from app.core.constants import messages
from app.database.bison_model import BisonFrame, BoundingBox, BisonDetection
from app.yolo_utils import load_model_file

settings = get_settings()


class BisonTrackerService:
    def __init__(self):
        self.is_running = False
        self.model = load_model_file()


    async def start(self):
        if self.is_running:
            logger.warning(messages["server_running"])
            return
        if not self.model:
            logger.error(messages['model_not_loaded'])
            return

        self.is_running = True
        logger.info(messages["start_server"])
        await self._process_stream()


    def stop(self):
        if not self.is_running:
            logger.warning("Stop command received, but tracker is not running.")
            return
        logger.info(messages["stop_server"])
        self.is_running = False


    async def _process_stream(self):
        cap = cv2.VideoCapture(settings.RTSP_URL)
        if not cap.isOpened():
            logger.error(f"{messages["rtsp_error"]} {settings.RTSP_URL}")
            self.is_running = False
            return None

        logger.info(messages["stream_success"])

        while self.is_running:
            try:
                ret, frame = cap.read()
                if not ret:
                    logger.error(messages["stream_ended"])
                    cap.release()
                    await asyncio.sleep(5)
                    cap = cv2.VideoCapture(settings.RTSP_URL)
                    if not cap.isOpened():
                        logger.error("Failed to reconnect to the stream. Stopping service.")
                        self.is_running = False
                    continue

                results = self.model.track(
                    source=frame,
                    tracker=settings.TRACKER_CFG_PATH,
                    conf=0.3,
                    persist=True,
                    verbose=True
                )[0]

                bison_detections = []
                if results.boxes is not None:
                    boxes = results.boxes
                    track_ids = boxes.id.tolist() if boxes.id is not None else [None] * len(boxes)

                    for box, track_id in zip(boxes, track_ids):
                        coords = box.xyxy[0].tolist()
                        detection = BisonDetection(
                            track_id=int(track_id) if track_id is not None else None,
                            confidence=box.conf[0].item(),
                            box=BoundingBox(
                                x1=coords[0],
                                y1=coords[1],
                                x2=coords[2],
                                y2=coords[3]
                            ),
                        )
                        bison_detections.append(detection)

                analysis_docs = BisonFrame(
                    bison_count=len(bison_detections),
                    detections=bison_detections,
                    timestamp=datetime.now(timezone.utc),
                )
                await analysis_docs.insert()

                logger.info(f"{messages["docs_success"]} {analysis_docs.bison_count} detections")

            except Exception as e:
                logger.error(f"{messages['docs_failed']} {e}")
            await asyncio.sleep(0.01)

        cap.release()
        logger.info("RTSP stream capture released.")
        return None


bison_service = BisonTrackerService()