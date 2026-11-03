# ノートを検索する

検索では、ユーザーがタイトルか本文のテキストでノートを見つけ、一致したノートを確認し、一致がない状態と、検索が使えない状態を区別できます。

## サブ機能（Sub-features）

- `search-open` は、対応する各ブラウザ入口から検索を開きます。
- `search-match` は、ノートのデータを変えずに、タイトルと本文の一致を返します。
- `search-open-result` は、結果をノートエディタで開きます。
- `search-empty` は、一致のないクエリに対して、完全な空の状態を表示します。
- `search-clear` は、クエリを消して、最近のノートの表示に戻します。
- `search-cli` は、ターミナルから同じ一致のノートを返します。

## たどり着き方（How to get to it (user POV)）

- ブラウザのツールバーで `Search` ボタンを選んでください。
- ブラウザで、フォーカスが編集可能なフィールドの外にあるときに `/` を押してください。
- ターミナルで `notes search <query>` を実行してください。

## control-notes での操作（Driving it with control-notes）

Preconditions:

- Notes が `http://127.0.0.1:4173` で正常に動いている。
- 使い捨てのデータディレクトリに、本文が `Draft budget` の `Quarterly plan` が入っている。
- `control-notes doctor` が、期待する URL とデータディレクトリを報告する。

- **ツールバーからの入口。** `Search` ボタンを選んでください。`control-notes browser click --role button --name "Search"` を実行してください。`Search notes` という名前のダイアログが現れ、その searchbox にフォーカスがあります。
- **キーボードからの入口。** ダイアログを閉じ、ページにフォーカスして `/` を押してください。`control-notes browser press --key "/"` を実行してください。同じダイアログが現れ、ページにスラッシュは入力されません。
- **タイトルの一致。** `quarterly` を入力してください。`control-notes browser fill --role searchbox --name "Search notes" --value "quarterly"` を実行してください。`Search results` のリストに `Quarterly plan` が入り、`Grocery list` は入りません。
- **本文の一致。** クエリを `budget` に置き換えてください。`control-notes browser fill --role searchbox --name "Search notes" --value "budget"` を実行してください。結果の `Quarterly plan` が、本文一致の抜粋とともに表示されたままになります。
- **結果を開く。** `Quarterly plan` を選んでください。`control-notes browser click --role link --name "Quarterly plan"` を実行してください。ダイアログが閉じ、エディタの見出しが `Quarterly plan` になります。
- **空の状態。** 検索を開き直し、`volcano` を入力してください。`control-notes browser fill --role searchbox --name "Search notes" --value "volcano"` を実行してください。検索が終わると、`No matching notes` という名前のステータスが現れます。
- **クエリを消す。** `Clear search` を選んでください。`control-notes browser click --role button --name "Clear search"` を実行してください。searchbox が空になり、`Recent notes` の領域が結果のリストに代わります。
- **CLI での一致。** ターミナルから検索してください。`control-notes cli -- notes search "quarterly" --format json` を実行してください。終了コードが `0` で、stdout にタイトルが `Quarterly plan` のオブジェクトが 1 つ含まれます。
- **CLI での不一致。** 存在しない値を検索してください。`control-notes cli -- notes search "volcano" --format json` を実行してください。終了コードが `0` で、stdout が `[]` です。
- **証拠。** 結果が並んだ状態を記録してください。`control-notes browser snapshot --aria --path artifacts/search/results.aria.txt` と `control-notes browser screenshot --path artifacts/search/results.png` を実行してください。どちらの成果物も、Notes、クエリ、`Quarterly plan` を特定できます。

## 落とし穴（Gotchas）

- エディタか searchbox にフォーカスがあるときに `/` を押すと、検索が開かず、テキストが入力されます。
- 結果は短いデバウンスの後に更新されます。固定の sleep ではなく、結果のリストか空のステータスを待ってください。
- アーカイブしたノートは、ユーザーが `Include archived` を有効にしない限り除外されます。
- CLI は既定で人間向けの出力をします。安定した検証には `--format json` を使ってください。
- 結果を開くとブラウザの状態が変わります。別のクエリを証明する前に、検索を開き直してください。
