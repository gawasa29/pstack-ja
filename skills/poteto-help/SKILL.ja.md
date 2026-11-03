---
name: poteto-help
description: Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question.
disable-model-invocation: true
---

# Poteto ヘルプ（Poteto help）

pstack についてのユーザーの質問に答え、そのまま送れるプロンプトを渡し、答えの出どころになったファイルをリンクします。ヘルプの質問では、作業を始めないでください。ユーザーが聞いたのはやり方であり、pstack の実行は実際にトークンを消費するので、プロンプトを送るのはユーザーに任せます。

「pstack を使ってこのバグを直して」のように作業を依頼するメッセージは、ヘルプの質問ではありません。[`poteto-mode`](../poteto-mode/SKILL.ja.md) を読み、その下で作業を行い、カスタムモードにすれば有効なままになることを一度だけ伝えます。

このファイルは、質問を、答えを持っているスキルとガイドページに対応づけます。詳細はそれらのファイルが持ちます。案内先のファイルは、引用する前に読み、このマップと食い違うときはそのファイルを信じてください。ここにあるリンクはインストール済みのプラグインの中を指していて、ユーザーが開けないことがあるので、ユーザーにはそのファイルの公開版、つまり `https://github.com/cursor/plugins/blob/main/pstack/` にパスを続けた URL を渡します。

## 何が必要かを見極める

メッセージと会話から必要性を推測します。「PR をレビューするのはどのスキル？」のように状況が名指しされていれば、そのセクションへ直接進みます。必要がまだ不明なら、次の選択肢で多肢選択の質問を 1 つだけ出し、選ばれたセクションだけに答えます。

- セットアップする
- `/poteto-mode` でタスクを始める
- 状況に合うスキルを選ぶ
- うまくいかなかった実行を直す
- pstack を自分好みにする

答えを変える状態を確認し、実際に変えるときだけ触れます。

- `~/.cursor/rules/pstack-models.mdc` がなければ、このユーザーでは `/setup-pstack` がまだ走っていないので、どの役割も既定のモデルを使います。
- プロジェクトに `verify-*` スキルも他のアプリ用ハーネスもなければ、エージェントにはアプリを動かすスクリプト化された手段がありません。変更が動くことを証明する話なら、`/create-verification-skill` に触れます。
- プロジェクトに形式検証スキルがなければ、テストが届く範囲より先の性質は何もチェックされません。競合、不変条件、テストがまれにしか踏まない他のケースの話なら、`/create-formal-verification-skill` に触れます。1 つあって、それが最後に同期したと記録しているコミットより後に、対象のコードが変わっているときは、そのコードに話が及ぶなら `/maintain-formal-verification-skill` に触れます。

モデルのルールがなく、それが問題になるときは、役割ごとのモデルと推論の予算を今選ぶかどうかを尋ねます。問題になるのは、ユーザーが初めてのとき、質問がセットアップやコストについてのとき、答えがどのモデルで動くかに依存するときです。質問は 1 チャットにつき最大 1 回です。必要性も不明なら、2 つの質問をまとめて出します。選択肢は 2 つです。

- 今すぐ: `/setup-pstack` を打ってもらい、そのうえで質問にも答えます。
- 後で: 質問に答え、`/setup-pstack` を走らせるまでどの役割も既定のモデルのままだという一行を添えます。

## セットアップする

1. チャットで `/add-plugin pstack` を実行するか、サイドバーの Customize からインストールします。
2. [`/setup-pstack`](../setup-pstack/SKILL.ja.md) を実行します。推論の予算を尋ね、役割ごとにモデルを対応づけ、ルールを書き出します。ルールは新しいチャットに適用されます。続いて、プロジェクトにまだなければ、検証スキルと形式検証スキルを 1 回ずつ生成するかどうかを尋ねます。
3. `/poteto-mode` にゴールと、合否の出るチェックを添えて、実際のタスクを始めます。

