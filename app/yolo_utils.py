from ultralytics import YOLO
from pathlib import Path
from app.core.logger import logger
from app.core.config import get_settings

settings = get_settings()

def load_model_file():
    model_path = Path(settings.MODEL_WEIGHTS_PATH).resolve()
    if not model_path.exists():
        logger.info(f"Model file not found at {model_path}")
        return None

    try:
        model = YOLO(str(model_path))
        logger.info(f"Model file load successfully {model_path}")
        return model
    except Exception as e:
        logger.info(f"Model file load failed {e}")
        return None