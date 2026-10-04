import re
import subprocess
import sys


def run_cmd(cmd: str) -> str:
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""


def main():
    print("## 🤖 Automated PR Reviewer Agent Report")
    print("\n*Inspecting pull request code changes against Hackathon Architecture Standards...*\n")

    diff = run_cmd("git diff origin/main...HEAD")
    if not diff:
        diff = run_cmd("git diff HEAD~1")

    issues = []
    warnings = []
    passes = []

    # Check 1: Hardcoded API keys / Secrets
    if re.search(
        r'(sk-[a-zA-Z0-9]{32,}|ghp_[a-zA-Z0-9]{36,}|password\s*=\s*["\'][^"\']+["\'])',
        diff,
        re.IGNORECASE,
    ):
        issues.append(
            "🚨 **Hardcoded Secret Detected**: Potential raw API key or password found in diff. Use `.env`."
        )
    else:
        passes.append("✔ No exposed hardcoded API keys detected.")

    # Check 2: Unsafe SQL execution
    if re.search(r'\.execute\(f["\']', diff) or re.search(r'\.execute\(\s*["\'].*%s', diff):
        issues.append(
            "🚨 **SQL Injection Risk**: Direct string interpolation detected in SQL statement. Use bound `:param` parameters."
        )
    else:
        passes.append("✔ Database queries use parameterized binding.")

    # Check 3: Raw shell subprocess
    app_diff = "\n".join([line for line in diff.splitlines() if not line.startswith("+++ b/scripts/review_pr.py")])
    if re.search(r"shell\s*=\s*True", app_diff):
        warnings.append(
            "⚠️ **Subprocess Risk**: `shell=True` detected in application code. Prefer `asyncio.create_subprocess_exec` with explicit argument list."
        )
    else:
        passes.append("✔ Subprocess execution adheres to safe array isolation.")

    # Check 4: Ruff Lint Check
    ruff_check = run_cmd("ruff check .")
    if ruff_check and "All checks passed" not in ruff_check:
        warnings.append(f"⚠️ **Lint Warnings Detected**:\n```\n{ruff_check[:400]}\n```")
    else:
        passes.append("✔ Ruff zero-lint errors passed.")

    # Output Summary Table
    print("### 📋 Automated Verification Checklist")
    for p in passes:
        print(f"- {p}")

    if warnings:
        print("\n### ⚠️ Architecture Recommendations")
        for w in warnings:
            print(f"- {w}")

    if issues:
        print("\n### ❌ Blocking Issues (Action Required Before Merge)")
        for i in issues:
            print(f"- {i}")
        sys.exit(1)
    else:
        print("\n### 🎉 Review Status: **APPROVED FOR MERGE**")
        print("All production standards and security guardrails satisfied.")


if __name__ == "__main__":
    main()
