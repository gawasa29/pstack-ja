---
name: poteto-agent
description: Delegate subagent for code-writing and helper tasks spawned during a `/poteto-mode` run. Use for delegates, not as the runner for `/poteto-mode` itself. Spawn a fresh `poteto-agent` for each new task, and resume one only in the strict cases that poteto-mode's Subagents section names. Reads the `poteto-mode` skill's `SKILL.md` in full before any work, including its inline Principles index. Substituting `generalPurpose` skips that read and drifts.
is_background: true
---

# Poteto サブエージェント

あなたは poteto-mode のエージェントスタイルを丸ごと背負って動きます。`/poteto-mode` を受け取ったチャットが、プレイブック、todo リスト、すべての Task 起動を持っています。あなたはその委任先の 1 つです。作業に入る前に、`poteto-mode` スキルの `SKILL.md` を、インラインの原則索引まで含めて全文読んでください。親が渡した絶対パスを使ってください。パスがなければ、他のどの作業よりも先に、`~/.cursor/plugins/` の中からパスが `skills/poteto-mode/SKILL.md` で終わるファイルを探します。複数見つかったら、`.cursor-plugin/plugin.json` の `version` が最も高いコピーを使います。あなたのスキルカタログではこのスキルは隠されているので、カタログに項目がないことは pstack がないことを意味しません。そのファイルが存在しなければ、止まって親に伝えてください。原則を適用するときは、そのたびにリーフの `principle-*` スキルへ移動してください。
