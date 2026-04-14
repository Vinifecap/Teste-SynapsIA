# ⚙️ Execution (Camada 3 - Fazer o trabalho)

Este diretório contém todos os **scripts Python determinísticos** do projeto Synapsia SaaS.

## Princípios

1. **Determinístico**: Mesma entrada → mesma saída, sempre
2. **Testável**: Cada script deve ter testes correspondentes
3. **Bem comentado**: Código claro e documentado
4. **Sem decisões complexas**: A lógica de decisão fica na Camada 2 (Orquestração)

## Estrutura

```
execution/
├── README.md          # Este arquivo
├── utils/             # Utilitários compartilhados
│   ├── __init__.py
│   ├── config.py      # Carregamento de configuração (.env)
│   ├── logger.py      # Sistema de logging padronizado
│   └── validators.py  # Validações comuns
├── auth/              # Scripts de autenticação
├── data/              # Scripts de processamento de dados
├── api/               # Scripts de integração com APIs
└── tests/             # Testes automatizados
```

## Convenções

- Nomes de arquivo: `snake_case.py`
- Cada script deve ter docstring explicando seu propósito
- Usar variáveis de ambiente do `.env` (nunca hardcode de secrets)
- Tratar erros com mensagens claras
- Retornar dados estruturados (dicts/JSON) para a camada de orquestração