インストールしても、ユーザーがスキルを呼ぶまでは何も変わりません。ユーザーの言葉から読み込まれるのは `/setup-pstack` だけです。詳細は [README](../../README.ja.md) と [ガイドの 1 ページ目](../../docs/guide/01-setup.ja.md) にあります。最初のプロンプトの文面を一緒に考えることを申し出てください。手順は [`references/prompting.md`](references/prompting.ja.md) に従います。

コストが気がかりなら、トークンがどこへ行くのか、どうすれば少なく使えるのかを伝えます。pstack はサブエージェントとレビューのパネルに余分なトークンを使います。`/setup-pstack` を再実行し、より小さな予算か、より安いモデルを選びます。`auto` か `inherit-parent` にした役割はチャットのモデルで動くので、チャットが Auto か安いモデルで動いているときはトークンを節約できます。パネルの一覧を短くすると、実行するサブエージェントが減ります。1 項目につき 1 体です。`/poteto-mode` は、厳密さが要る作業のために取っておきます。

pstack は Cursor 向けに作られていますが、Claude Code にも `/plugin marketplace add cursor/plugins` でインストールでき、続けて `/plugin install pstack@cursor-plugins` を実行します。そこでは各コマンドに `pstack:` の接頭辞が付き、たとえば `/pstack:poteto-mode` になります。[Claude Code アダプタ](../../docs/harness/claude-code.ja.md) が Cursor の名前を対応づけ、Bugbot や Automations のように Cursor 専用の機能が要るステップは、一行の注記を付けて飛ばされます。

他のツールもスキルを読めます。Agent Skills 形式を使っているからです。ただし `/poteto-mode`、`/how`、`/why`、`/teach` を含むほとんどのワークフロー系スキルは、役割ごとのモデルを指定して Cursor のサブエージェントを起動しますし、カスタムモードと `/loop` は Cursor の機能なので、それらの部分は動かないかもしれません。

## `/poteto-mode` でタスクを始める

`/poteto-mode` はタスクをプレイブックに照合し、プレイブックのステップを todo リストにコピーし、ステップが必要とする他のスキルを実行します。飛ばしたステップは `skip: <reason>` としてリストに残ります。よいプロンプトは、ゴールと、終わったかどうかの見分け方を書きます。スキルは列挙しません。手書きの手順列は、プレイブックなら残すステップを落としたり順序を変えたりしがちだからです。文面を手伝う前に [`references/prompting.md`](references/prompting.ja.md) を読んでください。例は [ガイドの 2 ページ目](../../docs/guide/02-poteto-mode.ja.md) にあります。

`/poteto-mode` が有効なままかは、ユーザーがどう始めたかで決まります。

- `/poteto-mode` で Enter を押すと、スキルは 1 つのメッセージに付きます。チャットが進むにつれて薄れていきます。
- Mac なら Option+Enter、Windows なら Alt+Enter、またはスキルの項目にある Use as Mode で、カスタムモードになります。ユーザーがモードを抜けるまで毎ターン文脈に残り、雑談のターンには入りません。
- Cursor のドキュメントでは、カスタムモードは Agents Window と CLI にあるとされています。それ以外では、新しいタスクごとに `/poteto-mode` で始めます。

