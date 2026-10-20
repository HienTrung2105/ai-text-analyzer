from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class AnalysisResult(BaseModel):
    summary: str
    sentiment: str
    keywords: list[str]


class AnalysisResponse(AnalysisResult):
    id: int
    input_text: str
    model: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

