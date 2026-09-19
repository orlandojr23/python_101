# 🎤 Group 1 - Complete Presentation Script
**IAS1 Module 9 | September 22, 2026**
**Members: OJ · Enzy · Angel · Andrey · Rodney · Harry**

---

## 👥 Assignment Overview

| Member | Part | What They Do |
|---|---|---|
| **OJ** (Leader) | Intro + Launch | Opens terminal, introduces the project, runs `python main.py` |
| **Enzy** | GUEST Demo | Demonstrates Guest role - shows access denials |
| **Angel** | EMPLOYEE Demo | Demonstrates Employee role - shows group-level access |
| **Andrey** | OWNER + Encryption | Demonstrates decryption sequence (the highlight of the demo) |
| **Rodney** | Audit Log + CIA Triad | Shows the live audit log, reads the CIA Triad justification |
| **Harry** | Checklist + Risk Analysis | Reads the audit checklist, presents the vulnerability and fix |

> [!IMPORTANT]
> Only **one person sits at the keyboard** at a time. Everyone else stands beside them. Pass the keyboard cleanly between parts.

---

## 🎬 FULL SCRIPT - Follow This Exactly

---

### 🟢 OJ - PART 1: Introduction (≈ 2 minutes)

**OJ stands at the front. Keyboard in hand.**

> *"Good [morning/afternoon], we are Group 1 - OJ, Enzy, Angel, Andrey, Rodney, and Harry.*
>
> *For our IAS1 Module 9 activity, we built a text-based console application in Python that simulates a Secure File Storage system called SECURE_STORAGE_LAB.*
>
> *Our application demonstrates three security principles: Role-Based Access Control or RBAC, the Principle of Least Privilege, and Encryption-at-Rest.*
>
> *We have three files in our storage: public.txt, internal.txt, and sensitive.txt - each with different access levels. Let me run the app now."*

**OJ opens the terminal and types:**
```
cd c:\Users\orlan\python_101\secure_storage_lab
python main.py
```

> *"The app launches and automatically creates our SECURE_STORAGE_LAB with all three files. You can see the startup message here."*

**OJ hands keyboard to Enzy.**

---

### 🔵 Enzy - PART 2: GUEST Role Demo (≈ 2 minutes)

**Enzy sits at keyboard. Main menu is visible on screen.**

> *"I'll now demonstrate the GUEST role - this simulates a random visitor with no account in our system."*

**Type:** `1` → Enter

> *"We're now logged in as Guest. You can see the file list and which files are accessible."*

**Type:** `1` → Enter *(public.txt)*

> *"public.txt - Guest can read this. It's a public notice, so availability is the priority. Anyone can access it."*

**Type:** `0` → Enter *(back)*, then `2` → Enter *(internal.txt)*

> *"internal.txt - watch what happens."*

*(Screen shows ACCESS DENIED)*

> *"ACCESS DENIED. Guest has no permission here. This is the Principle of Least Privilege in action - you only get what you absolutely need, nothing more."*

**Type:** `0` → Enter *(back)*, then `3` → Enter *(sensitive.txt)*

> *"And sensitive.txt?"*

*(Screen shows ACCESS DENIED again)*

> *"Denied again. Guest cannot touch sensitive data at all. Our RBAC system is working correctly."*

**Type:** `0` → Enter *(back to main menu)*

**Enzy hands keyboard to Angel.**

---

### 🟡 Angel - PART 3: EMPLOYEE Role Demo (≈ 2 minutes)

**Angel sits at keyboard. Main menu is visible.**

> *"Now I'll show the EMPLOYEE role - this is a staff member with higher clearance than a Guest."*

**Type:** `2` → Enter

> *"Logged in as Employee."*

**Type:** `1` → Enter *(public.txt)*

> *"Employee can still read public.txt - it's available to everyone."*

**Type:** `0` → Enter *(back)*, then `2` → Enter *(internal.txt)*

> *"internal.txt - this time..."*

*(Content displays)*

> *"Access granted. Employee can read internal documents. This is group-level access - only Employees and Owners can see this. Integrity is preserved because unauthorized users cannot read or tamper with internal records."*

**Type:** `0` → Enter *(back)*, then `3` → Enter *(sensitive.txt)*

> *"But sensitive.txt?"*

*(Screen shows ACCESS DENIED)*

> *"Still denied. Even an Employee cannot access the owner's sensitive data. Least Privilege means you only get exactly what your role requires - no more."*

**Type:** `0` → Enter *(back to main menu)*

**Angel hands keyboard to Andrey.**

---

### 🔴 Andrey - PART 4: OWNER + Encryption/Decryption (≈ 3 minutes)

> [!IMPORTANT]
> This is the most important part of the whole demo. Take it slow and dramatic.

**Andrey sits at keyboard. Main menu is visible.**

**Before logging in as Owner - show the raw encrypted file first:**

> *"Before I log in as Owner, I want to show you what sensitive.txt actually looks like on disk right now."*

