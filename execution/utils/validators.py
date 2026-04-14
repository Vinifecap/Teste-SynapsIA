"""
validators.py — Validações comuns para o Synapsia SaaS.

Uso:
    from execution.utils.validators import validate_email, validate_password
    
    is_valid, error = validate_email("user@example.com")
    is_valid, errors = validate_password("MinhaSenh@123")
"""

import re
from typing import Optional, Tuple, List


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Valida um endereço de email.
    
    Args:
        email: Endereço de email para validar.
    
    Returns:
        Tupla (is_valid, error_message).
    """
    if not email or not email.strip():
        return False, "Email é obrigatório"
    
    email = email.strip().lower()
    
    # Regex básico para email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Formato de email inválido"
    
    if len(email) > 254:
        return False, "Email muito longo (máximo 254 caracteres)"
    
    return True, None


def validate_password(password: str) -> Tuple[bool, List[str]]:
    """
    Valida uma senha com critérios de segurança.
    
    Critérios:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    
    Args:
        password: Senha para validar.
    
    Returns:
        Tupla (is_valid, list_of_errors).
    """
    errors = []
    
    if not password:
        return False, ["Senha é obrigatória"]
    
    if len(password) < 8:
        errors.append("Senha deve ter pelo menos 8 caracteres")
    
    if len(password) > 128:
        errors.append("Senha muito longa (máximo 128 caracteres)")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Senha deve conter pelo menos 1 letra maiúscula")
    
    if not re.search(r'[a-z]', password):
        errors.append("Senha deve conter pelo menos 1 letra minúscula")
    
    if not re.search(r'\d', password):
        errors.append("Senha deve conter pelo menos 1 número")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]', password):
        errors.append("Senha deve conter pelo menos 1 caractere especial")
    
    return len(errors) == 0, errors


def validate_required_fields(data: dict, required: List[str]) -> Tuple[bool, List[str]]:
    """
    Verifica se todos os campos obrigatórios estão presentes e não vazios.
    
    Args:
        data: Dicionário com os dados.
        required: Lista de campos obrigatórios.
    
    Returns:
        Tupla (is_valid, list_of_missing_fields).
    """
    missing = []
    for field in required:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(f"Campo '{field}' é obrigatório")
    
    return len(missing) == 0, missing


def validate_string_length(
    value: str,
    field_name: str,
    min_len: int = 1,
    max_len: int = 255,
) -> Tuple[bool, Optional[str]]:
    """
    Valida o comprimento de uma string.
    
    Args:
        value: String para validar.
        field_name: Nome do campo (para mensagem de erro).
        min_len: Comprimento mínimo.
        max_len: Comprimento máximo.
    
    Returns:
        Tupla (is_valid, error_message).
    """
    if not value or len(value.strip()) < min_len:
        return False, f"{field_name} deve ter pelo menos {min_len} caracteres"
    
    if len(value) > max_len:
        return False, f"{field_name} deve ter no máximo {max_len} caracteres"
    
    return True, None


if __name__ == "__main__":
    # Testes rápidos
    print("=== Teste de Validação de Email ===")
    tests_email = ["user@test.com", "invalid", "", "a@b.c", "user@domain.com.br"]
    for email in tests_email:
        valid, err = validate_email(email)
        status = "✅" if valid else "❌"
        print(f"  {status} '{email}' → {err or 'OK'}")
    
    print("\n=== Teste de Validação de Senha ===")
    tests_pwd = ["123", "abcdefgh", "Abcdefg1!", "Aa1!aaaa"]
    for pwd in tests_pwd:
        valid, errs = validate_password(pwd)
        status = "✅" if valid else "❌"
        print(f"  {status} '{pwd}' → {errs or 'OK'}")
    
    print("\n=== Teste de Campos Obrigatórios ===")
    data = {"name": "João", "email": "", "age": None}
    valid, missing = validate_required_fields(data, ["name", "email", "age", "phone"])
    print(f"  {'✅' if valid else '❌'} Campos faltando: {missing}")
