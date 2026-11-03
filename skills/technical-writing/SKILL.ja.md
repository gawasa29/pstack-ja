---
name: technical-writing
description: "Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages."
disable-model-invocation: true
---

# テクニカルライティング（Technical writing）

疲れたエンジニアが最初に読んだだけで理解できるように書きます。4 つの層すべてを適用します。

層の上に 3 つのルールがあります。

- **仕事をしない語はすべて削ります。** その語を抜いても文が成り立つなら、その語は落とします。"In order to" は "to" です。"It is important to note that" は何でもありません。
- **短く、日常的な語を使います。** "utilize" ではなく "use"。"facilitate" ではなく "help"。"perform" ではなく "do"。長い語は、その長さを精密さで買い取らなければなりません。
- **ルールが文を悪くするときは、別のやり方で直すか、そのままにします。** すべてのルールに従っていて、機械が書いたように響く文は、失敗です。

語彙リストの役割はコードベースが果たします。同義語や説明ではなく、実際のシンボル、ファイル、フラグ、コマンド名を書きます。

ジャーゴンを発明しないでください。開発者が口に出す語を使います。"evacuate"、"ratchet"、"endgame" ではなく、"move"、"delete"、"a budget that only decreases" です。名前の付いたパターンは、そのドキュメントが最初に意味を書いていれば構いません。新しい違反例とその置き換えは、返信の中で、`unslop` の抽象メタファーのルールへの追加として、diff を添えて提案します。そのスキルは編集しないでください。

## リズムを変える

ドキュメントはすべての層に従っていても、機械が書いたように読めることがあります。どの文も短く切り詰められ、どこにも見解がなく、具体的なものが何もない場合です。

- 文の長さを意図的に混ぜます。短い文は論点を決めます。長い文は、事実をその条件や結果とともに運びます。
- 1 文に 1 つの考えは、1 文に 1 つの長さという意味ではありません。2 つの考えを運ぶ文は分けます。1 つの考えを運ぶ長い文は残します。
- モードが許すところでは見解を持ちます。説明はトレードオフを量るので、長所と短所を並べるのではなく、そこから何を思うかを書きます。リファレンスは淡々としたままです。
- 無菌より具体的に。「スキーマの変更は問題を起こしうる」ではなく「カラム名の変更はビルドを失敗させる」と書きます。

## まずモードを選ぶ（Diátaxis）

1 つのドキュメントに 1 つのモードです。2 つの問いで選びます。その内容は行動（doing）に役立つのか、理解（thinking）に役立つのか。そして学習に役立つのか、仕事に役立つのか。

- 行動 + 学習: **チュートリアル**。
- 行動 + 仕事: **ハウツー**。
- 理解 + 仕事: **リファレンス**。
- 理解 + 学習: **説明**。

このコンパスは、ドキュメント全体にも 1 文にも使えます。

**チュートリアル: やりながら学ぶ。** 学習者が成功するのは、学習者の仕事ではなく、あなたの仕事です。何を「学ぶ」かではなく、何を作るかを最初に言います。どのステップも、早く、何度も、目に見える結果を生みます。何が見えるはずかを伝えます。期待される出力、プロンプトの変化、ログの行です。説明は 1 つの節とリンクに削ります。具体的なままにします。"we" として、コマンドで書きます。"First, do x. Now, do y."

**ハウツー: ゴールまでの手順。** 機械が実行できる操作ではなく、人が抱えている問題を解きます。能力を前提にして、教えることは省きます。行動だけです。脱線も背景も、それ自体のための網羅性もありません。それらはリンクにします。分岐と判断は許します。"If you want x, do y." ガイドはタスクで名付けます。"Radar array calibration" ではなく "How to calibrate the radar array" です。

**リファレンス: 引くための事実。** 記述するだけです。指示も説得も意見もありません。淡々と、完全に、確実に書きます。事実、選択肢、制限、エラーを、ぼかさずに述べます。説明する対象の構造を写し、コードとドキュメントを並べてたどれるようにします。読者が期待する場所に材料を置きます。可能ならコードから生成します。

**説明: 理解と理由。** 区切られた 1 つの話題で、プロダクトから離れても読めます。各タイトルは、前に暗黙の "About..." を付けても耐えるべきです。実際の why の問いに錨を下ろします。文脈を与えます。設計判断、歴史、制約、代替案です。意見が許されるのはここだけで、他のどこでもありません。

モードを混ぜないでください。チュートリアルの中にリファレンスの表を置かず、リファレンスの中にチュートリアルの手取り足取りを入れず、ハウツーの中で議論しません。分けてリンクします。

## 読者に向けて文を書く（Google developer style）

