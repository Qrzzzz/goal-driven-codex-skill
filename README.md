<div align="center">

# 🎯 Controlled Goal-Driven Codex Skill

**A practical, bounded, and validation-first Codex skill for complex engineering tasks.**

[中文说明 🇨🇳](./README.zh-CN.md) · [Original Inspiration](https://github.com/lidangzzz/goal-driven)

</div>

---

## ✨ What is this?

This repository provides a **controlled goal-driven skill** for Codex.

It is designed for tasks where progress can be measured objectively, such as:

- 🐞 test-driven bug fixing
- 🔧 large refactors
- 🚚 migration tasks
- ⚡ benchmark-driven optimization
- 🧪 generated test-suite validation
- 📦 repeated checks against known expected outputs

💡 Core idea:

> Don’t just “try harder”. Work toward a clear goal, validate results, and stop when further attempts are not justified.

---

## 🧭 Why this version exists

The workflow is inspired by Li Dang’s goal-driven pattern, but this project focuses on **safe and auditable execution** in Codex.

Compared with open-ended looping prompts, this skill adds:

- 🔢 explicit iteration budgets
- ✅ mandatory validation commands
- 🛑 clear stop conditions
- 🧱 strict scope awareness
- 🧾 concise final reporting
- 🐢 conservative defaults when user constraints are missing

---

## 🚫 Why not run forever?

Long-running workflows only make sense if success can be validated.

✅ Good examples:

```bash
npm test
pytest
cargo test
make test
go test ./...
```

❌ Bad examples:

```text
Make this project better.
Keep optimizing until it feels good.
```

If the goal is vague, the skill should **plan and stop**, rather than burn tokens indefinitely.

---

## 🚀 Usage

🛠️ Install the `skill/` directory as a Codex skill and invoke it explicitly.

```text
$controlled-goal-driven

Goal:
Fix the parser so all syntax tests pass.

Success criteria:
- npm test passes
- no unrelated files modified
- maximum 3 iterations
- stop if the same error repeats twice
```

---

## 🧩 Recommended input format

## Why this version exists

This workflow is inspired by [Li Dang (@lidangzzz)](https://x.com/lidangzzz)'s [goal-driven](https://github.com/lidangzzz/goal-driven) pattern, but this project focuses more on safety, controllability, and auditable execution in Codex.

Compared with open-ended looping prompts, this skill adds:

- explicit iteration budgets
- mandatory validation commands
- clear stop conditions
- strict scope awareness
- concise final reporting
- conservative defaults when user constraints are missing

## Why not run forever?

Long-running workflows only make sense if success can be validated.

Good examples:

```bash
npm test
pytest
cargo test
make test
go test ./...
```

---

## 📋 Final report should include

- 🎯 Goal
- 🛠️ Changes made
- ✅ Validation results
- ⚠️ Remaining issues
- 👉 Recommended next action

---

## 🙏 Acknowledgement

✨ Inspired by Li Dang’s original goal-driven workflow:

- GitHub: [lidangzzz/goal-driven](https://github.com/lidangzzz/goal-driven)
- X: [@lidangzzz](https://x.com/lidangzzz)

This repository is an independent, controlled adaptation for safer Codex usage.
