from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Company, Invoice
from logger import logger
from schemas import *
from flask_cors import CORS
from utilities import date_utilities

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
company_tag = Tag(name="Empresa", description="Adição, visualização e remoção de empresas à base")
invoice_tag = Tag(name="Fatura", description="Adição, visualização e remoção de faturas à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# --- tags relacionadas a empresa ---

@app.post('/addCompany', tags=[company_tag],
          responses={"200": CompanyViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_company(form: CompanySchema):
    """Adiciona uma nova empresa à base de dados

    Retorna uma representação da empresa
    """

    print(f"CNPJ: {form.CompanyCNPJ}")
    print(f"Nome: {form.CompanyName}\n")

    company = Company(
        company_cnpj=form.CompanyCNPJ,
        company_name=form.CompanyName)
    
    logger.debug(f"Adicionando empresa de nome: '{company.company_name}'")

    try:
        # criando conexão com a base
        session = Session()

        # verificar se cnpj já existe

        existing_cnpj = session.query(Company).filter(Company.company_cnpj == company.company_cnpj).first()

        if existing_cnpj:
            error_msg = f"CNPJ {form.CompanyCNPJ} já cadastrado!"
            logger.warning(error_msg)
            return {"message": error_msg}, 409
        
        # verificar se nome já existe

        existing_name = session.query(Company).filter(Company.company_name == company.company_name).first()

        if existing_name:
            error_msg = f"Nome {form.CompanyName} já cadastrado!"
            logger.warning(error_msg)
            return {"message": error_msg}, 409

        # adicionando empresa
        session.add(company)

        # efetivando o comando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado empresa de nome: '{company.company_name}'")

        return apresenta_company(company), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        print(company.company_cnpj, company.company_name)
        logger.warning(f"Erro ao adicionar empresa '{company.company_name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/getCompanies', tags=[company_tag],
         responses={"200": ListagemCompanySchema, "404": ErrorSchema})
def get_companies():
    """Faz a busca por todas as Empresas cadastradas

    Retorna uma representação da listagem Empresas.
    """

    logger.debug(f"Coletando empresas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    companies = session.query(Company).all()

    if not companies:
        # se não há empresas cadastradas
        return {"companies": []}, 200
    else:
        logger.debug(f"%d empresas econtradas" % len(companies))
        # retorna a representação de empresas
        print(companies)
        return apresenta_companies(companies), 200

@app.get('/getCompany', tags=[company_tag],
         responses={"200": CompanyViewSchema, "404": ErrorSchema})
def get_company(query: CompanyBuscaSchema):
    """Faz a busca por uma empresa a partir do cnpj da empresa

    Retorna uma representação da empresa.
    """
    company_cnpj = query.CompanyCNPJ
    logger.debug(f"Coletando dados sobre a empresa de CNPJ #{company_cnpj}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    company = session.query(Company).filter(Company.company_cnpj == company_cnpj).first()

    if not company:
        # se a empresa não foi encontrada
        error_msg = "empresa não encontrado na base :/"
        logger.warning(f"Erro ao buscar empresa '{company_cnpj}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Empresa econtrada: '{company.company_name}'")
        # retorna a representação de produto
        return apresenta_company(company), 200

@app.delete('/deleteCompany', tags=[company_tag],
            responses={"200": CompanyDelSchema, "404": ErrorSchema})
def del_company(query: CompanyBuscaSchema):
    """Deleta uma Empresa a partir do cnpj da empresa

    Retorna uma mensagem de confirmação da remoção.
    """
    company_cnpj = unquote(unquote(query.CompanyCNPJ))
    logger.debug(f"Deletando dados sobre a empresa #{company_cnpj}")
    # criando conexão com a base
    session = Session()

    try:

        # busca pelo cnpj no banco
        company = session.query(Company).filter(Company.company_cnpj == company_cnpj).first()

        if not company:
            error_msg = f"Empresa com CNPJ {company_cnpj} não encontrada!"
            logger.warning(error_msg)
            return {"message": error_msg, "CompanyCNPJ": company_cnpj}, 404
        
        # verifica se empresa tem faturas na base

        invoices_count = session.query(Invoice).filter(Invoice.company_cnpj == company_cnpj).count()

        if invoices_count > 0:
            error_msg = (f"Empresa com CNPJ {company_cnpj} com faturas na base de dados. " 
                "Deletar as faturas primeiro para poder deletar a empresa.")
            logger.warning(error_msg)
            return {"message": error_msg, "CompanyCNPJ": company_cnpj}, 404

        company_name = company.company_name
        session.delete(company)
        session.commit()

        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada empresa #{company.company_name}")
        return {
            "message": "Empresa removida com sucesso",
            "CompanyCNPJ": company_cnpj,
            "CompanyName": company_name
        }, 200
    
    except Exception as e:
        session.rollback()
        error_msg = f"Erro ao deletar empresa: {str(e)}"
        logger.error(error_msg)
        return {"message": error_msg}, 500
    finally:
        session.close()

# --- tags relacionadas a faturas ---

@app.post('/addInvoice', tags=[invoice_tag],
          responses={"200": InvoiceSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_invoice(form: InvoiceSchema):
    """Adiciona uma nova fatura à base de dados

    Retorna uma representação da fatura
    """

    try:
        payment_date_iso = date_utilities.validate_convert_date(form.PaymentDate)
    except ValueError as e:
        logger.warning(f"Data de pagamento inválida: {str(e)}")
        return {"message": str(e), "field": "PaymentDate"}, 400

    invoice = Invoice(
        invoice_number=form.InvoiceNumber,
        company_cnpj=form.InvoiceCompanyCNPJ,
        value=form.Value,
        payment_date=payment_date_iso
        )
    
    logger.debug(f"Adicionando fatura de número: '{invoice.invoice_number}'")

    try:
        # criando conexão com a base
        session = Session()

        # verifica se cnpj existe na tabela de empresas

        existing_company = session.query(Company).filter(Company.company_cnpj == invoice.company_cnpj).first()

        if not existing_company:
            error_msg = f"Empresa de CNPJ {form.InvoiceCompanyCNPJ} não cadastrada! Por favor cadastre-a primeiro"
            logger.warning(error_msg)
            return {"message": error_msg}, 409


        # verificar se número da fatura já existe para a empresa correspondente ao cnpj inserido

        existing_invoice = session.query(Invoice).filter(Invoice.invoice_number == invoice.invoice_number, 
            Invoice.company_cnpj == invoice.company_cnpj).first()

        if existing_invoice:
            error_msg = f"Fatura {form.InvoiceNumber} da empresa de CNPJ {form.InvoiceCompanyCNPJ} já cadastrado!"
            logger.warning(error_msg)
            return {"message": error_msg}, 409

        # adicionando empresa
        session.add(invoice)

        # efetivando o comando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionada fatura de número: '{form.InvoiceNumber}'")

        return apresenta_invoice(invoice), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar fatura de número '{form.InvoiceNumber}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/getInvoices', tags=[invoice_tag],
         responses={"200": ListagemInvoiceSchema, "404": ErrorSchema})
def get_invoices():
    """Faz a busca por todas as faturas cadastradas

    Retorna uma representação da listagem de faturas.
    """

    logger.debug(f"Coletando faturas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    invoices = session.query(Invoice).all()

    if not invoices:
        # se não há faturas cadastradas
        return {"invoices": []}, 200
    else:
        logger.debug(f"%d faturas econtradas" % len(invoices))
        # retorna a representação de faturas
        return apresenta_invoices(invoices), 200
    
@app.get('/getInvoiceByNumber', tags=[invoice_tag],
         responses={"200": InvoiceViewSchema, "404": ErrorSchema})
def get_invoice_by_number(query: InvoiceBuscaSchema):
    """Faz a busca por uma fatura a partir do seu número

    Retorna uma representação da fatura.
    """
    invoice_number = query.InvoiceNumber
    company_cnpj = query.InvoiceCompanyCNPJ

    logger.debug(f"Coletando dados sobre a fatura #{invoice_number} de CNPJ {company_cnpj}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    invoice = session.query(Invoice).filter(Invoice.invoice_number == invoice_number, 
        Invoice.company_cnpj == company_cnpj).first()

    if not invoice:
        # se a fatura não foi encontrada
        error_msg = "fatura não encontrado na base :/"
        logger.warning(f"Erro ao buscar fatura '{invoice_number}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Fatura econtrada: '{invoice_number}'")
        # retorna a representação de produto
        return apresenta_invoice(invoice), 200
    
@app.get('/getInvoicesOfCnpj', tags=[invoice_tag],
         responses={"200": InvoiceViewSchema, "404": ErrorSchema})
def get_invoices_of_CNPJ(query: InvoiceCNPJBuscaSchema):
    """Faz a busca de todas as faturas com CNPJ dado

    Retorna representação das faturas.
    """
    company_cnpj = query.InvoiceCompanyCNPJ

    logger.debug(f"Coletando dados sobre as faturas de CNPJ {company_cnpj}")
    # criando conexão com a base
    session = Session()

    # busca pelo cnpj no banco
    company = session.query(Company).filter(Company.company_cnpj == company_cnpj).first()

    if not company:
        error_msg = f"Empresa com CNPJ {company_cnpj} não encontrada!"
        logger.warning(error_msg)
        return {"message": error_msg, "CompanyCNPJ": company_cnpj}, 404

    # fazendo a busca
    invoices = session.query(Invoice).filter(Invoice.company_cnpj == company_cnpj).all()

    if not invoices:
        # se náo tiver faturas
        logger.debug(f"Empresa de CNPJ {company_cnpj} sem faturas registradas'")
        return {"invoices": []}, 200
    else:
        logger.debug(f"%d faturas econtradas" % len(invoices))
        # retorna a representação de produto
        return apresenta_invoices(invoices), 200

@app.delete('/deleteInvoice', tags=[invoice_tag],
         responses={"200": InvoiceDelSchema, "404": ErrorSchema})
def del_invoice(query: InvoiceBuscaSchema):
    """Deleta uma fatura a partir do número e cnpj da empresa correspondente

    Retorna uma mensagem de confirmação da remoção.
    """
    invoice_number = query.InvoiceNumber
    company_cnpj = query.InvoiceCompanyCNPJ
    logger.debug(f"Deletando dados da fatura #{invoice_number}")
    # criando conexão com a base
    session = Session()

    try:

        # busca pela fatura no banco
        invoice = session.query(Invoice).filter(Invoice.invoice_number == invoice_number, 
            Invoice.company_cnpj == company_cnpj).first()

        if not invoice:
            error_msg = f"Fatura {invoice_number} de CNPJ {company_cnpj} não encontrada!"
            logger.warning(error_msg)
            return {"message": error_msg, "invoice_number": invoice_number}, 404

        session.delete(invoice)
        session.commit()

        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada fatura {invoice_number}")
        return {
            "message": "Fatura removida com sucesso",
            "InvoiceNumber": company_cnpj,
            "InvoiceCNPJ": company_cnpj
        }, 200
    
    except Exception as e:
        session.rollback()
        error_msg = f"Erro ao deletar fatura: {str(e)}"
        logger.error(error_msg)
        return {"message": error_msg}, 500
    finally:
        session.close()