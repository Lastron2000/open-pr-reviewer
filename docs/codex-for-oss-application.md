# Codex for Open Source — 申请文案（定稿 · 已实测字符数）

> 申请地址：https://openai.com/form/codex-for-oss
> 项目地址：https://github.com/Lastron2000/open-pr-reviewer
>
> 三段文案均已用脚本实测字符数，压在 500 限制内（489 / 495 / 490）。
> 表单是纯前端提交，字段和限制是从真实页面抓的。

---

## 表单全字段（实测）

| # | 字段（原文） | 必填 | 填什么 |
|---|---|---|---|
| 1 | First name | ✅ | 你的名，拼音 |
| 2 | Last name | ✅ | 你的姓，拼音 |
| 3 | Email | ✅ | **必须是 ChatGPT 账号那个邮箱** |
| 4 | GitHub username | ✅ | `Lastron2000` |
| 5 | GitHub repository URL | ✅ | `https://github.com/Lastron2000/open-pr-reviewer` |
| 6 | Describe your role | ✅ | 选 **Primary maintainer** |
| 7 | Why does this repository qualify? | ✅ | 限 500 → 贴 A |
| 8 | I'm interested in... | 可选 | **两个都勾**（Codex Security + API credits） |
| 9 | OpenAI Organization ID | ✅ | **要登录平台查** |
| 10 | How will you use API credits? | ✅ | 限 500 → 贴 B |
| 11 | Anything else we should know? | 可选 | 限 500 → 贴 C |

**注意**：第 7 栏官方明确要"star 数、月下载量、为什么对生态重要"。
所以别绕开数字说话——藏不住，审核点进主页就看得到。

---

## A. Why does this repository qualify? — 489 字符

```
Open PR Reviewer is an MIT-licensed tool that reviews pull requests with OpenAI. Unlike paid reviewers, the diff goes straight to your own API key - nothing touches a third-party server. I built it after noticing PRs on my own side projects sat unreviewed for months, so I wanted "review in ten minutes" to be the default. New project: 18 tests pass, 0 stars, not yet battle-tested in production. Still fully functional, and I plan to maintain it properly rather than just collect credits.
```

**为什么这么写**：
- 差异化放第一句：不过第三方服务器，这是唯一站得住的技术理由
- 动机放中间：我自己的项目卡在这，比"解决行业痛点"可信
- 主动报 0 star + 承认没实战验证。反直觉但有效——夸自己项目很火的要么刷要么二手，诚实反而像真来办事的。**藏着不提才叫找死**
- 收尾"maintain it properly rather than just collect credits"：直接回应审核的顾虑

---

## B. How will you use API credits for your project? — 495 字符

```
Three things. First, six months of real reviews will show what the model misses, so I can tune the prompt with data instead of guessing - the 0.7 threshold in models.py is a guess today. Second, maintenance: reviewing PRs, triaging issues, running tests - two to three hours a week I would rather spend on code. Third, my own usage will not eat six months of credits, so I will spend the rest reviewing small repos with no API key. I was there myself, and the point is letting others try it too.
```

**为什么这么写**：
- 每段都有**可核实的抓手**：`0.7` 真在 `models.py` 里、`两到三小时/周` 是真实维护成本
- 说"要调优提示词"是空话；说"0.7 是我拍的，要用数据定它"是实话
- 第三段是**最强的动机**：额度自己吃不完，分给别人。一句话证明三件事——你不是冲着白拿来的、你懂互助、你的项目有真实用户

---

## C. Anything else we should know? — 490 字符

```
The repository is new, so I will not overstate its maturity. What I can commit to: the code is real and tested, I am the sole maintainer and will respond to issues, and I will report what actually happens when real users try it. If it turns out the tool does not work well, I would rather find that out and fix it than keep the appearance of an active project. I am applying because I want to keep building this, and the credits let me do it on evenings and weekends the way I actually can.
```

**为什么建议填**：
这是唯一能**主动交代弱点**的地方。上面两栏都在讲项目好，这栏讲"我清楚它现在什么水平、会怎么对待它"。审核看到前面是新人申请、后面主动说"我不装成熟"，可信度立刻不一样。

---

## 提交前必做的两件事

### 1. 确认 GitHub 资料为公开（审核会核对，私有直接拒）

- 主页：https://github.com/settings/profile → `Public profile` 打开
- 仓库：已是 public，确认没误设

### 2. 查 OpenAI Organization ID

登录 [platform.openai.com/settings/organization](https://platform.openai.com/settings/organization)，
找形如 `org-xxxxxxxxxxxx` 的 ID。没建过组织的话，开卡后默认会生成个人组织，照着取。

### 3. 贴表

| 字段 | 贴哪段 |
|---|---|
| Why does this repository qualify? | A |
| How will you use API credits? | B |
| Anything else we should know? | C |

其余字段照上面表格填。`First name` / `Last name` 用拼音，
`Email` 填 ChatGPT 账号那个，`role` 选 `Primary maintainer`，`I'm interested in` 两个都勾。

---

## 提交之后

1. **盯邮箱含垃圾箱**。官方说滚动审核，快的一两周，慢的一个月。
2. **两周没回音**可礼貌重投，在补充说明里写这期间做了什么。
3. **别买 star**。刷来的时间分布异常，审核一眼看出；追问"有谁在用"就露馅。
   自然攒的 10 个真星比 200 个刷的管用。

## 提通过率最狠的一招

在你自己另一个仓库（`home-renovation-notes`）挂上这个 action 跑一次，
把结果贴进 README。**有真实调用记录**比任何文案都硬——证明不是空壳。
