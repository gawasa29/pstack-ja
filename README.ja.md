# pstack

私は [poteto](https://x.com/poteto) です。社長でも CEO でもありませんが、Meta、Netflix、Cursor で数百万行のコードに携わってきました。React コアチームにも参加していて、React Compiler の開発と保守を手伝っています。

AI が中身の薄いコード（slop）を書きすぎている、という空気が強まっています。私もそう思います。20 人分の slop 職人のように出荷したいわけではありません。品質を伴わないスループットは目指すところではありません。速く行きたいなら、まず深く潜ることです。

**pstack はその答えです。** Cursor で高品質なコードを出荷するために、私が毎日使っているスキルそのものです。これで Cursor は本物のエンジニアリングチームになります。目的は LOC を最大化することではなく、むしろその逆です。pstack は、より少なく、より高品質なコードを書くためのものです。

**pstack は恐れのない並列化を実現します。** 1 体のエージェントに深く取り組み、検証可能で良いコードを書くと信頼できて初めて、安心して並列化できます。`poteto-mode` で複数のエージェントを立ち上げ、厳格なエンジニアリング原則を適用してくれると信頼してください。

**Cursor ならいいとこ取りができます。** フロンティアモデルにはそれぞれ長所と短所があります。pstack はどのモデルでも使えます。実際、私のスキルの多くはマルチモデルのワークフローで、各モデルの強みを活かしています。

fork して改善し、自分のものにしてください。PR も歓迎です！

## インストール

```bash
/add-plugin pstack
```

Claude Code の場合:

```bash
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
```

Claude Code は第三者のマーケットプレイスでは自動更新をオフのままにします。つまり pstack はインストールした版に固定されます。オンにするには `/plugin` を実行し、**marketplaces** タブを開き、`cursor-plugins` を選んで **enable auto-update** を選びます。一度だけ手動で更新するなら `claude plugin update pstack@cursor-plugins` を実行します。

Claude Code はプラグインのコマンドとエージェントに接頭辞を付けるので、`/poteto-mode` は `/pstack:poteto-mode` になります。[Claude Code アダプタ](docs/harness/claude-code.ja.md)が他の Cursor 名との対応をまとめています。Claude Code では `/pstack:setup-pstack` がモデルの選択を `~/.claude/rules/pstack-models.md` に書き、bugbot や automations のような Cursor 専用機能が必要なステップは一行の注記を出してスキップされます。

Claude Code は、リポジトリ直下の [`harness/pstack/`](https://github.com/cursor/plugins/tree/main/harness/pstack) から生成済みの pstack コピー（この README とガイドを含む）をインストールします。pstack を変更したら、リポジトリ直下で `node scripts/generate-pstack-harness-trees.mjs` を実行し、結果をコミットしてください。生成コピーが古いままだと CI が失敗します。

## はじめに

2 ステップです。

1. [`/setup-pstack`](skills/setup-pstack/SKILL.ja.md) を実行し、推論の予算を選び、使いたいモデルを選ぶ。
2. 厳格さが必要な作業では、いつでも [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) を使う。

初めての方は [pstack ガイド](docs/guide/README.ja.md) が、セットアップとプロンプトから検証、夜間実行までの最初の実タスクを案内します。詰まったときや、どのスキルが合うか分からないときは [`/poteto-help`](skills/poteto-help/SKILL.ja.md) に聞いてください。

これだけです。他のスキルは状況依存で、モードのスキルが必要に応じて使ってくれます。初期設定では、モードがモデルの強みで作業を分けます。コード系の委任（feature、refactoring、bug fix、perf、hillclimb）は grok へ、最も難しい変更・文章・判断は opus 5.5 へ。既定のパネルは opus 5.5 / grok です。[`/setup-pstack`](skills/setup-pstack/SKILL.ja.md) でどこでも変えられます。

## 使い方

タスクの開始時に [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) を使ってください。あなたの依頼を読み、プレイブックの集合から選び、各ステップが必要とする他のスキルを実行します。

タスクを打ち込む前に `/` メニューから `/poteto-mode` を選ぶと、Cursor がそのスキルをメッセージに添付します。

### とにかく [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) を使う

このスキルが主な近道です。厳格なエンジニアリング作業が必要なときはいつも使っています。23 のプレイブックが付いてきます。

```
/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro
first, then fix and verify.
```

```
/poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by
morning.
```

<details>
<summary>23 のプレイブック</summary>

| プレイブック | 用途 |
|---|---|
| [investigation](skills/poteto-mode/playbooks/investigation.ja.md) | 読み取り専用の質問。x はどう動くのか、y はなぜこう作られたのか、本当にそうか。 |
| [bug fix](skills/poteto-mode/playbooks/bug-fix.ja.md) | 不具合を再現し、根本原因を突き止め、実行時の証拠とともに直す。 |
| [perf](skills/poteto-mode/playbooks/perf-issue.ja.md) | 計測された遅さをトレースし、基準値に対して改善する。 |
| [hillclimb](skills/poteto-mode/playbooks/hillclimb.ja.md) | 1 つの指標を目標に向けて科学的に改善し続ける。仮説ループ、前後の計測、採用した改善ごとに 1 コミット。 |
| [runtime forensics](skills/poteto-mode/playbooks/runtime-forensics.ja.md) | 生きた症状（リーク、アイドル時の CPU スピン、画面の乱れ）を計装から診断する。 |
| [trace forensics](skills/poteto-mode/playbooks/trace-forensics.ja.md) | 取得済みのプロファイリング成果物（cpuprofile、trace、spindump、ヒープスナップショット）を診断する。 |
| [feature](skills/poteto-mode/playbooks/feature.ja.md) | 新しい、あるいは変わる振る舞いを、名前を付けたデータの形から組み立てる。 |
| [refactoring](skills/poteto-mode/playbooks/refactoring.ja.md) | 構造や形を変える、振る舞いを保つ変更。 |
| [prototype](skills/poteto-mode/playbooks/prototype.ja.md) | 使い捨ての試作で、設計や振る舞いの判断を安く決める。あるいは実験で決着をつける。 |
| [visual parity](skills/poteto-mode/playbooks/visual-parity.ja.md) | 2 つの実装の間でピクセル単位の UI 一致を取る。 |
| [authoring a skill](skills/poteto-mode/playbooks/authoring-a-skill.ja.md) | SKILL.md を書く、編集する。 |
| [eval](skills/poteto-mode/playbooks/eval.ja.md) | スキルやプロンプトの変更がエージェントの振る舞いにどう効くかを、ブラインドで試す。 |
| [babysit](skills/poteto-mode/playbooks/babysit.ja.md) | PR やスタックをマージ可能な状態まで進める。コンフリクト、レビューのスレッド、CI。 |
| [shipping](skills/poteto-mode/playbooks/shipping.ja.md) | グリーンなスタックを独立に検証し、検証済みの連続した範囲を下から順に GitHub（既定）または origin 経由で取り込む。 |
| [autonomous run](skills/poteto-mode/playbooks/autonomous-run.ja.md) | 止まらずに長いタスクを完遂させる。 |
| [orchestrate](skills/poteto-mode/playbooks/orchestrate.ja.md) | 1 つの調整役チャットに任せる常設プロジェクト。数日がかり、多数のスタック PR、サブエージェントの群れ。 |
| [autopilot-full](skills/poteto-mode/playbooks/autopilot-full.ja.md) | 独立した PR を 1 PR 1 オーナーでマージまで進める。swarm がコード完了時点の head を検証し、その後の変更ごとに新しい検証を付ける。 |
| [autopilot-stack](skills/poteto-mode/playbooks/autopilot-stack.ja.md) | 1 本の線形なベースブランチのスタックを組み立てて検証し、運用者がレビューして取り込む。 |
| [session pickup](skills/poteto-mode/playbooks/session-pickup.ja.md) | 先行エージェントの進行中の作業を再開する、引き継ぐ。 |
| [pause safely](skills/poteto-mode/playbooks/pause-safely.ja.md) | 進行中の作業をきれいに中断し、あとで再開できるようにする。 |
| [multi-phase plan](skills/poteto-mode/playbooks/multi-phase-plan.ja.md) | フェーズやスタック PR にまたがる作業。 |
| [worktree cleanup](skills/poteto-mode/playbooks/worktree-cleanup.ja.md) | マージ済み・放置されたワークツリーや古い iOS シミュレータを安全確認のうえで間引いて、ディスクを取り戻す。 |
| [opening a pr](skills/poteto-mode/playbooks/opening-a-pr.ja.md) | 小さく順序立てたコミットから、Conventional Commits のタイトルとブリーフィング形式の本文で PR を開く。他のすべてのプレイブックの最後に呼ばれる。 |

</details>

呼ばれると次のことをします。

1. タスクを [プレイブック](./skills/poteto-mode/playbooks/) に照合し、その手順をそのまま先頭項目にコピーした todo リストを開く。
2. ステップが発火するたびに、他のスキルへルーティングする。
3. 読み手と保守者のために枠組みを整えた、slop でない返答を書く。

ルールとプレイブックの全体は [`skills/poteto-mode/SKILL.md`](skills/poteto-mode/SKILL.ja.md) にあります。

[`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) をターンをまたいで効かせ続けるには、`/` メニューから選んで enter ではなく option+enter（Mac）または alt+enter（Windows）を押します。すると[カスタムモード](https://cursor.com/docs/skills#using-a-skill-as-a-custom-mode)になり、Cursor がエージェントウィンドウと CLI で提供します。モードを抜けるまで、毎ターン文脈に残ります。普通に enter を押すと 1 メッセージにだけ添付されます。

[`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) は Cursor の `/loop` コマンドと非常に相性が良いです。厳格さを犠牲にせず、何時間も Cursor に働かせられます。

## スキル

[`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) は、ステップが必要とするときにこれらの多くを実行します（`how`、`why`、`architect`、`arena`、`swarm`、`interrogate`、`unslop`、`no-comments`、`technical-writing`、`tdd`、そして各原則）。下の表は、自分で直接使いたいときのためのものです。

```
/how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
/interrogate review this pr.
```

<details>
<summary>すべてのスキル</summary>

| スキル | 使うとき |
|---|---|
| [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) | 自明でないタスクの既定の入口。 |
| [`/poteto-help`](skills/poteto-help/SKILL.ja.md) | pstack が初めて、またはどのスキル・プレイブック・原則が合うか分からないとき。何をしたいのかを聞き出し、その部分に答え、打ち込むプロンプトを渡す。`/poteto-help` と打ったときだけ動く。 |
| [`/in-your-own-words`](skills/in-your-own-words/SKILL.ja.md) | 作業を始める前に、エージェントにゴールと問題を言い直してほしいとき。`/in-your-own-words` と打ったときだけ動く。 |
| [`/sharpen`](skills/sharpen/SKILL.ja.md) | 送る前にプロンプトを大きくではなく深くしたいとき。一流の専門家なら頼まれなくてもやることは何か、その人が着手する生の材料、使う手法と道具、結果が正しいことを外部で確かめる方法を挙げる。書き直したプロンプトを返し、選択肢は開いたままにする。タスクは実行しない。`/sharpen` と打ったときだけ動く。 |
| [`/how`](skills/how/SKILL.ja.md) | サブシステムがどう動くかの解説がほしいとき。 |
| [`/why`](skills/why/SKILL.ja.md) | なぜこう作られたのかを知りたいとき。実行時に利用可能な MCP を見つけ、証拠の各カテゴリ（ソース管理、課題管理、長文ドキュメント、リアルタイムチャット、インフラの可観測性、エラー追跡、分析基盤）を並列に問い合わせる。 |
| [`/recall`](skills/recall/SKILL.ja.md) | 作業を始める・再開するときに、ある話題についての直近の文脈を自分のチャット履歴と共有記録から再構築し、簡潔な現状ブリーフとして返してほしいとき。 |
| [`/ketchup`](skills/ketchup/SKILL.ja.md) | 最後のメッセージ以降にこのチャットで何が変わったかを、平易な言葉と小さな図で知りたいとき。あなたの判断待ちの項目をすべて、返答だけで判断できる形で並べる。そのために長くなってもよい。 |
| [`/ketchup-video`](skills/ketchup-video/SKILL.ja.md) | `/ketchup` のキャッチアップを、短い無音のスライド動画として見たいとき。判断待ちの項目はその下にテキストで並ぶ。 |
| [`/blast-radius`](skills/blast-radius/SKILL.ja.md) | 小さく見える変更が他に何を壊しうるかを知りたいとき。安全だと言える根拠となる 1 つの事実を、主張ではなく実行したコードで示す。 |
| [`/architect`](skills/architect/SKILL.ja.md) | 関数の境界を越えるコードを書く前に、呼び出し側の使い方、型、モジュールの形を先に固めたいとき。 |
| [`/arena`](skills/arena/SKILL.ja.md) | 同じものに対して N 通りの並列の試みを出し、それぞれの良いところを拾いたいとき。 |
| [`/swarm`](skills/swarm/SKILL.ja.md) | 異なる切り口やレースに N 体の並列ワーカーを置き、1 つの報告に集約したいとき。 |
| [`/interrogate`](skills/interrogate/SKILL.ja.md) | diff があり、別のモデルにそれを壊しにいってほしいとき。厳しいコード品質の観点も含む。 |
| [`/automate-me`](skills/automate-me/SKILL.ja.md) | 自分の `-mode` スキルを、実際の働き方から下書きしてほしいとき。 |
| [`/make-bot-ui`](skills/make-bot-ui/SKILL.ja.md) | ボタンが Webhook 経由で Grok Bot を起こすページやダッシュボードがほしいとき。送信キーの受け渡しと Tailscale も含む。 |
| [`/setup-pstack`](skills/setup-pstack/SKILL.ja.md) | pstack が役割ごとに使うモデルを選びたいとき。利用可能なモデルを検出し、設定ルールを書く。 |
| [`/reflect`](skills/reflect/SKILL.ja.md) | 長いタスクが着地したあと、そのレシピをスキルの編集として残したいとき。 |
| [`/correct`](skills/correct/SKILL.ja.md) | 同じ間違いで何度もエージェントを直しているとき。履歴から間違いの種類を掘り、効く最も高い層（アーキテクチャ、次に型、lint、CI、次にテスト、ドキュメントは最後）でそれぞれを直し、各ルールとそれを強制するものを対にした表を保つ。 |
| [`/teach`](skills/teach/SKILL.ja.md) | 変更やサブシステムを要約ではなく本当に理解したいとき。how と why を実行し、図を積み上げながら 1 つの平易な説明に織り上げる。 |
| [`/tdd`](skills/tdd/SKILL.ja.md) | バグを直していて、ローカルで安く回せるテスト経路があるとき。まず落ちるテストを書き、それから直す。 |
| [`/benchmark-checklist`](skills/benchmark-checklist/SKILL.ja.md) | ベンチマークを回した、あるいは高速化や退行を測ったとき。報告や判断の前に、その数字を検証する（リミッタ、チューニング、誤差、繰り返し実行、エンドツーエンドでの妥当性）。 |
| [`/no-comments`](skills/no-comments/SKILL.ja.md) | レビューの前にコメントをはがしたいとき。Comment Sicko を起動し、受け入れた指摘を直し、主張された制約にはエンコード案を出す。 |
| [`/typescript-best-practices`](skills/typescript-best-practices/SKILL.ja.md) | TypeScript を読む・編集するとき。型システム規律の原則を構文に落とし込む。 |
| [`/figure-it-out`](skills/figure-it-out/SKILL.ja.md) | 同梱のプレイブックが合わないとき。そのタスク用の厳格で監査可能なプレイブックを設計する。 |
| [`/show-me-your-work`](skills/show-me-your-work/SKILL.ja.md) | レビューできる判断の記録がほしいとき。判断をコミット可能な TSV に記録する。 |
| [`/create-verification-skill`](skills/create-verification-skill/SKILL.ja.md) | プロジェクトにアプリの振る舞いを証明するスクリプト化された手段がないとき。機能マップ付きのプロジェクト固有の検証スキルを、任意の言語・プラットフォーム向けに生成する。 |
| [`/maintain-verification-skill`](skills/maintain-verification-skill/SKILL.ja.md) | 検証スキルの機能マップがアプリからずれているとき。ソースの一巡と、実際に動かしての確認 1 回、証明済みの修正の PR は最大 1 本。 |
| [`/create-formal-verification-skill`](skills/create-formal-verification-skill/SKILL.ja.md) | レース、リトライ、状態機械、パーサ、unsafe なコードを壊すケースにテストが届かないとき。1 つの性質を適した道具で検証し、変更のたびに再確認するプロジェクト固有のスキルを生成する。 |
| [`/maintain-formal-verification-skill`](skills/maintain-formal-verification-skill/SKILL.ja.md) | 形式検証が対象にしているコードが前回の確認から変わったとき。モデル、ハーネス、性質をコードに合わせて更新し、再実行し、各失敗が検証側のずれかコードのバグかを言う。 |
| [`/statechart`](skills/statechart/SKILL.ja.md) | 振る舞いの持ち主に仕様を読ませるのではなく見せたいとき。TLA+ モデルを確認し、ユーザーに見えるものを mermaid のステートチャートとして描き、ルールを破る状態に印を付け、それぞれへの最短経路を示す。 |
| [`/unslop`](skills/unslop/SKILL.ja.md) | 文章を片付けたいとき。AI っぽさを取り除く。 |
| [`/bro`](skills/bro/SKILL.ja.md) | 直前のメッセージを、専門用語なしの平易な言葉で言い直してほしいとき。 |
| [`/technical-writing`](skills/technical-writing/SKILL.ja.md) | ドキュメント、RFC、README、PR の説明、コミットメッセージ向けの階層化された文書標準（Diátaxis + Google developer style + STE + Global English）。 |

</details>

### 例

基本はタスクの最初に [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) と打ち、プレイブックへの振り分けは任せます。他のスキルはステップが必要になったときに発火します。いくつかは直接使います。

<details>
<summary>すべての例</summary>

```
bug fix:           /poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              /poteto-mode a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           /poteto-mode build a small feature behind a feature flag. verify it really works.
prototype:         /poteto-mode build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       /poteto-mode open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     /poteto-mode i'm going to bed. land the stack even if ci flakes. i want
                   everything merged by morning.
babysit:           /poteto-mode check on pr 123. anything outstanding?
visual parity:     /poteto-mode the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     /poteto-mode i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               /how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               /why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. /architect
                   this first.
arena:             /arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
swarm:             /swarm check every package under packages/ against its check.sh. one worker per
                   package. one report.
interrogate:       /interrogate review this pr.
tdd:               /tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           /reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
correct:           /correct
show-me-your-work: /show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       /automate-me
help:              /poteto-help which skill should i use to review this branch?
```

</details>

## `poteto-agent` と Comment Sicko のサブエージェント

[`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) は、それを受け取ったチャットの中で動きます。そのチャットがプレイブック、todo リスト、すべてのサブエージェントの起動を持ちます。

pstack は [`subagent_type: "poteto-agent"`](agents/poteto-agent.ja.md) も、実行中に起動される委任先のラッパーとして同梱しています。これは作業に入る前に `poteto-mode` を、インラインの原則索引まで含めて全文読みます。`generalPurpose` で代用するとこの読み込みが抜けて、ずれていきます。プレイブック自体を実行するために `poteto-agent` を起動しないでください。

[`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) と [`subagent_type: "poteto-agent"`](agents/poteto-agent.ja.md) は同じラッパーを通ります。

pstack は [Comment Sicko](agents/comment-sicko.ja.md) も同梱しています。コメントだけを見る読み取り専用のレビュアーで、`subagent_type: "comment-sicko"` として使えます。通常は [`/no-comments`](skills/no-comments/SKILL.ja.md) 経由で呼び、直接は呼びません。

## 原則

1 原則につき 1 本、短いスキルが 24 本あります。`poteto-mode` はそれらをインラインで索引化し、タスク開始時にその索引を読みます。独立したファイルがあるのは、他のスキルが原則を名前で参照できるようにするためと、索引が各原則の完全なルールを指せるようにするためです。

<details>
<summary>24 の原則すべて</summary>

| 原則 | グループ | ルール |
|---|---|---|
| [laziness-protocol](skills/principle-laziness-protocol/SKILL.ja.md) | core | 削除と、問題を解く最小の変更に傾ける。 |
| [foundational-thinking](skills/principle-foundational-thinking/SKILL.ja.md) | core | ロジックを書く前に適用する。中核の型とデータ構造を選ぶこと、足場と機能のどちらを先に進めるか、並行して動く主体が何を共有するか。データ構造を正しくすれば、下流のコードは自明になる。 |
| [redesign-from-first-principles](skills/principle-redesign-from-first-principles/SKILL.ja.md) | core | その要件が初日から基盤的な前提だったかのように設計し直す。後付けするのではない。 |
| [attack-the-premise](skills/principle-attack-the-premise/SKILL.ja.md) | core | 同じ前提を共有する修正が 2 つ以上、同じゲートで失敗したときに適用する。前提を書き出し、それを直接試してから、次の前提依存の修正を書く。 |
| [subtract-before-you-add](skills/principle-subtract-before-you-add/SKILL.ja.md) | core | まず死んだ重み、重複した検証、スタブへの参照を取り除き、より単純な土台の上に建てる。 |
| [minimize-reader-load](skills/principle-minimize-reader-load/SKILL.ja.md) | core | 問いと答えの間の層の数、読み手の頭の中の隠れた状態を数える。呼び出しが 1 つだけのラッパーを畳み、可変のスコープを縮める。 |
| [outcome-oriented-execution](skills/principle-outcome-oriented-execution/SKILL.ja.md) | core | 明示的なフェーズ境界を持つ計画的な書き換えや移行に適用する。目標のアーキテクチャに収束させる。捨てるだけの互換コードで、中途半端な状態を滑らかに保たない。 |
| [experience-first](skills/principle-experience-first/SKILL.ja.md) | core | プロダクト、UX、機能範囲のトレードオフで、実装の都合よりユーザーの喜びを選ぶ。粗い機能を多く出すより、磨いた機能を少なく出す。 |
| [exhaust-the-design-space](skills/principle-exhaust-the-design-space/SKILL.ja.md) | core | 前例のない新しいインタラクションやアーキテクチャの判断では、2〜3 の競合する試作を作り、並べて比べてから決める。 |
| [build-the-lever](skills/principle-build-the-lever/SKILL.ja.md) | core | 非自明な作業すべて（一括作業だけでなく、編集、移行、分析、チェック）に適用する。手作業ではなく、それを実行する・証明する道具（codemod、スクリプト、ジェネレータ、サブエージェントが従うスキル）を作る。その道具こそがレビュアーが再実行できる成果物になる。 |
| [model-the-domain](skills/principle-model-the-domain/SKILL.ja.md) | architecture | ドメインを、散らばった条件分岐ではなく構造として表現する。 |
| [boundary-discipline](skills/principle-boundary-discipline/SKILL.ja.md) | architecture | ガードはシステムの境界（CLI、設定、ネットワーク、外部 API）に集中させる。内部の型を信頼し、ビジネスロジックは純粋関数に保つ。 |
| [type-system-discipline](skills/principle-type-system-discipline/SKILL.ja.md) | architecture | 不正な状態を表現できなくする。意味を持つプリミティブにはブランドを付ける。外部データは境界でパースする。バリアントは網羅する。正となるスキーマから導出する。 |
| [make-operations-idempotent](skills/principle-make-operations-idempotent/SKILL.ja.md) | architecture | 途中まで実行されていても、同じ最終状態に収束させる。 |
| [migrate-callers-then-delete-legacy-apis](skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.ja.md) | architecture | 呼び出し側を移行し、同じ波で古い API を削除する。互換層で残さない。 |
| [separate-before-serializing-shared-state](skills/principle-separate-before-serializing-shared-state/SKILL.ja.md) | architecture | まず共有そのものをなくす。1 つの共有ライターが本当の不変条件であるときだけ、構造として直列化する。 |
| [prove-it-works](skills/principle-prove-it-works/SKILL.ja.md) | verification | タスクを終え、完了と言う前に適用する。代理や自己申告や「コンパイルが通った」ではなく、本物の成果物（機能を実行する、実際の値を読む、diff を見る）で確かめる。 |
| [fix-root-causes](skills/principle-fix-root-causes/SKILL.ja.md) | verification | 症状をたどり、システムが最初に壊れた場所まで戻って、そこで直す。ガードは、扱う状態が正当なものであるときだけ修正になる。 |
| [sequence-verifiable-units](skills/principle-sequence-verifiable-units/SKILL.ja.md) | verification | 多段の作業（一括変更、移行、似た編集の連続）と、コミットや PR の積み方に適用する。作業を小さな単位に分け、各単位が検証可能な状態で終わるようにし、次に進む前に確認する。そして、その順序自体がレビュアーへの証明になるように届ける。 |
| [test-behavior-not-implementation](skills/principle-test-behavior-not-implementation/SKILL.ja.md) | verification | テストを書く、変える、残すときに適用する。コードの利用者が観測できるものを assert する。そうすれば、振る舞いが壊れたときにテストが落ち、内部だけが変わったときは通り続ける。 |
| [explain-the-number](skills/principle-explain-the-number/SKILL.ja.md) | verification | 測った数字（高速化、退行、スループット、レイテンシ、eval の結果）を信じる・報告する・動く前に適用する。何がその値を制限しているかを見つけ、思っている作業とは別のものを測っていないか排除する。 |
| [guard-the-context-window](skills/principle-guard-the-context-window/SKILL.ja.md) | delegation | 大量のものはサブエージェントへ回す。生のペイロードではなく要約をメインのスレッドに残す。 |
| [never-block-on-the-human](skills/principle-never-block-on-the-human/SKILL.ja.md) | delegation | 前に進め、結果を見せ、人間が後から軌道修正すればよい。確認を取るのは不可逆な操作だけ。 |
| [encode-lessons-in-structure](skills/principle-encode-lessons-in-structure/SKILL.ja.md) | meta | ルールを、文章ではなく lint、メタデータのフラグ、実行時チェック、スクリプトとしてエンコードする。 |

</details>

## ここには含まれないもの

`poteto-mode` が参照するが同梱していないものがいくつかあります。

- `/deslop` と `deslop` スキルは `cursor-team-kit` プラグインに入っています。
- `control-cli`（CLI と TUI 向け）と `control-ui`（ブラウザ、Electron、Web 向け）も `cursor-team-kit` に入っています。
- `/create-skill` は Cursor の組み込みです。Cursor は PR を見張る `/autopilot` も組み込みで提供します。`poteto-mode` の中では、PR の状態確認の依頼は [babysit プレイブック](skills/poteto-mode/playbooks/babysit.ja.md) に行きます。

フルセットが欲しいときは、pstack と一緒に `cursor-team-kit` をインストールしてください。

## なぜ計画用のスキルがないのか

Cursor には優れた plan mode があり、pstack とよく合います。ですが個人的に、計画は信じていません。最高の仕様はコードです。計画を作りたい場合も [`/poteto-mode`](skills/poteto-mode/SKILL.ja.md) がカバーしますが、既定ではありません。

## 自分のものにする

`poteto-mode` は私のスタイルです。あなたはそのままがいいとは限りません。

[`/automate-me`](skills/automate-me/SKILL.ja.md) と打ってください。直近のトランスクリプトを掘り、実際の働き方から `<あなたの名前>-mode` スキルを下書きし、その下で pstack にルーティングします。pstack を土台に残しつつ、`poteto-mode` と並ぶ自分のルーティングスキルができます。

モデルも設定できます。[`/setup-pstack`](skills/setup-pstack/SKILL.ja.md) と打つと、利用できるモデルを検出し、役割（コード、判断、レビューのパネル）ごとにモデルを対応付ける、常時適用の小さなルールを書きます。どのスキルもそのルールを読み、ルールがなければ妥当な既定に戻るので、変えたい部分だけ上書きすれば済みます。

既定が変わったとき、変更前に書かれたルールは古い既定を固定したままです。その役割の行を消すか、ファイルを消してから `/setup-pstack` を再実行してください。再実行では、既定と異なるモデルになっている役割は保持されます。

## オートメーション

pstack は休眠状態の [benny オートメーションパック](./automations/benny/) も同梱しています。benny は Slack の不具合報告をトリアージし、確認できた不具合を実際の UI の証拠とともに再現・修正します。同梱ファイルはスラッシュスキルとしては登録されません。

セットアップするには、Cursor で [`FOR_AGENTS.md`](automations/benny/FOR_AGENTS.ja.md) を指定します。セットアップはパックを対象リポジトリの `.cursor/automations/benny/` にコピーし、そこで pstack を有効にして共有スキルを使えるようにし、ユーザー設定はコピーしたパックの外に保ちます。benny は Cursor の automations 上で動くので、Cursor 専用です。

## ライセンス

MIT
