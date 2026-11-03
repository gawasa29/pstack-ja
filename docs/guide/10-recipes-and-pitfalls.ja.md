# レシピと落とし穴

コピーする価値のあるプロンプトと、誰もが一度はやるミス。パスと完了条件は自分のものに置き換えてください。レシピはわざとくだけています。実際にはそう入力されるものですし、スキルは意図をちゃんと読み取ります。

![ロボットたちがレシピ箱から料理を作る横で、彼女が完成した皿を味見している。カウンターの上には /how、/tdd、/loop と書かれたカードが留められている。](./images/recipes.jpg)

## なじみのないサブシステムを理解する

```text
use /how first to understand how this initialization works. then use /why to figure out why it broke recently.
```

まず仕組み、次に履歴。各スキルのレポートは、どのソースを検索したかを示すので、答えが何に基づいているかが分かります。

## コードに触る前に、ノイズの多いレポートを言い換える

```text
/poteto-mode read this thread. restate the underlying issue in your own words, in plain english. don't change any code yet.
```

読み違いは言い換えの中に現れ、そこなら1メッセージで直せます。エージェントが自分の見立てを述べるまでは、あなたの説は胸にしまっておきましょう。`/in-your-own-words` はプレイブックなしで、言い換えだけを求めます。

## 送る前にプロンプトを研ぐ

```text
/sharpen write the onboarding doc for the new billing service.
```

エージェントは、専門家ならやるのにあなたが頼んでいなかったこと、出発点にする素材、その手法とツール、結果が正しいかを外部から確かめる手段を挙げます。そしてそれを求めるように書き直したプロンプトを返し、タスク自体は実行しません。読み心地が良ければ、その書き直しを送りましょう。

## 選ぶ前にプロトタイプを作る

```text
/poteto-mode prototype a few options for the settings layout. put them behind a switcher and send me screenshots of each.
```

説明ではなく、動くものから選びます。エージェントはその過程で、レイアウトやタイミングについての自分の問いに自分で答えていきます。

## 固まった設計を計画に変える

```text
/poteto-mode turn this design into a plan. small verifiable PRs, each with its own proof.
```

設計が固まってから頼みましょう。計画そのものが成果物で、それを実行するプレイブックを名指しします。

## 設計についてセカンドオピニオンを得る

```text
ask /arena for a second opinion on this thread and our approach
```

今の設計が複数の候補の1つになり、統合結果が、パネルがより良いものを見つけたのか、あなたの案を裏付けたのかを教えてくれます。後戻りに高くつく設計に比べれば、コストはわずかです。

## 独立したスライスを並行してチェックする

