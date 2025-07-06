from pydantic import BaseModel
from typing import Optional, List
from model.company import Company

class CompanySchema(BaseModel):
    """ Define como uma nova empresa a ser inserida deve ser representada
    """    
    CompanyCNPJ: str = "12.345.678/0001-90"
    CompanyName: str = "nome comercial"

class CompanyBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no CNPJ da empresa.
    """
    CompanyCNPJ: str = "12.345.678/0001-90"

class ListagemCompanySchema(BaseModel):
    """ Define como uma listagem de empresas será retornada.
    """
    companies:List[CompanySchema]


def apresenta_companies(Companies: List[Company]):
    """ Retorna uma representação de empresas seguindo o schema definido em
        CompanyViewSchema.
    """
    result = []
    for Company in Companies:
        result.append({
            "CompanyCNPJ": Company.company_cnpj,
            "CompanyName": Company.company_name,
        })

    return {"companies": result}

class CompanyViewSchema(BaseModel):
    """ Define como uma emore será retornada: company.
    """

    CompanyCNPJ: str = "12.345.678/0001-90"
    CompanyName: str = "nome comercial"

class CompanyDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    CompanyCNPJ: str
    CompanyName: str
    

def apresenta_company(company: Company):
    """ Retorna uma representação de uma fatura seguindo o schema definido em
        CompanyViewSchema.
    """
    return {
            "CompanyCNPJ": company.company_cnpj,
            "CompanyName": company.company_name,
    }