# 自分のものにする

poteto-mode はある1人のスタイルです。その下にあるプレイブック、ルーティング、モデルの役割分担は、あなたのスタイルでも同じように機能します。このページでは、個人用モードの生成、セッションからの学びの取り込み、エージェントが同じミスを繰り返さないようにリポジトリを直すこと、焦点を絞ったスキルの執筆、スキル変更を信頼する前のテストを扱います。

思うより小さく始めましょう。初日から多くのスキルは要りませんし、このプラグイン全体さえ不要です。素朴にプロンプトを書き、エージェントがどこで失敗するかを見て、同じ失敗が2回現れたらスキルかチェックを1つ足します。

## `/automate-me` で自分のモードを生成する

```text
/automate-me
```

スタイルを説明する必要はありません。[`/automate-me`](../../skills/automate-me/SKILL.ja.md)が履歴から読み取るからです。アクティブなワークスペースの最近のトランスクリプトを掘り、返信の仕方、委任の仕方、検証、コード、文章、進め方について繰り返し現れる好みを洗い出し、どのパターンが本当にあなたなのかを尋ねます。Cursor 組み込みの `create-skill` フローで `.cursor/skills/<your-name>-mode/SKILL.md` のドラフトを作り、そのドラフトを [`/unslop`](../../skills/unslop/SKILL.ja.md) に通し、ワークツリーから PR を開くので、他の変更と同じようにレビューできます。

習慣が移ろったら、いつでもまた実行します:

```text
/automate-me update my mode skill with everything since its last edit
```

更新モードは、スキルが最後に変わって以降の履歴だけを掘ります。あなたが否定していないルールは残し、新しい証拠があるものは改訂し、新しいパターンに限ってセクションを追加します。

## `/reflect` でセッションの学びを取り込む

何かを教えてくれたタスクの直後に、次を実行します:

```text
/reflect that took way too long. capture what we learned so the next run doesn't repeat it.
```

[`/reflect`](../../skills/reflect/SKILL.ja.md)はトランスクリプトを3つの並行するレビュアーに送り、その後シンセサイザーが提案を `Accepted`、`Rejected`、`Backlog` に振り分け、スキルが変わる前にあなたの承認を待ちます。将来の判断を変える提案だけを承認しましょう。1回の奇妙なセッションは逸話であって、ルールではありません。

## `/correct` で環境を直す

エージェントに同じミスを何度も注意しているなら、修正は次のプロンプトではなくリポジトリに入るべきです。選択肢を、どのくらい効き続けるかで並べます:

1. アーキテクチャやより良いデータ構造で、そのミスを不可能にする。
2. 型で塞ぐ。あるいは、エラーが修正方法を示す lint や CI チェックで塞ぐ。
3. テストで捕まえる。
4. ドキュメントやエージェント向けのルールとして書き残す。エージェントがルールを飛ばしても何も失敗しないので、これは最後に来ます。

人のレビューはこのリストに入りません。毎回の PR で同じミスを捕まえなければならないレビュアーこそ、これが直そうとしている問題です。[`/correct`](../../skills/correct/SKILL.ja.md)がその仕事をします:

```text
/correct agents keep calling the database client directly instead of going through the repository layer
```

直近のコミット、リバート、レビューコメント、回避策を説明するコメントを読み、ミスをクラスにまとめます。クラスは2回起きた時点で数えます。頻度の高いクラスから1つずつコミットで直し、効く中で最も高いレベルで行い、新しいチェックが過去の実際のミスで失敗することを証明します。また、エージェント指示ファイルに、各ルールとそれを強制するものを対にした表を保つので、何も強制していないルールは繰り返しとして現れます。返信には、各クラスとその証拠、選んだレベル、より高いレベルがうまくいかなかった理由が並びます。

引数なしで実行すると、履歴からクラスを自分で見つけます。`/reflect` と `/correct` は仕事を分担します。`/reflect` は1つのセッションからスキルを良くします。`/correct` はミスのクラスが戻ってこないようにリポジトリを変えます。修正が新しい境界になる場合は `/architect` と組み合わせます。[多数のプロジェクトを並行実行する](07-overnight.ja.md)には、リポジトリ全体で両方を行うプロンプトがあります。

## 焦点を絞ったスキルを書く

取り込みたいワークフローがもう分かっているとき:

```text
/poteto-mode write a skill for verifying database migrations in this repo
```

