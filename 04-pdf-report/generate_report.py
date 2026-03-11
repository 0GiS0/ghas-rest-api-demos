"""
GHAS PDF Report Generator

Genera un reporte PDF con las alertas de GitHub Advanced Security,
opcionalmente filtradas por custom properties.

Uso:
    python generate_report.py
    python generate_report.py --property environment --value production
    python generate_report.py --output mi-reporte.pdf
"""

import argparse
import os
import sys
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"


def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN no configurado en .env")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
    }


def handle_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    if remaining == 0:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait_seconds = max(reset_time - int(time.time()), 1)
        print(f"  Rate limit alcanzado. Esperando {wait_seconds}s...")
        time.sleep(wait_seconds)


def paginated_get(url, params=None):
    headers = get_headers()
    all_items = []
    params = params or {}
    params["per_page"] = 100

    while url:
        response = requests.get(url, headers=headers, params=params)
        handle_rate_limit(response)

        if response.status_code != 200:
            break

        all_items.extend(response.json())
        url = response.links.get("next", {}).get("url")
        params = {}

    return all_items


def get_repos_by_properties(org, properties):
    """Obtiene repos filtrados por custom properties."""
    query_parts = [f"props.{name}:{value}" for name, value in properties]
    query = " ".join(query_parts)

    items = paginated_get(
        f"{BASE_URL}/orgs/{org}/properties/values",
        params={"repository_query": query},
    )
    return [item["repository_full_name"].split("/")[-1] for item in items]


def get_org_repos(org):
    """Obtiene todos los repos de la org."""
    repos_data = paginated_get(f"{BASE_URL}/orgs/{org}/repos")
    return [r["name"] for r in repos_data]


