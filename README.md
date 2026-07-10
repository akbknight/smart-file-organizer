# Smart File Organizer Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Safety: move--only](https://img.shields.io/badge/safety-move--only%2C%20never%20deletes-blue.svg)](#the-safety-model)
[![OCR](https://img.shields.io/badge/scanned%20PDFs-OCR%20supported-orange.svg)](#what-it-does)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Point an agent at ten years of Downloads chaos. Get back a clean, person-by-person document archive — every file read, renamed, and filed by what's actually inside it. Nothing deleted, ever.**

Most "file organizers" sort by extension and filename. That's why they fail: `result.pdf` tells you nothing, `scan0001.pdf` even less, and the prescription with a doctor's name in huge letters doesn't belong to the doctor. This skill makes the agent open every document, OCR the scanned ones, work out *what it is* and *whose it is*, and file it accordingly.

Distilled from organizing a real 100,000-file folder: every rule in the skill exists because skipping it caused a real mistake.

---

## What it does

| Capability | Meaning |
|---|---|
| **Deep scan + OCR** | Detects image-only PDFs and runs OCR so scans are classified by their contents, not their filenames |
| **Context-aware renaming** | `YYYY-MM-DD_DocumentType_Subject.ext`, using the date printed *inside* the document |
| **Entity resolution** | Routes by patient — not doctor. Applicant — not university. Account holder — not bank. A parent's name on your certificate doesn't make it their file |
| **Alias handling** | One person under two official names? One folder titled with both, filenames untouched |
| **Auto-routing** | Creates per-person subfolders on demand and files each document under its true owner |
| **Hash-verified dedup** | Byte-identical copies are found by checksum, the best-named original kept, and every copy tracked in a checklist |
| **Version awareness** | Five revisions of the same form? It reads all five, promotes the latest to `Current Docs`, archives the rest by date |
| **Full audit trail** | One log line per move (`source -> destination [reason]`), a review folder for anything uncertain, and a final count reconciliation |

## Quickstart

```bash
git clone https://github.com/<your-username>/smart-file-organizer.git
cd smart-file-organizer
python3 tools/preflight.py ~/Downloads   # check tooling + estimate OCR workload
```

1. Open **`organizer_skill.md`** and fill in the config table — your name, source folder, destination, and (optionally) known family members and their aliases. See [`examples/config.example.md`](examples/config.example.md) for a filled-in sample.
2. Load the skill into your agent framework of choice (drop it into your skills folder, or paste it as the task brief) and point it at the folder.
3. The agent scans first, shows you a summary, and asks its structural questions **in one batch** before moving anything.
4. When it finishes, read `_Organize_Log.txt` (every move), `_Needs_My_Review/` (the honest "I wasn't sure" pile), and `_For Deletion (Empty Folders)/` (retired empty shells — deleting is *your* job, by design).

### Prerequisites

- An agent framework that can execute a markdown skill with file and shell access (the skill is written framework-agnostic)
- **poppler-utils** (`pdftotext`, `pdftoppm`) — `apt-get install poppler-utils` / `brew install poppler`
- **tesseract-ocr** — `apt-get install tesseract-ocr` / `brew install tesseract`
- Python 3.8+ for the preflight script and office-file parsing

## Before / after

```
BEFORE                                      AFTER
Downloads/                                  Downloads/
├── scan0001.pdf                            ├── Jordan Rivera/
├── Doctor_s prescription.pdf               │   ├── Health Record/
├── IMG-4482 (1).pdf                        │   │   └── 2025-05-10_Prescription_Jordan Rivera (Dr Sharma).pdf
├── final_FINAL_lease v2 (dup 3).pdf        │   ├── Housing/
├── result.pdf                              │   │   └── 2025-09-12_Lease_3004 Oak St NW (signed).pdf
├── marksheet__1.pdf                        │   └── Education/
└── ...9,994 more                           │       └── 2020-07-13_Class 12 Marksheet_Jordan Rivera.pdf
                                            ├── Family Docs/
                                            │   └── Sam Rivera/
                                            │       └── Education/
                                            │           └── 2020-07-15_Class 12 Result_Sam Rivera.pdf
                                            ├── _Needs_My_Review/        ← uncertainties, listed with reasons
                                            ├── _For Deletion (Empty Folders)/
                                            └── _Organize_Log.txt        ← every single move
```

`result.pdf` turned out to be **Sam's** exam result, not Jordan's — the content said so, and the file went to Sam's folder. `Doctor_s prescription.pdf` had no patient name in the *filename*; OCR found it in the header. That's the difference between sorting names and reading documents.

## The safety model

| Guarantee | Enforced by |
|---|---|
| Nothing is deleted | Move-only operations; "deletable" items are parked in a holding folder for the user |
| Nothing is lost | Before/after file counts reconciled with identical scan rules |
| Nothing is guessed | Genuine two-folder conflicts stop and ask; unknowns go to `_Needs_My_Review` with reasons |
| Everything is traceable | Per-move logging, flushed immediately; interrupted runs resume without duplicating work |
| Code stays intact | Repositories and package folders move as sealed units — never reorganized internally |

## Repository layout

```
organizer_skill.md          The skill itself — config table, hard rules, 7-phase procedure
examples/config.example.md  A filled-in sample configuration
tools/preflight.py          Read-only readiness check: tooling, folder stats, OCR estimate
CONTRIBUTING.md             How to add document-type recipes and regional rules
LICENSE                     MIT
```

## FAQ

**Does my data leave my machine?**
The skill itself sends nothing anywhere — it's a procedure executed by whatever agent runtime *you* choose, on folders *you* point it at. Pick a runtime whose privacy posture you trust; documents this personal deserve that diligence.

**What happens to duplicates — does it delete them?**
Never. They're hash-verified, renamed `<original name> (copy N)`, and either quarantined with a checklist or filed beside their original (your choice, asked up front). Deleting is always your decision.

**What if it can't figure a file out?**
It says so. Unidentifiable files land in `_Needs_My_Review` with a one-line explanation each — no silent guessing.

**Will it reorganize my code projects?**
No. Repos move as intact units; exploded `node_modules` debris gets swept into one recovery folder rather than "sorted."

## Roadmap

- [ ] Document-type recipe library (region-specific forms, IDs, statements)
- [ ] Multi-language OCR presets
- [ ] Optional dry-run report mode (plan file, zero moves)
- [ ] Scheduled maintenance mode: keep an already-organized folder clean

## Contributing

Regional entity-resolution rules are the most wanted contribution — see [CONTRIBUTING.md](CONTRIBUTING.md). Never include real personal documents in issues or PRs.

## License

[MIT](LICENSE) © 2026 Akshay Kumar
