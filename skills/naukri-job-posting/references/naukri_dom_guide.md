# Naukri Portal DOM & Automation Reference Guide

This reference details the exact DOM selectors and JavaScript event patterns required to automate the modern React / Material UI interface of Naukri Employer (`https://hiring.naukri.com`).

---

## 1. Controlled React Inputs

Setting `.value = ...` directly on React controlled inputs does not trigger component state updates. Always use the native prototype property setter:

```javascript
function setNativeValue(element, value) {
    const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, "value").set;
    const prototype = Object.getPrototypeOf(element);
    const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, "value").set;
    if (prototypeValueSetter && valueSetter !== prototypeValueSetter) {
        prototypeValueSetter.call(element, value);
    } else {
        valueSetter.call(element, value);
    }
    element.dispatchEvent(new Event("input", { bubbles: true }));
    element.dispatchEvent(new Event("change", { bubbles: true }));
}
```

---

## 2. Pointer Event Dispatcher

Custom dropdowns (`multilevelDD`), chips, and autocomplete lists in Naukri ignore standard `click()` events. Dispatch full pointer down/up pairs:

```javascript
function dispatchPointerClick(element) {
    if (!element) return;
    element.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new PointerEvent("pointerup", { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent("mouseup", { bubbles: true, cancelable: true, view: window }));
    element.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
}
```

---

## 3. Draft.js Rich Text Editor Synchronization

Facebook's Draft.js editor (`.public-DraftEditor-content`) rejects programmatic DOM edits (`execCommand`, `innerHTML`). The only reliable method to update the description:

```python
import subprocess, time

def set_draft_description(draft_url_fragment, jd_text):
    # 1. Place text on system clipboard
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    p.communicate(jd_text.encode("utf-8"))

    # 2. Focus editor inside Chrome tab
    focus_cmd = f"""
    tell application "Google Chrome"
        activate
        repeat with w in windows
            set idx to 0
            repeat with t in tabs of w
                set idx to idx + 1
                if URL of t contains "{draft_url_fragment}" then
                    set active tab index of w to idx
                    set index of w to 1
                    execute t javascript "(() => {{ const el = document.querySelector('.public-DraftEditor-content'); if (el) {{ el.focus(); el.click(); }} }})()"
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    """
    subprocess.run(["osascript", "-e", focus_cmd])
    time.sleep(1)

    # 3. Simulate Cmd+A, Delete, Cmd+V via System Events
    paste_cmd = """
    tell application "System Events"
        tell process "Google Chrome"
            set frontmost to true
            keystroke "a" using {command down}
            delay 0.2
            key code 51 -- delete key
            delay 0.2
            keystroke "v" using {command down}
            delay 1
        end tell
    end tell
    """
    subprocess.run(["osascript", "-e", paste_cmd])
    time.sleep(1)

    # 4. Blur and click Next (#jpSubmit)
    save_cmd = f"""
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "{draft_url_fragment}" then
                    execute t javascript "(() => {{
                        const editor = document.querySelector('.public-DraftEditor-content');
                        if (editor) editor.blur();
                        const nextBtn = document.getElementById('jpSubmit');
                        if (nextBtn) nextBtn.click();
                    }})()"
                end if
            end repeat
        end repeat
    end tell
    """
    subprocess.run(["osascript", "-e", save_cmd])
```

---

## 4. Key Selectors Cheatsheet

| Step | Purpose | Selector |
| :--- | :--- | :--- |
| **Step 1** | Job Title | `#desigSugg` (textarea, max 70 chars) |
| **Step 1** | Department | `#deptRoleCat` |
| **Step 1** | Role Specialization | `#role` |
| **Step 1** | Employment Type | `#employmentType` |
| **Step 1** | Min Experience | `#minExpSmb` (`#minExpSmb-listbox li`) |
| **Step 1** | Max Experience | `#maxExpSmb` (`#maxExpSmb-listbox li`) |
| **Step 1** | Min Salary | `#minSalary` (`#minSalary-listbox li`) |
| **Step 1** | Max Salary | `#maxSalary` (`#maxSalary-listbox li`) |
| **Step 1** | Hide Salary Checkbox | `#hideSalary` |
| **Step 1** | Work Mode Remote | `#PERMANENT` |
| **Step 1** | Location Input | `#location` (autocomplete chip list) |
| **Step 1** | Next / Save Draft | `#jpSubmit` |
| **Step 2** | Add Key Skills | `#keySkillSugg` (press Enter to chip) |
| **Step 2** | Mark Preferred Skill | `.keySkills_prefChipBtn__mG8tV` (mandatory) |
| **Step 2** | Education | `#Education` (`#Education-opt-1.9501` for graduation not required) |
| **Step 3** | Rich Text Editor | `.public-DraftEditor-content` |
| **Step 4** | Question Chips | `.suggestion_suggestion__IIFLn` (click to add) |
| **Step 5** | Preview & Post CTA | `#jpSubmit` (*Do not click without confirmation*) |
| **Hub** | Drafts Tab | `#mjr-tab-DRAFT` on `https://hiring.naukri.com/hiring/job-listing` |
