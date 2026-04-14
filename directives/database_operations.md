# Diretiva: Operações de Banco de Dados

## Objetivo
Gerenciar operações de banco de dados do Synapsia SaaS de forma segura e consistente.

## Inputs
- Tipo de operação: `migration` | `seed` | `backup` | `restore`
- Ambiente: `development` | `staging` | `production`

## Ferramentas/Scripts
1. `execution/data/db_migrate.py` — Executar migrações
2. `execution/data/db_seed.py` — Popular banco com dados iniciais
3. `execution/data/db_backup.py` — Criar backup do banco
4. `execution/data/db_restore.py` — Restaurar backup

## Passos

### Migrações
1. Criar arquivo de migração em `execution/data/migrations/`
2. Rodar `execution/data/db_migrate.py --action up`
3. Verificar que a migração foi aplicada

### Seed
1. Definir dados de seed em `execution/data/seeds/`
2. Rodar `execution/data/db_seed.py`

### Backup
1. Rodar `execution/data/db_backup.py --env <ambiente>`
2. Backup salvo em `.tmp/backups/`

### Restore
1. Rodar `execution/data/db_restore.py --file <caminho_do_backup>`
2. Verificar integridade dos dados

## Outputs
- Banco de dados atualizado/restaurado
- Logs de operação
- Backup (se aplicável)

## Casos de Borda
- **NUNCA** rodar migrations destrutivas em produção sem backup
- Sempre verificar se há conexões ativas antes de restore
- Migrações devem ser reversíveis (up/down)

## Aprendizados
_Atualizar esta seção conforme descobrir edge cases_
