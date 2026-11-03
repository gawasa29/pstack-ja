### 多段階・複数 PR の計画（Multi-phase or multi-PR plan）

**計画はあなたが持ちます。コードではありません。計画は、オーナーが1つずつ実行し、オペレーターが証拠から監査するチェックリストです。** 成果物は計画です。実装はしないでください。

1. 変更が1〜2ファイルで、アプローチも明らかなときは計画を省きます。その旨を伝えて止めます。
2. 書く前に、未解決の問いをプロトタイプで決着させます。問いごとに `playbooks/prototype.md` を実行します。ブランチ、SHA、スクリーンショットは付録 A のために残します。オペレーターに聞くのは、実行では決着できないプロダクト判断や好みの判断だけです。選択肢を添えて聞きます（**never-block-on-the-human** 原則スキル）。
3. サブエージェントで調べます。`subagent_type: "poteto-agent"` を使い、モデルを明示します（Subagents セクション、**guard-the-context-window** 原則スキル）。サブエージェントごとに、その作業に合った推論レベルと、fast か standard の速度を選んでください（Subagents セクション参照）。各自はファイルのポインタ、慣習、テストコマンド、入口を返します。中身をそのまま貼り付けさせません。
4. 下の骨組みを計画ファイルにコピーし、すべてのプレースホルダーを埋めます。オペレーターがパスを指定しない限り、エージェントストアの `docs/` の下に書きます。見出しとサブブロックはすべて、示された順序のまま残します。PR 1本につき1セクションです。PR 1本は、それ自身の証拠を持つ1つの変更です（**sequence-verifiable-units** 原則スキル）。**How to read this** で実行プレイブックを名指しします。その実行がマージまで行うなら `playbooks/autopilot-full.md`、オペレーターが PR を取り込むなら `playbooks/autopilot-stack.md` を選びます。常設のプログラムには `playbooks/orchestrate.md` を使います。
5. `/technical-writing` に従って全面的に書き、そのうえで `/unslop` を適用します。本文は Diátaxis の1つのモード、how-to です。付録が説明とリファレンスを持ちます。各見出しは、作業か発見を述べます。長いダッシュを使いません。文中のコロンも使いません。
6. `node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan.md>` を実行し、出力された行をすべて直します（**encode-lessons-in-structure** 原則スキル）。
7. 引き渡します。計画のパスとスクリプトの出力を投稿して、止まります。実行は、計画が名指しした実行プレイブックの下で、オペレーターの明示的な許可から始まります。

**検証。** テストだけでは検証として十分ではありません。PR が検証済みと言えるのは、unit、live、perf の3つのボックスがすべてチェックされたときだけです（**prove-it-works** 原則スキル）。この文が検証のルールであり、すべての検証ブロックはこの文で始まります。live のブロックは必須です。PR の head で10本のレーンが、**swarm** スキルに従い、`swarm workers` モデル（既定は `grok-4.7-xhigh-fast`）で、制御スキルを通して本物のサーフェスを動かします。各レーンは1つのボックスで、具体的なシナリオ、保存するスクリーンショット、合格の述語を持ちます。1本は **Regression lane against trunk.** です。trunk と head で同じ、支えになるシナリオを走らせます。trunk にその機能が無いなら、その事実を記録し、trunk の結果をでっち上げる代わりに、diff が足す振る舞いと、ユーザーが待つ最終状態をゲートします。性能のゲートは両側です。trunk と head の両方が、名指しした指標を出さなければなりません。trunk に機能が無いなら、diff が足す作業を切り出し、その作業とユーザーが待つ端から端までの状態に絶対の予算を設定します。条件の違うシナリオ同士の比を主張してはいけません。perf のブロックは、指標、インターリーブした計測、先に測る trunk のベースライン、失敗となる数値を含むルールを名指しします。インタラクションを変える PR はレビューゲート付きです。オペレーターがマージ前に、スクリーンショットと動画を添えてチャットでレビューします。インタラクションを変えない PR は `**Review gate.** None. <PR id> is not review-gated.` と書き、その下にボックスを置きません。

