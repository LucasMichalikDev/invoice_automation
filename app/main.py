from fastapi import FastAPI, HTTPException, UploadFile, File
from contextlib import asynccontextmanager
import pymupdf

from app.processor import (extract_invoice_data, extract_text_from_pdf)
from app.databaseSQLite import (initialize_database, save_invoice, get_all_invoices, get_invoice, delete_invoice)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()

    yield
    print("API got closed")


app = FastAPI(
    lifespan=lifespan,
    title="Invoice Automation API",
    description="Automated invoice-pdf data extraction and processing",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Invoice Automation API is runnning"
    }

@app.get("/invoices")
def get_invoice_list():
    return get_all_invoices()


@app.get("/invoices/{invoice_id}")
def get_invoice_by_id(invoice_id):
    return get_invoice(invoice_id)
    

@app.post("/invoices")
async def upload_invoice(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="only allowed to upload .pdf files"
        )
    pdf_content = await file.read()

    try:
        text = extract_text_from_pdf(pdf_content)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="not able to read the pdf file"
        )

    invoice_data = extract_invoice_data(text)
    invoice_id = save_invoice(invoice_data)

    return{
        "id": invoice_id,
        "filename": file.filename,
        "invoice": invoice_data
    }

@app.delete("/invoices/{invoice_id}")
def delete_invoice_by_id(invoice_id):
    deleted = delete_invoice(invoice_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found, therefore could not delete"
        )
    return {
        "message": "Invoice was deleted successfully"
    }
