# Diretiva: Setup do Projeto

## Objetivo
Configurar o ambiente de desenvolvimento do Synapsia SaaS do zero.

## Pré-requisitos
- Python 3.10+
- Node.js 18+ (para o frontend)
- Git instalado
- Arquivo `.env` configurado

## Inputs
- Tipo de ambiente: `development` | `staging` | `production`

## Ferramentas/Scripts
1. `execution/utils/config.py` — Carrega variáveis de ambiente
2. `execution/setup/init_project.py` — Inicializa dependências e estrutura

## Passos

### 1. Configurar ambiente Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Copiar `.env.example` para `.env` e preencher as variáveis necessárias.

### 3. Verificar instalação
Rodar `execution/setup/init_project.py` para validar que tudo está configurado.

## Outputs
- Ambiente virtual Python configurado
- Dependências instaladas
- Arquivo `.env` validado

## Casos de Borda
- Se `pip install` falhar, verificar versão do Python
- Em Windows, usar `.\venv\Scripts\activate` ao invés de `source`
- Se `.env` não existir, copiar de `.env.example`

## Aprendizados
_Atualizar esta seção conforme descobrir edge cases_
