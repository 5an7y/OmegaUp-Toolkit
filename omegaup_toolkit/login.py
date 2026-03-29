import getpass
import sys

from omegaup_toolkit import auth


def run_login():
    print("Para crear un API token, abre esta URL en tu navegador:")
    print()
    print("  https://omegaup.com/profile/#manage-api-tokens")
    print()
    print("Crea un nuevo token, copia el valor hexadecimal (no el nombre)")
    print("y pégalo aquí.")
    print()

    existing = auth.load_token()
    if existing:
        answer = input("Ya tienes una sesión guardada. ¿Reemplazarla? (Y/N) ").strip().upper()
        if answer != 'Y':
            print("Login cancelado.")
            return

    # Retry loop for format errors
    while True:
        token = getpass.getpass("Token: ").strip()

        valid_format, fmt_error = auth.validate_format(token)
        if not valid_format:
            print(f"\nError: {fmt_error}")
            retry = input("¿Intentar de nuevo? (Y/N) ").strip().upper()
            if retry != 'Y':
                sys.exit(1)
            continue

        print("Verificando token con OmegaUp...")
        valid_api, result = auth.verify_with_api(token)
        if not valid_api:
            print(f"\nError: {result}")
            retry = input("¿Intentar de nuevo? (Y/N) ").strip().upper()
            if retry != 'Y':
                sys.exit(1)
            continue

        # Success
        auth.save_token(token)
        username = result if result else "desconocido"
        print(f"\n✓ Autenticado como @{username}")
        print(f"  Credenciales guardadas en {auth.CREDENTIALS_PATH}")
        break


def run_logout():
    deleted = auth.delete_token()
    if deleted:
        print("Sesión cerrada. Credenciales eliminadas.")
    else:
        print("No había ninguna sesión guardada.")
