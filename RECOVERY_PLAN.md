# 🛡️ Recovery & Security Plan

This document outlines how to restore your development environment and manage your secrets securely.

## 💾 Restoring from Backup
If you accidentally lose your `.env` or need to restore a previous state:

1.  **Locate Backups**:
    - Local: `secrets_backup/` (ignored by Git)
    - Desktop: Look for files named `env_backup_YYYYMMDD_HHMMSS.txt` on your Desktop.
2.  **Restore .env**:
    ```powershell
    Copy-Item "secrets_backup\.env.backup_TIMESTAMP" ".env"
    ```
3.  **Restore Database**:
    If you need to restore the SQLite data:
    ```powershell
    Copy-Item "backups\db_backup_TIMESTAMP.sqlite3" "db.sqlite3"
    ```

## 🔄 Rotating Secrets
After your friend finishes hosting or if you suspect a leak:
1.  **Generate new Django SECRET_KEY**:
    Use a tool like `https://djecrety.ir/` or generate via Python:
    ```python
    import secrets; print(secrets.token_urlsafe(50))
    ```
2.  **Update Cloudinary/API Keys**:
    Log in to the respective dashboards (Cloudinary, Africa's Talking, M-Pesa) and regenerate the API keys.
3.  **Update .env**: Update the local `.env` with the new values.

## 🌍 Separate Dev vs Prod Credentials
- **Local Dev**: Use `USE_SQLITE=True` and a development `SECRET_KEY`.
- **Production**: Use `USE_SQLITE=False`, a production `SECRET_KEY`, and a real database (PostgreSQL/MySQL).

## 🔒 Sharing Secrets Securely
**DO NOT** send secrets via Email, WhatsApp, or Git. Use one of these methods:
1.  **Password Manager**: Share a vault (e.g., Bitwarden, LastPass).
2.  **Encrypted Text**: Use a "burn-after-reading" service like `1Password's Psst!` or `Bitwarden Send`.
3.  **Encrypted File**: Create an encrypted ZIP or use GPG to encrypt the `.env` file before sending.
    ```powershell
    # Windows built-in encryption (if available)
    Cipher /E ".env"
    ```

## 🚀 Pushing to a Private GitHub Repo
1.  **Create a New Private Repo** on GitHub (e.g., `swms-private`).
2.  **Add the Remote**:
    ```bash
    git remote add production https://github.com/yourusername/swms-private.git
    ```
3.  **Push the Clean Branch**:
    ```bash
    git push -u production deploy-clean:main
    ```
    *This pushes your local `deploy-clean` branch to the `main` branch of the new private repository.*
