# 📋 Directives (Camada 1 - O que fazer)

Este diretório contém todas as **SOPs (Standard Operating Procedures)** do projeto Synapsia SaaS.

## Estrutura

Cada diretiva é um arquivo Markdown que define:
- **Objetivo**: O que precisa ser feito
- **Inputs**: O que é necessário para começar
- **Ferramentas/Scripts**: Quais scripts da camada de execução usar
- **Outputs**: O que deve ser produzido
- **Casos de borda**: Situações especiais e como lidar

## Convenções

- Nomes de arquivo: `snake_case.md`
- Cada diretiva deve ser autocontida
- Sempre atualizar diretivas quando aprender algo novo (API limits, edge cases, etc.)
- Manter referência aos scripts de execução correspondentes

## Diretivas Disponíveis

| Diretiva | Descrição |
|----------|-----------|
| `setup_project.md` | Configuração inicial do projeto |
| `deploy.md` | Processo de deploy |
| `database_operations.md` | Operações de banco de dados |
| `auth_flow.md` | Fluxo de autenticação |
| `error_handling.md` | Tratamento de erros padrão |
