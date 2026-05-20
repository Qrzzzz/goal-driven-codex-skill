<div align="center">

# 🎯 Controlled Goal-Driven Codex Skill（中文版）

**一个面向复杂工程任务、强调边界与验证的 Codex 实用技能。**

[English README 🌍](./README.md) · [灵感来源](https://github.com/lidangzzz/goal-driven)

</div>

---

## ✨ 这是什么？

本仓库提供了一个 **可控的目标驱动型 Codex Skill**。

它适用于“可客观衡量进展”的任务，例如：

- 🐞 基于测试的 Bug 修复
- 🔧 大规模重构
- 🚚 迁移类任务
- ⚡ 基于基准测试的优化
- 🧪 生成测试集并验证
- 📦 与已知结果进行反复比对

核心思想：

> 不只是“更努力地试”，而是围绕明确目标迭代、持续验证，并在不值得继续时及时停止。

---

## 🧭 为什么要做这个版本

该工作流灵感来自 [立党（@lidangzzz）](https://x.com/lidangzzz) 的 [goal-driven](https://github.com/lidangzzz/goal-driven) 模式，但本项目更强调在 Codex 中的 **安全性、可控性与可审计性**。

相较于无限循环式提示词，这个版本增加了：

- 🔢 显式迭代预算
- ✅ 强制验证命令
- 🛑 明确停止条件
- 🧱 严格作用域意识
- 🧾 清晰最终报告
- 🐢 在缺少约束时使用保守默认值

---

## 🚫 为什么不无限运行？

只有在“成功可验证”时，长流程才有意义。

合理示例：

```bash
npm test
pytest
cargo test
make test
go test ./...
```

不合理示例：

```text
把这个项目变得更好。
一直优化到感觉不错为止。
```

如果目标本身模糊，技能应当 **先产出计划并停止**，而不是无限消耗 token。

---

## 🚀 使用方式

将 `skill/` 目录安装为 Codex Skill，并在需要时显式调用：

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

## 🧩 推荐输入模板

```text
Goal:
Codex 要完成的具体目标。

Success criteria:
如何判断任务完成。

Validation:
用于验证进展的命令。

Scope:
允许修改的文件或目录范围。

Budget:
最多允许的迭代/尝试次数。

Stop conditions:
何时应停止并报告，而不是继续尝试。
```

---

## 📋 最终报告建议包含

- 目标
- 已完成修改
- 验证结果
- 剩余问题
- 下一步建议

---

## 🙏 致谢

本项目灵感来自 Li Dang 的目标驱动工作流：

- GitHub: [lidangzzz/goal-driven](https://github.com/lidangzzz/goal-driven)
- X: [@lidangzzz](https://x.com/lidangzzz)

本仓库是面向 Codex 的独立、可控改写版本。
