import json
import pathlib
import re

import omegaup.api

CREDENTIALS_PATH = pathlib.Path.home() / ".config" / "omegaup" / "credentials.json"

_TOKEN_RE = re.compile(r'^[a-f0-9]{40}$')


def validate_format(token: str) -> tuple[bool, str]:
    """
    Returns (is_valid, error_message).
    error_message is empty string when valid.
    """
    token = token.strip()
    if not token:
        return False, "No ingresaste ningún token."

    # Detect likely token name vs actual token
    if ' ' in token or not all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in token):
        return False, (
            "Eso no parece un token válido. "
            "Copia el valor hexadecimal que aparece debajo del nombre del token, no el nombre."
        )

    if not re.match(r'^[a-f0-9]+$', token, re.IGNORECASE):
        return False, (
            "Eso parece el nombre del token, no el token en sí. "
            "En la página de OmegaUp, copia el valor que aparece debajo del nombre."
        )

    if len(token) != 40:
        return False, (
            f"El token debe tener exactamente 40 caracteres (el tuyo tiene {len(token)}). "
            "Asegúrate de copiarlo completo."
        )

    return True, ""


def verify_with_api(token: str) -> tuple[bool, str]:
    """
    Validates token against the OmegaUp API.
    Returns (is_valid, username_or_error_message).
    """
    try:
        client = omegaup.api.Client(api_token=token)
        session = client.session.currentSession()
        username = session.get('identity', {}).get('username', '') or session.get('user', {}).get('username', '')
        return True, username
    except Exception as e:
        msg = str(e).lower()
        if '401' in msg or 'unauthorized' in msg or 'invalid' in msg:
            return False, "Token inválido. Verifica que lo copiaste completo y que fue creado en OmegaUp."
        return False, f"No se pudo conectar con OmegaUp: {e}"


def save_token(token: str) -> None:
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_PATH, 'w') as f:
        json.dump({"api_token": token}, f)


def load_token() -> str | None:
    if not CREDENTIALS_PATH.exists():
        return None
    try:
        with open(CREDENTIALS_PATH) as f:
            return json.load(f).get("api_token")
    except Exception:
        return None


def delete_token() -> bool:
    """Returns True if credentials existed and were deleted."""
    if CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.unlink()
        return True
    return False


def get_client() -> omegaup.api.Client:
    """
    Returns an authenticated API client.
    Exits with an error message if no token is saved.
    """
    token = load_token()
    if not token:
        import sys
        print("Error: no has iniciado sesión. Ejecuta 'omegaup login' primero.")
        sys.exit(1)
    return omegaup.api.Client(api_token=token)
