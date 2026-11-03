# 変更をビルドして diff を片付ける

ビルド系のプレイブックには共通する規律があります。自分が観察したことを書き、証拠を要求するのはプレイブックに任せる、というものです。このページでは、よくあるビルド作業ごとにプロンプトへ何を書くか、そのあとに diff をレビュー可能に保つ片付けの習慣を紹介します。

## 各ビルドプレイブックには、わかっていることを書いて渡す

バグのプロンプトでは症状を書き、まず再現を求めます。

```text
/poteto-mode this command emits two records after a retry. repro first, then fix and verify.
```

機能のプロンプトでは、振る舞いと、変わってはいけないものを書きます。

```text
/poteto-mode add a --json flag. text output stays byte-identical. verify both forms.
```

リファクタリングのプロンプトでは、構造を動かす前に振る舞いを固定します。

```text
/poteto-mode move parsing into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

パフォーマンスのプロンプトでは、印象ではなく計測値を書きます。

```text
/poteto-mode startup takes 1.8s on this fixture. trace it, fix the measured cause, show me before and after.
```

これらはそれぞれのプレイブック（[Bug fix](../../skills/poteto-mode/playbooks/bug-fix.ja.md)、[Feature](../../skills/poteto-mode/playbooks/feature.ja.md)、[Refactoring](../../skills/poteto-mode/playbooks/refactoring.ja.md)、[Perf issue](../../skills/poteto-mode/playbooks/perf-issue.ja.md)）に振り分けられ、打ち込まなかった手順はプレイブックが補います。直す前に再現する、実装する前にデータの形を名指しする、作り直す前に振る舞いを固定する、最適化する前にプロファイルする、といった具合です。

1つの数値を継続的に改善したいときは、[Hillclimb プレイブック](../../skills/poteto-mode/playbooks/hillclimb.ja.md) があります。指標と目標と試行回数の下限を渡すと、凍結した計測ハーネスを使い、仮説を1つずつループで試します。勝ったものは残し、それ以外はすべて巻き戻します。

パフォーマンス系のプレイブックはどちらも、自分の数値に対して [`/benchmark-checklist`](../../skills/benchmark-checklist/SKILL.ja.md) を実行します。Perf issue はベースラインと、そのあとのすべての数値を吟味し、Hillclimb はハーネスを凍結する前に吟味します。自分でこれを打つべきタイミングは[検証して出荷する](06-verify-and-ship.ja.md)で説明します。

原因を先に、修正は後で、という場合もあります。リーク、アイドル時の CPU スピン、表示のちらつきといったライブの症状なら、[Runtime forensics プレイブック](../../skills/poteto-mode/playbooks/runtime-forensics.ja.md) が実行中のプロセスに計測を仕込みます。すでに取得したプロファイルがあるなら、[Trace forensics プレイブック](../../skills/poteto-mode/playbooks/trace-forensics.ja.md) がその成果物を読み、ホットなフレームをソースに対応づけます。どちらが返すのも診断であり、修正ではありません。

```text
/poteto-mode here's a cpuprofile from the slow startup. tell me where the time goes and which source lines own it. no fix yet.
```

## `/tdd` で失敗するテストを先に書く

バグに安価なローカルテストの道筋があるなら、プロンプト全体が2語で済みます。

```text
/tdd implement
```

文脈があれば、それで十分です。[`/tdd`](../../skills/tdd/SKILL.ja.md) は意図した理由で失敗する最小のテストを書き、次に修正を書き、それからテストを再実行します。テストに大がかりなハーネスの準備や脆いモックが必要になるなら、スキルはそう告げて、代わりにいちばん近い実行可能なチェックを使います。本物のコマンドのほうが強い証拠になる場面で、テストを無理に使わないでください。

## TypeScript のルールは名前で読み込む

[`typescript-best-practices`](../../skills/typescript-best-practices/SKILL.ja.md) は型システムの原則を具体的なルールに変えます。判別可能ユニオン（discriminated union）、境界での `unknown`、網羅的なバリアント、スキーマから導出した型、といったものです。これは自動では読み込まれないので、`.ts` や `.tsx` ファイルに触るタスクでは `/typescript-best-practices` と打ち込んでください。

## コミットする前に片付ける

[Opening a PR プレイブック](../../skills/poteto-mode/playbooks/opening-a-pr.ja.md) は各コミットの前に diff へ `/deslop` をかけ、PR の説明とコミット本文には [`/unslop`](../../skills/unslop/SKILL.ja.md) を適用します。`/deslop` は `cursor-team-kit` プラグインに入っていて、pstack には入っていません。持っていない場合は、同じ結果を普通の言葉で頼んでください。実況中継のようなコメント、裏付けのないガード、死んだ互換パス、無関係な編集を消す、といった具合です。

文章に対しては、`/unslop` は対象と、あれば追加のルールを受け取ります。

```text
/unslop the readme changes, no emdashes
```

そのうち自分なりの略記ができるでしょう。このスキルは `unslop that, tighten it` のような短いプロンプトからでも意図をきちんと読み取ります。

## `/no-comments` でコメントを削る

コメントには専用のレビュー工程が必要で、しかも書いたエージェントにやらせるべきではありません。書き手は自分が書いたコメントを、あなたが自分のコメントを擁護するのと同じように擁護します。なのでレビューの前に、まっさらな目に渡します。

```text
/no-comments the diff
```

[`/no-comments`](../../skills/no-comments/SKILL.ja.md) は [Comment Sicko](../../agents/comment-sicko.ja.md) を起動します。読み取り専用のレビュアーで、残してよいもののリストは短いものです。ライセンスヘッダー、公開 API のドキュメントコメント、コードでは説明できないことを説明するリンク、自分では変えられない外部依存によって強制される振る舞い。それ以外はすべて落とします。自分のコードの中の「え、これ？」には、そうした猶予はありません。コメントはリファクタリングの指摘として返され、`/no-comments` は受け入れた指摘を根本原因で直します。コメントが制約を主張している場合（「削除しないこと」）、スキルはその主張を型、テスト、lint のいずれかで表現することを提案します。どちらにしても、コメントは消えます。

役割分担は整理しておく価値があります。`/deslop` はコードから slop（中身の薄い量産コード）を取り除き、`/unslop` は文章からそれを取り除き、`/no-comments` はコメントを、書いていないレビュアーに渡します。

**落とし穴:** 片付けは任意の磨き上げではありません。実況中継のようなコメントや、保身のための死んだコードが付いた diff は、レビュアーには未完成に見えますし、余分なコードは次のバグが潜む場所です。diff が水増しされていると感じたら、レビューで指摘されてからではなく、コミットする前に `deslop it` と言ってください。

次: [検証して出荷する](06-verify-and-ship.ja.md)。
