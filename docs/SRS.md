# AutoExam LK — Requirements (interim)

The full SRS will be added and expanded later (DECISIONS.md #5). Until then, this file is the
agreed scope. The review of the original SRS is in `SRS_REVIEW.md`.

## MVP scope
- Grade 5 Scholarship Examination, English medium, text-only mathematics questions.
- MCQ and structured (short-answer) questions (DECISIONS.md #6).
- Teachers/parents generate a model paper and its marking scheme, then download them as
  Word or PDF. No online answering in the MVP (#7).
- Marking schemes follow the published Department of Examinations schemes (#8).
- Difficulty levels defined by number of steps and number ranges (#9).

## How questions are made
Question bank first: generate offline → validate (answer checked by code, similarity check
against past papers, syllabus and number-range checks) → review by Shehan → store → assemble
papers from the bank. Live generation is secondary and its questions are marked `unreviewed`.

## Users and data
- Roles: students/parents, teachers/tutors, admins. Email + password login; student profiles
  are managed by a parent account and hold the minimum data (students are minors).
- Admins upload past papers, textbooks and syllabus material; the system uses them by
  retrieval only, and never shows past-paper questions verbatim.

## Later phases
- Phase 2: diagram and IQ-type questions, more Grade 5 content.
- Future: Grades 6–13, more subjects, Sinhala and Tamil medium, Sinhala UI.