def get_alerts_for_repo(org, repo, state="open"):
    """Obtiene todas las alertas de GHAS para un repo."""
    result = {"code_scanning": [], "secret_scanning": [], "dependabot": []}

    # Code Scanning
    for a in paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/code-scanning/alerts",
        params={"state": state},
    ):
        result["code_scanning"].append(
            {
                "number": a.get("number"),
                "rule": a.get("rule", {}).get("id", "N/A"),
                "severity": a.get("rule", {}).get("severity", "N/A"),
                "description": a.get("rule", {}).get("description", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at", "")[:10],
            }
        )

    # Secret Scanning
    for a in paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/secret-scanning/alerts",
        params={"state": state},
    ):
        result["secret_scanning"].append(
            {
                "number": a.get("number"),
                "secret_type": a.get("secret_type_display_name", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at", "")[:10],
            }
        )

    # Dependabot
    for a in paginated_get(
        f"{BASE_URL}/repos/{org}/{repo}/dependabot/alerts",
        params={"state": state},
    ):
        result["dependabot"].append(
            {
                "number": a.get("number"),
                "package": a.get("dependency", {})
                .get("package", {})
                .get("name", "N/A"),
                "severity": a.get("security_vulnerability", {}).get(
                    "severity", "N/A"
                ),
                "summary": a.get("security_advisory", {}).get("summary", "N/A"),
                "state": a.get("state"),
                "created_at": a.get("created_at", "")[:10],
            }
        )

    return result


# ── PDF Generation ──────────────────────────────────────────


class GHASReport(FPDF):
    def __init__(self, org, filters=None):
        super().__init__()
        self.org = org
        self.filters = filters or []

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(130, 130, 130)
            self.cell(
                0, 10, f"GHAS Report - {self.org}", align="L"
            )
            self.cell(0, 10, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cell(0, 10, f"Generated: {date_str}", align="C")

    def add_cover(self):
        self.add_page()
        self.ln(60)

        # Title
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(36, 41, 47)
        self.cell(0, 15, "GitHub Advanced Security", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(88, 96, 105)
        self.cell(0, 12, "Security Alerts Report", align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(20)

        # Org name
        self.set_font("Helvetica", "", 16)
        self.set_text_color(36, 41, 47)
        self.cell(0, 10, f"Organization: {self.org}", align="C", new_x="LMARGIN", new_y="NEXT")

        # Date
        self.set_font("Helvetica", "", 14)
        self.set_text_color(88, 96, 105)
        date_str = datetime.now().strftime("%B %d, %Y")
        self.cell(0, 10, date_str, align="C", new_x="LMARGIN", new_y="NEXT")

        # Filters
        if self.filters:
            self.ln(15)
            self.set_font("Helvetica", "I", 12)
            self.set_text_color(88, 96, 105)
            filter_str = ", ".join(
                [f"{name}={value}" for name, value in self.filters]
            )
            self.cell(
                0, 10, f"Filtered by: {filter_str}", align="C", new_x="LMARGIN", new_y="NEXT"
            )

    def add_summary(self, results):
        self.add_page()
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(36, 41, 47)
        self.cell(0, 12, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

        # Count totals
        total_cs = sum(len(r["code_scanning"]) for r in results.values())
        total_ss = sum(len(r["secret_scanning"]) for r in results.values())
        total_dep = sum(len(r["dependabot"]) for r in results.values())
        total = total_cs + total_ss + total_dep

        # Summary boxes
        self.set_font("Helvetica", "", 12)
        self.set_text_color(36, 41, 47)
        self.cell(0, 8, f"Total repositories analyzed: {len(results)}", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, f"Total alerts found: {total}", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

        # Alerts by type table
        self._add_section_title("Alerts by Type")
        col_widths = [80, 50, 50]
        headers = ["Alert Type", "Count", "% of Total"]
        self._table_header(col_widths, headers)

        pct_cs = f"{(total_cs / total * 100):.1f}%" if total > 0 else "0%"
        pct_ss = f"{(total_ss / total * 100):.1f}%" if total > 0 else "0%"
        pct_dep = f"{(total_dep / total * 100):.1f}%" if total > 0 else "0%"

        self._table_row(col_widths, ["Code Scanning", str(total_cs), pct_cs])
        self._table_row(col_widths, ["Secret Scanning", str(total_ss), pct_ss])
        self._table_row(col_widths, ["Dependabot", str(total_dep), pct_dep])
        self._table_row(
            col_widths, ["TOTAL", str(total), "100%"], bold=True
        )

        self.ln(10)

        # Severity breakdown (code scanning + dependabot)
        severities = {}
        for repo_alerts in results.values():
            for a in repo_alerts["code_scanning"]:
                sev = a.get("severity", "unknown")
                severities[sev] = severities.get(sev, 0) + 1
            for a in repo_alerts["dependabot"]:
                sev = a.get("severity", "unknown")
                severities[sev] = severities.get(sev, 0) + 1

        if severities:
            self._add_section_title("Alerts by Severity (Code Scanning + Dependabot)")
            col_widths_sev = [90, 90]
            self._table_header(col_widths_sev, ["Severity", "Count"])
            for sev in ["critical", "high", "medium", "low", "warning", "note", "unknown"]:
                if sev in severities:
                    self._table_row(
                        col_widths_sev,
                        [sev.capitalize(), str(severities[sev])],
                    )

    def add_repo_details(self, results):
        for repo, alerts in results.items():
            total = (
                len(alerts["code_scanning"])
                + len(alerts["secret_scanning"])
                + len(alerts["dependabot"])
            )
            if total == 0:
                continue

            self.add_page()
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(36, 41, 47)
            self.cell(0, 12, f"Repository: {repo}", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

            # Code Scanning
            if alerts["code_scanning"]:
                self._add_section_title(
                    f"Code Scanning ({len(alerts['code_scanning'])} alerts)"
                )
                col_widths = [15, 35, 25, 95]
                self._table_header(col_widths, ["#", "Rule", "Severity", "Description"])
                for a in alerts["code_scanning"][:50]:
                    desc = a["description"][:60] + ("..." if len(a["description"]) > 60 else "")
                    self._table_row(
                        col_widths,
                        [str(a["number"]), a["rule"][:20], a["severity"], desc],
                    )

            # Secret Scanning
            if alerts["secret_scanning"]:
                self.ln(5)
                self._add_section_title(
                    f"Secret Scanning ({len(alerts['secret_scanning'])} alerts)"
                )
                col_widths = [15, 80, 30, 45]
                self._table_header(col_widths, ["#", "Secret Type", "State", "Created"])
                for a in alerts["secret_scanning"][:50]:
                    self._table_row(
                        col_widths,
                        [
                            str(a["number"]),
                            a["secret_type"][:45],
                            a["state"],
                            a["created_at"],
                        ],
                    )

            # Dependabot
            if alerts["dependabot"]:
                self.ln(5)
                self._add_section_title(
                    f"Dependabot ({len(alerts['dependabot'])} alerts)"
                )
                col_widths = [15, 45, 25, 85]
                self._table_header(col_widths, ["#", "Package", "Severity", "Summary"])
                for a in alerts["dependabot"][:50]:
                    summary = a["summary"][:50] + ("..." if len(a["summary"]) > 50 else "")
                    self._table_row(
                        col_widths,
                        [
                            str(a["number"]),
                            a["package"][:25],
                            a["severity"],
                            summary,
                        ],
                    )

    def _add_section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(36, 41, 47)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def _table_header(self, col_widths, headers):
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(36, 41, 47)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, border=1, fill=True)
        self.ln()

    def _table_row(self, col_widths, values, bold=False):
        self.set_font("Helvetica", "B" if bold else "", 7)
        self.set_text_color(36, 41, 47)
        for i, value in enumerate(values):
            self.cell(col_widths[i], 6, str(value), border=1)
        self.ln()


def main():
    parser = argparse.ArgumentParser(
        description="Generar reporte PDF de alertas GHAS"
    )
    parser.add_argument(
        "--property", action="append", help="Custom property para filtrar"
    )
    parser.add_argument(
        "--value", action="append", help="Valor del custom property"
    )
    parser.add_argument(
        "--state", default="open", help="Estado de alertas (default: open)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Nombre del archivo PDF (default: ghas-report-YYYY-MM-DD.pdf)",
    )

    args = parser.parse_args()

    org = os.getenv("GITHUB_ORG")
    if not org:
        print("Error: GITHUB_ORG no configurado en .env")
        sys.exit(1)

    # Determinar repos a analizar
    properties = []
    if args.property and args.value:
        if len(args.property) != len(args.value):
            print("Error: Cada --property necesita un --value")
            sys.exit(1)
        properties = list(zip(args.property, args.value))
        print(f"Filtrando repos por: {properties}")
        repos = get_repos_by_properties(org, properties)
    else:
        print(f"Obteniendo todos los repos de {org}...")
        repos = get_org_repos(org)

    if not repos:
        print("No se encontraron repos")
        sys.exit(0)

    print(f"Analizando {len(repos)} repos...")

    # Obtener alertas
    results = {}
    for i, repo in enumerate(repos, 1):
        print(f"  [{i}/{len(repos)}] {repo}...")
        results[repo] = get_alerts_for_repo(org, repo, args.state)

    # Generar PDF
    output_file = args.output or f"ghas-report-{datetime.now().strftime('%Y-%m-%d')}.pdf"

    print(f"\nGenerando PDF: {output_file}")
    pdf = GHASReport(org, filters=properties)
    pdf.add_cover()
    pdf.add_summary(results)
    pdf.add_repo_details(results)
    pdf.output(output_file)

    print(f"Reporte generado: {output_file}")


if __name__ == "__main__":
    main()
