# V2EX / Reddit 发帖草稿

> 用途：给项目攒真实使用反馈和 star。审核看的是"有没有人真用过"，这是最有效的加分项。
> **发布前必改**：换成你自己的话。特别是别原样发，里面有些句子不像人写的。

---

## 版本 A：V2EX（中文社区，主推这个）

**标题**（选一个）：

- `开源了一个 GitHub PR 自动评审工具，跑在 Actions 上，代码不过第三方服务器`
- `写了个 AI 评审 PR 的开源项目，MIT 协议，配置两行就能用`
- `open-pr-reviewer：让开源项目的 PR 十分钟内拿到 review`

**正文**：

> 说个问题，不知道有没有人跟我一样。
>
> 我自己做的开源项目都是业余时间写的。每次提 PR 完就石沉大海，半年后自己翻记录才发现压根没人 review，代码就这么合进去了。不是不想看，是真的没时间——业余时间做项目的人自己都忙不过来，谁还天天盯别人的 PR。
>
> 市面上有 AI 评审的工具，但两个问题：要么按席位收费个人项目负担不起，要么把你的代码发到别人的服务器上。开源项目大多涉及点商业逻辑，代码外传这事我不太放心。
>
> 所以我自己写了一个：https://github.com/Lastron2000/open-pr-reviewer
>
> 用法很简单，仓库里加个 workflow：
>
> ```yaml
> name: AI PR Review
> on:
>   pull_request:
>     types: [opened, synchronize]
> permissions:
>   contents: read
>   pull-requests: write
> jobs:
>   review:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: Lastron2000/open-pr-reviewer@v0.1.0
>         with:
>           openai_api_key: ${{ secrets.OPENAI_API_KEY }}
> ```
>
> 然后在仓库设置里加一个 `OPENAI_API_KEY` secret，收工。之后每次 PR 自动评审，评论直接挂在出问题的行上，分 critical / warning / suggestion 三档。
>
> 几个我自己比较在意的点：
>
> - 代码不过任何第三方服务器，diff 直接发给你自己的 OpenAI key
> - 评审内容、条数、关注重点都可以配（只要不要 style 检查，默认关掉）
> - 有 dry-run，CI 里跑一下看看它会说什么，不满意可以不真的发
> - MIT 协议
>
> 刚发出来，还在早期，star 0，18 个测试是过的但没经过实战检验。发上来主要是想找人一起用用，看它在线上会不会翻车。
>
> 仓库地址在上面，有问题或者想吐槽代码烂的，欢迎直接开 issue。
>
> 顺便问一下，有没有本身就做开源的朋友，你们平时 PR 怎么 review 的？纯靠自觉吗（我是没那个毅力）。

**为什么这么写**：
- 开头讲自己的问题，不是讲项目功能——技术社区吃这个
- 承认"star 0""没经过实战检验"，反而更容易有人愿意试
- 结尾抛一个真问题邀请讨论，V2EX 最反感纯广告
- 给了完整可复制的配置，不让人自己猜

---

## 版本 B：Reddit（r/github、r/opensource、r/programming）

**Title**：

```
I built an open-source AI PR reviewer that runs in GitHub Actions (no third-party server)
```

**Body**：

> Most AI code-review tools are either expensive per-seat or send your code to someone else's server. Neither works well for small OSS projects.
>
> So I built one that runs entirely in your own Actions workflow: https://github.com/Lastron2000/open-pr-reviewer
>
> **What it does**
> - Reviews every PR on open/sync/reopen
> - Posts inline comments anchored to the exact diff line, tagged critical / warning / suggestion
> - Adds a summary comment and an `ai-reviewed` label
> - Skips issues it already flagged on earlier commits
>
> **Why self-hosted matters for OSS**
>
> Your diff goes straight to your own OpenAI key. Nothing lands on a third party's servers. For projects with any commercial sensitivity, that's the whole ballgame.
>
> **Setup** — drop this in `.github/workflows/`:
>
> ```yaml
> name: AI PR Review
> on:
>   pull_request:
>     types: [opened, synchronize, reopened]
> permissions:
>   contents: read
>   pull-requests: write
> jobs:
>   review:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: Lastron2000/open-pr-reviewer@v0.1.0
>         with:
>           openai_api_key: ${{ secrets.OPENAI_API_KEY }}
> ```
>
> Add `OPENAI_API_KEY` in repo settings and you're done.
>
> **Current state:** new project, 0 stars, 18 passing tests, no production battle-testing yet. Posting mainly to find people who'd try it and tell me where it breaks.
>
> MIT licensed. Issues welcome, especially ones that make it fail.
>
> Curious how everyone else here handles PR review — is it mostly people you trust, or do you actually review?
```

---

## 发完之后

**必须回帖**：有人在 issue 里问问题就及时回，哪怕"我也不确定"也比不回应强。
维护活跃度本身就是审核看的指标。

**把链接用上**：
- 贴到仓库 README（"有人用"）
- 贴到申请表的补充说明里（如果有这一栏）
- 如果 V2EX 帖子有回复，截个图存着

**别买 star**。文章提过这路子，但：
- 审核会看 star 增长的时间分布，一夜之间涨几百个反而可疑
- 刷来的 star 不会变成用户，审核追问"有谁在用"就露馅
- 几十块钱换 $1200 不值当——一旦被判定虚假信息，资格直接取消

自然攒的 10 个真 star，比 200 个刷的管用。
