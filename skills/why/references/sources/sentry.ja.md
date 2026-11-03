# Sentry のエラー履歴

## 検索の仕方

Sentry の MCP を使ってください。

1. **位置を把握します。** プロジェクトのスラッグと組織がわからない場合:

   ```
   find_organizations
   find_projects
   ```

2. **対象に関連するイシューを検索します。**

   ```
   search_issues (natural language, e.g., "errors in PaymentService timeout", "unhandled exceptions in uploadFile")
   ```

   対象が扱っている例外クラス名、関数名やクラス名、対象が検査しているエラーメッセージの文字列、ファイルパスからクエリを組み立ててください。

3. **リリースと期間で絞り込みます。**

   ```
   search_issue_events (filter by release, time, environment, trace ID, tags)
   get_issue_tag_values (for an issue, see distribution across versions, users, environments)
   ```

   疑わしいイシューについては、**初回観測（first seen）** と **最終観測（last seen）**（止まった時期が対象の出荷日と合いますか）、**影響リリース（affected releases）**（どのリリースで発生し、どれが修正でしたか）、**頻度の推移（frequency trajectory）**（急増してから解消しましたか）を確認してください。

4. **文脈のためにイベント全体を取得します。**

   ```
   get_sentry_resource (pass a Sentry URL or type+ID)
   ```

   スタックトレースは対象のコードを通っていますか。タグとブレッドクラムは、対象が防御している条件と一致しますか。

5. **対象の近くで入ったリリースを確認します。**

   ```
   find_releases (around the commit date of the target)
   ```

   リリースのバージョンを、PR のマージ日と突き合わせてください。

6. **Seer は控えめに使います。**

   ```
   analyze_issue_with_seer
   ```

   Seer の AI による根本原因分析は、仮説の生成器です。権威あるものではなく、推論として扱ってください。実際のイベントとスタックトレースが一次の証拠です。

## 返すもの

関連するイシューごとに:
- イシュー ID とタイトル
- プロジェクトと組織
- 初回観測 / 最終観測のタイムスタンプ
- イベント数（わかればサンプリングレート）
- 影響したリリース
- 対象との関連を示す代表的なスタックトレースの抜粋（要約ではなく、そのままの抜粋）
- 初回 / 最終観測と対象の出荷日の相関
- イシューへのリンク
- 作成者のコメントや解決のメモがあれば
