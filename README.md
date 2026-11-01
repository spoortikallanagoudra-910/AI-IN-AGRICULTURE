# AgriAI — Photo-Analysis Agriculture Assistant

A prototype decision-support assistant for farmers, growers, extension
workers, and livestock keepers. It answers farm questions **and** analyzes
uploaded photographs (leaf close-ups, pests, whole plants, animals, fields,
and equipment) through a vision-capable LLM, with safety guardrails and a
built-in demo mode that needs no API key.

> Decision support only — not a substitute for a licensed agronomist,
> veterinarian, extension specialist, or other qualified professional.

## Features

- **Multipart photo upload** — up to 4 JPEG / PNG / WEBP images per request.
- **Image validation & preparation** (`app/images.py`) — format allow-list,
  10 MB cap, 2048 px resize, and safe re-encode via Pillow.
- **Vision-capable prompting** (`app/prompt_library.py`) — observation-first
  analysis, ranked differential diagnoses with uncertainty, and rules that
  forbid diagnosing or dosing from an image alone.
- **Safety screening** (`app/safety.py`) — advisory `chemical_safety` and
  `veterinary_safety` findings shown beside the answer.
- **Demo mode** — without an `API_KEY` the app still runs and accepts uploads.
- **Web UI** (`static/index.html`) — domain picker, farm-context fields, live
  photo previews, and rendered answers with safety banners.

## Project layout

```
app/
  config.py           # settings from env / .env
  images.py           # image validation & preparation
  llm.py              # OpenAI-compatible client (text + images) + demo mode
  main.py             # FastAPI app, endpoints, multipart handling
  models.py           # Pydantic request/response models
  prompt_library.py   # system, vision, and domain prompts
  safety.py           # message safety screening
static/index.html     # browser interface
tests/test_chat.py    # API tests (health, domains, demo mode, safety)
presentation/
  deck.html           # self-contained HTML slide deck (photos embedded)
  build_deck.py       # regenerates deck.html from presentation/photos
  photos/             # sample farm photos used by the deck & for testing
```

## Run it

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# Optional: live mode with a vision-capable model
cp .env.example .env   # set API_KEY, BASE_URL, MODEL_NAME (e.g. gpt-4o-mini)

uvicorn app.main:app --reload
# open http://127.0.0.1:8000
```

With no `API_KEY`, the app runs in **demo mode** and still accepts uploads.

## API

| Method | Path         | Purpose                                             |
| ------ | ------------ | --------------------------------------------------- |
| GET    | `/`          | Web UI                                             |
| GET    | `/health`    | Status, mode, model, `photos_supported`             |
| GET    | `/domains`   | List of supported domains                           |
| POST   | `/api/chat`  | Multipart form: `message`, `domain`, context fields, `photos` |

## Tests

```bash
pip install pytest
python -m pytest
```

## Presentation & sample photos

`presentation/deck.html` is a keyboard-navigable slide deck (←/→ or Space)
that explains the photo-analysis upgrade and embeds the four sample photos.
The same photos live in `presentation/photos/` and can be uploaded directly
to test the app. Regenerate the deck after editing photos or slides:

```bash
python presentation/build_deck.py
```