この話が出たら [Cursor のスキルのドキュメント](https://cursor.com/docs/skills) をリンクします。チャットの途中で「新しいタスク」と言えば、モードは新しいプレイブックに照合します。`/poteto-mode` は、プレイブックのステップが起動するサブエージェントにすでに `poteto-agent` を使っています。自分のサブエージェントで同じ流儀を得るには、`subagent_type: "poteto-agent"` で起動します。

## スキルを選ぶ

既定の答えは `/poteto-mode` です。ステップが必要とするとき、他のほとんどのスキルを実行します。プレイブックが与えるより多く、または少なく何かが欲しいときは、スキルを直接名指しします。勧める前にそのスキルを読み、プロンプトの例を 1 つ渡します。

| やりたいこと | スキル |
|---|---|
| 自明でないタスクを厳密に進める | [`/poteto-mode`](../poteto-mode/SKILL.ja.md) |
| エージェントが始める前に、ゴールと問題を理解したか確かめる | [`/in-your-own-words`](../in-your-own-words/SKILL.ja.md) |
| 送る前にプロンプトを、大きくではなく深く書き直す。一流の専門家なら何を足すか、その人たちの素材と手法、外部のチェック。プロンプトを返すだけで、タスクは実行しない | [`/sharpen`](../sharpen/SKILL.ja.md) |
| コードが今どう動くか、新しいコードをどこに置くべきかを知る | [`/how`](../how/SKILL.ja.md) |
| コードがなぜこの形なのか、数字がどこから来たのかを知る | [`/why`](../why/SKILL.ja.md) |
| 変更やサブシステムを、平易な説明で理解する | [`/teach`](../teach/SKILL.ja.md) |
| ある話題について、自分の直近の作業に追いつく | [`/recall`](../recall/SKILL.ja.md) |
| このチャットで最後のメッセージ以降に何が変わったかを、平易な言葉と小さな図で追いつく。ユーザーの判断待ちの項目はすべて列挙し、返答だけで判断できるようにする | [`/ketchup`](../ketchup/SKILL.ja.md) |
| `/ketchup` のように追いつくが、字幕付きの短いスライド動画で、判断待ちの案件はその下にテキストで示す | [`/ketchup-video`](../ketchup-video/SKILL.ja.md) |
| 小さな diff が自分の外で何を壊しうるかを知る | [`/blast-radius`](../blast-radius/SKILL.ja.md) |
| 関数の境界を越えるコードの前に、型とモジュールの形を決める | [`/architect`](../architect/SKILL.ja.md) |
| 1 つのブリーフに対して複数の試行を得て、最良の 1 つに統合する | [`/arena`](../arena/SKILL.ja.md) |
| スライスごとの並列チェックやワーカーのレースを、クラウドエージェントとして実行する | [`/swarm`](../swarm/SKILL.ja.md) |
| 別々のモデルに diff をレビューさせ、壊しにかからせる | [`/interrogate`](../interrogate/SKILL.ja.md) |
| 安いローカルテストがあるとき、テストファーストでバグを直す | [`/tdd`](../tdd/SKILL.ja.md) |
| `.ts` や `.tsx` の作業に TypeScript のルールを適用する | [`/typescript-best-practices`](../typescript-best-practices/SKILL.ja.md) |
| レビューの前にコメントを落とす。使うのは、そのコメントを書いていないレビュアー | [`/no-comments`](../no-comments/SKILL.ja.md) |
| 文章から AI の痕跡を取り除く | [`/unslop`](../unslop/SKILL.ja.md) |
| ドキュメント、RFC、README、PR の説明、コミットメッセージを、基準に沿って書く | [`/technical-writing`](../technical-writing/SKILL.ja.md) |
| 直前の返答を平易な言葉でもう一度聞く | [`/bro`](../bro/SKILL.ja.md) |
| エージェントに、アプリを動かして振る舞いを証明するスクリプト化された手段を与える | [`/create-verification-skill`](../create-verification-skill/SKILL.ja.md) |
| 検証スキルとその機能マップを、アプリに合わせ直す | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.ja.md) |
| テストがほとんど届かない競合、不変条件、その他の性質を形式検証する | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.ja.md) |
| 対象のコードが変わった後で形式検証を合わせ直し、失敗がドリフトなのかバグなのかを見極める | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.ja.md) |
| PM やデザイナーに、ユーザーが見ているものを、TLA+ モデルで検証したチャートとして見せる。ルールを破る各状態への最短経路付き | [`/statechart`](../statechart/SKILL.ja.md) |
| 性能の数値を、報告したり動いたりする前に吟味する | [`/benchmark-checklist`](../benchmark-checklist/SKILL.ja.md) |
| 大規模な、または横断的な変更を回す。離席してからレビューする変更も | [`/figure-it-out`](../figure-it-out/SKILL.ja.md) |
| 実行中に決定ログを残し、後で見直す | [`/show-me-your-work`](../show-me-your-work/SKILL.ja.md) |
| 役割ごとのモデルと推論の予算を選ぶ | [`/setup-pstack`](../setup-pstack/SKILL.ja.md) |
| 自分の仕事の習慣を、自分専用のモードスキルにする | [`/automate-me`](../automate-me/SKILL.ja.md) |
| 終わったタスクが教えたことを、スキルの編集に変える | [`/reflect`](../reflect/SKILL.ja.md) |
| このリポジトリでエージェントが同じ間違いを繰り返すのを止める | [`/correct`](../correct/SKILL.ja.md) |
| ボタンが webhook 経由で Grok Bot を起こすページを作る | [`/make-bot-ui`](../make-bot-ui/SKILL.ja.md) |
| pstack のどこに何があるか知る | `/poteto-help` |

