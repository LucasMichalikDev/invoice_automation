# Invoice Automation API

This project focuses on demonstration the use of an API to automate the upload, storaging and processing of invoices in text-based PDFs.

## Features
- REST-API for upload of invoices
- text extraction of text-based PDFs
- automated extraction of important invoice data
- categorisation of invoices
- storaging the details of uploaded invoices in SQLite database
- containerized with docker
- automated tests with pytest

## Technologies
- python
- FastAPI
- PyMuPDF
- pytest
- Docker
- SQLite

## Installation
1. Make sure you have installed Docker and Git
2. Clone this Repository: 
    git clone https://github.com/LucasMichalikDev/invoice_automation.git
3. Build docker image in project root:
    docker build -t invoice-automation .
4. Start the docker container:
    docker run -d -p 8000:8000 --name invoice-app invoice-automation
5. Access the API in your browser: http://127.0.0.1:8000/docs
5. Stop application with:
    docker stop invoice-app
6. Restart application with
    docker start invoice-app


## API Endpoints
| Method | Endpoint | Description | Return Value |
|-------------|-------------|-------------|-------------|
| POST | /invoices | Upload invoice | Generated ID, Filename, extracted invoice Data |
| DELETE | /invoices/{id} | Delete invoice by ID| confirmation message |
| GET | /invoices | Get all invoices | Invoice Data (of all invoices) |
| GET | /invoices/{id} | Get invoice by ID| Invoice Data |

## Improvement Ideas
- Adding AI-based data extraction (for image based PDFs)
- Extraction of data in different languages (currently only in German)
- Cloud deployment
- Improving validation and categorization rules
- Adding fuctionalities like: get average/mean cost, delete latest, get total cost

## by Lucas Michalik
