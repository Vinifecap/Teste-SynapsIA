# SynapsIA

Atualmente, este projeto contém somente a Homepage da SynapsIA, desenvolvida com React e Vite.

O MVP anterior de processamento de exames fMRI foi removido. Por isso, não há backend, fluxo de upload ou página de relatório nesta versão. O item **Portal MVP** da barra de navegação está temporariamente desativado até a integração do novo MVP.

## Pré-requisitos

- Git
- Node.js 20 ou superior
- npm

## Como executar localmente

Na raiz do projeto, acesse o diretório do frontend e instale as dependências:

```bash
cd frontend
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

Se o PowerShell bloquear a execução de `npm.ps1`, use os comandos equivalentes `npm.cmd install`, `npm.cmd run dev` e `npm.cmd run build`.

A Homepage ficará disponível em:

```text
http://localhost:5173
```

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

## Build de produção

Para gerar e validar a versão de produção:

```bash
cd frontend
npm run build
```

Os arquivos gerados ficam em `frontend/dist`.
