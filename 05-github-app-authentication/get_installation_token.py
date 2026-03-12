"""
GitHub App Authentication Demo

Este script demuestra cómo autenticarse contra la API de GitHub
usando una GitHub App en lugar de un Personal Access Token.

Uso:
    python get_installation_token.py

Requiere:
    - PyJWT
    - cryptography
    - requests
    - python-dotenv
"""

import os
import sys
import time
import json
from datetime import datetime, timezone

import jwt
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_APP_INSTALLATION_ID = os.getenv("GITHUB_APP_INSTALLATION_ID")
GITHUB_APP_PRIVATE_KEY_PATH = os.getenv("GITHUB_APP_PRIVATE_KEY_PATH", "./github-app.pem")
GITHUB_ORG = os.getenv("GITHUB_ORG")

BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"


def load_private_key(key_path: str) -> str:
    """Carga la clave privada desde un archivo .pem"""
    # Si es ruta relativa, buscar desde el directorio del script
    if not os.path.isabs(key_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, key_path)
        
        # Si no existe, buscar en el directorio padre
        if not os.path.exists(key_path):
            parent_dir = os.path.dirname(script_dir)
            key_path = os.path.join(parent_dir, os.path.basename(GITHUB_APP_PRIVATE_KEY_PATH))
    
    if not os.path.exists(key_path):
        print(f"❌ Error: No se encontró la clave privada en: {key_path}")
        print("   Descarga la clave desde la configuración de tu GitHub App")
        print("   y guárdala como 'github-app.pem' en la raíz del proyecto.")
        sys.exit(1)
    
    with open(key_path, "r") as f:
        return f.read()


def generate_jwt(app_id: str, private_key: str) -> str:
    """
    Genera un JWT firmado para autenticarse como GitHub App.
    
    El JWT tiene una validez máxima de 10 minutos según la documentación de GitHub.
    """
    now = int(time.time())
    
    payload = {
        # Issued at time (60 segundos en el pasado para evitar problemas de clock drift)
        "iat": now - 60,
        # Expiration time (máximo 10 minutos)
        "exp": now + (10 * 60),
        # GitHub App ID
        "iss": app_id
    }
    
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


def get_installation_token(jwt_token: str, installation_id: str) -> dict:
    """
    Obtiene un installation access token usando el JWT.
    
    El token de instalación tiene una validez de 1 hora y es el que
    se usa para hacer llamadas a la API en nombre de la App instalada.
    """
    url = f"{BASE_URL}/app/installations/{installation_id}/access_tokens"
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code != 201:
        print(f"❌ Error al obtener el installation token: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        sys.exit(1)
    
    return response.json()


def test_authentication(token: str) -> dict:
    """Prueba el token obteniendo información del usuario/app autenticado"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION
    }
    
    # Las GitHub Apps no tienen /user, usamos /app
    response = requests.get(f"{BASE_URL}/app", headers=headers)
    
    if response.status_code == 401:
        # Si falla con /app, intentar con el installation token que sí tiene acceso a repos
        response = requests.get(f"{BASE_URL}/installation/repositories", headers=headers)
    
    return response.json() if response.status_code == 200 else {"error": response.text}


def get_org_repos(token: str, org: str) -> list:
    """Lista los repositorios de una organización"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION
    }
    
    response = requests.get(f"{BASE_URL}/orgs/{org}/repos", headers=headers, params={"per_page": 10})
    
    if response.status_code != 200:
        print(f"⚠️  No se pudieron obtener los repos: {response.status_code}")
        return []
    
    return response.json()


def get_code_scanning_alerts(token: str, org: str, repo: str) -> list:
    """Obtiene las alertas de code scanning de un repositorio"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION
    }
    
    url = f"{BASE_URL}/repos/{org}/{repo}/code-scanning/alerts"
    response = requests.get(url, headers=headers, params={"per_page": 5})
    
    if response.status_code == 404:
        return {"message": "Code scanning no habilitado o sin alertas"}
    elif response.status_code != 200:
        return {"error": f"Status {response.status_code}: {response.text}"}
    
    return response.json()


def main():
    """Función principal"""
    print("=" * 60)
    print("🔐 GitHub App Authentication Demo")
    print("=" * 60)
    
    # Validar configuración
    if not GITHUB_APP_ID:
        print("❌ Error: GITHUB_APP_ID no está configurado en .env")
        sys.exit(1)
    
    if not GITHUB_APP_INSTALLATION_ID:
        print("❌ Error: GITHUB_APP_INSTALLATION_ID no está configurado en .env")
        sys.exit(1)
    
    print(f"\n📋 Configuración:")
    print(f"   App ID: {GITHUB_APP_ID}")
    print(f"   Installation ID: {GITHUB_APP_INSTALLATION_ID}")
    print(f"   Organización: {GITHUB_ORG or '(no configurada)'}")
    
    # Paso 1: Cargar la clave privada
    print(f"\n🔑 Paso 1: Cargando clave privada...")
    private_key = load_private_key(GITHUB_APP_PRIVATE_KEY_PATH)
    print("   ✅ Clave privada cargada correctamente")
    
    # Paso 2: Generar JWT
    print(f"\n🎫 Paso 2: Generando JWT...")
    jwt_token = generate_jwt(GITHUB_APP_ID, private_key)
    print(f"   ✅ JWT generado (válido por 10 minutos)")
    print(f"   JWT: {jwt_token[:50]}...")
    
    # Paso 3: Obtener installation token
    print(f"\n🔓 Paso 3: Obteniendo installation access token...")
    token_response = get_installation_token(jwt_token, GITHUB_APP_INSTALLATION_ID)
    installation_token = token_response["token"]
    expires_at = token_response["expires_at"]
    
    print(f"   ✅ Installation token obtenido")
    print(f"   Token: {installation_token[:20]}...")
    print(f"   Expira: {expires_at}")
    
    # Mostrar el token completo para usar en .http
    print(f"\n" + "=" * 60)
    print("📋 TOKEN PARA USAR EN REST CLIENT O POSTMAN:")
    print("=" * 60)
    print(f"\n{installation_token}\n")
    print("=" * 60)
    
    # Paso 4: Probar el token
    print(f"\n🧪 Paso 4: Probando el token...")
    
    if GITHUB_ORG:
        repos = get_org_repos(installation_token, GITHUB_ORG)
        if repos:
            print(f"   ✅ Acceso confirmado. Repositorios visibles: {len(repos)}")
            for repo in repos[:5]:
                print(f"      - {repo['name']}")
            
            # Intentar obtener alertas del primer repo
            if repos:
                first_repo = repos[0]["name"]
                print(f"\n🔍 Paso 5: Consultando alertas de code scanning en '{first_repo}'...")
                alerts = get_code_scanning_alerts(installation_token, GITHUB_ORG, first_repo)
                
                if isinstance(alerts, list):
                    print(f"   ✅ Alertas encontradas: {len(alerts)}")
                    for alert in alerts[:3]:
                        print(f"      - [{alert.get('state', 'unknown')}] {alert.get('rule', {}).get('description', 'Sin descripción')[:50]}")
                else:
                    print(f"   ℹ️  {alerts.get('message', alerts)}")
        else:
            print("   ⚠️  No se encontraron repositorios")
    else:
        print("   ⚠️  GITHUB_ORG no configurado, saltando prueba de repos")
    
    print(f"\n✅ ¡Demo completada!")
    print(f"   Usa el token de arriba en el archivo ghas-api.http")
    print(f"   Recuerda: el token expira en 1 hora ({expires_at})")


if __name__ == "__main__":
    main()
