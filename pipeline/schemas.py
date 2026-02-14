from typing import List
from pydantic import BaseModel, Field, HttpUrl

class FAQItem(BaseModel):
    theme: str = Field(..., min_length=2)
    question: str = Field(..., min_length=5)
    answer: str = Field(..., min_length=5)
    confidence: float = Field(..., ge=0.0, le=1.0)

class FAQResponse(BaseModel):
    url: HttpUrl
    items: List[FAQItem] = Field(default_factory=list)
