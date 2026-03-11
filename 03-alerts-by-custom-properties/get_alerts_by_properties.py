"""
GHAS Alerts by Custom Properties

Script que obtiene alertas de GitHub Advanced Security (GHAS) filtradas
por custom properties de los repositorios.

Uso:
    python get_alerts_by_properties.py --property environment --value production
    python get_alerts_by_properties.py --property team --value backend --state open
    python get_alerts_by_properties.py --property environment --value production --output json
"""

import argparse
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (busca en el directorio actual y padre)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"


def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN no está configurado en .env")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
    }


def handle_rate_limit(response):
    """Espera si estamos cerca del rate limit."""
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    if remaining == 0:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait_seconds = max(reset_time - int(time.time()), 1)
        print(f"⏳ Rate limit alcanzado. Esperando {wait_seconds}s...")
        time.sleep(wait_seconds)


def paginated_get(url, params=None):
    """GET con paginación automática."""
    headers = get_headers()
    all_items = []
    params = params or {}
    params["per_page"] = 100

    while url:
        response = requests.get(url, headers=headers, params=params)
        handle_rate_limit(response)

        if response.status_code != 200:
            print(f"⚠️  Error {response.status_code} al consultar {url}")
            print(f"   {response.json().get('message', 'Sin mensaje')}")
            break

        all_items.extend(response.json())

        # Siguiente página
        url = response.links.get("next", {}).get("url")
        params = {}  # Los params ya van en la URL de la siguiente página

    return all_items


def get_repos_by_properties(org, properties):
    """Obtiene repos que cumplen un filtro de custom properties."""
    query_parts = [f"props.{name}:{value}" for name, value in properties]
    query = " ".join(query_parts)

    print(f"🔍 Buscando repos con: {query}")

    items = paginated_get(
        f"{BASE_URL}/orgs/{org}/properties/values",
        params={"repository_query": query},
    )

    repo_names = [item["repository_full_name"].split("/")[-1] for item in items]
    print(f"   Encontrados: {len(repo_names)} repos")
    return repo_names


def get_code_scanning_alerts(org, repo, state="open"):
    """Obtiene alertas de code scanning de un repo."""
    return paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/code-scanning/alerts",
        params={"state": state},
    )


def get_secret_scanning_alerts(org, repo, state="open"):
    """Obtiene alertas de secret scanning de un repo."""
    return paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/secret-scanning/alerts",
        params={"state": state},
    )


def get_dependabot_alerts(org, repo, state="open"):
    """Obtiene alertas de Dependabot de un repo."""
    return paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/dependabot/alerts",
        params={"state": state},
    )


def get_all_alerts(org, repos, state="open"):
    """Obtiene todas las alertas de GHAS para una lista de repos."""
    results = {}

    for i, repo in enumerate(repos, 1):
        print(f"\n📦 [{i}/{len(repos)}] Obteniendo alertas de: {repo}")
        repo_alerts = {
            "code_scanning": [],
            "secret_scanning": [],
            "dependabot": [],
        }

        # Code Scanning
        alerts = get_code_scanning_alerts(org, repo, state)
        repo_alerts["code_scanning"] = [
            {
                "number": a.get("number"),
                "rule": a.get("rule", {}).get("id", "N/A"),
                "severity": a.get("rule", {}).get("severity", "N/A"),
                "description": a.get("rule", {}).get("description", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at"),
                "tool": a.get("tool", {}).get("name", "N/A"),
            }
            for a in alerts
        ]

        # Secret Scanning
        alerts = get_secret_scanning_alerts(org, repo, state)
        repo_alerts["secret_scanning"] = [
            {
                "number": a.get("number"),
                "secret_type": a.get("secret_type_display_name", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at"),
                "push_protection_bypassed": a.get("push_protection_bypassed", False),
            }
            for a in alerts
        ]

        # Dependabot
        alerts = get_dependabot_alerts(org, repo, state)
        repo_alerts["dependabot"] = [
            {
                "number": a.get("number"),
                "package": a.get("dependency", {})
                .get("package", {})
                .get("name", "N/A"),
                "ecosystem": a.get("dependency", {})
                .get("package", {})
                .get("ecosystem", "N/A"),
                "severity": a.get("security_vulnerability", {}).get(
                    "severity", "N/A"
                ),
                "summary": a.get("security_advisory", {}).get("summary", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at"),
            }
            for a in alerts
        ]

        results[repo] = repo_alerts

        cs = len(repo_alerts["code_scanning"])
        ss = len(repo_alerts["secret_scanning"])
        dep = len(repo_alerts["dependabot"])
        print(
            f"   Code Scanning: {cs} | Secret Scanning: {ss} | Dependabot: {dep}"
        )

    return results


def print_summary(results):
    """Imprime un resumen de las alertas en consola."""
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE ALERTAS")
    print("=" * 60)

    total_cs = total_ss = total_dep = 0

    for repo, alerts in results.items():
        cs = len(alerts["code_scanning"])
        ss = len(alerts["secret_scanning"])
        dep = len(alerts["dependabot"])
        total_cs += cs
        total_ss += ss
        total_dep += dep
        total = cs + ss + dep

        if total > 0:
            print(f"\n  📦 {repo}")
            if cs > 0:
                print(f"     🔍 Code Scanning:   {cs}")
            if ss > 0:
                print(f"     🔑 Secret Scanning: {ss}")
            if dep > 0:
                print(f"     📦 Dependabot:      {dep}")

    print(f"\n{'─' * 60}")
    print(f"  TOTAL: {total_cs + total_ss + total_dep} alertas")
    print(f"     🔍 Code Scanning:   {total_cs}")
    print(f"     🔑 Secret Scanning: {total_ss}")
    print(f"     📦 Dependabot:      {total_dep}")
    print(f"{'─' * 60}")


def main():
    parser = argparse.ArgumentParser(
        description="Obtener alertas de GHAS filtradas por custom properties"
    )
    parser.add_argument(
        "--property",
        action="append",
        required=True,
        help="Nombre del custom property (se puede usar múltiples veces)",
    )
    parser.add_argument(
        "--value",
        action="append",
        required=True,
        help="Valor del custom property (debe coincidir en orden con --property)",
    )
    parser.add_argument(
        "--state",
        default="open",
        choices=["open", "closed", "dismissed", "fixed"],
        help="Estado de las alertas (default: open)",
    )
    parser.add_argument(
        "--output",
        default="table",
        choices=["table", "json"],
        help="Formato de salida (default: table)",
    )

    args = parser.parse_args()

    if len(args.property) != len(args.value):
        print("❌ Error: Cada --property debe tener un --value correspondiente")
        sys.exit(1)

    org = os.getenv("GITHUB_ORG")
    if not org:
        print("❌ Error: GITHUB_ORG no está configurado en .env")
        sys.exit(1)

    properties = list(zip(args.property, args.value))

    # Paso 1: Obtener repos por custom properties
    repos = get_repos_by_properties(org, properties)

    if not repos:
        print("ℹ️  No se encontraron repos con esas properties")
        sys.exit(0)

    # Paso 2: Obtener alertas de cada repo
    results = get_all_alerts(org, repos, args.state)

    # Mostrar resultados
    if args.output == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
