Este é o back-end do trabalho de Engenharia de Software do aluno Fernando Oliveira

-----------------------------------------------------------------------------------

# API de inclusão de faturas de pagamento e empresas

Esta API tem como objetivo a inclusão de faturas de pagamento e suas empresas, a possibilidade da busca por todas as faturas
ou empresas, procura de todas as faturas de uma empresa, procura de empresas por cnpj, faturas por cnpj e seu número e 
exclusão de empresas e faturas da base.
Conta também com verificações de integridade na base tais como a existência da empresa quando a fatura for inscrita e
da existência de faturas quando uma empresa for excluída. 

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
venv\Scripts\activate
```

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
