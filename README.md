# LegalEase AI Document Generator

A runnable Naan Mudhalvan student project based on the attached project brief. It contains a Streamlit interface, a FastAPI backend, optional Gemini generation, an offline template mode, editable previews, and TXT/DOCX/PDF export.

## Features

- Draft an NDA, employment agreement, residential lease, or freelance services agreement.
- Provide parties, date, jurisdiction, and terms.
- Use Gemini when an API key is configured, or run with local template generation without a key.
- Edit the generated draft and download it as TXT, DOCX, or PDF.
- API health check and interactive API documentation.

## Requirements

- Windows 10/11 (the commands below use PowerShell)
- Python 3.10 or newer and VS Code
- Internet access to install Python packages
- Optional: a Gemini API key for AI generation. Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Open in VS Code

1. Extract the project ZIP if you downloaded the ZIP.
2. In VS Code, choose **File > Open Folder** and select the `LegalEase` folder.
3. Open **Terminal > New Terminal**. Confirm the terminal is PowerShell.
4. Create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in that terminal and activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Optional Gemini setup: copy `.env.example` to `.env`, then paste your key after `GEMINI_API_KEY=`. Do not share or upload `.env`. If you skip this, the app uses its offline template generator.
7. In VS Code, press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and select the interpreter in `.venv`.

## Run the project

The backend and frontend need separate terminals. Keep both running.

**Terminal 1 - FastAPI backend:**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` to view the interactive API docs.

**Terminal 2 - Streamlit frontend:**

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Streamlit opens the app at `http://localhost:8501`. Select a document, fill each field, and press **Generate document**. Edit the preview and use the download buttons.

To stop either server, focus its terminal and press `Ctrl+C`.

## Test API manually

Open `http://127.0.0.1:8000/docs`, expand `POST /generate`, choose **Try it out**, and submit:

```json
{
  "document_type": "Non-Disclosure Agreement (NDA)",
  "parties": "Example Client (Disclosing Party); Example Consultant (Receiving Party)",
  "effective_date": "03 October 2026",
  "jurisdiction": "India",
  "terms": ["Use confidential information only for project evaluation", "Return materials when discussions end"]
}
```

## Project structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── .env.example
├── .gitignore
├── app.py                 # Streamlit interface
├── exports.py             # TXT, DOCX, PDF generation
├── main.py                # FastAPI application
├── requirements.txt
├── routes.py              # /health and /generate endpoints
└── schemas.py             # Validated API models
```

## Common fixes

- **`py` is not recognized:** install Python 3.10+ from [python.org](https://www.python.org/downloads/) and select **Add Python to PATH**, then reopen VS Code.
- **`uvicorn` or `streamlit` is not recognized:** activate `.venv` and run `python -m pip install -r requirements.txt` again.
- **Frontend says it cannot reach backend:** make sure Terminal 1 is still running `uvicorn main:app --reload` on port 8000.
- **Gemini error:** verify the key in `.env`, check API access/quota, and restart the backend after changing `.env`. Without a key, template mode works locally.
- **PDF exports have font limitations:** the exporter uses built-in PDF fonts; use standard Latin characters for best compatibility.

## Important use note

This is an academic demonstration, not a legal service. Generated text can be incorrect, incomplete, or inappropriate for local law. No draft is guaranteed valid or enforceable. Do not enter confidential personal or business data into Gemini; when enabled, prompts are sent to Google's API. Ask a qualified lawyer to review any document before signing or relying on it.
