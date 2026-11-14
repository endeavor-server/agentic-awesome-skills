---
name: naukri-job-posting
description: Automate creating, configuring, and updating job postings on the Naukri Employer portal (hiring.naukri.com). Handles React controlled inputs, Draft.js editor synchronization, key skills selection, screening questions, and safe draft management without consuming paid Hot Vacancy credits unasked.
example-prompt: Create a job post on Naukri for 3B2 Pagination Specialist on freelance remote basis with our Google Form quick apply link and HR email.
---

# Naukri Job Posting Skill

Automate the end-to-end creation, updating, and management of job postings on the Naukri Employer portal (`https://hiring.naukri.com`).

## Core Rules & Constraints

> [!CRITICAL]
> **Never consume paid credits without user confirmation.**
> Always leave new job postings in **Draft** status (`/savedraft/<draftId>`). Do not click final post/publish or consume Hot Vacancy / NVite credits unless the user explicitly confirms via an `openbot.ask_ui` confirmation card.

- **Environment**: Operates via Google Chrome where the recruiter session is active (`https://hiring.naukri.com`).
- **Drafts Hub**: Manage drafts at `https://hiring.naukri.com/hiring/job-listing` under the **Drafts** tab (`#mjr-tab-DRAFT`).
- **New Job URL**: `https://hiring.naukri.com/hiring/job/h?referrer=mjr`

---

## 5-Step Posting Workflow

### Step 1: Job Details (`#desigSugg`)
1. **Job Title (`#desigSugg`)**:
   - Controlled textarea (max 70 characters).
   - Use descriptive, candidate-targeted titles: e.g., `3B2 Pagination Specialist / Typesetter (Remote Freelance)` or `Copyeditor - Level 3 (STM / Academic Journals - Remote Freelance)`.
   - Set value via native prototype setter and dispatch `input` and `change` events.
2. **Department & Role (`#deptRoleCat`, `#role`)**:
   - Focus and search department (e.g. `Editing` or `Content, Editorial & Journalism`).
   - Click the exact option in `#deptRoleCat-lb` using `PointerEvent` (`pointerdown`, `mousedown`, `pointerup`, `mouseup`, `click`).
   - Select role specialization (e.g. `Editor` or `Copy Editor`).
3. **Employment Type (`#employmentType`)**:
   - Open `#employmentType`, find the target `<li>` (e.g. `Full Time, Freelance/Homebased`), and click its inner `span`.
4. **Experience & Salary (`#minExpSmb`, `#maxExpSmb`, `#minSalary`, `#maxSalary`)**:
   - Click `#minExpSmb`, select minimum years (e.g. `3 years`).
   - Click `#maxExpSmb`, select maximum years (e.g. `8 years`).
   - Click `#minSalary`, select min CTC (e.g. `3 lacs`).
   - Click `#maxSalary`, select max CTC (e.g. `8 lacs`).
   - Check `#hideSalary` checkbox if salary is confidential/hidden.
5. **Work Mode & Location (`#PERMANENT`, `#location`)**:
   - Click `#PERMANENT` for **Remote** (or `#HYBRID`, `#IN_OFFICE`).
   - If Remote, enter base location (e.g. `Delhi / NCR` in `#location`).
6. **Save Draft / Advance**:
   - Click `#jpSubmit` ("Next").
   - Naukri automatically assigns a Draft ID: URL transitions to `/hiring/job/h/savedraft/<draftId>`.

---

### Step 2: Preferred Candidate Details
1. **Key Skills (`#keySkillSugg`)**:
   - Click available suggested skill buttons (`Typesetting`, `Publishing`, `Copy Editing`, etc.).
   - Type custom skills into `#keySkillSugg` and trigger `keydown` (Enter, keyCode 13) to chip them.
2. **Mark Preferred Skill**:
   - **Mandatory**: Naukri requires at least 1 key skill marked as preferred.
   - Click `.keySkills_prefChipBtn__mG8tV` on 1–2 core skills to star them.
3. **Education Qualification (`#Education`)**:
   - Multilevel dropdown. Select `Graduation Not Required` (`#Education-opt-1.9501`) or `Graduate` → `Any Graduate`.
4. **Advance**:
   - Click `#jpSubmit` ("Next") to move to Step 3.

---

### Step 3: Job Description (Draft.js Rich Text Editor)

> [!IMPORTANT]
> **Draft.js State Synchronization**:
> Naukri uses Facebook's Draft.js editor (`.public-DraftEditor-content`). Standard `document.execCommand('insertText')` or `innerHTML` edits do **not** persist into Draft.js internal Redux/React state and will revert upon page reload!
> **The only reliable way to save**:
> 1. Copy the formatted JD text to the macOS system clipboard via `pbcopy`.
> 2. Bring Google Chrome to the foreground and focus `.public-DraftEditor-content`.
> 3. Send keyboard events: `Cmd+A` → `Delete` → `Cmd+V`.
> 4. Blur the editor (`editor.blur()`) and click `#jpSubmit`.

#### Standard Structure for Endeavor Job Descriptions:
```text
About the Role:
[High-impact hook detailing the position, publishing domain, and remote/freelance nature]

Roles and Responsibilities:
* [Key responsibility 1: Core composition, language editing, software tools]
* [Key responsibility 2: Workflow standards, XML/style guide compliance]
* [Key responsibility 3: Layout/grammar quality, tables, equations, cross-refs]
* [Key responsibility 4: Proof stages, author queries, deliverable standards]

Desired Candidate Profile:
* 3 to 8+ years of dedicated professional experience with leading academic publishers.
* Master's / Ph.D. or specialized software mastery (3B2 / InDesign / LaTeX / CMOS / AMA).
* High accuracy and proven daily throughput.

Commercial Terms & Remuneration:
* Engagement Type: Contractual / Freelance (Remote / Work from Home).
* Remuneration Model: Competitive per-page pricing or dedicated monthly retainer.
* Volume: Continuous, high-volume recurring pipeline with prompt monthly payouts.

How to Apply (Quick Apply / Direct Application):
Option 1 — Fast-Track Screening Form:
👉 Quick Apply Form: [Google Form Link with File Upload]

Option 2 — Direct Email Application:
Send your updated CV, rate expectations, and work samples directly to our HR team:
📧 Email: hr@endeavoracademy.co.in
Subject Line: "Application: [Job Title] — [Candidate Name]"
```

---

### Step 4: Screening Questions
1. Review suggested screening question chips.
2. Select relevant question chips (e.g., years of experience in core skill, notice period / availability).
3. Click `#jpSubmit` ("Next").

---

### Step 5: Advanced Options & Verification
1. Review response notification settings (default: summary to registered email).
2. The final CTA button reads **"Preview & post job"**.
3. **Do NOT click "Preview & post job" without user confirmation.**
4. Progress is already safely stored in Drafts.
5. Return to `https://hiring.naukri.com/hiring/job-listing` → **Drafts** (`#mjr-tab-DRAFT`) to verify the draft title, date, and draft ID.

---

## Technical Reference & DOM Helpers

See `references/naukri_dom_guide.md` for exact JavaScript and AppleScript code snippets.
See `scripts/naukri_poster.py` for automated headless or assisted posting execution.
