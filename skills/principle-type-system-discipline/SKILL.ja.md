---
name: principle-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas."
disable-model-invocation: true
---

# Type System Discipline

コンパイラが、不可能な状態、取り違えたプリミティブ、扱い忘れたバリアントを拒否するようにします。ハンドラを増やすより、エラーと特殊ケースを定義から存在しないようにすることを選びます。TypeScript の構文は `typescript-best-practices` スキルを参照してください。

- **意味を持つプリミティブにブランドを付ける。** `UserId` と `OrderId` は中身が文字列ですが、互換であってはいけません。それぞれに独自の型を与えます。TypeScript ならブランド付きの交差型、他の言語なら newtype などです。生成時に一度バリデーションし、下流ではその型を信頼します。2 つの引数が同じプリミティブ型を共有しながら意味が違うなら、ブランドを付けます。
- **外部データはパースするまで型なしである。** RPC のペイロード、JSON、IPC メッセージ、CLI 引数、設定ファイル、環境変数、データベースの行です。境界ごとに、構造化されていない入力を型付きモデルに変えるパース関数を持たせます。バリデーションをどこに置くかは **boundary-discipline** 原則スキルが述べています。
- **型は正となるスキーマから導出する。** protocol buffer、OpenAPI の spec、GraphQL スキーマ、データベースのマイグレーション、デザイントークンのファイルなど、形を所有するファイルがあるなら、同じ形の型を手書きするのではなく、そこから導出します。**encode-lessons-in-structure** 原則スキルを参照してください。
