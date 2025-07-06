from pydantic import BaseModel
from typing import Optional, List
from model.invoice import Invoice

class InvoiceSchema(BaseModel):
    """ Define como uma nova fatura a ser inserida deve ser representada
    """    
    InvoiceNumber: str = "240615-001"
    InvoiceCompanyCNPJ: str = '12.345.678/0001-90'
    Value: float = 1122.33
    PaymentDate: str = '01/02/2023'

class InvoiceBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no número da fatura e do CNPJ da empresa correspondente.
    """
    InvoiceNumber: str = "240615-001"
    InvoiceCompanyCNPJ: str = '12.345.678/0001-90'

class InvoiceCNPJBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no CNPJ da empresa.
    """
    InvoiceCompanyCNPJ: str = '12.345.678/0001-90'

class ListagemInvoiceSchema(BaseModel):
    """ Define como uma listagem de faturas será retornada.
    """
    invoices:List[InvoiceSchema]


def apresenta_invoices(Invoices: List[Invoice]):
    """ Retorna uma representação de faturas seguindo o schema definido em
        InvoiceViewSchema.
    """
    result = []
    for Invoice in Invoices:
        result.append({
            "InvoiceNumber": Invoice.invoice_number,
            "InvoiceCompanyCNPJ": Invoice.company_cnpj,
            "Value": Invoice.value,
            "PaymentDate": Invoice.payment_date,
        })

    return {"invoices": result}

class InvoiceViewSchema(BaseModel):
    """ Define como uma fatura será retornada: invoice.
    """

    InvoiceNumber: str = "240615-001"
    InvoiceCompanyCNPJ: str = '12.345.678/0001-90'
    Value: float = 1122.33
    PaymentDate: str = '01/02/2023'

class InvoiceDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    InvoiceNumber: str

def apresenta_invoice(invoice: Invoice):
    """ Retorna uma representação de uma fatura seguindo o schema definido em
        InvoiceViewSchema.
    """
    return {
        "InvoiceNumber": invoice.invoice_number,
        "InvoiceCompanyCNPJ": invoice.company_cnpj,
        "Value": invoice.value,
        "PaymentDate": invoice.payment_date,
    }