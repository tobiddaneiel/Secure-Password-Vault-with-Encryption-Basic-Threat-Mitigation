# Secure Password Vault with Encryption & Basic Threat Mitigation

## Project Overview

This project is a simple yet secure password vault application that enables users to safely store their credentials. It uses strong encryption standards and basic threat mitigation techniques to protect sensitive data. The vault can be implemented as a command-line tool or a minimal web app.

---

## Features and Implementation Details

### 1. Secure Credential Storage
- Credentials are stored encrypted at rest using **AES-256** symmetric encryption.
- The encryption key is derived securely from a user-supplied master password using industry-standard key derivation functions such as **PBKDF2**, **bcrypt**, or **Argon2**.
- Data is never stored or handled in plaintext on disk.

### 2. Access Control
- Access to the vault requires the master password.
- The vault decrypts the stored credentials only after successful authentication.
- Decryption occurs only in memory during the session to reduce exposure.

### 3. Intrusion Detection and Mitigation
- The system logs all failed login attempts to a local log file.
- After a configurable number of failed attempts (e.g., 3), the vault temporarily locks access to prevent brute-force attacks.

### 4. User Interface
- Basic Command-Line Interface (CLI) to add, retrieve, and delete credentials.
- Optionally, a lightweight web interface can be provided for ease of use.

### 5. Testing & Documentation
- Comprehensive unit tests cover encryption, decryption, access control, and logging functionality.
- The README contains detailed usage instructions, security considerations, and known limitations.

---

## Getting Started

### Prerequisites
- Python 3.7+ or Node.js (depending on implementation choice)
- Required libraries:
  - For Python: `cryptography`, `bcrypt`/`argon2-cffi`, `pytest` (for testing)
  - For Node.js: `crypto`, `bcrypt`, testing frameworks like `jest`

### Installation
1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/password-vault.git
   cd password-vault
