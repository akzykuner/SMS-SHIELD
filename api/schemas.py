from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1)
    simulate: Optional[str] = None

class URLInfo(BaseModel):
    url: str
    domain: str
    host_type: Literal["ip", "domain"]

class ClassifyResponse(BaseModel):
    label: Literal["smishing", "ham"]
    probability: float
    verification_status: Literal["ok", "pending"]
    urls: List[URLInfo] = []
    meta: Optional[dict] = None

class FeedbackRequest(BaseModel):
    text: str
    user_label: Literal["smishing", "ham", "unknown"] = "unknown"
    predicted_label: Optional[Literal["smishing", "ham"]] = None
    probability: Optional[float] = None
    user_id: Optional[str] = None
    notes: Optional[str] = None