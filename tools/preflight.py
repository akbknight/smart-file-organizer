#!/usr/bin/env python3
"""Preflight check for Smart File Organizer.

Run this before launching the skill. It verifies the required tooling is
installed, sizes up the target folder, and estimates how much OCR work a
run will involve (by sampling PDFs for missing text layers).

Usage:
    python3 tools/preflight.py /path/to/messy/folder

No files are modified. Read-only, always.
"""
import os
import random
import shutil
import subprocess
import sys

PRUNE = {"node_modules", ".git", ".next", "dist", "build", "vendor",
         "__pycache__", ".venv", ".pytest_cache"}
DOC_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
           ".jpg", ".jpeg", ".png", ".heic", ".webp", ".txt", ".csv", ".eml"}
SAMPLE_SIZE = 25


def check_tool(name, hint):
    path = shutil.which(name)
    status = "OK " if path else "MISSING"
    print(f"  [{status}] {name:<10} {'-> ' + path if path else '   install: ' + hint}")
    return bool(path)


def is_image_only_pdf(path):
    """True if the first two pages carry (almost) no extractable text."""
    try:
        out = subprocess.run(["pdftotext", "-f", "1", "-l", "2", path, "-"],
                             capture_output=True, timeout=10).stdout
        return len(out.decode("utf-8", "replace").strip()) < 40
    except Exception:
        return None  # unreadable / timed out


def walk_stats(root):
    total, docs, pdfs, dup_marked = 0, 0, [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE]
        for f in filenames:
            total += 1
            ext = os.path.splitext(f)[1].lower()
            if ext in DOC_EXT:
                docs += 1
            if ext == ".pdf":
                pdfs.append(os.path.join(dirpath, f))
            stem = f.lower()
            if "__1" in stem or "_copy" in stem or "(dup" in stem or "- copy" in stem:
                dup_marked += 1
    return total, docs, pdfs, dup_marked


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__)
        sys.exit(1)
    root = sys.argv[1]

    print("Tooling:")
    have_poppler = check_tool("pdftotext", "poppler-utils")
    check_tool("pdftoppm", "poppler-utils")
    have_tess = check_tool("tesseract", "tesseract-ocr")

    print(f"\nScanning {root} (code-project internals skipped) ...")
    total, docs, pdfs, dup_marked = walk_stats(root)
    print(f"  files total:              {total:>8,}")
    print(f"  document-type files:      {docs:>8,}")
    print(f"  PDFs:                     {len(pdfs):>8,}")
    print(f"  duplicate-marked names:   {dup_marked:>8,}   (__1 / _copy / (dup n) / - Copy)")

    if pdfs and have_poppler:
        sample = random.sample(pdfs, min(SAMPLE_SIZE, len(pdfs)))
        image_only = sum(1 for p in sample if is_image_only_pdf(p))
        pct = 100 * image_only / len(sample)
        print(f"\nOCR estimate (sample of {len(sample)} PDFs):")
        print(f"  image-only (need OCR):    {image_only}/{len(sample)}  (~{pct:.0f}%)")
        if image_only and not have_tess:
            print("  -> install tesseract before running, or scanned PDFs cannot be classified.")
    print("\nPreflight complete. Nothing was modified.")


if __name__ == "__main__":
    main()
