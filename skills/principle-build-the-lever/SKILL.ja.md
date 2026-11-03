---
name: principle-build-the-lever
description: "Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun."
disable-model-invocation: true
---
# Build the Lever

仕事が自明でないなら、手作業でやるのではなく、それを実行する道具を作ります。

codemod、ジェネレータ、スクリプトは、毎回同じやり方で仕事をこなし、無料で再実行できます。道具は 1 つの成果物であり、レビュアーはそれを読んで再実行し、仕事を確かめられます。手作業の変更は、やり直すことでしか再検証できません。決定的なスクリプトは、「私を信じて」を「これを実行して」に変えます。

既定ではレバーを作ります。省いてよいのは、タスクが自明なとき、つまり一目でわかる明白な編集が 2、3 個のときだけです。

- 最初の 1 単位は手作業で行い、手順を学んでから道具を作ります。その単位に対して道具を再実行し、手作業の版と diff を取って証明します。レバーは安全に再実行できるようにします。
- 編集には codemod かスクリプト、繰り返し現れるファイルにはジェネレータ、分析には sqlite に流し込むクエリ、検証には再実行可能なチェックを使います。
- 決定的なレバーはファンアウトに勝ります。道具がすべての単位を 1 パスで処理できるなら、自分で実行します。スクリプトにできることを、委譲先に手作業で適用させてはいけません。
- 作業をサブエージェントにファンアウトするときは、レバーを全員が読むスキルとして書きます。手順、検証の契約、触れてはいけない領域（fence）を 1 つの成果物に入れます。委譲先の書き込み範囲の外に置き、契約をこっそり書き換えられないようにします。
- この原則を適用すると、ファイルが 1 つ生まれます。原則を引用したのに、diff に codemod、スクリプト、ジェネレータ、委譲先のスキルのどれもないなら、適用していません。
- 仕事がセッションより長く続くなら、レバーをコミットします。

基準は繰り返しの有無ではなく、自明かどうかです。一度きりの作業でも、レバーがあることで仕事が検証可能になるなら、レバーを作る価値があります。[Laziness Protocol](../principle-laziness-protocol/SKILL.ja.md) に従い、その仕事を実行する・証明する最小のスクリプトを作ります。フレームワークは作りません。

これは、繰り返す指示を持続するガードレールにする [Encode Lessons in Structure](../principle-encode-lessons-in-structure/SKILL.ja.md) とは別のものです。こちらは、目の前の仕事のスループットとレビュー可能性です。検証そのものをスクリプトにする方法は [Prove It Works](../principle-prove-it-works/SKILL.ja.md) を参照してください。
