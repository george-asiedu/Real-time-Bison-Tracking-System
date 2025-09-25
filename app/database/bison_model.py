from beanie import Document, Indexed
from datetime import datetime, timezone
from pydantic import Field, BaseModel
from typing import Annotated, List

class BindingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class BisonDetection(BaseModel):
    track_id: int | None = None
    confidence: float
    box: BindingBox


class BisonFrame(Document):
    bison_count: int
    directions: List[BisonDetection]
    timestamp: Annotated[datetime, Indexed()] = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "bison_frame"