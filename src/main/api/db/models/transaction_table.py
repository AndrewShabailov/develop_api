from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey('account.id'))
    from_account_id = Column(Integer, ForeignKey('account.id'))
    credit_id = Column(Integer, ForeignKey('credit.id'))
    amount = Column(Float)
    transaction_type = Column(String)
    created_at = Column(DateTime)

    def __repr__(self):
        return (
            f"<Transaction("
                f"id={self.id},"
                f" to_account_id={self.to_account_id},"
                f" from_account_id={self.from_account_id},"
                f" credit_id={self.credit_id},"
                f" amount={self.amount},"
                f" transaction_type={self.transaction_type},"
                f" created_at={self.created_at})>"
                )
