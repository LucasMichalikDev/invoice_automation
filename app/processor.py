import pymupdf
import re

def extract_text_from_pdf(pdf_file_bytestream):
    document = pymupdf.open(stream=pdf_file_bytestream, filetype="pdf")
    extracted_text = ""
    for page in document:
        extracted_text += page.get_text()
    document.close()
    return extracted_text


def extract_invoice_data(text):
    invoice_number = re.search(
        r"Rechnungsnummer:\s(.+)",
        text
    )

    invoice_issuer = re.search(
        r"Rechnungssteller:\s(.+)",
        text
    )

    invoice_date = re.search(
        r"Rechnungsdatum:\s(\d{2}\.\d{2}\.\d{4})",
        text
    )

    invoice_amount = re.search(
        r"Rechnungsbetrag:\s(\d+(?:\.\d{1,2})?)\sEUR",
        text
    )

    data = {
        "invoice_number": invoice_number.group(1).strip() if invoice_number else None,
        "invoice_issuer": invoice_issuer.group(1).strip() if invoice_issuer else None,
        "invoice_date": invoice_date.group(1).strip() if invoice_date else None,
        "invoice_amount": float(invoice_amount.group(1).strip()) if invoice_amount else None
    }

    data["category"] = categorize_invoice(data["invoice_amount"])

    status, missing_fields = validate_invoice(data)
    data["status"] = status
    data["missing_fields"] = missing_fields

    return data


def categorize_invoice(amount):
    if amount is None:
        return "unknown"

    if amount < 10:
        return "small_amount"

    if amount < 100:
        return "medium_amount"

    return "high_amount"


def validate_invoice(data):
    required_fields = [
        "invoice_number",
        "invoice_issuer",
        "invoice_date",
        "invoice_amount"
    ]

    missing_fields = []

    for field in required_fields:
        if data.get(field) == None:
            missing_fields.append(field)

    if len(missing_fields) != 0:
        return "needs_review", missing_fields

    if data["invoice_amount"] >= 10000:
        return "needs_review", []

    return "success", []
