# 機能マップの例

Benny が再現する可能性のある、ユーザーから見える機能をすべてマップします。アプリを操作する前に、該当するセクションを読みます。このマップはユーザーの視点に保ちます。内部の作りや現在のコードパスは、ここに固定するのではなく、実行時に見つけます。

このファイルを `.cursor/automations/benny/` の外、たとえば `.cursor/benny/feature-map.md` にコピーし、`control.feature_map_path` をそのコピーに設定します。パックの更新がそれを上書きしてはいけません。

## 機能ごとのテンプレート

### `<feature name>`

`<one-line user-visible purpose>`

#### ユーザーがたどり着く方法

- クリックのパス: `<screen> -> <menu, tab, or panel> -> <control>`
- キーボードショートカット: `<shortcut or none>`

#### control アダプタがどう操作するか

- `<adapter action>` に `<inputs>` を渡すと、`<visible result>` になるはずです。
- リセット: `<how the adapter returns to a fresh state>`。

#### 安定したセレクタ

- `<role and accessible name>`
- `<ARIA relationship>`
- `<data-component or purpose-named data attribute>`

生成された CSS や StyleX のクラス、動的なハッシュ、子のインデックス、壊れやすい DOM の位置を決して使いません。

#### 動かしてみる状態

- default、hover、focus-visible、active、disabled
- loading、empty、error
- selected、open、expanded
- `<relevant feature-specific variants>`

当てはまらない状態には、その旨を記します。

#### 前提条件とセットアップ

- 認証: `<account state>`
- データ: `<fixture>`
- 権限: `<role>`
- フラグ: `<flag or none>`
- サービス: `<required availability>`

#### 証拠と突き合わせ

- スクリーンショット: `<app identity, feature, and discriminating state>`
- 動画: `<entry path, interaction, and final state>`
- 突き合わせ: `<read-only state or value that confirms the UI>`

#### 落とし穴

- `<known dead end or wrong surface>`
- `<safe environment translation>`

## 架空の例

これらの機能は、架空のタスクアプリのものです。例であって、Benny に必須の機能ではありません。

### サインイン

ユーザーがタスクアプリに入れるようにします。

#### ユーザーがたどり着く方法

- アプリを開き、`Sign in` を選びます。ショートカットはありません。

#### control アダプタがどう操作するか

- `open_app`、`click Sign in`、`fill credentials`、`click Continue` で、アイテム一覧が開くはずです。
- サインアウトし、使い捨てのセッションを消してリセットします。

#### 安定したセレクタ

- ボタン `Sign in`、テキストボックス `Email` と `Password`、`data-component="sign-in-form"`

#### 動かしてみる状態

- default、focus-visible、submitting、disabled、loading、error

#### 前提条件とセットアップ

- 使い捨てのアカウントと、利用可能な認証サービス

#### 証拠と突き合わせ

- ランディングページからアイテム一覧までを録画します。セッションの状態を読み取り専用で確認します。

#### 落とし穴

- マーケティングページは、対象の画面ではありません。認証サービスが無いことはブロックです。

### アイテム一覧と詳細

ユーザーがアイテムを眺めて、1 つ開けるようにします。

#### ユーザーがたどり着く方法

- `Items` タブを開き、行を選びます。

#### control アダプタがどう操作するか

- `select_tab Items` と `click <fixture item>` で、その詳細が開くはずです。
- 詳細を閉じ、選択を消してリセットします。

#### 安定したセレクタ

- `Items` という名前のタブと一覧、フィクスチャの名前を持つ行、`data-component="item-detail"`

#### 動かしてみる状態

- loading、empty、error、selected、open、expanded

#### 前提条件とセットアップ

- 名前付きのフィクスチャのアイテム、読み取り権限、利用可能なアイテムサービス

#### 証拠と突き合わせ

- 選択と、それに合う詳細のタイトルを示します。選択中のアイテム ID を確認します。

#### 落とし穴

- 検索結果は似て見えても、別のパスを使います。

### アイテムエディタ

ユーザーがアイテムを作成または編集できるようにします。

#### ユーザーがたどり着く方法

- 詳細から `Edit` を選ぶか、一覧から `New item` を選びます。

#### control アダプタがどう操作するか

- `click Edit`、`fill <field>`、`click Save` で、詳細が更新されるはずです。
- フィクスチャを戻してリセットします。

#### 安定したセレクタ

- ボタン `Edit`、`New item`、`Save`、フォーム `Item editor`、ラベルと結び付いたフィールド

#### 動かしてみる状態

- default、focus-visible、dirty、validating、disabled、saving、error、success

#### 前提条件とセットアップ

- 編集可能なフィクスチャ、書き込み権限、利用可能な保存サービス

#### 証拠と突き合わせ

- フィールドの変更が、更新された詳細に現れることを示します。保存されたアイテムの値を読み取り専用で確認します。

#### 落とし穴

- フォームの状態を注入してはいけません。読み取り専用の詳細フィールドは、エディタではありません。

### 設定

ユーザーが個人の設定を変えられるようにします。

#### ユーザーがたどり着く方法

- プロフィールメニューを開き、`Settings` を選びます。

#### control アダプタがどう操作するか

- `open_menu Profile`、`click Settings`、`toggle <preference>` で、コントロールが更新されるはずです。
- 最初の設定に戻してリセットします。

#### 安定したセレクタ

- ボタン `Profile`、メニュー項目 `Settings`、リージョン `Settings`、用途にちなんで名付けた設定の属性

#### 動かしてみる状態

- closed、open、selected、focus-visible、disabled、loading、error

#### 前提条件とセットアップ

- サインイン済みのテストアカウント、既知の設定、利用可能な設定サービス

#### 証拠と突き合わせ

- メニューのパスと最終的なコントロールの状態を示します。設定の値を読み取り専用で確認します。

#### 落とし穴

- OS の設定は、別の画面です。

## 完成度のチェックリスト

- 再現可能な、ユーザーから見える機能すべてにセクションがある。
- 各セクションが、ユーザーのパス、アダプタのアクション、リセットを明記している。
- セレクタが、ロール、名前、ARIA、安定したコンポーネントのマーカー、用途にちなんだ属性を使っている。
- 生成されたクラスや DOM の位置を使っているセレクタが無い。
- 関係する interaction、loading、empty、error、selected、expanded の状態がカバーされている。
- 認証、フィクスチャ、権限、フラグ、サービスが明示されている。
- スクリーンショット、動画、根拠となる突き合わせの要件が明示されている。
- 間違った画面、行き止まり、安全な環境の言い換えが列挙されている。
- 実装の詳細は、実行時に見つけるものとして残っている。
