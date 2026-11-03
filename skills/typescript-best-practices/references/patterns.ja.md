# TypeScript のパターン

`SKILL.md` の各ルールに対応するコード例です。根底にある原則は言語に依存しません。**type-system-discipline** と **boundary-discipline** の原則スキルを参照してください。

## ブランド型（branded types）

プリミティブにブランドを付けて、取り違えられないようにします。境界で一度だけ検証します。下流のコードはその型を信頼します。

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function isAgentId(input: string): input is AgentId {
  return isUUID(input);
}

function parseAgentId(input: string): AgentId {
  if (!isAgentId(input)) throw new Error(`Invalid agent id: ${input}`);
  return input;
}

function focusAgent(id: AgentId): void {
  /* input is trusted */
}
```

`readonly __brand: 'X'` の形に合わせてください。新しい流儀を発明しないでください。

## 判別可能ユニオン（discriminated unions）

リテラルの判別子でバリアントをモデル化します。すべてのバリアントが同じフィールド名を共有し、各バリアントの値は一意なので、あり得ない組み合わせを表現できません。

```ts
// Don't. Boolean + optionals lets contradictory states exist.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do. Only valid states exist.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

判別子の名前は 1 つ選び（`kind`、`type`、`tag`）、それに統一してください。

## 構成的なモデリング（constructive modeling）

緩い型を実行時のチェックで制限するのではなく、すべて合法な部品から型を組み立てます。

空を許さない型を、可変長タプルで:

```ts
type NonEmpty<T> = [T, ...T[]];

// Don't: T[] plus a length check every caller must repeat
function pickWinner(entries: string[]): string {
  if (entries.length === 0) throw new Error("no entries");
  return entries[Math.floor(Math.random() * entries.length)];
}

// Do: an empty value of the type can't exist
function pickWinner(entries: NonEmpty<string>): string {
  return entries[Math.floor(Math.random() * entries.length)];
}
```

素の `T[]` が届く場合は、ガードで一度だけ絞ってください。その事実は型の中を伝わります:

```ts
const isNonEmpty = <T>(arr: T[]): arr is NonEmpty<T> => arr.length > 0;
```

偶数長を、ペアで:

```ts
type Pairs<T> = [T, T][];
```

時間範囲を、開始と長さで:

```ts
// Don't: a comment holds the invariant
type TimeRange = { start: Date; end: Date }; // start <= end

// Do: a negative range can't be written; derive end when needed
type TimeRange = { start: Date; durationMs: number };
```

`durationMs` は素の数値のままにしてください。ブランドを付ける（ブランド型を参照）のは、長さを期待する場所に生の数値が渡りうる場合だけで、反射的に付けてはいけません。不正な状態を構築不能にする表現を選び、その上に必要な読み出し口（`pairs.flat()`、`rangeEnd()` ヘルパー）を用意してください。

## 最も単純な全域型（simplest total type）

すべてを強くしないでください。すべての操作が全域的なら `T[]` のままにします:

```ts
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0); // [] is 0, fine
```

緩い型が使用箇所で嘘を強いるなら強くします。見分け方は `!`、`arr[0] as T`、「起こるはずがない」という throw です:

```ts
// Don't: partiality smuggled past the compiler
function newestSession(sessions: Session[]): Session {
  return sessions.at(0)!;
}

// Do: strengthen the input; the assertion disappears
function newestSession(sessions: NonEmpty<Session>): Session {
  return sessions[0];
}
```

結果を `Session | undefined` に弱めるのは、もう 1 つの全域的なシグネチャです。

## `any` より `unknown`

外部のデータは常に `unknown` です。使う前に絞ってください。

```ts
// Don't
function handle(input: any) {
  return input.foo.bar;
}

// Do
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) {
    // narrowed; compiler verifies access
  }
}
```

外部の源には、RPC のペイロード、`JSON.parse`、`postMessage`、IPC、ファイルの内容、環境変数、データベースの結果が含まれます。

## 手書きのガードよりスキーマ

外部データのためのプロパティごとの型ガードを書く前に、リポジトリの実行時スキーマライブラリと既存のスキーマを探してください。検証は 1 つのスキーマに任せ、そこから TypeScript の型を導きます。スキーマ、重複したインターフェース、ずれていくガードを並べて保守しないでください。

```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  role: z.enum(["admin", "member"]),
});

type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}
```