**制御スキル。** サーフェスで選びます。ブラウザ、Electron、Web UI は `cursor-team-kit` の `control-ui` を使います。CLI と TUI は `cursor-team-kit` の `control-cli` を使います。ネイティブモバイルは、リポジトリが持っているシミュレータ操作のスキルを使います。2つのサーフェスに触れる PR は、両方にレーンを持ちます。制御スキルの無いサーフェスは付録 C のリスクとし、その live のブロックで各レーンがどう動かすかを名指しします。

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `pstack/skills/poteto-mode/playbooks/<execution playbook>.md`. <Who merges, and which PR ids are the operator's items that stop at merge-ready.>

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] Read these from trunk at program start. Re-read them at every tick.
  - [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/<execution playbook>.md`
  - [ ] `git show origin/main:pstack/skills/swarm/SKILL.md`
  - [ ] `git show origin/main:<control skill path>`
  - [ ] `git show origin/main:pstack/skills/poteto-mode/playbooks/opening-a-pr.md`
  - [ ] `git show origin/main:pstack/skills/<each other leaf skill the program uses>`
- [ ] On the operator's go, arm the audit tick as `/loop 1h` with the tick prompt below. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk. Audit the operation against it and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the operator's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`; if `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, per **Opening a PR**. Use the run's built-in PR tool when it has one, else `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run `/deslop` before each commit and `/no-comments` before review.
- [ ] Triage every Bugbot and security-reviewer comment per `../references/bugbot-triage.md`.
- [ ] Rebase onto current trunk before the code-ready report and babysit. Keep that merge base in fix rounds. Rebase again only at merge prep, on a `git merge-tree` conflict with trunk, on a CI failure that comes from a change on trunk, or when a known concurrent change to the same files lands.

### Verdict and merge, for every PR

- [ ] A full swarm runs once, at the code-ready head. Another full swarm runs only for new behavior, a redesign, or a large new diff. A rebase, a merge-conflict resolution, or a minor fix gets a single verifier at the new head, and a wording-only change gets none. Run each full swarm per `pstack/skills/swarm/SKILL.md`. One gates lane. The ten live lanes from the PR's **Verify, live** block. The perf lane from its **Verify, perf** block. Two or more audit lanes, each with its own focus, that read the diff and the receipts and distrust the PR body. The root audits the receipts in the merge-ready report before the verdict.
- [ ] Judge every finding by the execution playbook's blocking rule. The verdict is clean when none blocks. A failure on trunk behavior in a lane marked `Regression lane against trunk.` is recorded against trunk and does not block the PR. A new head gets a fresh verdict, except for results that stay valid under the patch-id rule in `playbooks/shipping.md`.
- [ ] <The merge or handoff rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for every live lane

Each live lane runs on its own cloud VM at the PR head. Drive through `control-ui` or `control-cli` from `cursor-team-kit`.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the control skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot to `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png` and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `<swarm workers model>` at the PR head, per the boot recipe.

- [ ] Lane 1. Regression lane against trunk. Run <the same load-bearing scenario> at trunk and head. If trunk lacks the feature, record that and gate <the behavior the diff adds plus the end state the user waits for>. Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 3. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 4. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 5. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 6. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 7. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 8. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 9. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 10. <Scenario.> Save `<slug>.png`. Pass when <predicate>.

**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

- [ ] Metric. <What is measured at both trunk and head. If trunk lacks the feature, also name the diff-added work and the end-to-end state the user waits for.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved. Both sides must produce the metric.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails. If the scenarios differ, add absolute budgets for the diff-added work and the user-visible end state instead of an invalid ratio.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change on a lane VM. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the operator's click.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <The owner squash-merges its own PR, or the root appends it to the base-branch stack and the operator lands it bottom-up.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs get `pstack/skills/how/SKILL.md` and `pstack/skills/interrogate/SKILL.md`. The trail per `pstack/skills/show-me-your-work/SKILL.md`.>
````

**返信内容：** 計画のパス、PR の id とその依存関係、レビューゲート付きの集合、プロトタイプが証明したことと未証明のままのこと、チェックスクリプトの出力。
