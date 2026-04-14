# Diretiva: Fluxo de Autenticação

## Objetivo
Gerenciar autenticação e autorização de usuários no Synapsia SaaS.

## Inputs
- Tipo de operação: `register` | `login` | `logout` | `refresh_token` | `reset_password`
- Dados do usuário (quando aplicável)

## Ferramentas/Scripts
1. `execution/auth/auth_handler.py` — Operações de autenticação
2. `execution/auth/token_manager.py` — Geração e validação de tokens JWT
3. `execution/auth/password_handler.py` — Hash e validação de senhas

## Fluxos

### Registro
1. Validar dados de entrada (email, senha, nome)
2. Verificar se email já existe
3. Hash da senha
4. Criar usuário no banco
5. Gerar token JWT
6. Enviar email de confirmação

### Login
1. Validar credenciais
2. Verificar senha com hash
3. Gerar par de tokens (access + refresh)
4. Retornar tokens

### Refresh Token
1. Validar refresh token
2. Verificar se não está revogado
3. Gerar novo par de tokens
4. Revogar token antigo

### Reset de Senha
1. Validar email
2. Gerar token temporário (30 min)
3. Enviar email com link de reset
4. Ao receber novo password, validar token e atualizar

## Outputs
- Tokens JWT (access + refresh)
- Status da operação
- Dados do usuário (sem senha)

## Segurança
- Senhas: bcrypt com salt rounds = 12
- Access Token: expira em 15 minutos
- Refresh Token: expira em 7 dias
- Rate limiting: máx 5 tentativas de login por minuto
- NUNCA logar senhas ou tokens em plain text

## Aprendizados
_Atualizar esta seção conforme descobrir edge cases_
