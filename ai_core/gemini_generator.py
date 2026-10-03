"""Gemini integration with a deterministic offline fallback."""
import os

from dotenv import load_dotenv

load_dotenv()


def _template_document(document_type: str, parties: str, effective_date: str,
                       jurisdiction: str, terms: list[str]) -> str:
    clauses = "\n".join(f"{i}. {term}" for i, term in enumerate(terms, 1))
    return f"""{document_type.upper()}

Draft for discussion - review with a qualified lawyer before signing.

1. PARTIES
{parties}

2. EFFECTIVE DATE
{effective_date}

3. JURISDICTION
{jurisdiction}

4. AGREED TERMS
{clauses}

5. GENERAL
The parties intend to record their understanding in this document. Any missing
details, statutory requirements, remedies, notices, and signing formalities should
be reviewed and completed for the applicable jurisdiction before use.

SIGNATURES

Party 1: ______________________________    Date: ______________

Party 2: ______________________________    Date: ______________

IMPORTANT: This educational draft is AI-generated (or template-generated), is not
legal advice, and is not guaranteed to be complete, accurate, enforceable, or suitable
for any particular situation. Obtain independent legal review before relying on it.
"""


def generate_document(document_type: str, parties: str, effective_date: str,
                      jurisdiction: str, terms: list[str]) -> tuple[str, str]:
    """Generate with Gemini when configured; otherwise return local template text."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return _template_document(document_type, parties, effective_date,
                                  jurisdiction, terms), "Local template (no API key)"

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        prompt = f"""Draft a clear, structured educational first draft of the document below.
Use only the supplied facts. Do not invent names, dates, amounts, or obligations.
If key facts are missing, mark them [TO BE COMPLETED]. Use plain, professional language.
Include numbered sections and signature lines. End with a notice that this is not legal
advice and requires review by a qualified lawyer in the stated jurisdiction. Do not
claim that the draft is legally valid, enforceable, or ready to sign.

Document type: {document_type}
Parties and roles: {parties}
Effective date: {effective_date}
Jurisdiction: {jurisdiction}
User-supplied terms:\n""" + "\n".join(f"- {term}" for term in terms)
        response = client.models.generate_content(model=model, contents=prompt)
        if not response.text:
            raise RuntimeError("Gemini returned an empty response")
        return response.text.strip(), f"Gemini ({model})"
    except Exception as exc:
        # Do not silently disguise an API failure as a successful AI draft.
        raise RuntimeError(f"Gemini generation failed: {exc}") from exc
