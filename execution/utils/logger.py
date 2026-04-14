"""
logger.py — Sistema de logging padronizado para o Synapsia SaaS.

Uso:
    from execution.utils.logger import get_logger
    logger = get_logger("meu_modulo")
    logger.info("Operação concluída com sucesso")
    logger.error("Falha na operação", extra={"request_id": "abc-123"})
"""

import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


class SynapsiaFormatter(logging.Formatter):
    """Formatador customizado para logs do Synapsia."""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Verde
        "WARNING": "\033[33m",   # Amarelo
        "ERROR": "\033[31m",     # Vermelho
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors
    
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname
        
        # Request ID (se disponível)
        request_id = getattr(record, "request_id", None)
        rid_str = f" [{request_id}]" if request_id else ""
        
        if self.use_colors:
            color = self.COLORS.get(level, "")
            formatted = f"{timestamp} {color}{level:8s}{self.RESET}{rid_str} [{record.name}] {record.getMessage()}"
        else:
            formatted = f"{timestamp} {level:8s}{rid_str} [{record.name}] {record.getMessage()}"
        
        # Incluir exceção se houver
        if record.exc_info and record.exc_info[0]:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


def get_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Cria e retorna um logger configurado.
    
    Args:
        name: Nome do módulo/componente.
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Se None, usa LOG_LEVEL do ambiente ou INFO.
        log_file: Caminho para arquivo de log. Se None, loga apenas no console.
    
    Returns:
        Logger configurado.
    """
    import os
    
    if level is None:
        level = os.environ.get("LOG_LEVEL", "INFO")
    
    logger = logging.getLogger(f"synapsia.{name}")
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Handler para console (com cores)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(SynapsiaFormatter(use_colors=True))
    logger.addHandler(console_handler)
    
    # Handler para arquivo (sem cores)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(SynapsiaFormatter(use_colors=False))
        logger.addHandler(file_handler)
    
    return logger


def generate_request_id() -> str:
    """Gera um ID único para rastreamento de requisições."""
    return str(uuid.uuid4())[:8]


if __name__ == "__main__":
    # Demo do logger
    logger = get_logger("demo", level="DEBUG")
    rid = generate_request_id()
    
    logger.debug("Mensagem de debug")
    logger.info("Sistema iniciado com sucesso")
    logger.warning("Memória acima de 80%%")
    logger.error("Falha ao conectar no banco", extra={"request_id": rid})
    logger.critical("Sistema indisponível")
