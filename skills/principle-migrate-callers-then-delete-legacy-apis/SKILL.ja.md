---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
disable-model-invocation: true
---

# Migrate Callers Then Delete Legacy APIs

- テストは新しい契約を assert するように更新し、リファクタ前の実装詳細を守るだけのテストは削除する

**適用される場面:**
- 外部のユーザーが後方互換性に依存していない
- プロジェクトが、調整済みの破壊的変更を受け入れられる
- 新しい API が、単純化やリファクタの取り組みの一部である
