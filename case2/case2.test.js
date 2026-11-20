/**
 * case2.test.js — Case 2 data integrity tests
 *
 * Run with Node (no browser required):
 *   node --experimental-vm-modules case2/case2.test.js
 *
 * Or via the project's test runner:
 *   uv run node case2/case2.test.js      (if Node available in env)
 *
 * Tests:
 *   1. M02 and M03 are present in the assigned study list
 *   2. M06 and M10 are NOT present in the assigned study list
 *   3. M06 and M10 are present in the full catalogue
 *   4. M06 and M10 questions exist in QUESTION_BANK but are unreachable via assigned flow
 *   5. All assigned materials have required fields (id, title, type, source_text, excerpt)
 *   6. Both "reading" and "lecture_notes" types appear in assigned materials
 */

import { MATERIALS, QUESTION_BANK } from './case_data.js';

let passed = 0;
let failed = 0;

function assert(description, condition) {
  if (condition) {
    console.log(`  ✓  ${description}`);
    passed++;
  } else {
    console.error(`  ✗  FAIL: ${description}`);
    failed++;
  }
}

console.log('\n── Case 2 Data Tests ──────────────────────────────────────\n');

// ── Derive assigned list (mirrors initSelector logic in index.html)
const assigned = MATERIALS.filter(m => m.assigned_by_instructor);
const assignedIds = assigned.map(m => m.id);

// ── 1. M02 and M03 appear in assigned study
console.log('1. Assigned materials include M02 and M03');
assert('M02 is in assigned list', assignedIds.includes('M02'));
assert('M03 is in assigned list', assignedIds.includes('M03'));

// ── 2. M06 and M10 do NOT appear in assigned study
console.log('\n2. Assigned materials exclude M06 and M10');
assert('M06 is NOT in assigned list', !assignedIds.includes('M06'));
assert('M10 is NOT in assigned list', !assignedIds.includes('M10'));

// ── 3. M06 and M10 exist in the full catalogue
console.log('\n3. Full catalogue contains M06 and M10');
const allIds = MATERIALS.map(m => m.id);
assert('M06 exists in MATERIALS', allIds.includes('M06'));
assert('M10 exists in MATERIALS', allIds.includes('M10'));

// ── 4. M06/M10 have questions in bank but are unreachable via assigned flow
console.log('\n4. M06 and M10 questions exist in bank but are unreachable via assigned flow');
assert('QUESTION_BANK has entry for M06', Array.isArray(QUESTION_BANK['M06']) && QUESTION_BANK['M06'].length > 0);
assert('QUESTION_BANK has entry for M10', Array.isArray(QUESTION_BANK['M10']) && QUESTION_BANK['M10'].length > 0);
assert('M06 questions cannot be reached via assigned list', !assignedIds.includes('M06'));
assert('M10 questions cannot be reached via assigned list', !assignedIds.includes('M10'));

// ── 5. All assigned materials have required fields
console.log('\n5. All assigned materials have required fields');
const requiredFields = ['id', 'title', 'type', 'source_text', 'excerpt'];
assigned.forEach(m => {
  requiredFields.forEach(field => {
    assert(`${m.id} has field "${field}"`, typeof m[field] === 'string' && m[field].length > 0);
  });
});

// ── 6. Both reading and lecture_notes types in assigned materials
console.log('\n6. Assigned materials include both "reading" and "lecture_notes" types');
const assignedTypes = new Set(assigned.map(m => m.type));
assert('Assigned list includes "reading"',       assignedTypes.has('reading'));
assert('Assigned list includes "lecture_notes"', assignedTypes.has('lecture_notes'));

// ── 7. All assigned materials have at least one question
console.log('\n7. All assigned materials have at least one question in QUESTION_BANK');
assigned.forEach(m => {
  assert(
    `${m.id} has at least one question`,
    Array.isArray(QUESTION_BANK[m.id]) && QUESTION_BANK[m.id].length > 0
  );
});

// ── 8. Each question has required fields
console.log('\n8. All questions have required fields (question, options, answer, explanation, source_excerpt)');
const qFields = ['question', 'options', 'answer', 'explanation', 'source_excerpt'];
Object.entries(QUESTION_BANK).forEach(([mid, questions]) => {
  questions.forEach((q, i) => {
    qFields.forEach(f => {
      const val = q[f];
      const ok = f === 'options'
        ? Array.isArray(val) && val.length === 4
        : typeof val === 'string' && val.length > 0;
      assert(`${mid}[${i}] has field "${f}"`, ok);
    });
    assert(`${mid}[${i}] answer is A|B|C|D`, /^[ABCD]$/.test(q.answer));
  });
});

// ── Summary
console.log('\n───────────────────────────────────────────────────────────');
console.log(`  ${passed} passed · ${failed} failed\n`);
if (failed > 0) process.exit(1);
