---
name: principle-foundational-thinking
description: "Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious."
disable-model-invocation: true
---

# Foundational Thinking

**構造の判断**は選択肢の価値（option value）を守ります。**コードレベルの判断**は単純さを守ります。

**まずデータ構造。** ロジックを書く前にデータの形を正しくします。中核の型を早く定義し、すべてのアクセスパターンをたどり、主要な経路に合う構造を選びます。

コードレベルでは、構造を DRY にし、すべての行を DRY にしません。型とデータモデルは収束すべきです。似た 3 つの文は、早すぎる抽象化に勝ります。賢さより明示性を選びます。テストするのは振る舞いとエッジケースであり、行数ではありません。

**並行性の帰結。** 主体間で状態を共有する前に、「別の主体がこれを並行して変更したら何が起きるか」を問います。「何も起きない」でないなら、隔離します。

**まず足場。** 後のすべてのフェーズに役立つものは、最初にやります。「その後のすべてのフェーズは、これが存在することで利益を得るか」を問います。CI、lint、テスト基盤、共有の型は足場です。選択肢の価値のために順序を決めます。セットアップを機能より先に、テストを修正より先に。コミットは小さく、単一目的に保ちます。

各増分は、一貫した抽象化を着地させるか、既存のものを深めるべきです。新しい能力を、呼び出し側に特殊ケースの調整として散らばせてはいけません。

足場より先に削除があります。まず死んだコードを消し、それから土台を敷きます。
