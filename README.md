# PDF Processor

O **PDF Processor** é um projeto Python desenvolvido para extrair, processar e salvar dados tabulares de arquivos PDF. Ele utiliza a biblioteca [Camelot](https://camelot-py.readthedocs.io/) para extração de tabelas e automatiza a transformação desses dados em formatos estruturados, como CSV.

Este projeto é ideal para processar PDFs contendo tabelas com formatação consistente, extraindo informações úteis para análise posterior.

## Funcionalidades
- **Extração de tabelas de PDFs:** Usa Camelot para detectar e extrair tabelas em PDFs.
- **Visualização de contornos:** Gera gráficos que mostram as áreas detectadas no PDF.
- **Processamento customizado de dados:** Reorganiza as tabelas extraídas em um formato estruturado.
- **Exportação para CSV:** Salva os dados processados em arquivos CSV no diretório desejado.

---

## Estrutura do projeto

```plaintext
├── .venv/                  # Ambiente virtual
├── data/                   # Diretório de saída para arquivos CSV
├── funcs/                  # Módulo contendo as funções principais
│   ├── __init__.py         # Arquivo de inicialização do módulo
│   └── pdf_extractor.py    # Script com as funções de extração e processamento de PDFs
├── pdf/                    # Diretório contendo os arquivos PDF a serem processados
├── main.py                 # Script principal do projeto
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
└── .gitignore              # Arquivo para ignorar arquivos/diretórios no Git
```

---

## Requisitos
- Python 3.10 ou superior
- Bibliotecas Python:
  - camelot
  - matplotlib
  - pandas
  - opencv-python
  - python-dotenv
  - isort
  - black
- Dependências de sistema:
  - **Ghostscript** (necessário para a biblioteca Camelot)
  - **Tkinter** (para exibir gráficos gerados pelo matplotlib)

### Instalando dependências
Use o `requirements.txt` para instalar as dependências necessárias:
```bash
pip install -r requirements.txt
```
