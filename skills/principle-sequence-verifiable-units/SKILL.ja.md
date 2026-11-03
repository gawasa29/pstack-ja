---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer."
disable-model-invocation: true
---

# Sequence work into verifiable units

仕事を小さな単位の連なりとして順序づけます。各単位はチェックできる状態で終わり、現在の単位がグリーンになるまで次に進みません。

**なぜ:** 引き起こした単位で捕まえた破損は、特定するのが安く済みます。バッチの後で捕まえた破損は埋もれ、その時点で壊れた土台の上にすでに築き進めています。同じ単位を、レビュアーが順にたどり直せる届け方に順序づければ、「私を信じて」が「赤くなるところを見て、それから緑になるところを見て」に変わります。

**実行。** 一括変更、移行、似た編集の連続では、次の変更を始める前に各変更を検証します。各単位は before/after の対です。既知の良好な状態、1 つの変更、チェックの実行、それから次へ。最初にクリーンなトランクへ rebase し、すべてのチェックが本当のベースラインに対して測られるようにします。レバーが編集を行うときは、単位ごとのチェックはほぼ無料です。それでも実行します。

**届け方。** コミットと PR を、仕事を証明する順序で積みます。定番の形は、失敗するテストを先に、その上に修正を載せる形です。ほかのストーリーの順序は、作り直す前の削除、処理の前のベースライン取得、機能の前の足場です。各コミットは単独で成立し、その連なりは論証として読めます。

これは、各チェックを本物に保つ **prove-it-works** 原則スキルと、単位ごとのチェックを安くする **build-the-lever** 原則スキルを補う、順序づけの面です。
