from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from pipeline.fetch import fetch_html
from pipeline.clean import clean_html_to_text
from pipeline.model_faq import extract_faq_with_model

app = FastAPI(title="FAQ Generator (Gemini)")

class GenerateRequest(BaseModel):
    url: HttpUrl

@app.post("/generate-faq")
def generate_faq(req: GenerateRequest):
    url = str(req.url)

    try:
        html = fetch_html(url)
        clean_text = clean_html_to_text(html)

        if len(clean_text) < 200:
            return {"url": url, "items": []}

        result = extract_faq_with_model(clean_text=clean_text, url=url)
        return result.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
