AOBP Platform Architecture - version 2.3
2 November 2026

Start with AOBP_Platform_Architecture_Design.pdf for the formatted document.
The Markdown file is the editable source. Keep assets/ alongside it so its
seven relative PNG image links resolve. PDF narrative pages are A4; diagram
plates use A3 landscape for readable printed labels and high-resolution zoom.

The 23 original main sections are retained. The selected browser business
route is ALB -> Spring Cloud API Gateway -> Spring Boot BFF -> private APIs.
Static assets and machine integrations have distinct documented routes.
Proposed sizes, lifetimes and recovery choices require implementation testing.
This package is an architecture specification, not runnable application code.

assets/ contains seven PNG diagrams, each 3200 pixels wide.
scripts/ contains diagram and PDF authoring sources. To regenerate, run from
this directory with Python, Pillow, ReportLab and DejaVu Sans fonts installed:
  python3 scripts/diagrams.py
  python3 scripts/build_pdf.py
The scripts expect deliverables under output/ in the authoring workspace;
place the Markdown and assets in output/ when reproducing the build.
