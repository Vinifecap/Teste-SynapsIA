"""
error_handler.py — Tratamento padronizado de erros para o Synapsia SaaS.

Uso:
    from execution.utils.error_handler import SynapsiaError, handle_error, create_error_response
    
    try:
        # operação
    except SynapsiaError as e:
        response = e.to_response()
    except Exception as e:
        response = handle_error(e, request_id="abc-123")
"""

import traceback
from typing import Optional, List
from execution.utils.logger import get_logger, generate_request_id

logger = get_logger("error_handler")


class SynapsiaError(Exception):
    """Erro base do Synapsia SaaS com suporte a respostas padronizadas."""
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: Optional[List[str]] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        self.request_id = request_id or generate_request_id()
    
    def to_response(self) -> dict:
        """Converte o erro em resposta padronizada."""
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "request_id": self.request_id,
            }
        }


class ValidationError(SynapsiaError):
    """Erro de validação (400)."""
    def __init__(self, message: str, details: Optional[List[str]] = None, **kwargs):
        super().__init__("VALIDATION_ERROR", message, 400, details, **kwargs)


class AuthenticationError(SynapsiaError):
    """Erro de autenticação (401)."""
    def __init__(self, message: str = "Credenciais inválidas", **kwargs):
        super().__init__("AUTHENTICATION_ERROR", message, 401, **kwargs)


class AuthorizationError(SynapsiaError):
    """Erro de autorização (403)."""
    def __init__(self, message: str = "Acesso negado", **kwargs):
        super().__init__("AUTHORIZATION_ERROR", message, 403, **kwargs)


class NotFoundError(SynapsiaError):
    """Recurso não encontrado (404)."""
    def __init__(self, resource: str = "Recurso", **kwargs):
        super().__init__("NOT_FOUND", f"{resource} não encontrado(a)", 404, **kwargs)


class RateLimitError(SynapsiaError):
    """Rate limit excedido (429)."""
    def __init__(self, message: str = "Muitas requisições. Tente novamente em instantes.", **kwargs):
        super().__init__("RATE_LIMIT_EXCEEDED", message, 429, **kwargs)


def handle_error(
    error: Exception,
    request_id: Optional[str] = None,
) -> dict:
    """
    Trata um erro genérico e retorna resposta padronizada.
    Loga o erro completo internamente, mas retorna mensagem genérica ao cliente.
    
    Args:
        error: Exceção capturada.
        request_id: ID da requisição para rastreamento.
    
    Returns:
        Dicionário com resposta de erro padronizada.
    """
    rid = request_id or generate_request_id()
    
    # Se for um erro do Synapsia, já tem formato
    if isinstance(error, SynapsiaError):
        error.request_id = rid
        logger.error(
            f"[{rid}] {error.code}: {error.message}",
            extra={"request_id": rid}
        )
        return error.to_response()
    
    # Erro genérico — logar detalhes internamente
    logger.error(
        f"[{rid}] Erro inesperado: {str(error)}\n{traceback.format_exc()}",
        extra={"request_id": rid}
    )
    
    # Retornar mensagem genérica ao cliente (NUNCA expor stack trace)
    return {
        "success": False,
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Ocorreu um erro interno. Tente novamente mais tarde.",
            "details": [],
            "request_id": rid,
        }
    }


def create_success_response(data: dict, message: str = "Operação realizada com sucesso") -> dict:
    """
    Cria resposta de sucesso padronizada.
    
    Args:
        data: Dados da resposta.
        message: Mensagem de sucesso.
    
    Returns:
        Dicionário com resposta de sucesso padronizada.
    """
    return {
        "success": True,
        "message": message,
        "data": data,
    }


if __name__ == "__main__":
    # Demo
    print("=== Demo Error Handler ===\n")
    
    # Erro de validação
    err = ValidationError("Dados inválidos", details=["Email é obrigatório", "Senha muito curta"])
    print("Validação:", err.to_response())
    
    # Erro genérico
    try:
        raise ValueError("algo deu errado internamente")
    except Exception as e:
        response = handle_error(e)
        print("\nErro genérico:", response)
    
    # Sucesso
    print("\nSucesso:", create_success_response({"user_id": 1, "name": "João"}))
