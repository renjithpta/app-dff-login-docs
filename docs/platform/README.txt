AOBP Platform Architecture

The Markdown is the editable source; keep assets/ alongside it. This edition
uses the shared API convention in ../api-standards.md. The PDF is rebuilt from
the Markdown on US Letter pages; diagrams are high-resolution PNGs.

Run tools/build_diagrams.py and tools/build_pdfs.py from a full repository
checkout. The scripts/ files are compatibility entry points to those tools.
Dependencies: Python 3, ReportLab, PyMuPDF, Pillow and DejaVu Sans fonts.

This package is a design specification, not runnable application code.
Changes to paths require coordinated client, routing, security and API
implementation updates before deployment.
