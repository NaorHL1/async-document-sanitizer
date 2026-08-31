from celery_app import celery_app

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from sqlmodel import Session,select
from database import DocumentRecord, engine

# Load the Microsoft Presidio NLP models into memory
# (We put this OUTSIDE the task function so it doesn't load the heavy AI model every single time a document arrives)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

@celery_app.task
def mask_pii_document(doc_id: str, text: str):
    """
    This background task takes a document, analyzes it with Presidio (NLP),
    masks the PII, and returns the clean text.
    """
    print(f"[{doc_id}] Worker started masking process...")

    # Step A: Analyze the text to find PII (Credit cards, Emails, Names, etc.)
    results = analyzer.analyze(text=text, entities=["PERSON","PHONE_NUMBER","HOME_ADDRESS","EMAIL_ADDRESS","CREDIT_CARD"], language='en')
    print(results)

    # Step B: Anonymize the found PII by replacing it with <REDACTED>
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=results)

    clean_text = anonymized_result.text
    print(f"[{doc_id}] Masking complete!")

    with Session(engine) as session:
        statement = select(DocumentRecord).where(DocumentRecord.doc_id == doc_id)
        db_doc = session.exec(statement).first()

        if db_doc:
            db_doc.sanitized_text = clean_text
            db_doc.status = "COMPLETED"

            session.add(db_doc)
            session.commit()
            print(f"[{doc_id}] Database updated successfully!")


    return clean_text