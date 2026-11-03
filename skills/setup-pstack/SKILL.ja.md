---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# pstack をセットアップする（Setup pstack）

`~/.cursor/rules/pstack-models.mdc` を書きます。これは常に適用されるルールで、pstack がロールごとに使うモデルを設定します。

## 手順

### 1. 利用できるモデルを検出する

このセッションで `Task` サブエージェントに渡せるモデルのスラッグを列挙します。これが信頼できる情報源です。Cursor が、ユーザーが利用権を持つモデルを一覧する API や CLI も提供しているなら、網羅性のためにそちらを優先します。どちらでも検出できない場合は、アクセスできるスラッグを貼るようユーザーに頼みます。利用可能だと確認していない実在のスラッグを書くことは決してありません。エイリアス `inherit-parent` と `auto` は、検出されるスラッグではありませんが、常に有効です。

### 2. 現在の状態を読み込む

ロールとモデルの既定の対応は、下の手順 5 に示すルールの形です。`~/.cursor/rules/pstack-models.mdc` がすでにある場合は、それを読み、`# budget` 行と各ロールの値を現在の選択として扱います。無ければ、その既定値から始めます。ロールが手順 5 に無い行、たとえば `how critics` は、廃止されたロールのものです。削除します。

### 3. 予算を決め、対応づけ、確認する

**(a) 予算を尋ねる。** 自由記述よりも AskQuestion を優先します。次の 4 つの選択肢を、この正確なラベルで提示し、ルールに記録があれば現在の予算を伝えます。ルールが無ければ、`large` がスキルの既定値に一致すると伝えます。

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) 適用する。** スキルの既定値から作業用の表を作ります。再実行のときは、ファミリー、リスト、エイリアス（`inherit-parent`、`auto`）で変更したロールをそのまま保ちます。`unlimited`、`large`、`medium`、`small` は、パネルのエントリも含め、すべての実在のスラッグの effort トークンを `max`、`xhigh`、`high`、`medium` に設定します。effort トークンとは、`max` > `xhigh` > `high` > `medium` > `low` の階段で、末尾のトークン、または末尾の `fast` の 1 つ前のトークンです。その結果が検出済みのスラッグでなければ、同じファミリーの検出済みスラッグのうち、目標以下の effort で最も高いものを使います。それも無ければ、そのロールを選択が必要なものとして印を付けます。`inherit-parent` と `auto` は変わりません。したがって `unlimited` は `claude-opus-5-5-xhigh` を `claude-opus-5-5-max` に変えます。Grok のスラッグは `xhigh` が上限なので、`unlimited` ではフォールバックにより Grok は `xhigh` になり、`grok-4.7-xhigh-fast` はそのまま残ります。`large` は両方の既定値を保ちます。`small` はそれらを `claude-opus-5-5-medium` と `grok-4.7-medium-fast` に変えます。

**(c) ロールを提示して確認する。** すべてのロールをモデルとともに提示し、検出済みの集合に無い実在のスラッグには、選択が必要だと印を付けます。手順 2 で削除した行も列挙します。そのまま受け入れるか、特定のロールを変えるかを尋ねます。選択肢には、検出したモデルに加えて `inherit-parent` と `auto`（どちらも、このロールが親チャットのモデルで動くという意味で、Auto のユーザーが Auto のまま動く方法です）を提示します。自由記述よりも AskQuestion を優先します。パネルのロール（arena runners、architect runners、interrogate reviewers）の値はリストで、エントリごとにサブエージェントが 1 つ動きます。エイリアスのエントリも含むので、リストの長さがその数を決めます。`arena cross-judge pool` もリストですが、arena が実行する判定者は 1 つです。親とは別のファミリーの値だけを、リストの順に試します。好みの順に並べてください。`inherit-parent` や `auto` の値が判定を担当することはありません。`swarm workers` は、レースや比較がアームごとに別のモデルを割り当てない限り、すべてのワーカーが使う既定のモデルです。

### 4. 検証する

書く実在のスラッグはすべて、検出済みの集合に含まれていなければなりません。`inherit-parent` と `auto` は常に合格です。選んだ実在のスラッグが利用できなければ、止まって、もう一度尋ねます。

### 5. ルールを書く

`~/.cursor/rules/pstack-models.mdc` を、`alwaysApply: true`、選んだラベルと目標 effort を持つ `# budget` 行、ロールごとに 1 行（poteto-mode が使うのと同じラベル）で書きます。再実行が冪等になるよう、ファイル全体を上書きします。形は次のとおりです。

```
---
description: pstack per-role model choices (overrides skill defaults)
alwaysApply: true
---
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model`). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: grok-4.7-xhigh-fast
bug-fix: grok-4.7-xhigh-fast
perf-issue: grok-4.7-xhigh-fast
hillclimb: grok-4.7-xhigh-fast
judgment and prose: claude-opus-5-5-xhigh
hardest tasks: claude-opus-5-5-xhigh
how explorer: grok-4.7-xhigh-fast
how explainer: claude-opus-5-5-xhigh
why investigators: grok-4.7-xhigh-fast
why synthesizer: claude-opus-5-5-xhigh
reflect tooling: grok-4.7-xhigh-fast
reflect judgment, divergent, synthesizer: claude-opus-5-5-xhigh
arena runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
arena cross-judge pool: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
swarm workers: grok-4.7-xhigh-fast
architect runners: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
interrogate reviewers: claude-opus-5-5-xhigh, grok-4.7-xhigh-fast
```

### 6. 確認する

ルールを書いたことと、それが新しいセッションに適用されることをユーザーに伝えます。このスキルを再実行すると更新されます。

### 7. 検証スキルを提案する（任意）

プロジェクトに、証明のために実際のアプリを動かす手段（`verify-*` スキル、または既存のハーネス）があるかを確認します。無ければ一度だけ提案します。「プロジェクトローカルの検証スキルはどうですか。エージェントがユーザーと同じようにアプリを動かし、変更が動くことを証明できるようになります。/create-verification-skill で生成できます。」はいなら `/create-verification-skill` を呼び出します（pstack のインストール先に応じて、ワークスペース、ユーザー、プラグインのいずれかで解決されます）。いいえなら、押しつけずに先へ進みます。

### 8. 形式検証スキルを提案する（任意）

プロジェクトに形式検証スキル（モデルチェッカー、証明、その他の検証器をコードに対して実行するプロジェクトスキル）がすでにあるかを確認します。無ければ一度だけ提案します。「形式検証スキルはどうですか。テストが届くケースだけでなく、対象範囲のすべてのケースで、コードの重要な性質が成り立つことをエージェントが証明できるようになります。/create-formal-verification-skill で生成できます。」はいなら `/create-formal-verification-skill` を呼び出します（pstack のインストール先に応じて、ワークスペース、ユーザー、プラグインのいずれかで解決されます）。いいえなら、押しつけずに先へ進みます。
