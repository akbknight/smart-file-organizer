# Skill: Smart File Organizer

**Version:** 1.1.0
**Type:** Agent skill / operating procedure
**Purpose:** Deep-organize any messy folder of personal documents into a precise, person-centric folder structure — with content reading, OCR, deduplication, context-aware renaming, and entity resolution.

---

## Configuration

Fill these in before running. The agent must ask for any value that is missing.

| Placeholder | Meaning | Example |
|---|---|---|
| `[USER_PRIMARY_NAME]` | The owner of the documents. Their files form the main tree. | `Jordan Rivera` |
| `[SOURCE_MESSY_FOLDER]` | The folder to organize — **any folder, any name, new or old**: a Downloads dump, a Desktop, `D:\Old-Laptop-Backup`, a USB-stick copy, a network share. | `~/Downloads`, `E:\2019_backup\stuff` |
| `[DESTINATION_ROOT_FOLDER]` | Where the organized structure is built (may equal the source). | `~/Downloads` |
| `[RELATIVES_FOLDER_NAME]` | Folder for documents belonging to other people. | `Family Docs` |
| `[KNOWN_PEOPLE]` | Optional list of expected family/associates and known name aliases. | `Sam Rivera; Dana Rivera (a.k.a. D. K. Rivera)` |

**Scope is defined by the config, not by convention.** The skill operates *only* inside `[SOURCE_MESSY_FOLDER]` and `[DESTINATION_ROOT_FOLDER]` as the user gives them. Never assume a default location such as "Downloads," never substitute a folder the user didn't name, and never touch anything outside the configured paths. If the source folder isn't specified, **ask** — don't guess. The folder's name carries no meaning; classify by contents, not by what the folder is called.

---

## Hard Rules — never break these

1. **MOVE files only. NEVER delete any file.** Deletion decisions belong to the user. Anything that looks deletable (empty folder shells, junk artifacts) goes into a clearly named holding folder such as `_For Deletion (Empty Folders)` for the user to handle.
2. **NEVER create duplicate copies of a file.** If a file already exists at a destination name, add a ` (copy N)` or ` (2)` suffix — never write the same bytes twice.
3. **On a genuine conflict** (a file that plausibly belongs in two places), **stop and ask the user.** Do not guess. Do not copy it to both.
4. **Log every move** to `_Organize_Log.txt` at the destination root, in the form `MOVED  <source>  ->  <destination>  [reason]`. Directory-level moves may be logged as one line with a file count.
5. **Anything unidentifiable goes to `_Needs_My_Review`** — one flat folder plus a plain-text list explaining each item. Never invent a category to avoid admitting uncertainty.
6. **Skip the internals of code projects** (`node_modules`, `.git`, `dist`, `build`, `.next`, `vendor`, caches). Move a project as one intact unit. Never reorganize inside a repository.
7. **Do not create empty folders.** Create a subfolder only when a file is about to be placed in it. For people in `[RELATIVES_FOLDER_NAME]`, create only the category subfolders that person actually has documents for.
8. **Verify at the end.** File counts before and after must reconcile. Zero deletions, zero unexplained losses. Report any external changes detected (cloud sync and the user may add/remove files while you work).

---

## Phase 1 — Inventory

1. Recursively list the source, pruning code-project internals (rule 6) so the scan stays fast.
2. Produce a summary for the user before moving anything: total files, rough categories, obvious problem areas (duplicate storms, exploded package folders, mixed-owner documents).
3. Ask the user the *structural* questions now, in one batch — target layout, what to do with oddballs — not one interruption at a time.

## Phase 2 — Deduplicate

1. Group files by size first; hash (MD5 is fine for this purpose) only size-colliding groups.
2. Within each identical group, pick the canonical copy: prefer clean names over ones with `__1`, `_copy1`, `(dup 3)`, ` - Copy` markers; prefer copies already inside meaningful folder structure over flat-dump locations.
3. Route redundant copies per the user's chosen policy (holding folder, or beside the original as `<name> (copy N)`), and write a checklist mapping every copy to its kept original.

## Phase 3 — Read the content (never trust filenames alone)

For every file whose identity is not obvious from its name:

1. **Text-layer first:** extract text from page 1–2 (`pdftotext` or equivalent). Cheap and usually sufficient.
2. **OCR fallback — detect image-only PDFs:** if extraction returns (almost) no text, the PDF is a scan. Render page 1 to an image (`pdftoppm`) and run OCR (`tesseract`) to recover the text.
3. **Visual fallback:** if OCR output is garbled and the decision matters (identity documents, medical records, legal papers), render the page and have the agent read it visually.
4. Office files: read `docx/xlsx/pptx` content directly (unzip XML or use a library). **Run from a neutral working directory** — never from inside the messy folder, where stray files can shadow language modules.
5. Extract at minimum: **document type, subject (whose document it is), issue/registration date, issuer.**

