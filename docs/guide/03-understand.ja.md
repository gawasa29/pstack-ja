# 変更する前にコードを理解する

理解していないコードを編集することが、気付きにくいリグレッションを出荷する原因になります。これはあなたにもエージェントにも同じだけ当てはまります。エージェントの失敗はたいてい 2 つのどちらかです。あなたの意図を読み違えるか、作業を正しく行うためのコンテキストを持っていないかです。前者は [プロンプトに入れるもの](02-poteto-mode.ja.md) で扱います。このページは後者を扱います。

pstack は 4 つの入口を用意しています。`/how` はコードが今何をしているかを説明します。`/why` はなぜその形になったのか理由を掘り起こします。`/teach` は両方を 1 つの説明に混ぜ合わせます。`/recall` はある話題について、あなた自身の直近のコンテキストを組み立て直します。どれも、エージェントに、あなたが確認できる言葉で説明させます。コードのことをあなたよりよく知っているかもしれないエージェントを、こうやって監督します。

![探偵が虫眼鏡で機械の設計図を調べ、ロボットたちが事件ファイルを運んでくる。背後の証拠ボードでは、手がかりが /how と /why の下につながっている。](./images/understanding.jpg)

## 読み取り専用の調査から始める

原因がはっきりしないときは、修正ではなく調査結果を求めます:

```text
/poteto-mode investigate why background jobs time out every few hours. give me what we know, what data you used, and your best hypotheses. don't change any code yet.
```

「don't change any code yet」があるので、これは [Investigation プレイブック](../../skills/poteto-mode/playbooks/investigation.ja.md) に振り分けられます。`/how` を実行し、動機に関する問いには `/why` を足し、引用付きの説明を返します。選択肢の比較では、トレードオフ表付きの推奨を返します。「what data you used」と尋ねると、エージェントは証拠と推測を切り分けます。調査結果が修正を指し示したら、修正は新しいタスクとして始めます。

## `/how` で振る舞いをたどる

```text
/how do we dedupe notifications? is there an n+1 when we look up subscribers?
```

自分が本当に持っている疑問を尋ねてください。[`/how`](../../skills/how/SKILL.ja.md) はコードを読み、そのサブシステムにあなたを迎え入れるシニアエンジニアの水準で答えます。実行時の流れ、主要な型、自明でない部分を含みます。大きなサブシステムでは、まず読み取り専用の探索役を 2〜4 体、並行して起動します。狭い問いなら、ただ読んで説明します。

## `/why` で履歴を掘り起こす

```text
/why was the retry limit set to five? does the reason still hold?
```

[`/why`](../../skills/why/SKILL.ja.md) はソース管理から始め、そのうえで MCP が公開している証拠のカテゴリ、たとえば課題トラッカー、長文ドキュメント、チームチャット、可観測性、エラートラッキング、分析を並行して問い合わせます。レポートはすべてを引用し、直接の証拠と推論を分け、記録が薄いときは「appears to（〜のようだ）」と書きます。「何も見つからなかった」という結果も報告します。「誰も理由を書き残していない」こと自体が答えだからです。

この 2 つは自然に組み合わせられます。履歴がこの混乱を説明していると疑うときは、`do why first then how` が良いプロンプトです。

## `/teach` で本当に理解する

```text
/teach me how this PR changes retries. convince me it fixes the cause and not the symptom.
```

[`/teach`](../../skills/teach/SKILL.ja.md) は、要約では足りないときのためのものです。`/how` と `/why` を実行し、小さな変更ならそのうち片方だけを使い、調査結果を、図を 1 枚ずつ積み上げていく平易な説明に織り込みます。「convince me」という枠組みは再利用する価値があります。説明が、見て回るツアーではなく、検証できる論証になります。

エージェント自身の選択にも使えます:

```text
/teach me why you implemented it this way and not with a queue. what did you trade off, and why?
```

教えることは、あなたと同じくらいエージェントの助けにもなります。自分の仕事を説明しなければならないエージェントは、自信たっぷりに言い切って先へ進むのではなく、コードを読み、主張の 1 つ 1 つを証拠で裏付ける必要があります。

## `/recall` で自分のコンテキストを組み立て直す

```text
/recall catch me up on the export work from last week
```

[`/recall`](../../skills/recall/SKILL.ja.md) は、あなた自身の直近のチャットと共有の記録（課題、過去の修正、今も出ているエラー）を掘り、状況と次にやることをまとめたブリーフを返します。古いチャットには、新しいエージェントが持っていないコンテキストがあります。古い話題で新しい作業を始めるときは、まずそれを読み込み、そのうえで新しい入力を渡します:

```text
/recall my work on the virtualized list from yesterday, then read this bug report.
```

特定のチャットを 1 つ再開したい場合は、`/recall` ではなく、下の Session pickup プレイブックです。

## Session pickup で前の作業を引き継ぐ

別のエージェント（あるいは先週のあなた）がブランチを途中で放り出したときは:

```text
/poteto-mode take over this branch. read the decision log, figure out what's done, and continue from there. don't redo finished work.
```

[Session pickup プレイブック](../../skills/poteto-mode/playbooks/session-pickup.ja.md) は、前の足跡を信頼できるものとして扱います。ブランチの状態と決定を再構成し、再開点を明示し、引き継いだ主張を元のゴールに照らして検証します。すべてを一から導き直すことはしません。

**落とし穴:** 「エージェントはどうせコードを読むだろう」という理由で、このページのスキルを飛ばさないでください。コードのモデルをたどらずに編集を始めるエージェントは、最初のそれらしい箇所で症状を直しがちです。先に `/how` を実行するほうが、2 つ目のバグより安く済みます。

次: [変更を設計する](04-design.ja.md)。
