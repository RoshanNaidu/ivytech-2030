"""
case2_data_test.py — Case 2 data integrity tests (text-pattern approach).

Reads case_data.js as plain text and verifies structural properties using
regex rather than JSON parsing (the file uses JS-specific syntax: unquoted
keys, backtick literals, boolean values).

Run from project root:
    python3 case2/case2_data_test.py
"""

import re, sys
from pathlib import Path

src = Path("case2/case_data.js").read_text()

passed = 0
failed = 0

def check(description, condition):
    global passed, failed
    if condition:
        print(f"  ✓  {description}")
        passed += 1
    else:
        print(f"  ✗  FAIL: {description}")
        failed += 1

print("\n── Case 2 Data Tests ──────────────────────────────────────\n")

# ── Extract material entries: find all { id: "MXX", ... assigned_by_instructor: true/false ... }
# We scan for id + assigned_by_instructor pairs.
material_blocks = re.findall(
    r'\{\s*id:\s*"(M\d+)".*?assigned_by_instructor:\s*(true|false)',
    src, re.DOTALL
)
# material_blocks: list of (id, "true"|"false")

assigned_ids  = [mid for mid, flag in material_blocks if flag == 'true']
catalogue_ids = [mid for mid, _ in material_blocks]

print(f"   Full catalogue: {catalogue_ids}")
print(f"   Assigned:       {assigned_ids}\n")

# 1. M02 and M03 in assigned
print("1. Assigned materials include M02 and M03")
check("M02 is in assigned list", "M02" in assigned_ids)
check("M03 is in assigned list", "M03" in assigned_ids)

# 2. M06 and M10 NOT in assigned
print("\n2. Assigned materials exclude M06 and M10")
check("M06 is NOT in assigned list", "M06" not in assigned_ids)
check("M10 is NOT in assigned list", "M10" not in assigned_ids)

# 3. M06 and M10 in full catalogue
print("\n3. Full catalogue contains M06 and M10")
check("M06 exists in MATERIALS", "M06" in catalogue_ids)
check("M10 exists in MATERIALS", "M10" in catalogue_ids)

# 4. M06/M10 have questions in QUESTION_BANK but unreachable via assigned flow
print("\n4. M06 and M10 questions exist in QUESTION_BANK but are unreachable via assigned flow")
check("QUESTION_BANK has entry for M06", bool(re.search(r'M06\s*:\s*\[', src)))
check("QUESTION_BANK has entry for M10", bool(re.search(r'M10\s*:\s*\[', src)))
check("M06 questions cannot be reached via assigned list", "M06" not in assigned_ids)
check("M10 questions cannot be reached via assigned list", "M10" not in assigned_ids)

# 5. All assigned materials have required fields
print("\n5. All assigned materials have required fields")
required_fields = ['id', 'title', 'type', 'source_text', 'excerpt']
for mid in assigned_ids:
    # Find the material block for this id (between its opening brace and next top-level item)
    block_m = re.search(
        rf'id:\s*"{mid}"([\s\S]*?)(?=\{{\s*id:|QUESTION_BANK)',
        src
    )
    block = block_m.group(0) if block_m else ""
    for f in required_fields:
        present = bool(re.search(rf'\b{f}\s*:', block))
        check(f"{mid} has field \"{f}\"", present)

# 6. Both types present in assigned materials
print("\n6. Assigned materials include both reading and lecture_notes types")
assigned_types = set()
for mid in assigned_ids:
    block_m = re.search(rf'id:\s*"{mid}"([\s\S]*?)(?=\{{\s*id:|QUESTION_BANK)', src)
    block = block_m.group(0) if block_m else ""
    t_m = re.search(r'type:\s*"([^"]+)"', block)
    if t_m:
        assigned_types.add(t_m.group(1))
check('Assigned list includes "reading"',       'reading' in assigned_types)
check('Assigned list includes "lecture_notes"', 'lecture_notes' in assigned_types)

# 7. All assigned materials have at least one question
print("\n7. All assigned materials have at least one question")
for mid in assigned_ids:
    check(f"{mid} has at least one question", bool(re.search(rf'{mid}\s*:\s*\[', src)))

# 8. Each question entry has required fields (check per-id block in QUESTION_BANK)
print("\n8. Question bank entries have required fields")
qbank_m = re.search(r'const QUESTION_BANK\s*=\s*\{([\s\S]*?)\n\};', src)
if qbank_m:
    qbank_text = qbank_m.group(1)
    # Find all material IDs with question blocks
    q_ids = re.findall(r'\b(M\d+)\s*:\s*\[', qbank_text)
    q_required = ['question', 'options', 'answer', 'explanation', 'source_excerpt']
    for mid in q_ids:
        # Extract the per-material slice from "MXX: [" to the next "M\d\d:" or end
        blk_m = re.search(
            rf'\b{mid}\s*:\s*\[([\s\S]*?)(?=\n\s*M\d\d\s*:|\Z)',
            qbank_text
        )
        blk = blk_m.group(1) if blk_m else ""
        for f in q_required:
            check(f"QUESTION_BANK[{mid}] has field \"{f}\"", bool(re.search(rf'\b{f}\s*:', blk)))
        # answer must be A, B, C, or D
        ans_m = re.search(r'answer:\s*"([ABCD])"', blk)
        check(f"QUESTION_BANK[{mid}] answer is A|B|C|D", bool(ans_m))
else:
    check("QUESTION_BANK block found in source", False)

# 9. Selector: both reading and lecture_notes accepted (type attribute has both values)
print("\n9. case_data.js defines both material types")
check('File defines type "reading"',       bool(re.search(r'type:\s*"reading"', src)))
check('File defines type "lecture_notes"', bool(re.search(r'type:\s*"lecture_notes"', src)))

# ── Summary ──────────────────────────────────────────────────
print("\n───────────────────────────────────────────────────────────")
print(f"  {passed} passed · {failed} failed\n")
sys.exit(0 if failed == 0 else 1)