このファイルの隣にあるスキルのディレクトリで、表にないものがあれば、その frontmatter を読んで description で振り分けます。`principle-*` のディレクトリは下の「原則」で扱います。

紛らわしい選び分け:

- `/how` はコードが何をするかを説明します。`/why` は理由を説明します。`/teach` は片方または両方を実行し、結果を平易に説明します。
- `/arena` は全ワーカーに同じブリーフを与え、最良の部分を統合します。`/swarm` は作業をスライスかレースに分け、1 つのレポートを返します。
- `/architect` は設計を決めた直後に実装します。コードを書く前に設計をレビューしたいときは "with checkpoint" を付けます。
- `/interrogate` は diff をレビューします。`/blast-radius` は diff の外の破損を探し、変更を安全にするたった 1 つの事実を証明します。
- `/recall` は直近のチャットをまたいで文脈を組み直します。`/ketchup` はユーザーの最後のメッセージ以降の、このチャットだけを扱います。特定の 1 つのチャットやブランチを再開するのは Session pickup プレイブックです。
- `/figure-it-out` は厳密な実行を 1 回設計します。Orchestrate プレイブックは、何日にもわたり多くの PR にまたがるプログラムを回します。Autonomous run プレイブックは、1 つのタスクを完了条件まで駆動します。

pstack にないもの:

- `/deslop`、`control-cli`、`control-ui` は `cursor-team-kit` プラグインで提供されます。
- `/loop` と `/create-skill` は Cursor の組み込みです。
- pstack に `/orchestrate` スキルはありません。Orchestrate は `/poteto-mode` のプレイブックです。スラッシュメニューに `/orchestrate` が出るなら、別のプラグインが提供しています。

## プレイブックと原則

プレイブックは `/poteto-mode` の中のステップ一覧であって、スキルではないので、スラッシュコマンドはありません。`/poteto-mode` の中では、タスクを説明すればどれかが選ばれ、次の言い回しは直接名指しします。

- "babysit this pr" または "check on pr 123" は Babysit を実行します。PR をマージ可能な状態まで駆動し、そこで止まります。ユーザーがマージ、取り込み（land）、出荷（ship）を頼まない限りマージしません。
- "land the stack" は Shipping を実行します。
- "take over this branch" は Session pickup を実行します。
- "pause safely" は Pause safely を実行します。
- "full autopilot on this queue" は Autopilot-full を実行します。"autopilot, don't merge" は Autopilot-stack を実行します。
- "run the eval playbook" は Eval を実行します。

`/poteto-mode` なしでは、"babysit this pr" のような言い回しが、同じ仕事のための Cursor 自身のスキルを起動することがあります。[`poteto-mode`](../poteto-mode/SKILL.ja.md) の Playbooks セクションに、すべてのプレイブックと適用する場面が並んでいます。[ガイドの 6 ページ目](../../docs/guide/06-verify-and-ship.ja.md) は PR を開き、babysit し、取り込むまでを扱います。

