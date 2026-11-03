# コード考古学（git + リポジトリ内）

## このソースに含まれるもの

- コミットの履歴（メッセージ、日付、作成者、diff）
- PR の説明、レビューコメント、議論のスレッド（`gh` 経由）
- インラインのコードコメント、TODO、FIXME、非推奨の注記
- リポジトリが残していれば ADR（アーキテクチャ決定記録）
- テスト。その名前と assert は、変更の動機になったエッジケースをしばしば織り込んでいます
- 同じコミットで変更された関連ファイル（同時変更のシグナル）
- リポジトリ内の CHANGELOG の項目とリリースノート
- コミットメッセージと PR 本文にある課題 / チケット ID

もっとも信頼でき、コードに直接結びついており、もっとも完全なソースです。リポジトリを通ったものは、すべてここにあるはずです。

## 検索の仕方

シードのコミット一覧を広げます:

```bash
# History through renames
git log --follow --oneline -- <file>

# Pickaxe: commits that added or removed this exact text
git log -S '<exact_string_from_code>' -- <file>

# Or for patterns:
git log -G '<regex>' -- <file>

# Who wrote each line and when
git blame -L <start>,<end> <file>

# One commit's full diff
git show <hash>

# Commits between two points affecting this file
git log <old>..<new> -p -- <file>
```

別系統のドキュメントを探します:

```bash
# ADRs often live in docs/adr/ or similar
rg -l -i 'architecture.decision' --glob '*.md'

# TODOs and FIXMEs near the target
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>

# Related tests
rg -l '<symbol>' --glob '*test*'
```
