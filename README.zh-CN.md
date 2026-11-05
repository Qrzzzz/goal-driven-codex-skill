<div align="center">

# Controlled Goal-Driven Codex Skill（中文版）

**一个面向复杂工程任务、强调边界与验证的 Codex 实用技能。**

[English README](./README.md) · [灵感来源](https://github.com/lidangzzz/goal-driven)

</div>

---

## 🌟 概览

![可控目标驱动 Codex Skill 概览图](./assets/overview-zh-CN.png)

本仓库将可控的目标驱动工作流打包为一个小型 Codex Skill 项目。它适合用于进展可验证、迭代有意义、并且需要明确停止条件的任务。

## 🤔 这是什么？

这个技能会把宽泛的工程请求转化为一个有边界的循环：

1. 明确目标
2. 定义成功标准
3. 遵守允许修改的作用域
4. 运行验证命令
5. 只在进展可衡量时继续迭代
6. 最后输出简洁报告

核心思想：

> 不只是“更努力地试”，而是围绕明确目标推进、持续验证，并在不值得继续时及时停止。

v1.1 区分**单项检查结果**（PASS / FAIL / BLOCKED / NOT_RUN）、**每轮进展**（PROGRESS / NO_PROGRESS / REGRESSION / UNKNOWN）及**最终终止状态**（SUCCESS / NO_PROGRESS / REGRESSION / BLOCKED / BUDGET_EXHAUSTED / NEEDS_DECISION）。只要有可比较的客观进展，同一错误连续出现并不自动触发停止。

## 🛠️ 安装

将 `skill/` 目录复制到 Codex skills 目录中，例如：

```text
~/.agents/skills/controlled-goal-driven/
```

最终结构应为：

```text
~/.agents/skills/controlled-goal-driven/SKILL.md
~/.agents/skills/controlled-goal-driven/agents/openai.yaml
~/.agents/skills/controlled-goal-driven/references/
~/.agents/skills/controlled-goal-driven/scripts/check_scope.py
```

该技能有意禁用隐式调用。请显式调用：

```text
$controlled-goal-driven
```

## 🚀 使用方式

```text
$controlled-goal-driven

Goal:
修复解析器的嵌套表达式问题。

Success criteria:
- 解析器测试及新增回归测试通过
- 不改变无关行为和文件

Validation:
- npm test -- parser

Scope:
- src/parser/**, tests/parser/**

Budget:
- 最多 3 轮修改与验证

Stop conditions:
- 连续两轮可比较的执行没有进展时停止
- 验证受阻或必须扩大修改范围时停止
```

## 🔎 v1.2 验证与修改范围检查

新版核心指令采用精简结构，详细规则存放在[按需加载的参考文件](./skill/references/)中。新增可选的 **Git Scope 检查器**，可识别修改前已有的用户变更；即使无法运行检查器，也必须遵守用户指定的修改范围。

在 Git 项目内、开始修改前执行：

```bash
python skill/scripts/check_scope.py snapshot
```

每轮修改后检查：

```bash
python skill/scripts/check_scope.py check --allow 'src/parser/**' --allow 'tests/parser/**'
```

检查器覆盖已暂存、未暂存、未跟踪、删除和重命名的路径，不会自动回滚文件。它属于辅助核查工具，并非安全沙箱。参见 [Scope 检查说明](./skill/references/scope-check.md) 与 [基线及回归验证](./skill/references/baseline-and-validation.md)。

无需 API 密钥即可运行离线测试：

```bash
python -m unittest discover -s tests -v
```

**这些离线测试不会验证 Codex 的真实行为。** 另有[行为评测指南](./docs/evaluation.md)，包含十个需要手动或选择性运行的评测场景。

## ✅❌ 何时使用 / 何时不使用

适合使用这个技能的情况：

- 任务有客观成功标准
- 存在可执行检查或可独立核验的证据
- 允许修改的作用域清晰
- 多次迭代可以改善结果

不适合使用这个技能的情况：

- 目标很模糊
- 成功只取决于审美或感觉
- 没有可信的验证方法
- 用户只需要一次性的简单回答

## 💡 为什么要做这个版本

该工作流灵感来自 [Li Dang（@lidangzzz）](https://x.com/lidangzzz) 的 [goal-driven](https://github.com/lidangzzz/goal-driven) 模式，但本项目更强调在 Codex 中的安全性、可控性与可审计性。

相较于开放式循环提示词，这个技能增加了：

- 显式迭代预算
- 强制提供验证证据
- 明确停止条件
- 严格作用域意识
- 简洁最终报告
- 在缺少约束时使用保守默认值

## ⏱️ 为什么不无限运行？

只有在成功可验证时，长流程才有意义。

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

如果目标本身模糊，技能应当先产出计划并停止，而不是无限消耗 token。

## 🧭 推荐输入模板

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
最多允许的迭代或尝试次数。

Stop conditions:
何时应停止并报告，而不是继续尝试。
```

## 📚 示例

- [基于测试的 Bug 修复](./examples/test-driven-bugfix.md)
- [带作用域的重构](./examples/refactor-with-scope.md)
- [生成测试并验证](./examples/generated-test-validation.md)
- [v1.1 决策场景与预期终止状态](./examples/decision-traces.md)
- [v1.2 测试与行为评测流程](./docs/evaluation.md)

## 📝 最终报告建议包含

- 终止状态与原因
- 目标、允许范围及修改内容
- 修改前基线、最终证据及迭代次数
- 各成功标准的已验证 / 未满足 / 未验证状态
- 验证命令及 PASS / FAIL / BLOCKED / NOT_RUN 结果
- 剩余问题和下一步建议

## 🙏 致谢

本项目灵感来自 Li Dang 的目标驱动工作流：

- GitHub: [lidangzzz/goal-driven](https://github.com/lidangzzz/goal-driven)
- X: [@lidangzzz](https://x.com/lidangzzz)

本仓库是面向 Codex 的独立、可控改写版本。