```text
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

各ワーカーが1つのパッケージを持ちます。親はすべてのスライスを待ち、ワーカーの生のダンプではなく、`PASS`、`ISSUES`、`BLOCKED` のいずれか1つのレポートを返します。

## ブランチを懐疑的にレビューする

```text
/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's an actual bug or regression in behavior.
```

修飾語が実際に効きます。「don't change anything yet」で読み取り専用に保ち、細かい指摘のルールがノイズをあらかじめ除くので、検証済みの発見だけがあなたの時間に見合います。

## 失敗するテストを通してバグを直す

```text
/poteto-mode repro the duplicate write first. if there's a cheap test path, /tdd it. then fix and rerun.
```

「if there's a cheap test path」が効きます。脆いモックで無理にテストを書くのは、実際のコマンドを実行するより証明力が低く、プレイブックはそう言ってよいことになっています。

## レポートを再現し、証拠付きで修正する

```text
/poteto-mode repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.
```

「if it repros on main」があると、バグがすでに消えている場合に早く止まれます。動画があれば、diff を読む前に修正を確認できます。

## テストがほとんど届かない性質を証明する

```text
/create-formal-verification-skill the retry queue. a message must never be delivered twice.
```

宣言した範囲内のあらゆるケースで1つの性質がチェックされ、コードがすでにそれを破っていればコードの言葉で反例が示され、そのコードに変更が入るたびに次のエージェントが実行するプロジェクトスキルが得られます。

## 数値を公表する前に吟味する

```text
/benchmark-checklist vet this 40% speedup before it goes in the pr description
```

速くなった、遅くなった、測定できる差はない、判定不能のいずれかが、実行回数、範囲、その数値を制限しているものとともに返ります。

## 同じミスを注意し続けるのをやめる

```text
/correct agents keep adding new config flags without registering them in the schema
```

修正はアーキテクチャ、型、lint、テストとしてリポジトリに取り込まれ、次のエージェントがそのミスをすることはできません。

## 作業を始めずにやり方を尋ねる

```text
/poteto-help how do i get poteto-mode to stay on every turn?
```

答えと、送るべきプロンプトと、ソースへのリンクが返ります。そのプロンプトを送るまで何も実行されません。

## 離れている間も実行を誠実に保つ

```text
im going to bed, keep going autonomously until every fixture passes. do not stop. keep a decision log i can audit in the morning.
```

完全な契約は[夜間のページ](07-overnight.ja.md)にあります。タスクと完了条件がすでに会話にあるなら、短い形でも機能します。

## 漂流する実行の向きを変える

舵取りのプロンプトは1行です:

```text
i said the goal is to repro. i did not ask for a fix yet.
```

```text
apply prove it works. show me the real output, not the build log.
```

```text
/unslop that, no emdashes
```

言葉を多く必要とすることはほとんどありません。必要なのは正しい名前で、[原則のページ](08-principles.ja.md)がその語彙です。

## 返信を平易な言葉で受け取る

```text
/bro
```

プロンプトはこれだけです。[`/bro`](../../skills/bro/SKILL.ja.md)は、人間同士が話すように最後のメッセージを言い換えます。専門用語なしで、短く。返信が技術的に詳細なのに、何が言いたいのか分からないときに使います。

## 走らせたままのチャットの近況をつかむ

```text
/ketchup
```

[`/ketchup`](../../skills/ketchup/SKILL.ja.md)は、最後のメッセージ以降に何が変わったかを平易な言葉で伝え、続いてあなたの判断待ちの各案件を、推奨、証拠、リスクとともに列挙します。報告している間は何も変えません。

代わりに映像で追いたいときは、[`/ketchup-video`](../../skills/ketchup-video/SKILL.ja.md) を実行します。何が起きたかを字幕付きの短いスライド動画で見せ、判断待ちの案件はその下にテキストで並べます。

## 落とし穴

- **プロンプトでスキルを列挙する。**「use /how then /architect then /arena」は、プレイブックがすでに順序立てているステップを並べ替えてしまいます。ゴールと制約を述べましょう。スキルを名指しするのは、既定を上書きしたいときだけです。
- **あいまいな完了条件。**「make it better」では `/loop` がチェックできるものがありません。合否を判定できるコマンドか成果物を渡しましょう。
- **原因についての自分の説から始める。**エージェントはあなたが指した場所を探します。まず問題を言い換えさせ、それから自分の勘を共有しましょう。
- **最初の設計を採用する。**1回の試行で、モデルが最初に思いついた形が固定されます。プロトタイプか `/architect` を求め、証拠から選びましょう。
- **抽象的な計画を磨き込む。**コードの裏付けがない計画を敵対的にレビューすると、決して起きないリスクが生み出されます。未解決の問いはプロトタイプで決着させ、それから作られたものをレビューしましょう。
- **1つのワークツリーで並行エージェントを動かす。**互いを上書きし、どのエージェントが何を変えたか誰にも分かりません。クラウドエージェントとして動かすか、「own worktree per attempt」と伝えましょう。
- **ループを信頼する前にループを回す。**自分の仕事を検証できないループは、検証されていない仕事を速くするだけです。まず検証スキルを動くようにしましょう。
- **吟味していない数値を信じる。**温まったキャッシュや飛ばされたコードパスは、高速化を偽装できます。数値をどこかに出す前に `/benchmark-checklist` を実行しましょう。
- **同じミスを手で注意する。**チャットでの注意は1回の実行にしか効きません。`/correct` はリポジトリを直すので、後の実行がそれを繰り返しません。
- **カバレッジのために `/arena` を使う。**`/arena` は1つの設計やコードのお題を繰り返し、ベースを選んで最良の部分を接ぎ木します。`/swarm` はスライスや、あらかじめ宣言したレースの腕（arm）を分割し、1つのレポートにまとめます。
- **レビューコメントを全部受け入れる。**bot も人間も、本物の指摘とノイズを1つのリストに混ぜて出してきます。`/interrogate` は再実行で証明できた発見だけを残し、捨てたものとその理由を並べます。どちら向きにもあなたが上書きできます。
- **`auto` をモデルのスラッグとして扱う。**`auto` と `inherit-parent` は「model フィールドを省略して、サブエージェントが親チャットのモデルを引き継ぐ」という意味です。[セットアップ](01-setup.ja.md)で役割を扱っています。
- **ビルドが通ったことで成功を報告する。**ビルドが証明するのはコンパイルが通ることだけです。実際のコマンド、フロー、保存された値、プロファイルを求め、返信に証拠が来ることを期待しましょう。
- **`SKILL.md` をぶっつけで書く。**[Authoring or modifying a skill プレイブック](../../skills/poteto-mode/playbooks/authoring-a-skill.ja.md)に通して、検証とレビューが行われるようにしましょう。

以上がガイドです。飛ばし読みしたなら、[セットアップ](01-setup.ja.md)に戻って実際のタスクを1つ実行しましょう。習慣は読むことではなく、使うことから身につきます。

[ガイドの索引](README.ja.md)に戻る。
