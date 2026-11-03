# 原則名で方向を変える

pstack は24の原則を個別のスキルとして同梱しています。`/poteto-mode` は多段階タスクの開始時にそれらの索引を読み、タスクが引き金となる原則を適用し、適用した各原則を、それが変えた判断とともに返信で名指しします。

原則を呼び出すのではありません。その名前を使って舵を取るのです。それぞれの名前は、エージェントがすでに読んだ完全なルールを指しています。だから1つのフレーズで、段落いっぱいの指示よりも正確に仕事の方向を変えられます。

## 実際に舵を取る

エージェントが既存の3つのアダプターに新しいアダプターを継ぎ足そうとしているとします:

```text
use subtract before you add. delete the obsolete adapters first, then design what's left.
```

ビルドが通ったから成功だと言い張っているとします:

```text
apply prove it works. run the real import flow and show me the written records.
```

2つの並行する試行が同じブランチに書き込もうとしているとします:

```text
separate before serializing shared state. give each attempt its own worktree, no locks.
```

どのフレーズも、背後にあるルールが具体的だから効きます。それでもエージェントは、返信の中で、そのルールがどの判断を変えたかを言わなければなりません。判断が伴わない原則の引用は、そのルールを適用せずに名前を出しただけ、という意味です。

## 24の原則を手短に

中核の原則は、どれだけ作るか、いつ設計を考え直すかを決めます:

- [Laziness Protocol](../../skills/principle-laziness-protocol/SKILL.ja.md)は、削除と、問題を解決する最小の変更を好みます。
- [Foundational Thinking](../../skills/principle-foundational-thinking/SKILL.ja.md)は、ロジックを書く前に中核となるデータ構造を選びます。
- [Redesign from First Principles](../../skills/principle-redesign-from-first-principles/SKILL.ja.md)は、新しい要件を、初日からそこにあったかのように統合します。
- [Attack the Premise](../../skills/principle-attack-the-premise/SKILL.ja.md)は、2つ以上の失敗した修正が共有していた前提を書き出し、次の修正の前にそれを直接テストします。
- [Subtract Before You Add](../../skills/principle-subtract-before-you-add/SKILL.ja.md)は、その上に何かを築く前に、死んだ重りを取り除きます。
- [Minimize Reader Load](../../skills/principle-minimize-reader-load/SKILL.ja.md)は、読み手が頭の中に保持しなければならない層や隠れた状態を畳み込みます。
- [Outcome-Oriented Execution](../../skills/principle-outcome-oriented-execution/SKILL.ja.md)は、捨てる前提の互換状態を保つのではなく、書き換えを目標の設計へ収束させます。
- [Experience First](../../skills/principle-experience-first/SKILL.ja.md)は、実装の都合よりもユーザーの結果を選びます。
- [Exhaust the Design Space](../../skills/principle-exhaust-the-design-space/SKILL.ja.md)は、前例がないときに2つか3つの競合するプロトタイプを作ります。
- [Build the Lever](../../skills/principle-build-the-lever/SKILL.ja.md)は、その仕事を実行する、あるいは証明するスクリプトを作り、レビュアーが再実行できるようにします。エージェントが同じことを手作業で繰り返すなら、あったらいいと思うツールやスキルを書かせましょう。あるステップを毎回同じやり方でスクリプトができるなら、スクリプトを使い、エージェントは判断が必要な場面に取っておきます。

アーキテクチャの原則は、状態、検証、互換性をどこに置くかを決めます:

- [Model the Domain](../../skills/principle-model-the-domain/SKILL.ja.md)は、繰り返されるルールを、散らばった条件分岐ではなく1つの構造にエンコードします。
- [Boundary Discipline](../../skills/principle-boundary-discipline/SKILL.ja.md)は、境界で検証し、内部の型を信頼します。
- [Type System Discipline](../../skills/principle-type-system-discipline/SKILL.ja.md)は、不正な状態を表現不可能にします。
- [Make Operations Idempotent](../../skills/principle-make-operations-idempotent/SKILL.ja.md)は、リトライを同じ最終状態に収束させます。
- [Migrate Callers Then Delete Legacy APIs](../../skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.ja.md)は、マイグレーションと削除を1つの波で行います。
- [Separate Before Serializing Shared State](../../skills/principle-separate-before-serializing-shared-state/SKILL.ja.md)は、調整を加える前に、共有そのものを取り除きます。

検証の原則は、何を証明とみなすかを定義します:

- [Prove It Works](../../skills/principle-prove-it-works/SKILL.ja.md)は、代理物ではなく、実際の成果物を検証します。
- [Fix Root Causes](../../skills/principle-fix-root-causes/SKILL.ja.md)は、コードを変える前に再現し、原因までたどります。
- [Sequence Work into Verifiable Units](../../skills/principle-sequence-verifiable-units/SKILL.ja.md)は、小さな単位ごとにチェックで締めてから次を始めます。
- [Test Behavior, Not Implementation](../../skills/principle-test-behavior-not-implementation/SKILL.ja.md)は、コードの利用者が観察できることをアサートします。だから、その振る舞いが壊れればテストは失敗し、内部を変えてもテストは生き残ります。
- [Explain the Number](../../skills/principle-explain-the-number/SKILL.ja.md)は、測った数値を誰かが信じたり報告したりする前に、その数値を制限しているものが何か、別のものを測ってしまっていないかを明らかにします。[`/benchmark-checklist`](../../skills/benchmark-checklist/SKILL.ja.md)は、それを実際の実行から答える7つの問いに変えます。

委任の原則は、並行作業をまともな状態に保ちます:

- [Guard the Context Window](../../skills/principle-guard-the-context-window/SKILL.ja.md)は、大量の読み込みをサブエージェントに回し、発見はメインチャットに残します。
- [Never Block on the Human](../../skills/principle-never-block-on-the-human/SKILL.ja.md)は、可逆な作業を進めて、結果を提示します。

そしてメタ原則が1つ:

- [Encode Lessons in Structure](../../skills/principle-encode-lessons-in-structure/SKILL.ja.md)は、2回繰り返した助言を、lint、チェック、スクリプトに変えます。[`/correct`](../../skills/correct/SKILL.ja.md)はこれをリポジトリ全体に適用します。[自分のものにする](09-make-it-yours.ja.md)で示しています。

リストを暗記する必要はありません。今ざっと目を通して、ここにある名前を知っていれば防げたことをエージェントがやっているのに気づいたときに戻ってきましょう。そうやって語彙が身につきます。

次: [自分のものにする](09-make-it-yours.ja.md)。
