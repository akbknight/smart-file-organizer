# Contributing

Thanks for your interest in improving Smart File Organizer.

## What's most valuable

- **Entity-resolution rules for more regions.** Document conventions differ everywhere: relational name fields, transliteration variants, government form layouts. If the skill misidentifies a document type common in your country, open an issue with a *redacted or synthetic* example.
- **OCR guidance** for non-Latin scripts and mixed-language documents you have tested (Tesseract language packs, DPI settings that worked).
- **New document-type recipes:** how to recognize a type, where its date lives, what the subject field looks like.
- **Clarity fixes** to the skill text. If an agent misread an instruction, that's a bug in the instruction.

## Ground rules

1. **Never include real personal documents or data** in issues, PRs, or test fixtures. Use synthetic examples only.
2. Keep the skill framework-agnostic — no instructions that only work on one vendor's tooling.
3. The safety model is non-negotiable: move-only, log-everything, ask-on-conflict. PRs that weaken it will be declined.

## Process

1. Fork, branch from `main`.
2. Make your change; keep the skill file readable (it's meant to be read by humans *and* executed by agents).
3. Open a PR describing the failure mode you're fixing and how you verified the fix.
