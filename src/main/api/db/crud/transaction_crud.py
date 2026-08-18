from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session


class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(id=transaction_id).first()
