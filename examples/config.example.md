# Example configuration

A filled-in copy of the configuration table from `organizer_skill.md`, for a fictional household.
Copy this block into the skill file (or paste it alongside the skill when you launch your agent)
and replace the values with your own.

| Placeholder | Value |
|---|---|
| `[USER_PRIMARY_NAME]` | `Jordan Rivera` |
| `[SOURCE_MESSY_FOLDER]` | `C:\Users\jordan\Downloads` |
| `[DESTINATION_ROOT_FOLDER]` | `C:\Users\jordan\Downloads` |
| `[RELATIVES_FOLDER_NAME]` | `Family Docs` |
| `[KNOWN_PEOPLE]` | `Sam Rivera (brother); Dana Rivera (mother — also appears as "D. K. Rivera" on older documents); Alex Chen (roommate, lease co-signer)` |

## Notes that make runs go smoother

- **List known aliases up front.** The `[KNOWN_PEOPLE]` hints save a mid-run question when your mother's maiden name shows up on a decade-old certificate.
- **Same source and destination is fine.** The skill builds the clean tree beside the mess, then retires emptied folders into a holding folder for you to delete.
- **Mention your document "eras" if you have them.** For example: "I studied at North University 2018–2022, then South University 2023–." This helps version-detection put the right paperwork in `Current Docs` vs. archive folders.
- **Say what you want ignored.** e.g. "Leave my `game-mods/` folder untouched."
