# Diretiva: Tratamento de Erros

## Objetivo
Padronizar o tratamento de erros em todo o Synapsia SaaS para garantir resiliência e debuggabilidade.

## Princípios

### 1. Erros são oportunidades de aprendizado (Self-Annealing)
Quando algo quebra:
1. Ler mensagem de erro e stack trace
2. Corrigir o script
3. Testar novamente
4. Atualizar a diretiva relevante com o que aprendeu

### 2. Categorias de Erro

| Categoria | HTTP Code | Ação |
|-----------|-----------|------|
| Validação | 400 | Retornar detalhes do erro ao cliente |
| Autenticação | 401 | Redirecionar para login |
| Autorização | 403 | Retornar "acesso negado" |
| Não encontrado | 404 | Retornar mensagem amigável |
| Rate Limit | 429 | Retornar retry-after header |
| Erro interno | 500 | Logar detalhes, retornar mensagem genérica |

### 3. Formato Padrão de Resposta de Erro
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Mensagem amigável para o usuário",
    "details": ["campo X é obrigatório", "email inválido"],
    "request_id": "uuid-do-request"
  }
}
```

## Ferramentas/Scripts
1. `execution/utils/error_handler.py` — Middleware de tratamento de erros
2. `execution/utils/logger.py` — Sistema de logging

## Regras
- **NUNCA** expor stack traces para o cliente em produção
- **SEMPRE** logar o erro completo internamente
- **SEMPRE** incluir request_id para rastreabilidade
- Usar códigos de erro consistentes (UPPER_SNAKE_CASE)
- Mensagens para o cliente devem ser em Português do Brasil

## Aprendizados
_Atualizar esta seção conforme descobrir edge cases_