## Phase 4 — Entity resolution (the part everyone gets wrong)

The person whose name is *biggest on the page* is often not the owner.

* **Patient vs. provider:** on medical documents, route by the **patient**, never the doctor, hospital, or lab on the letterhead. A prescription written by *Dr. H. Sharma* for *[USER_PRIMARY_NAME]* belongs to `[USER_PRIMARY_NAME]`.
* **Applicant vs. issuer:** certificates, visas, admissions and offers belong to the applicant/holder, not the institution.
* **Account holder vs. bank:** statements and balance certificates belong to the account holder printed on them — verify by reading, not by which folder they were found in.
* **Relational name fields:** many documents (especially South Asian ones) print a father's/mother's/spouse's name on someone else's certificate. A parent's name on a marksheet does **not** make it the parent's document.
* **New people, discovered dynamically:** don't rely on `[KNOWN_PEOPLE]` being complete. When a document's true subject is a person not yet seen, create their folder under `[RELATIVES_FOLDER_NAME]` on the spot — after sanity-checking the name is a real subject (not a provider, author, official, or an OCR misread). List every newly discovered person in the final report for the user to confirm.
* **Aliases:** one person may appear under different official names on different documents. If evidence suggests two names are the same person, **ask the user**; on confirmation, use one folder titled with both names — `Dana Rivera (D. K. Rivera)` style — and leave individual file names untouched so each file still matches the name printed on the physical document.
* **Multi-subject bundles:** a single PDF containing several people's documents (e.g., a family's bank certificates compiled as visa evidence) is routed by its *purpose*, not split arbitrarily — e.g., to the visa-evidence folder — with all subjects named in the filename.
* **Media metadata beats labels:** for DICOM/radiology discs, read the embedded patient tag rather than trusting the folder or zip name.

## Phase 5 — Rename

Standard format: `YYYY-MM-DD_DocumentType_Subject.ext`

* Date = the date **inside** the document (issue/registration/report date), not the file's modified time. If only a year is known, use `YYYY_`. If no date is recoverable, lead with the document type.
* Add clarifiers in parentheses when useful: issuer, account, version — `2025-09-12_Lease_3004 Oak St (signed).pdf`.
* Version families (multiple visas, multiple I-20-style forms, revised leases): **read each one, identify the latest by its internal dates**, place the latest in the "current" folder and older ones in an archive folder, each named with its date/version.
* Bulk anonymous media (screenshots with GUID names) may keep their names inside a catch-all photos folder — renaming thousands of screenshots by content is a separate opt-in pass.

## Phase 6 — Route

1. `[USER_PRIMARY_NAME]`'s documents go into the main tree (Education / Identity / Immigration or Government / Work / Finance / Taxes / Health / Housing / Projects / Photos — adapt to the user's target structure).
2. Every other subject gets `[RELATIVES_FOLDER_NAME]/<Person Name>/` with only the subfolders they need, mirroring the main tree's category names.
3. New subjects discovered mid-run (a name on a document that isn't in `[KNOWN_PEOPLE]`) get a folder automatically — note them in the final report so the user can confirm they're real people, not entity-resolution mistakes.
4. Whole code projects → a Projects folder, moved intact. Exploded package debris (loose `node_modules` remains) → one clearly named recovery folder, moved wholesale, never individually sorted.

## Phase 7 — Close out

1. Move now-empty legacy folders into the holding folder (rule 1). Never delete them yourself.
2. Re-count files with identical rules as Phase 1 and reconcile. Investigate every discrepancy before reporting; distinguish your own actions from external activity.
3. Final report: a per-folder count table, the "current vs. archived" decisions made for versioned documents, every item left in `_Needs_My_Review` with a one-line reason, every entity-resolution judgment call (aliases merged, misfiled documents corrected), and every newly discovered person.

## Operational notes

* Work in **resumable batches** with per-item logging flushed immediately — long runs get interrupted; a re-run must skip completed work instead of redoing or duplicating it.
* Set tight subprocess timeouts on text extraction and OCR (a single corrupt PDF must not stall the run); mark failures and fall back to visual reading.
* Use parallel workers for OCR only with per-worker temp file names.
* Treat the folder as **live**: the user's browser and cloud sync may add or remove files during the run. Verify against reality, not cached listings.
