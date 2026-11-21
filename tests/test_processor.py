from app.processor import extract_text_from_pdf, extract_invoice_data, categorize_invoice, validate_invoice
import io

def test_extract_text_from_pdf():
    pdf_path = "sample_invoices/rechnung_001.pdf"

    with open(pdf_path, "rb") as file:
        bytestream = io.BytesIO(file.read())

    text = extract_text_from_pdf(bytestream)

    assert text is not None
    assert "RECHNUNG" in text
    assert "Microsoft" in text

def test_extract_invoice_data():
    pdf_path = "sample_invoices/rechnung_001.pdf"
    with open(pdf_path, "rb") as file:
        bytestream = io.BytesIO(file.read())
    text = extract_text_from_pdf(bytestream)

    data = extract_invoice_data(text)

    assert data.get("invoice_number") == "RE-2026-001"
    assert data.get("invoice_issuer") == "Microsoft"
    assert data.get("invoice_date") == "18.11.2026"
    assert data.get("invoice_amount") == 123.99


def test_categorize_invoice():
    assert categorize_invoice(None) == "unknown"
    assert categorize_invoice(0) == "small_amount"
    assert categorize_invoice(9.99) == "small_amount"
    assert categorize_invoice(10) == "medium_amount"
    assert categorize_invoice(99.99) == "medium_amount"
    assert categorize_invoice(100) == "high_amount"


def test_validate_invoice():
    data = {
        "invoice_number": "Ab-123",
        "invoice_issuer": "ABC",
        "invoice_date": "12.12.1234",
        "invoice_amount": 1.11
    }
    
    assert validate_invoice(data) == ("success", [])

    data["invoice_amount"] = 10000

    assert validate_invoice(data) == ("needs_review", [])

    del data["invoice_issuer"]
    del data["invoice_date"]

    assert validate_invoice(data) == ("needs_review", ["invoice_issuer", "invoice_date"])