pstack に計画用のスキルはありません。Cursor の Plan Mode が並んで使えます。フェーズやスタックした PR にまたがる作業なら、`/poteto-mode` に計画を頼むと [Multi-phase plan プレイブック](../poteto-mode/playbooks/multi-phase-plan.ja.md) が走り、計画を書いて実装はしません。設計の問いなら、Prototype プレイブックか `/architect` がまずコードで決着させます。

原則は 1 ルールのスキルで、`/poteto-mode` が読んで返信の中で引用します。ユーザーが自分で呼ぶことはほとんどありません。代わりに名前で舵を取ります。たとえば "apply prove it works. show me the real output." です。`/principle-<name>` と打てば、必要に応じて読み込むこともできます。[ガイドの 8 ページ目](../../docs/guide/08-principles.ja.md) に一覧があります。

## うまくいかなかった実行を直す

| 症状 | 対処 |
|---|---|
| モードが数ターンで効かなくなった | Enter で始めたためです。カスタムモードとして始めるか、タスクごとに `/poteto-mode` で始めます。 |
| 質問が、直前のタスクの次のステップとして扱われた | "new task" と言うか、そのターンにモードは要らないと伝えます。 |
| 新しいモデルの選択が効かなかった | `/setup-pstack` のルールは新しいチャットに適用されます。新しいチャットを始めます。 |
| 実行が想定より高くついた | セットアップの下のコストの段落を見てください。 |
| スキルが自分で読み込まれなかった | ユーザーの言葉から読み込まれるのは `/setup-pstack` だけです。他はユーザーが打ったとき、または `/poteto-mode` が実行したときに読み込まれ、`/poteto-mode` がすべてのスキルを実行するわけではありません。 |
| 並列のエージェントが互いを上書きした | 各エージェントに専用のワークツリーを与えるか、それぞれに専用のマシンが割り当てられるクラウドエージェントとして実行します。 |
| 夜間の実行が動いたのに何も終わらなかった | `/loop` に必要なのは、時間ではなく合否の出るチェックです。[ガイドの 7 ページ目](../../docs/guide/07-overnight.ja.md) を見てください。 |
| 返答が、ビルドが通ったことだけを根拠に成功を主張している | 実際のコマンド、フロー、保存された値、プロファイルを求めてください。それが prove-it-works の原則です。 |

ずれていく実行には、[`references/prompting.md`](references/prompting.ja.md) に一行の舵取りがあります。[ガイドの 10 ページ目](../../docs/guide/10-recipes-and-pitfalls.ja.md) には、他の落とし穴と、コピーする価値のあるレシピがあります。

## pstack を自分好みにする

- [`/automate-me`](../automate-me/SKILL.ja.md) は、ユーザー自身の履歴から個人用のモードスキルの下書きを作ります。`/poteto-mode` と並べて使うものです。
- [`/reflect`](../reflect/SKILL.ja.md) は、セッションの後に、その教訓を、ユーザーが承認するスキル編集に変えます。
- `/poteto-mode write a skill for <workflow>` は、オーサリングのプレイブックを実行します。eval プレイブックは、スキルの変更をブラインドで試します。
- 挙動がおかしいスキルは、それ専用の PR で直します。それが壊れた機能の作業の中で直してはいけません。

[ガイドの 9 ページ目](../../docs/guide/09-make-it-yours.ja.md) が、これらのそれぞれを扱っています。

## 返答

答えを先頭に書きます。コードブロックのプロンプト例は最大 1 つ、当てはまるものがあれば [`references/recipes.md`](references/recipes.ja.md) から採って添え、そのあとにそのファイルへのリンクを置きます。ユーザーが地図全体を求めたのでなければ、短く保ちます。
