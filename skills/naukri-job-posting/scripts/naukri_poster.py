#!/usr/bin/env python3
"""
Naukri Job Poster Helper Script
Automates inspecting, configuring, and updating job drafts on Naukri Employer portal.
"""

import sys
import time
import json
import subprocess
import argparse

def run_applescript(script):
    """Run an AppleScript string and return stdout."""
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"AppleScript error: {res.stderr.strip()}")
    return res.stdout.strip()

def find_naukri_tab():
    """Find the tab ID and URL of an active Naukri job creation or listing tab."""
    script = """
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "hiring.naukri.com" then
                    return (id of t as text) & "|" & (URL of t as text)
                end if
            end repeat
        end repeat
        return "not_found"
    end tell
    """
    out = run_applescript(script)
    if out == "not_found":
        return None, None
    tab_id, url = out.split("|", 1)
    return tab_id, url

def update_draft_jd(draft_id_or_fragment, jd_text):
    """Paste formatted JD text into Draft.js editor on the specified draft tab."""
    # Place text on system clipboard
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    p.communicate(jd_text.encode("utf-8"))

    # Focus and scroll to editor
    focus_cmd = f"""
    tell application "Google Chrome"
        activate
        repeat with w in windows
            set idx to 0
            repeat with t in tabs of w
                set idx to idx + 1
                if URL of t contains "{draft_id_or_fragment}" then
                    set active tab index of w to idx
                    set index of w to 1
                    execute t javascript "(() => {{ const el = document.querySelector('.public-DraftEditor-content'); if (el) {{ el.focus(); el.click(); }} }})()"
                    exit repeat
                end if
            end repeat
        end repeat
    end tell
    """
    run_applescript(focus_cmd)
    time.sleep(1)

    # Cmd+A, Delete, Cmd+V
    paste_cmd = """
    tell application "System Events"
        tell process "Google Chrome"
            set frontmost to true
            keystroke "a" using {command down}
            delay 0.2
            key code 51 -- delete
            delay 0.2
            keystroke "v" using {command down}
            delay 1
        end tell
    end tell
    """
    run_applescript(paste_cmd)
    time.sleep(1)

    # Blur and click Next (#jpSubmit)
    save_cmd = f"""
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "{draft_id_or_fragment}" then
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
    run_applescript(save_cmd)
    print(f"Successfully updated Job Description for draft: {draft_id_or_fragment}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naukri Job Poster Helper")
    parser.add_argument("--find-tab", action="store_true", help="Find active Naukri tab")
    parser.add_argument("--update-jd", help="Draft ID or URL fragment to update")
    parser.add_argument("--jd-file", help="File containing JD text to paste")
    args = parser.parse_args()

    if args.find_tab:
        tab_id, url = find_naukri_tab()
        print(f"Tab ID: {tab_id}, URL: {url}")
    elif args.update_jd and args.jd_file:
        with open(args.jd_file, "r", encoding="utf-8") as f:
            jd_text = f.read()
        update_draft_jd(args.update_jd, jd_text)
    else:
        parser.print_help()