- 読者に "you" で、現在形で話します。"Will" は、本当に後で起きることだけに使います。
- 誰が何をするかを書きます。"is checked" ではなく "the compiler checks"。受動態がよいのは、行為者が不明か、論点から外れているときだけです。
- 指示は命令として書きます。"Click Submit." 事実は平に述べます。"should be done" は決して使いません。
- 条件を指示の前に置きます。"To delete the document, click Delete."
- 一般的なケースを先に置きます。例外は後に。
- 知識のある友人のように響かせます。バズワードも比喩もなく、指示に "please" を付けず、手順に "simply"、"easy"、"quickly" を決して入れません。簡単なら、読者はここにいません。
- 先回りして予告せず（"we will soon support..."）、同じ言い回しで連続する文を始めません。
- リンクは、どこへ行くかを言う語で貼ります。ページのタイトルか短い説明です。"click here" は決して使いません。外部へのリンクより、ページ内の文脈を 1 文添えるほうを優先します。
- 見出しは話題だけでなく論点を運びます（"Modes" ではなく "Pick the mode first"）。sentence case で書きます。タスクの見出しは動詞句そのもの（"Create an instance"）です。概念の見出しは名詞句です。h1 は 1 ページに 1 つ、レベルを飛ばしません。
- 順序には番号付きリスト、それ以外には箇条書きを使います。リストは完全な文で導入します。項目は並列に保ちます。
- コードはコードフォントで書きます。UI 要素は太字にします。直列コンマを使います。"etc." は落とし、リストが一部であることは最初に言います。

## 記述を 1 つずつ読ませる（STE のルール）

- 1 文に 1 つの指示。それ以外では 1 文に 1 つの考え。
- 約 20 語を超える指示と、約 25 語を超えるその他の文は分けます。
- 警告や条件は、それが守るステップの前に置きます。"If hot oil touches your skin, injuries can occur."
- "the" と "a" は残します。"Remove backup file" は 2 通りに読めます。"Remove the backup file" は 1 通りです。
- 各語に 1 つの意味と 1 つの役割を与え、それを保ちます。"check" が inspect を意味するなら、restrain の意味にも使わないでください。
- 動作ごとに 1 つの語を選び、それに従います。ここでは "start"、そこでは "initiate" ではなく、どちらも "start" です。
- 手順は直接の命令として書き、語りでも受動態でも書きません。"the component must be installed" ではなく "Install the component" です。
- できるところでは "-ing" の語を避けます。

## 1 文を二通りに読ませない（Global English）

- "only" や "not" のような語は、それが変える語の隣に置きます。"only fails on growth" と "fails only on growth" は違うことを言います。
- 長い名詞の連なりは分解します。"the proto import budget check script" は "the script that checks the proto-import budget" になります。
- すべての "it"、"they"、"this" を、明らかな 1 つのものを指すようにします。迷ったら名詞を繰り返します。"this" や "which" で節全体を指してはいけません。
- 動詞を落とさないでください。"Phase 1 moves the converters and Phase 2 the runtime" は Phase 2 に動詞がありません。与えます。
- 構造を示す小さな語は残します。"Ensure that the switch is off" の "that" です。明瞭さを語数と引き換えにしてはいけません。
- 誤読を防ぐなら、並列の中で冠詞を繰り返します。2 つのものなら "the client and host" ではなく "the client and the host" です。
- 文が 2 通りにまとまりうるときは、"and" や "or" が何をつなぐかを書きます。"Both...and"、"either...or"、"if...then" は無料の曖昧さ解消です。
- セミコロンではなくピリオドを使います。長いダッシュ（em dash）は新しい文に置き換えます。
- 括弧の中のテキストは、文法上の完全な単位か、独立した文にします。"(s)" で複数形を作ってはいけません。
- スラッシュは使いません。"a/b" や "and/or" ではなく "a, b, or both" と書きます。
- 各物を、どこでも 1 つの名前で呼びます。1 つのものを "the gate"、"the ratchet"、"the budget check" と呼ぶドキュメントは、3 つのことを教えています。変わっていないものをかき混ぜないでください。
- 慣用句、口語、ラテン語の略語、メタファーは省きます。

## 語り口とリポジトリ固有の事情

- このスキルが扱うすべてのドキュメントに **unslop** スキルを適用します。slop のパターンのカタログはそのスキルが持ちます。AI の語彙、埋め草、ヘッジ、書式の痕跡です。
- PR の説明とコミットメッセージも文章です。Diátaxis を除くすべての層が適用されます。PR の本文は、レビュアーが 1 分以内に読めるブリーフィングです。swarm のログ、SHA の一覧、指標の表を貼らないでください。リンクします。
- プロダクトの UI 文字列はドキュメントではありません。それにはプロダクトのコピーガイドラインを使ってください。
- コードの断片はタブでインデントします。実際のパスを書きます。件数やツリーの主張は、それを取り込むコミットの時点で真にし、再生成するコマンドを添えます。

## 書き換え例

変更前:

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

変更後:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.
