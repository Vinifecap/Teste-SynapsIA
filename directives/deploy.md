# Diretiva: Deploy

## Objetivo
Realizar o deploy do Synapsia SaaS em diferentes ambientes.

## Inputs
- Ambiente alvo: `staging` | `production`
- Branch: nome da branch a ser deployada (default: `main`)

## Ferramentas/Scripts
1. `execution/deploy/deploy_app.py` — Script principal de deploy
2. `execution/utils/config.py` — Carrega variáveis de ambiente

## Passos

### 1. Pré-deploy
- Verificar que todos os testes passam
- Verificar que a branch está atualizada com `main`
- Gerar build de produção

### 2. Deploy
- Rodar `execution/deploy/deploy_app.py --env <ambiente>`
- Monitorar logs de deploy

### 3. Pós-deploy
- Verificar health check do serviço
- Rodar smoke tests
- Notificar equipe

## Outputs
- Aplicação deployada no ambiente alvo
- URL de acesso ao serviço
- Relatório de status do deploy

## Casos de Borda
- Se o health check falhar, fazer rollback automático
- Se o deploy demorar mais de 10 minutos, investigar
- Manter os últimos 3 deploys para rollback rápido

## Aprendizados
_Atualizar esta seção conforme descobrir edge cases_