**Open a second terminal (right-click taskbar → new terminal window) and type:**
```
type c:\Users\orlan\python_101\secure_storage_lab\SECURE_STORAGE_LAB\sensitive.txt
```

*(Screen shows scrambled ciphertext - gibberish)*

> *"This is what the file looks like sitting on your hard drive. Pure ciphertext - completely unreadable. Even if someone steals this file, they get nothing. That is encryption-at-rest."*

**Close or minimize the second terminal. Go back to the app.**

**Type:** `3` → Enter *(select OWNER)*

> *"Now I'll log in as Owner - the highest privilege role."*

**Type:** `3` → Enter *(select sensitive.txt)*

> *"The app asks for a decryption key. Let me try the wrong key first."*

**Type:** `hello123` → Enter

*(Screen shows: Wrong decryption key)*

> *"Even the Owner is blocked without the correct key. The file stays encrypted. Let me now enter the real key."*

**Type:** `IAS1-SecureOwner-2026` → Enter

*(Decrypted content displays on screen)*

> *"There it is. The sensitive data is now decrypted - but only in memory, only right now, only for the Owner. The file on disk is still encrypted. This is the complete encryption and decryption sequence."*

**Type:** `0` → Enter *(back to main menu)*

**Andrey hands keyboard to Rodney.**

---

### 🟣 Rodney - PART 5: Audit Log + CIA Triad (≈ 3 minutes)

**Rodney sits at keyboard. Main menu is visible.**

> *"Every access attempt we just made - successful or denied - has been automatically recorded. Let me show you our audit log."*

**Type:** `4` → Enter

*(Audit log displays with all the timestamped entries)*

> *"You can see every action from all three roles: timestamps, who accessed what, and whether it was approved or denied. This is our Monitoring and Logging control - a key part of any security audit."*

**Type:** `0` → Enter *(back to main menu)*

> *"Now let me open our built-in presentation notes for the CIA Triad justification."*

**Type:** `5` → Enter

*(Presentation notes display)*

**Read from the screen:**

> *"For public.txt - we prioritize Availability. The file is unencrypted and world-readable because it contains only public notices. Any user must be able to access it instantly without friction.*
>
> *For internal.txt - we focus on Integrity. RBAC restricts access to Employee and Owner roles only, preventing unauthorized users from reading or tampering with internal records.*
>
> *For sensitive.txt - Confidentiality is the priority. Two security layers work together: RBAC limits access to the Owner, and AES encryption ensures the file is unreadable on disk without the correct key."*

**Rodney hands keyboard to Harry.**

---

### ⚫ Harry - PART 6: Audit Checklist + Risk Analysis (≈ 2 minutes)

**Harry takes over. Still on the presentation notes screen - or can refer to WRITTEN_PLAN.txt.**

> *"Here is our completed Storage Security Audit Checklist:"*

**Read each item clearly:**

> *"Data Location - YES. We use a local file system, the SECURE_STORAGE_LAB folder.*
>
> Access Roles - YES. Guest, Employee, and Owner are clearly defined with privilege levels.*
>
> Least Privilege - YES. No 'everyone' access. Each file has a strict minimum role requirement.*
>
> Encryption-at-Rest - YES. sensitive.txt is encrypted with AES using Python's cryptography library.*
>
> Monitoring and Logging - YES. All access attempts are logged automatically to audit_log.txt."*

**Then for the Risk Analysis:**

> *"For our Coaching Prompt - we identified one vulnerability in our implementation.*
>
> The Risk: Our decryption passphrase is hardcoded inside the setup file. Anyone who reads our source code can find the key and bypass the encryption.*
>
> Our Proposed Fix: In a real production system, we would store the key inside a Key Management Service - like AWS KMS or Azure Key Vault. The app would request the key at runtime only after the user authenticates, so the key never appears in the source code or in any repository."*

---

### 🟢 OJ - CLOSING (≈ 30 seconds)

**OJ returns to front.**

> *"That concludes our demonstration. Our application successfully simulates a secure file storage environment with Role-Based Access Control, Least Privilege, Encryption-at-Rest, and Audit Logging - all running directly in the terminal with no external database or server required.*
>
> Thank you. We're open for questions."*

---

## ⏱️ Total Estimated Time: ~12–15 minutes

| Part | Member | Time |
|---|---|---|
| Intro + Launch | OJ | ~2 min |
| GUEST Demo | Enzy | ~2 min |
| EMPLOYEE Demo | Angel | ~2 min |
| OWNER + Encryption | Andrey | ~3 min |
| Audit Log + CIA Triad | Rodney | ~3 min |
| Checklist + Risk | Harry | ~2 min |
| Closing | OJ | ~30 sec |

---

## 🚨 Emergency Backup

> [!WARNING]
> If anything breaks, OJ just says:
> *"Let me restart the app quickly."*
> Then runs `python main.py` again. The lab files are already created, so it picks up instantly.

**The one key to never forget:**
```
IAS1-SecureOwner-2026
```
