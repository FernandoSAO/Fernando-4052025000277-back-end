from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Invoice(Base):

    __tablename__ = 'InvoiceTable'

    invoice_number = Column(String(40))
    company_cnpj = Column(String(40), ForeignKey('CompaniesTable.company_cnpj'))
    value = Column(Float)
    payment_date = Column(String(10))
    insertion_date = Column(DateTime, default=datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint('invoice_number', 'company_cnpj'),
    )

    def __init__(self, invoice_number:str, company_cnpj:str, value:float,
                payment_date:Union[DateTime, None] = None):
        """
        Cria uma Fatura

        Arguments:
            invoice_number: código da fatura, pode conter letras e/ou números, componente da PrimaryKey
            company_cnpj: cnpj da empresa para qual é o pagamento, precisa estar presente na tabela companies,
                chave estrangeira para a tabela CompaniesTable, componente da PrimaryKey
            value: valor a ser pago
            payment_date: data limite de quando o pagamento deverá ser feito
            insertion_date: data de quando a fatura foi inserida
        """
        self.invoice_number = invoice_number
        self.company_cnpj = company_cnpj
        self.value = value
        self.payment_date = payment_date