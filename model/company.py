from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Company(Base):

    __tablename__ = 'CompaniesTable'

    company_cnpj = Column(String(40), unique=True, primary_key=True)
    company_name = Column(String(40), unique=True)
    insertion_date = Column(DateTime, default=datetime.now)

    def __init__(self, company_cnpj:str, company_name:str, insertion_date:Union[DateTime, None] = None):
        """
        Registra uma empresa

        Arguments:
            company_cnpj: cnpj da empresa, valor único na tabela, chave primária
            company_name: nome da empresa, valor único na tabela
            insertion_date: data de quando a empresa foi inserido à base
        """
        self.company_cnpj = company_cnpj
        self.company_name = company_name
