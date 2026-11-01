from typing import Annotated

import httpx
from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.images import (
    ImageValidationError,
    validate_and_prepare_image,
)
from app.llm import LLMClient
from app.models import ChatResponse
from app.safety import screen_safety

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description=(
        "A prototype agriculture AI assistant with optional photo analysis."
    ),
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

client = LLMClient()

MAX_PHOTOS = 4


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "mode": "live" if settings.api_key else "demo",
        "model": settings.model_name if settings.api_key else None,
        "photos_supported": True,
    }


@app.get("/domains")
async def domains():
    return {
        "domains": [
            "crop_management",
            "livestock",
            "vision",
            "soil_water",
            "pest_disease",
            "market",
            "weather",
            "farm_business",
            "sustainability",
            "general",
        ]
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    message: Annotated[str, Form(min_length=1, max_length=10_000)],
    domain: Annotated[
        str,
        Form(
            pattern=(
                "^(crop_management|livestock|vision|soil_water|"
                "pest_disease|market|weather|farm_business|"
                "sustainability|general)$"
            ),
        ),
    ] = "general",
    crop: Annotated[str | None, Form()] = None,
    growth_stage: Annotated[str | None, Form()] = None,
    location: Annotated[str | None, Form()] = None,
    soil_type: Annotated[str | None, Form()] = None,
    photos: Annotated[
        list[UploadFile] | None,
        File(),
    ] = None,
):
    photos = photos or []

    if len(photos) > MAX_PHOTOS:
        raise HTTPException(
            status_code=400,
            detail=f"A maximum of {MAX_PHOTOS} photos is allowed.",
        )

    findings = screen_safety(message)

    context = {
        "crop": crop,
        "growth_stage": growth_stage,
        "location": location,
        "soil_type": soil_type,
    }

    context = {
        key: value
        for key, value in context.items()
        if value not in (None, "")
    }

    prepared_images = []

    for upload in photos:
        if not upload.filename:
            continue

        content = await upload.read()

        try:
            prepared, media_type, metadata = (
                validate_and_prepare_image(content)
            )
        except ImageValidationError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        metadata["filename"] = upload.filename
        prepared_images.append(
            {
                "content": prepared,
                "media_type": media_type,
                **metadata,
            }
        )

    try:
        answer, mode = await client.generate(
            message=message,
            domain=domain,
            context=context,
            images=prepared_images,
        )
    except httpx.HTTPStatusError as exc:
        detail = "Model provider rejected the request."

        try:
            error_body = exc.response.json()
            detail = error_body.get("error", {}).get(
                "message",
                detail,
            )
        except ValueError:
            pass

        raise HTTPException(
            status_code=502,
            detail=detail,
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Model provider request failed: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The assistant could not generate a response.",
        ) from exc

    return ChatResponse(
        answer=answer,
        domain=domain,
        mode=mode,
        safety_findings=findings,
    )
