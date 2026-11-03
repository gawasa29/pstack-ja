# ノートを作る

ノートの作成では、ユーザーがブラウザか CLI からタイトル付きのノートを保存し、書きかけの下書きをキャンセルし、保存したノートを別のユーザー向け画面で確認できます。

## サブ機能（Sub-features）

- `create-open` は、ブラウザの各入口から空のエディタを開きます。
- `create-save` は、タイトルと本文を永続化します。
- `create-cancel` は、書きかけのブラウザの下書きを破棄します。
- `create-cli` は、ターミナルから同じ形のノートを作ります。

## たどり着き方（How to get to it (user POV)）

- ブラウザのツールバーで `New note` ボタンを選んでください。
- ブラウザで、フォーカスが編集可能なフィールドの外にあるときに `n` を押してください。
- ターミナルで `notes create --title <title> --body <body>` を実行してください。

## control-notes での操作（Driving it with control-notes）

Preconditions:

- Notes が `http://127.0.0.1:4173` で正常に動いている。
- `Release checklist` というタイトルのノートが存在しない。
- `control-notes doctor` が、期待する URL と使い捨てのデータディレクトリを報告する。

- **エディタを開く。** `New note` を選んでください。`control-notes browser click --role button --name "New note"` を実行してください。`Note editor` という名前のフォームが現れ、`Title` テキストボックスにフォーカスがあります。
- **内容を入力する。** タイトルと本文を入力してください。`control-notes browser fill --role textbox --name "Title" --value "Release checklist"` と `control-notes browser fill --role textbox --name "Body" --value "Tag and publish"` を実行してください。`Save note` ボタンが有効になります。
- **ノートを保存する。** `Save note` を選んでください。`control-notes browser click --role button --name "Save note"` を実行してください。`Note saved` という名前のステータスが現れ、見出しが `Release checklist` になります。
- **永続化を確認する。** ノート一覧に戻り、ノートを開き直してください。`control-notes browser click --role link --name "All notes"` と `control-notes browser click --role link --name "Release checklist"` を実行してください。エディタに、保存した 2 つの値が表示されます。
- **下書きをキャンセルする。** 新しいノートを開き、`Discard me` を入力し、`Cancel` を選んでください。`control-notes browser click --role button --name "New note"`、`control-notes browser fill --role textbox --name "Title" --value "Discard me"`、`control-notes browser click --role button --name "Cancel"` を実行してください。ノート一覧に戻り、`Discard me` のリンクはありません。
- **CLI からの入口。** 2 つ目のノートを作ってください。`control-notes cli -- notes create --title "CLI note" --body "Created from terminal" --format json` を実行してください。終了コードが `0` で、stdout に新しいノートの ID とタイトルが含まれます。
- **証拠。** `All notes` から保存した 2 つのノートを開き直してください。`control-notes browser snapshot --aria --path artifacts/create-note/list.aria.txt` と `control-notes browser screenshot --path artifacts/create-note/list.png` を実行してください。成果物に `Release checklist` と `CLI note` が写っています。

## 落とし穴（Gotchas）

- テキストボックスにフォーカスがあるときに `n` を押すと、新しいエディタが開かず、文字が入力されます。
- 保存時にタイトルは前後の空白が取り除かれます。下書きの入力値ではなく、描画されたタイトルを検証してください。
- 保存のステータスだけでは、証拠として不十分です。一覧からノートを開き直してください。
- フィクスチャの片付けで `Release checklist` と `CLI note` を削除しますが、その証拠の成果物は残してください。
