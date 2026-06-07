"""
⚠️ DEPRECATED - This module has been moved!

PDF QNA functionality has been reorganized into the pdf_reader module.

📍 New Location: pdf_reader/
  ├── reader.py        # PDFReader class
  ├── pdf_utils.py     # Helper functions
  ├── config.py        # Configuration
  └── __init__.py      # Exports

📖 Usage:
    from pdf_reader import PDFReader
    
    reader = PDFReader()
    status = reader.load_pdf("document.pdf")
    answer = reader.ask("Your question here")

🔗 For more info: See pdf_reader/README.md
"""

# Legacy import for backward compatibility
from pdf_reader import PDFReader

__all__ = ["PDFReader"]

