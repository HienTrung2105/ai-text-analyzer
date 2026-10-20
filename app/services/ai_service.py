import json

from openai import OpenAI

from app.config import get_settings
from app.schemas import AnalysisResult


ANALYSIS_INSTRUCTIONS = """
Bạn là hệ thống phân tích văn bản. Hãy trả về duy nhất một JSON object hợp lệ với:
- summary: bản tóm tắt ngắn bằng cùng ngôn ngữ với đầu vào
- sentiment: một trong positive, neutral, negative
- keywords: mảng 3 đến 7 từ khóa quan trọng
Không dùng Markdown và không thêm nội dung ngoài JSON.
""".strip()


def analyze_with_ai(text: str) -> tuple[AnalysisResult, str]:
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY chưa được cấu hình")

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.openai_model,
        instructions=ANALYSIS_INSTRUCTIONS,
        input=text,
        store=False,
    )

    try:
        payload = json.loads(response.output_text)
        result = AnalysisResult.model_validate(payload)
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("AI trả về dữ liệu không đúng định dạng") from exc

    return result, settings.openai_model

