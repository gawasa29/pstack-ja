---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate Before Serializing Shared State

並行して動く主体が可変の状態を共有しうるときは、まず同じ可変オブジェクトを必要とするかを問います。必要としないなら、共有そのものをなくします。共有が本物であるときは、直列化を構造として強制します。ロックファイル、順序づけられたフェーズ、排他的な所有権です。指示や慣習は並行性の制御ではありません。

**なぜ:** 共有状態への並行書き込みはレースコンディションを生み、それは断続的で、再現しにくく、デバッグに高くつきます。

**パターン:**
1. **共有された可変状態を特定する**（双方が読み書きするファイル、双方が push するブランチ、双方が定義し消費する API）。
2. **既定: 共有の書き込み先をなくす。** 問います。これらの主体は 1 つの正となるオブジェクトを必要とするのか、それとも独立した事実を発行しているのか。各主体に自分の所有するファイル、キー、ブランチ、状態ディレクトリを与え、読み取り・報告の境界でだけマージします。2 人のワーカーがそれぞれの `lastX` フィールドを 1 つの `state.json` に書くのは、依然として共有された変更です。`indexer-state.json` + `metrics-state.json` なら違います。
3. **1 つの共有書き込み先が本当の不変条件であるときだけ、アクセスを構造として直列化する**（ロックファイル、順序づけられたフェーズ、単一ライターの主体、原子的な compare-and-swap）。「ロックが必要だ」は、既定の答えではなく、確認すべき設計の匂いとして扱います。
