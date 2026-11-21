import sqlite3

DATABASE_NAME = "invoices.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        invoice_issuer TEXT,
        invoice_date TEXT,
        invoice_amount FLOAT,
        category TEXT,
        status TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_invoice(data):
    connection = get_connection()
    cursor = connection.execute("""
        INSERT INTO invoices (
            invoice_number,
            invoice_issuer,
            invoice_date,
            invoice_amount,
            category,
            status
        )
        VALUES (?,?,?,?,?,?)
        """, 
        (
            data["invoice_number"],
            data["invoice_issuer"],
            data["invoice_date"],
            data["invoice_amount"],
            data["category"],
            data["status"]
        )
    )

    connection.commit()
    invoice_id = cursor.lastrowid
    connection.close()
    return invoice_id


def get_all_invoices():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT * FROM invoices"
    )

    invoices = []
    for row in cursor.fetchall():
        invoices.append(dict(row))
    connection.close()
    return invoices


def get_invoice(invoice_id):
    connection = get_connection()
    cursor = connection.execute(
        "SELECT * FROM invoices WHERE id = ?",
        (invoice_id)
    )

    invoice = cursor.fetchone()
    connection.close()
    return dict(invoice) if invoice else None


def delete_invoice(invoice_id):
    connection = get_connection()
    cursor = connection.execute(
        "DELETE FROM invoices WHERE id = ?",
        (invoice_id)
    )
    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted