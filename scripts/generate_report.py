#!/usr/bin/env python3
"""Simple report generator converting Markdown into styled HTML and optional PDF."""

from __future__ import annotations

import argparse
from pathlib import Path
from string import Template


def simple_markdown_to_html(text: str) -> str:
    """Very small subset of Markdown to HTML."""
    lines = text.splitlines()
    html_lines = []
    in_list = False
    for line in lines:
        if line.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        elif line.strip() == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{line.strip()}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate HTML report from Markdown")
    parser.add_argument("markdown", help="Markdown source file")
    parser.add_argument("-o", "--output", default="report.html", help="Output HTML file")
    parser.add_argument("--template", default="templates/base_template.html", help="Path to HTML template")
    parser.add_argument("--title", default="Report", help="Report title")
    parser.add_argument("--company", default="AI Forward Inc.", help="Company name")
    parser.add_argument("--client", default="Client", help="Client name")
    parser.add_argument("--date", default="2023", help="Report date")
    parser.add_argument("--section", default="Executive Summary", help="Section heading for first page")
    parser.add_argument("--page", default="01", help="Page number for first page")
    args = parser.parse_args()

    md_text = Path(args.markdown).read_text()
    try:
        import markdown  # type: ignore

        html_content = markdown.markdown(md_text)
    except Exception:
        html_content = simple_markdown_to_html(md_text)

    template_str = Path(args.template).read_text()
    template = Template(template_str)
    output_html = template.safe_substitute(
        title=args.title,
        company_name=args.company,
        report_title=args.title,
        subtitle="",
        client_name=args.client,
        date=args.date,
        section_name=args.section,
        content=html_content,
        page_number=args.page,
    )

    Path(args.output).write_text(output_html)
    print(f"Wrote {args.output}")

    # Attempt PDF generation with WeasyPrint if available
    try:
        from weasyprint import HTML

        pdf_file = Path(args.output).with_suffix(".pdf")
        HTML(args.output).write_pdf(pdf_file)
        print(f"Wrote {pdf_file}")
    except Exception as exc:  # ImportError or runtime failure
        print(f"PDF generation skipped: {exc}")


if __name__ == "__main__":
    main()