スキルの執筆は[Authoring or modifying a skill プレイブック](../../skills/poteto-mode/playbooks/authoring-a-skill.ja.md)に対応します。これは Cursor 組み込みの `create-skill` を通し、フロントマターとリンクを検証し、結果を Opening a PR プレイブックで出荷します。エージェント向けの文章は人間向けの文章より基準が高いです。役に立たない一文が、未来のエージェントが従う指示になるからです。`SKILL.md` をぶっつけで書くのではなく、その基準はプレイブックに守らせましょう。

2つの特別なケースには専用の生成器があります。アプリを動かして振る舞いを証明する必要があるスキルは検証スキルなので、代わりに [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.ja.md) と [`/maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.ja.md) を使います。モデル検査器、証明、または別の検証器でコードの性質を確かめるスキルは形式検証スキルなので、[`/create-formal-verification-skill`](../../skills/create-formal-verification-skill/SKILL.ja.md) と [`/maintain-formal-verification-skill`](../../skills/maintain-formal-verification-skill/SKILL.ja.md) を使います。[検証して出荷する](06-verify-and-ship.ja.md)では両方の種類を扱っています。

## `/technical-writing` で基準に沿ってドキュメントを書く

出荷する文章はスキルだけではありません。ドキュメント、RFC、readme、PR の説明、コミットメッセージには:

```text
/technical-writing review the readme changes
```

[`/technical-writing`](../../skills/technical-writing/SKILL.ja.md)は、層になった基準を適用します。目標は、疲れたエンジニアが一度読んで理解できる文章です。まず文書のモード（チュートリアル、ハウツー、リファレンス、説明）を選び、それから文単位で作業します。誰が何をするのか、1文に1つの考え、2通りに読める表現を残さない、という具合です。自分やエージェントが書いたものをレビューするのに使ってもいいですし、ドキュメントを依頼するときに最初から名指ししてもいいです。

## スキルの変更をブラインドでテストする

スキルの編集は今後のすべてのセッションに影響するので、それが実験であるかのようにテストしましょう。他人のスキルを取り入れるときも同じです。自分の仕事に対してエージェントを良くするか確かめてから、使い続けましょう。

```text
/poteto-mode run the eval playbook on this skill change. same task for both variants, candidates stay blind.
```

スキルが何度も外していて、どう振る舞うべきかが分かっているときは、変更とテストを1つのタスクで行います:

```text
/poteto-mode update the review skill so it flags missing migrations, and eval the change.
```

最初から評価を求めておくと、編集が誠実になります。1回の悪いセッションから書いた修正はそのセッションに過適合しがちで、編集を重ねるとスキルは漂流します。評価は出荷前にその漂流を捕まえます。

[Eval プレイブック](../../skills/poteto-mode/playbooks/eval.ja.md)は、1つの失敗モードである観察者効果を中心に組まれています。評価されていると知っているエージェントは違う振る舞いをします。そこで候補エージェントには、sanitize 済みのディレクトリで自然に見えるタスクを与え、「eval」や「candidate」という言葉を決して見せず、互いの存在も見せません。1人の審判がすべての出力を中立のラベルで採点し、チェーン追跡は、候補が主張することではなく、実際にどのファイルを読んだかで評価されます。

判定を受け入れる前に、すべての出力を自分で読みましょう。審判に同意できないときは、自分の判断を疑う前に、ルーブリックを疑いましょう。

## `/make-bot-ui` で bot UI を作る

状況依存のスキルが1つ、Grok Bot のユーザー向けにあります。[`/make-bot-ui`](../../skills/make-bot-ui/SKILL.ja.md)は、ボタンが webhook ルーチン経由で bot を起こす小さなページを作ります。たとえば、レビューキューをスワイプして回り、スワイプのたびにその項目への対応を bot に頼む、といったことができます。webhook の送信者キーはあなたのマシン上のサーバーが保持するので、キーがブラウザやチャットに渡ることはありません。このスキルは Tailscale でページを公開する方法も扱います。

**落とし穴:** スキルがうまく動かないからと、タスクの途中で編集しないこと。専用の PR で直し、タスクは進めましょう。機能開発に絡まったまま出荷されたスキルの編集は、レビューから見えず、評価もできません。

次: [レシピと落とし穴](10-recipes-and-pitfalls.ja.md)。
