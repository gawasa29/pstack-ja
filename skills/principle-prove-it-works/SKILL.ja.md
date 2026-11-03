---
name: principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
disable-model-invocation: true
---

# Prove It Works

すべてのタスクの出力を、本物そのものを直接見て検証します。代理物、自己申告、「コンパイルが通った」から推論してはいけません。

**なぜ:** 検証されていない仕事の正しさは不明です。間接的な検証（ファイルの mtime、出力の新しさ、エージェントの自己申告、キャッシュされたスクリーンショット）は、直接観察より安く感じます。間違った推論に基づいて動くコストは、元を確かめるコストよりはるかに大きいです。

本物を確かめ、代理物を確かめない:
- プロセスの生存は、派生した状態を介して間接的にではなく、直接確かめる
- 実際の値を読む。キャッシュされた、あるいは派生した表現を読まない
- 検証が失敗したら、システムを疑う前に観察の方法を疑う

## 可能ならチェックをスクリプトにする

最も強い証明は、同じ比較を再実行する決定的なスクリプトであり、一度きりの目視ではありません。スクリプトを書き、実行し、その出力を成果物として残します。レビュアーはあなたの言葉を信じる代わりに、それを再実行できます。

成果物は人間に見える状態に保ちます。コミットするのは、後から証跡を監査できる必要がある、大きく複雑な仕事だけです。大きな移植や移行などです（**show-me-your-work** スキル）。