失敗が想定される分岐なら `safeParse` を使ってください。リポジトリが別のスキーマライブラリを使っているなら、それに対応する型推論ヘルパーを使います。ガード 1 つのために新しいスキーマ依存を足さないでください。このルールは、コードベースがすでに信頼しているスキーマの仕組みを優先します。

## `as` キャストを使わない

`as` はどれも実行時クラッシュの可能性です。型システムが主張を検証した後にだけキャストしてください。

```ts
import { z } from "zod";

// Don't
const user = data as User;

// Don't
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}

// Do
const userSchema = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof userSchema>;

function parseUser(data: unknown): User {
  return userSchema.parse(data);
}
```

型が先にある場合は、検証器に、それが証明する型を注釈として付けます。そうすればコンパイラは、型より弱いことしか証明しない検証器を拒否します。下のオブジェクトから `name` を消すと、代入がコンパイルできなくなります。

```ts
type User = { id: string; name: string };

const userSchema: z.ZodType<User> = z.object({ id: z.string(), name: z.string() });
```

既存のコードから `as` を外すリファクタリングでは、TypeScript が推論できない理由を特定してください:

- 判別子がない: 判別子を足し、判別可能ユニオンに切り替える。
- 元の型が広すぎる（`Record<string, unknown>` など）: 型を絞る。
- 型のない境界: その形を所有するスキーマでパースする。スキーマは、存在しない箇所にだけ足す。
- 本当に表現できない: ブランド型か `satisfies` を使う。

## 絞り込みの優先順位（narrowing hierarchy）

良い順から最後の手段まで:

1. **判別可能ユニオンの switch / if。** コンパイラが自動で絞り込みます。
2. **`in` 演算子。** `"key" in obj` は、そのキーを持つバリアントに絞り込みます。
3. **`typeof` / `instanceof`。** プリミティブとクラスのインスタンス向け。
4. **ユーザー定義の型ガード。** 上で足りないとき。
5. **`as` キャスト。** 検証の後だけ。

```ts
function area(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2; // narrowed to circle
  return s.width * s.height; // narrowed to rect
}
```

## 型ガード（type guards）

ガードは実際に主張を検証しなければなりません。嘘をつくガードは `as` より悪いです。

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

可能なら判別子による絞り込みを優先してください。

## 網羅性（exhaustiveness）

default 節では、判別子を `never` 型のローカル変数に代入してください。

```ts
// Value-returning switch
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}

// Void switch
function handle(s: Shape): void {
  switch (s.kind) {
    case "circle":
      drawCircle(s);
      break;
    case "rect":
      drawRect(s);
      break;
    default: {
      const _exhaustive: never = s;
      void _exhaustive;
    }
  }
}
```

値を返す switch では return 形式、文としての switch では void 形式にします。

## `as` より `satisfies`

`satisfies` はリテラル型を広げずに検証します。

```ts
// Don't. Widens, loses literal types.
const config = { theme: "dark", cols: 3 } as Config;

// Do. Validates AND preserves literal types.
const config = { theme: "dark", cols: 3 } satisfies Config;
// config.theme is "dark" (literal), not string
```

## 境界での検証

データが入ってくる場所で一度だけ検証します。内側では型を信頼します。**boundary-discipline** 原則スキルを参照してください。

- **ワイヤーフォーマット**（proto、JSON-RPC）: `ignoreUnknownFields` でパースし、前方互換の変更が古いクライアントを壊さないようにする。
- **永続化した JSON:** バージョン付きの blob にし、パースを try/catch で囲む。
- **呼び出しの深いところで再検証しない。**

## スキーマから導く型

`.proto`、OpenAPI の仕様、GraphQL スキーマ、データベースのマイグレーションがすでに形を定義しているなら、それを複製せず、生成された型から導いてください。

```ts
// Don't. Duplicate shape, drifts when the schema changes.
type CheckSummary = {
  totalCount: number;
  checks: { name: string; status: string }[];
};
function renderChecks(s: CheckSummary) {
  /* ... */
}

// Do. Derive from the generated schema type.
import type { ChecksMessage } from "<generated module>";
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) {
  /* ... */
}
```

新しいインターフェースを書く前に、`Pick`、`Omit`、`Parameters`、`ReturnType`、`Awaited`、`typeof` を使えないか検討してください。

## オブジェクト引数（object args）

```ts
// Don't. Swap two args, still compiles.
openFile(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});

// Do. Order-independent, self-documenting.
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

ホットパスでは省いてください。フレームごとの描画、トークナイザー、パーサー、アロケーションのコストが効く密なループの中などです。
