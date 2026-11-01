import base64
import json
import re

import httpx

from app.config import settings
from app.prompt_library import (
    SYSTEM_PROMPT,
    VISION_INSTRUCTIONS,
    build_user_prompt,
)


class LLMClient:
    async def generate(
        self,
        *,
        message: str,
        domain: str,
        context: dict,
        images: list[dict] | None = None,
    ) -> tuple[str, str]:
        images = images or []

        if not settings.api_key:
            return (
                self._demo_response(
                    message,
                    domain,
                    context,
                    bool(images),
                ),
                "demo",
            )

        endpoint = f"{settings.base_url.rstrip('/')}/chat/completions"

        content = [
            {
                "type": "text",
                "text": build_user_prompt(
                    domain,
                    message,
                    context,
                ),
            }
        ]

        for image in images:
            encoded = base64.b64encode(
                image["content"]
            ).decode("ascii")

            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": (
                            "data:"
                            f"{image['media_type']};"
                            f"base64,{encoded}"
                        )
                    },
                }
            )

        payload = {
            "model": settings.model_name,
            "temperature": 0.2,
            "max_tokens": 1800,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        SYSTEM_PROMPT
                        + "\n\n"
                        + VISION_INSTRUCTIONS
                        if images
                        else SYSTEM_PROMPT
                    ),
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
        }

        async with httpx.AsyncClient(
            timeout=settings.request_timeout
        ) as client:
            response = await client.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {settings.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        answer = data["choices"][0]["message"]["content"]
        return answer, "live"

    def _demo_response(
        self,
        message: str,
        domain: str,
        context: dict,
        has_images: bool = False,
    ) -> str:
        crop = context.get("crop") or "the crop"
        location = context.get("location") or "your area"
        growth_stage = (
            context.get("growth_stage")
            or "the current crop stage"
        )

        photo_note = (
            """
A photo was uploaded, but demo mode does not perform computer vision.
Connect a vision-capable model to analyze the image. For now, provide the
crop, plant part, symptom location, severity, and recent weather so the
image can be interpreted by a specialist.
"""
            if has_images
            else ""
        )

        return f"""
### Initial recommendation

Review the field or herd for the requested issue before acting. The supplied
context identifies **{crop}** at **{growth_stage}** in **{location}**.

{photo_note}

### Suggested assessment

1. **Identify the limiting factor**
   - Compare plant or animal condition with a healthy reference.
   - Record the affected area, severity, date, and weather or management
     changes around the symptom.
   - Check whether the pattern follows rows, soil zones, irrigation lines,
     drainage areas, or animal groups.

2. **Use targeted diagnostics**
   - For crop problems, inspect roots, leaves, stems, fruit or seed heads, and
     soil moisture.
   - For pest problems, check both pest numbers and natural enemies.
   - For nutrient problems, use a calibrated soil or tissue test rather than
     visual symptoms alone.
   - For livestock problems, record age, weight, intake, temperature where
     safely available, and changes in behavior or droppings.

3. **Start with lower-risk interventions**
   - Correct irrigation or drainage problems.
   - Remove severely affected material where appropriate.
   - Improve rotation, sanitation, and monitoring frequency.
   - Use biological or mechanical controls before broad chemical treatment
     when locally appropriate.

4. **Verify before escalating**
   - Submit samples to a local diagnostic laboratory when the cause is
     uncertain or economically important.
   - For pesticide, fertilizer, or veterinary treatment, follow the current
     local label or veterinary instruction.

### Assumptions

This demo response does not independently verify the message, field records,
weather, soil measurements, disease identity, product labels, or local
regulations.

### Monitoring plan

- Scout the same area every 3–7 days, adjusting for crop development.
- Record severity and affected area using a consistent scale.
- Reassess after any intervention and document the response.
""".strip()


def parse_json_object(text: str) -> dict:
    """Best-effort helper for future structured-output features."""
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end > start:
            return json.loads(cleaned[start : end + 1])

        raise
