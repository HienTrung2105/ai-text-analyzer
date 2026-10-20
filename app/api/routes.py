from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis
from app.schemas import AnalyzeRequest, AnalysisResponse
from app.services.ai_service import analyze_with_ai


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)) -> Analysis:
    try:
        result, model = analyze_with_ai(payload.text)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    analysis = Analysis(
        input_text=payload.text,
        summary=result.summary,
        sentiment=result.sentiment,
        keywords=result.keywords,
        model=model,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/analyses", response_model=list[AnalysisResponse])
def list_analyses(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Analysis]:
    statement = select(Analysis).order_by(Analysis.created_at.desc()).limit(limit)
    return list(db.scalars(statement))

