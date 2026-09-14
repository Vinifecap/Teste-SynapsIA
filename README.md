# SynapsIA

Projeto com backend em Python/FastAPI e frontend em React/Vite preparado para rodar localmente, sem Docker.

## Pre-requisitos

- Git
- Python 3.14
- Node.js 20 ou superior

## Como clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd Teste-SynapsIA
```

Se voce ja tem a pasta do projeto no notebook, apenas abra a pasta `Teste-SynapsIA` no VS Code.

## Variaveis de ambiente

Use o arquivo `.env.example` como referencia:

```bash
copy .env.example .env
```

No frontend, se quiser configurar explicitamente a URL da API:

```bash
cd frontend
copy .env.example .env
```

Por padrao, o frontend usa `http://localhost:8000` para falar com o backend.

## Como iniciar o backend

Abra um terminal na raiz do projeto e execute:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

O backend ficara disponivel em:

```text
http://localhost:8000
```

Para testar rapidamente:

```text
http://localhost:8000/health
```

## Como iniciar o frontend

Abra outro terminal na raiz do projeto e execute:

```bash
cd frontend
npm install
npm run dev
```

No PowerShell, se o comando `npm` for bloqueado pela politica de execucao de scripts, use:

```bash
npm.cmd install
npm.cmd run dev
```

O frontend ficara disponivel em:

```text
http://localhost:5173
```

## Qual endereco abrir no navegador

Abra:

```text
http://localhost:5173
```

## Como parar cada servidor

No terminal do backend, pressione:

```text
Ctrl + C
```

No terminal do frontend, pressione:

```text
Ctrl + C
```

Se o ambiente virtual Python estiver ativo e voce quiser sair dele:

```bash
deactivate
```
