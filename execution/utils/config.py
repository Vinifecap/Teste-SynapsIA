"""
config.py — Carregamento de configuração a partir de variáveis de ambiente.

Uso:
    from execution.utils.config import get_config
    config = get_config()
    db_url = config.get("DATABASE_URL")
"""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None) -> dict:
    """
    Carrega variáveis de ambiente de um arquivo .env.
    
    Args:
        env_path: Caminho para o arquivo .env. Se None, procura na raiz do projeto.
    
    Returns:
        Dicionário com as variáveis carregadas.
    """
    if env_path is None:
        # Procurar .env na raiz do projeto (2 níveis acima de execution/utils/)
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / ".env"
    else:
        env_path = Path(env_path)
    
    env_vars = {}
    
    if not env_path.exists():
        print(f"⚠️  Arquivo .env não encontrado em: {env_path}")
        print("   Copie .env.example para .env e configure as variáveis.")
        return env_vars
    
    with open(env_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Ignorar linhas vazias e comentários
            if not line or line.startswith("#"):
                continue
            
            # Separar chave=valor
            if "=" not in line:
                print(f"⚠️  Linha {line_num} ignorada (formato inválido): {line}")
                continue
            
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            
            # Remover aspas se presentes
            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            
            env_vars[key] = value
            os.environ[key] = value
    
    return env_vars


def get_config() -> dict:
    """
    Retorna a configuração completa do projeto.
    Combina variáveis do .env com variáveis de ambiente do sistema.
    
    Returns:
        Dicionário com toda a configuração.
    """
    # Carregar .env primeiro
    env_vars = load_env_file()
    
    # Configurações padrão
    defaults = {
        "APP_NAME": "Synapsia SaaS",
        "APP_ENV": "development",
        "APP_DEBUG": "true",
        "APP_PORT": "3000",
        "LOG_LEVEL": "INFO",
    }
    
    # Merge: defaults < .env < sistema
    config = {**defaults, **env_vars}
    
    # Sobrescrever com variáveis do sistema (se existirem)
    for key in config:
        sys_val = os.environ.get(key)
        if sys_val is not None:
            config[key] = sys_val
    
    return config


def require_env(key: str) -> str:
    """
    Obtém uma variável de ambiente obrigatória.
    Lança exceção se não estiver definida.
    
    Args:
        key: Nome da variável de ambiente.
    
    Returns:
        Valor da variável.
    
    Raises:
        EnvironmentError: Se a variável não estiver definida.
    """
    value = os.environ.get(key)
    if value is None:
        raise EnvironmentError(
            f"❌ Variável de ambiente obrigatória não definida: {key}\n"
            f"   Adicione {key}=<valor> ao arquivo .env"
        )
    return value


if __name__ == "__main__":
    # Teste rápido
    config = get_config()
    print("📋 Configuração carregada:")
    for key, value in sorted(config.items()):
        # Mascarar valores sensíveis
        if any(s in key.lower() for s in ["secret", "password", "token", "key"]):
            display = value[:4] + "****" if len(value) > 4 else "****"
        else:
            display = value
        print(f"   {key} = {display}")
