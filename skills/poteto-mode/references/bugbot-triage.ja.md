# Bugbot のトリアージ

このリファレンスは、Babysit プレイブック（`../playbooks/babysit.md`）が Bugbot やレビュー自動化のコメントを扱うときに使います。目的は Bugbot を既定で無視することではありません。すべてのコメントを必須のコード変更として扱うのをやめることです。

## 判断のルーブリック

行動する前に、Bugbot のスレッドをそれぞれ分類します。

- `fix`: コメントが、もっともらしい正しさ・セキュリティ・プライバシー・データ損失・認証・課金・移行・冪等性・レース・出荷済みの振る舞いの問題を指している。所有する最も下の PR で直し、コミット SHA を添えて返信し、スレッドを解決する。
- `dismiss`: コメントが、記録済みの低リスクでノイズの多いパターンに当たり、現在のコードと文脈からコード変更が不要だと証明できる。短い理由を添えて返信し、スレッドを解決する。
- `ask`: コメントが新しい、重大度が高い、セキュリティ・プライバシー・データに関わる、あるいは曖昧。推測せず、ユーザーに聞く。

迷ったら聞く。ノイズの多いコード品質コメントを飛ばすのは安い。本物のデータやセキュリティのバグを飛ばすのは高くつく。

## 学習したパターンの形式

今後のパターンはこの形で追加します。

```markdown
### <short pattern name>

- Confidence: candidate | recurring | strong
- Skip when: <conditions that must be true>
- Do not skip when: <risk boundaries>
- Example signal: <phrases or code context that identify the pattern>
- Source: <PR/comment URL or short historical note>
```

例が 1、2 件なら `candidate`。実際の却下が複数回あれば `recurring`。パターンが狭く、繰り返し検証され、低リスクなときだけ `strong`。

## 繰り返し出るスキップ候補

### 意図的な UI やデザインシステムの見た目の変更

- Confidence: candidate
- Skip when: PR の説明、スクリーンショット、デザインレビュー、近くのコードが、その見た目の変更を明示していて、Bugbot のコメントが「共有の見た目の既定が変わった」と言い直しているだけ。
- Do not skip when: コメントがアクセシビリティ、フォーカスの可視性、キーボード操作、色のコントラスト、あるいは PR が意図的に変えていないコンポーネント API の契約を指している。
- Example signal: フォーカスリング、ボタンのサイズ、余白、共有コンポーネントの見た目の既定についてのコメントで、オーナーが「intentional」「intended」と返しているもの。

### Bugbot には見えない、スタック上やスタック内の利用

- Confidence: candidate
- Skip when: Bugbot がある export、コンポーネント、ヘルパー、ファイルを使われていないと指摘し、使用中の forge の PR 一覧と diff、スタック上の diff、PR の文脈から、スタックの後続 PR で使われていると分かる。
- Do not skip when: 現在の PR がスタックの一部ではない、シンボルが公開 API、あるいはスタック上での利用が確認できない。
- Example signal: 「Exported component is never used」に対して、人間が「used upstack」と返している。

### 並行実装中の一時的な重複

- Confidence: candidate
- Skip when: 削除・置換・検証中の古い経路と新しい経路を並行して保つため、少数のコードを意図的に重複させている。
- Do not skip when: 重複したコードがセキュリティ、課金、データアクセス、API の振る舞いを変える。あるいは長く残る共有の抽象化の方が明らかにリスクを下げる。
- Example signal: 「Significant duplication」「duplicated validation logic」に対して、オーナーが古い経路は削除予定、または重複は意図的にローカルだと説明している。

### フレームワークやコンポーネントの不変条件が警告をカバーしている

- Confidence: candidate
- Skip when: 指摘が、共有コンポーネント、フレームワークの契約、型の不変条件、単一の真実の源によって、現在の diff か近くのコードで保証済み。
- Do not skip when: 不変条件が前提されているだけで強制されていない、タイミングに依存する、あるいは値がずれうる非同期・状態の境界をまたぐ。
- Example signal: 内側のポップオーバーの max-height 欠如への指摘で、共有ポップオーバーがビューポートの境界を強制している。あるいは nullable な値で、ローカルで確認した値と渡す値が同じ源。

### オーナーが宣言したフォローアップや先送りした片付け

- Confidence: candidate
- Skip when: PR のオーナーが既知のフォローアップだと明言し、現在の PR で振る舞いが悪化しておらず、コメントが高リスク領域ではない。
- Do not skip when: エージェントがオーナーの入力なしに動いている、中〜高重大度のプロダクトの振る舞い、あるいは先送りすると新しい退行をマージしてしまう。
- Example signal: 「I'll worry about that later」「we'll delete this eventually」。

### 自己撤回された、または明示的な誤検知ルールのコメント

- Confidence: recurring
- Skip when: コメント本文か後続の Bugbot の返信が、指摘を撤回した、準拠している、誤検知だと明言し、エージェントが該当ルールをローカルで確認できる。
- Do not skip when: 唯一の証拠が、高リスクの指摘に対する説明なしの「false positive」という人間の言葉だけ。
- Example signal: ファイル命名ルールのコメントで、本文がそのファイルはすでに準拠していると言っている。

