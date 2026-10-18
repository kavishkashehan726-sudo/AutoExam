# AutoExam LK — SRS Review
## Review of the Software Requirements Specification for the Sri Lankan Automated AI Model Paper Generation System

### Summary
This is a well-organized SRS. The scope, roles, and requirements are clearly separated, and starting with a narrow MVP is the right call. The main weakness is that it describes what the system generates but says little about how you know the output is correct, and for an exam product that is the core of the system. The recommendations below are listed roughly in order of importance.

---

### 1. Add a validation layer as a functional requirement
At the moment, quality is covered only by NFR-1.2 ("strict prompt engineering and RAG grounding"). Prompting reduces errors; it doesn't prevent them. Suggested additions:

* **FR-3.4 Automated Validation:** Every generated question passes:
  * (a) answer verification by code for numeric questions,
  * (b) a similarity check against the past-paper corpus to enforce FR-3.2, and
  * (c) syllabus and number-range checks.
  * *Questions that fail are regenerated or flagged.*
* **FR-3.5 Traceability:** Each question stores the model, prompt version, and retrieved examples used, so bad output can be traced back to its cause.

---

### 2. Consider a question bank instead of live generation
This is the biggest architectural decision in the document. The current design implies generating every paper live. The alternative:

> **Generate offline → validate → teacher-review → store in a question bank → assemble papers from the bank.**

This one change helps with several requirements:
* **NFR-2.1 (15–30s):** Assembling a paper from stored questions takes under a second. Live generation of 20 questions with verification and retries will struggle to hit 30 seconds reliably.
* **NFR-1.1 ($\ge 99\%$ in syllabus):** Only reviewed questions reach users.
* **NFR-4.1 (diagrams):** Diagrams can be made and checked once rather than generated on the fly.
* **Cost:** You pay per question once, not per paper.

*Note: Live generation can still exist as a premium or teacher feature, with questions marked "unreviewed."*

---

### 3. Make the NFRs testable
* **NFR-1.1 ("99%+"):** Define how and by whom it is measured, e.g., *"on a monthly sample of N questions reviewed by qualified teachers, $\ge 99\%$ are judged in-syllabus."* Without that, the requirement cannot be verified.
* **FR-2.3 Difficulty:** Define what makes a question "Hard" in measurable terms (number of steps, cognitive level, number ranges), and later calibrate against how students actually perform.
* **Acceptance Criteria & Priority:** Add acceptance criteria and a priority (Must/Should/Could) for each requirement. As written, everything looks equally essential, which makes MVP planning hard.

---

### 4. Narrow the MVP further
Even "Grade 5 Scholarship" contains very different sub-problems:
* The **IQ-style section** (patterns, sequences, figure series) is highly visual. NFR-4.1 is really a major functional feature, and a hard one.
* **Text-based math word problems** are by far the easiest to generate and verify.

**Recommendation:** Make the MVP text-only math questions, and move diagram-heavy and IQ-type questions to phase 2. Also confirm the current exam structure (papers, sections, marks) with the Department of Examinations or a practising Grade 5 teacher before encoding it into the system, so you aren't building around an outdated format.

---

### 5. Missing sections
* **Data rights:** You plan to ingest NIE textbooks, Teachers' Guides, and past papers. Add a requirement covering what you are permitted to store and display, and ensure no past-paper question is ever shown to users verbatim. Get proper advice on this before launch.
* **Children's data:** Students are minors. Sri Lanka's Personal Data Protection Act applies, so you need a section on accounts, consent (parent-managed accounts for under-18s), and what you store.
* **Auth, roles and accounts:** Three roles are defined, but there are no requirements for login, permissions, or what each role can see and do.
* **Business model:** Free/paid tiers, generation limits, and cost per paper. LLM costs need to be an NFR.
* **Student mode:** FR-2 to FR-5 are teacher-oriented. Do students answer online with auto-marking, or only download PDFs? Auto-marking MCQs is easy; marking short written answers is a separate, much harder feature.
* **Admin quality dashboard:** Reject rates, flagged questions, and teacher feedback per topic.

---

### 6. Smaller fixes
* **"Exclusion: Sinhala Language subject"** is ambiguous. Do you mean the Sinhala subject or Sinhala medium? These are very different. Since most Grade 5 candidates sit in Sinhala medium, state the medium roadmap explicitly.
* **FR-4.2 "official marking criteria":** Detailed step-marking rules aren't always fully published. Clarify whether you will follow published schemes or define your own rubric modelled on them.
* **FR-2.1 lists Grades 5–13**, but the MVP is Grade 5 only. Mark the rest as future scope so developers don't build UI for unsupported options.

---

### 7. Tech stack
* **Don't pin model versions in the SRS.** Gemini 1.5 is already dated. NFR-3.2's abstraction layer is the right idea, so the architecture section should say "pluggable LLM provider" and keep model choice in configuration.
* **Choose one vector store.** Since questions carry a lot of relational metadata (grade, unit, competency level, difficulty, review status), PostgreSQL with `pgvector` may be simpler than a separate vector database: one database, real joins, and filtered vector search together.
* **LangChain/LlamaIndex are optional.** The pipeline is fairly linear (retrieve → generate → verify → store), and plain FastAPI code is often easier to debug than a framework.
* **Add a job queue** (e.g., Celery or RQ with Redis) for batch generation, which the question-bank approach needs anyway.

---

### Next steps
1. Revise the SRS with these changes, adding priorities and acceptance criteria to each requirement.
2. Design the question-bank data model, since most of the system depends on it.