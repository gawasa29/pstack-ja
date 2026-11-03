# pstack ガイド

pstack が最もよく働くのは、エージェントに細かく指示するのをやめたときです。欲しいものと、どうなれば完了か分かる基準を伝えます。`/poteto-mode` がプレイブックを選び、手順が必要とするスキルを実行し、証拠を見せてくれます。このガイドは、現実的なプロンプトでその習慣を身につけるためのものです。

学ぶ内容は次のとおりです:

1. [pstack をセットアップする](01-setup.ja.md)。プラグインをインストールし、使うモデルを選びます。
2. [作業を `/poteto-mode` に振り分ける](02-poteto-mode.ja.md)。ゴールを渡し、プレイブックを選ぶところを見ます。
3. [コードを理解する](03-understand.ja.md)。読み取り専用の調査から始め、何かを編集する前に `/how`、`/why`、`/teach`、`/recall` を使います。
4. [変更を設計する](04-design.ja.md)。コードが形を固める前に、`/architect`、`/arena`、`/swarm`、`/interrogate`、プロトタイプ、計画を使います。
5. [変更を実装して整える](05-build-and-clean.ja.md)。ビルドのプレイブック、`/tdd`、`/unslop`、`/no-comments` です。
6. [検証して出荷する](06-verify-and-ship.ja.md)。実際のアプリで動作を証明し、テストがほとんど届かない領域を形式検証し、数値を `/benchmark-checklist` で吟味し、そのうえで焦点を絞った PR を開いてマージまで進めます。
7. [寝ている間に作業を進める](07-overnight.ja.md)。ループを回す前に信頼を築くこと、夜間の契約、監査できる決定ログ、そして 1 エージェントの枠を超えて広がる Projects と自動化です。
8. [原則名で方向を変える](08-principles.ja.md)。作業の途中でエージェントの進路を変える 24 の名前です。
9. [自分のものにする](09-make-it-yours.ja.md)。自分用のモード、繰り返す失敗のための `/correct`、スキル変更のテスト方法です。
10. [レシピと落とし穴](10-recipes-and-pitfalls.ja.md)。コピーして使えるプロンプトと、避けるべき失敗です。

最初は順番に読んでください。それ以降は、各ページは独立しています。

行き詰まったときや、どのスキルが適しているか分からないときは、[`/poteto-help`](../../skills/poteto-help/SKILL.ja.md) に質問を続けて入力します:

```text
/poteto-help which skill should i use to review this branch?
```

答えを返し、送るためのプロンプトを渡し、答えの出どころであるスキルやガイドのページをリンクします。作業は開始しません。pstack の実行は実際にトークンを消費するので、プロンプトは準備ができたときにあなたが送ります。入力したときにだけ動きます。

## 1 つだけ覚えるなら

ゴールと、それを確認する方法を、自分の言葉でエージェントに渡してください:

```text
/poteto-mode the export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

プレイブックの名前を挙げる必要も、スキルを列挙する必要もありません。「repro first」と確認できる成果、それだけで `/poteto-mode` が振り分けるのに必要な信号は足ります。Bug fix プレイブックにマッチし、手順を todo リストにコピーし、各手順が発火するたびに適切なスキルを呼びます。

次: [pstack をセットアップする](01-setup.ja.md)。
