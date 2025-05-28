# HTML to PDF Report Framework

This repository contains an experimental framework for converting text content into styled HTML
reports, based on the "NPT" report design.

## Usage

The `generate_report.py` script converts a Markdown file into an HTML report using a simple
template. If the [WeasyPrint](https://weasyprint.org/) library is installed, a PDF will also be
produced.

```
python scripts/generate_report.py source.md -o output.html --title "My Report"
```

If the optional dependencies are unavailable, the script still creates the HTML file.