## 既定では聞く

次のカテゴリは、過去の PR で似たものを却下していても、自動でスキップしない。

- セキュリティ、プライバシー、認証、課金、データ保持、学習データ、権限境界の指摘。
- 重大度の高い指摘。
- 移行、スキーマ、冪等性、並行性、システム間の振る舞いの指摘。
- 提案された修正が小さく、プロダクトの意図を変えずにリスクを明らかに下げるコメント。

過去のデータでは、人間がセキュリティやデータフローのコメントを却下したこともある。それはオーナーの判断であり、チーム全体のスキップ規則として扱わない。

## 最近の babysit からの候補

チームに役立ちそうだがまだ成熟していない学びは、babysit 中または後にここへ追加します。複数の PR でパターンが確認できたら、上の節へ昇格させるのが望ましい。

### ブラウザ標準の振る舞いを手で再実装したもの

- Confidence: candidate
- Skip when: ほぼ決して飛ばさない。diff がブラウザ標準の振る舞いを手作りの等価物に置き換えているとき（ネイティブの sticky → JS で位置決めした複製、ネイティブのスクロール対象 → wheel/touch イベントの転送、paint-order の遮蔽 → mask/clip-path）、そのコードに対する Bugbot のロジックバグ指摘は一貫して妥当だった。
- Do not skip when: 指摘がイベント転送の欠落（wheel の deltaMode、touch のパン、端でのスクロール連鎖、タップの slop）、mask/clip のヒットテストのずれ、そのコードでの observer と React の状態更新のタイミング競合に関わる。既定は fix。
- Example signal: 「masks do not affect hit-testing」「overlay blocks wheel scroll」「ignores deltaMode」「runs in the IntersectionObserver callback before React applies state」。
- Source: sticky 遮蔽の 1 PR。Bugbot を 6 回通し、指摘は約 18 件。すべて却下せず修正した。

### 契約テストのずれの主張は安く検証できる。まずテストを実行する

- Confidence: candidate
- Skip when: 検証自体を飛ばすことは決してない。1 コマンドで済む。PR がプロトコルやドキュメントの文言を固定する契約テスト（SKILL.md への正規表現、ドキュメント文言のスナップショット）を出していて、Bugbot が「テストがドキュメントと合わなくなった」（またはその逆）と主張したら、分類する前に PR の先端でそのテストを実行する。赤なら主張が経験的に確認でき、緑なら却下の返信に対する具体的な反証になる。
- Do not skip when: 該当なし。これは却下パターンではなく検証の近道。なお、繰り返し通過を理由に軽く却下するヒューリスティクスはここでは誤作動する。文言を固定するテストは、まさに以前の修正ラウンドが文言を編集するからずれる。
- Example signal: PR の以前の修正コミットが固定対象の一節を書き換えていたのに、「Contract test omits the pre-fix wait」と言われ、先端でテストを実行したらまさにその assertion で落ちた。
- Source: 文言固定の 1 PR で Bugbot を 8 回通過。以前の通過はすべて修正して解決していたのに、7 回目の主張は本物だった。

### 同じ PR の後半ですでに直っている、古いセキュリティレビューの指摘

- Confidence: candidate
- Skip when: エージェント型のセキュリティレビュー（または同種のもの）が認可や検証の呼び出し漏れを主張し、現在の PR の先端にはまさにそのゲート（テスト付き）が含まれている。多くはレビュー実行後の後続の堅牢化コミットで追加されている。
- Do not skip when: 指摘されたヘルパーが、問題のプリンシパルにとって no-op、チェックが守るべき副作用の後に走る、あるいは主張されたプリンシパルのカバレッジが欠けている。
- Example signal: HIGH の「missing authorization check」があるが、先端では副作用の前にまさにそのガードが呼ばれている。
- Source: Webhook エンドポイントの 1 PR で、堅牢化コミットがレビュー実行より後だった。

### 意図的に狭いエラー条件を広げると、本当のエラーが隠れる

- Confidence: candidate
- Skip when: 指摘が、狭いエラー条件（特定の `errno`、エラーコード、ステータスクラス）を catch-all に広げろと言い、その狭さが本当の区別を表している。典型は `ENOENT` で分岐する依存のフォールバック。「バイナリが入っていない」は「コマンドが走って失敗した」とは別の状況。非ゼロ終了すべてでリトライすると、正当な失敗（見つからない、認証切れ、ネットワーク）に対してもフォールバックを走らせ、フォールバックのエラーを報告して本当のエラーを隠す。
- Do not skip when: 狭い条件が同じカテゴリのケースを取りこぼす（`EACCES` のような別の「バイナリが使えない」errno、別のトランスポート層の失敗）、未処理の経路がデータを失うか中途半端な状態を残す、あるいはリトライが冪等で元のエラーも依然として表面化する。
- Example signal: 「only retries when X fails with ENOENT … never tries the fallback even when a working Y exists」という指摘で、実際のフォールバックは失敗した操作ではなく欠けた依存のために存在していた。
- Source: CLI 改名の 1 PR。フォールバックは失敗したコマンドではなく、欠けたバイナリのためにあった。
