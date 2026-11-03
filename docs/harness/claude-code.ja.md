# Claude Code での pstack

pstack のスキルは Cursor の名前を使っています。Claude Code では、このファイルをセッションごとに 1 回読み、そのうえでスキル内の各 Cursor 名を下の表で対応付けます。`<pstack>` は `skills/` と `docs/` を置いているフォルダを指します。ある Cursor のフィールドに対応する行が無ければ、そのフィールドを落とし、そう伝えてください。ツールのスキーマが拒否するフィールドや値を渡してはいけません。

## ツール

| Cursor | Claude Code |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestion` | `AskUserQuestion`。`-p` モードでは存在しないので、プレーンテキストで質問します。 |
| todo リストを開く | セッションが提供していれば `TodoWrite` を使います。そうでなければ、リストを返信の中に持ち、フェーズごとに更新します。 |
| 別の pstack スキルを実行する（`/name` または「the **name** skill」） | `Read` で `<pstack>/skills/<name>/SKILL.md` を読み、それに従います。`Skill` ツールはほとんどの pstack スキルを拒否します。ユーザーにそれを入力するよう伝えるときは、`/pstack:<name>` と書きます。 |
| `Grep`, `Glob` | `Grep` や `Glob` が無いセッションでは、`rg` を実行する `Bash`。 |

## サブエージェントのフィールド

| Cursor | Claude Code |
| --- | --- |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |
| `poteto-agent`, `comment-sicko` | `pstack:poteto-agent`, `pstack:comment-sicko` |
| `readonly: true` | `subagent_type: "Explore"`。`Bash` はそのまま使えるので、指示書にも「do not edit files」と書き、後で `git status` を確認します。 |
| `readonly: false` | `general-purpose`。セッションの MCP サーバーはそのまま使えます。 |
| `environment: "cloud"` | `isolation: "worktree"`。ワーカーがチェックアウトするブランチかコミットを明示します。 |
| `environment: "local"` | 省略します。 |
| `cloud_base_branch: <b>` | ワーカーに `<b>` を先にチェックアウトするよう伝えます。 |
| `run_in_background: true` | 省略します。サブエージェントはデフォルトでバックグラウンドで動き、終わると通知します。 |
| `resume` | 新しいエージェントを起動し、以前の結果をその指示書に貼ります。 |
| `file_attachments` | 指示書にパスを列挙します。 |

## モデル

| Cursor | Claude Code |
| --- | --- |
| `claude-<family>-<version>-<effort>[-fast]`（例: `claude-opus-5-5-xhigh`） | `model: "opus"` と `effort: "xhigh"`。`model` に取れるのは `opus`、`sonnet`、`haiku`、`fable` だけです。`-fast` は落とします。 |
| `grok-*`、`gpt-*`、その他の Claude 以外のスラッグ | `model` を省略してセッションモデルで動かし、そう伝えます。 |
| `auto` または `inherit-parent` | `model` を省略します。 |
| `pstack-models.mdc` ルール、`~/.cursor/rules/pstack-models.mdc` | `~/.claude/rules/pstack-models.md`。Claude Code は新しいセッションごとにこれを読み込むので、ロールの行はすでにコンテキストにあります。無ければファイルを読みます。ファイルもロールの行も無い場合は、スキルのデフォルトのスラッグを使います。 |
| ロールの値 `<model> <effort>`（例: `opus high`） | `model: "opus"` と `effort: "high"`。 |

## setup-pstack

Claude Code は `~/.claude/rules/` にあるすべての `.md` ファイルを新しいセッションごとに読み込むので、`setup-pstack` はそこにルールを書きます。手順は次の変更を加えて従ってください:

- 検出。検出されるモデルは、`Agent` ツールのスキーマが挙げる `model` の値で、それぞれ `effort` の値から選んだ effort を伴います。実際のモデルは `<model> <effort>` の形で書き、たとえば `opus xhigh` です。effort は最後のトークンなので、予算の手順は書かれているとおりに動きます。
- デフォルト。各デフォルトのスラッグは上の行で対応付けます。`claude-opus-5-5-xhigh` は `opus xhigh`、`grok-4.7-xhigh-fast` は `inherit-parent` です。
- 書き込み。`~/.claude/rules/pstack-models.md` を、フロントマターなしで書きます。続いてコメント行、`# budget` の行、ステップ 5 の各ロール 1 行ずつを書きます。ファイル全体を上書きします。ロールの行を `CLAUDE.md` や `AGENTS.md` に入れてはいけません。

## パス

| Cursor | Claude Code |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/` | `.claude/skills/`, `~/.claude/skills/` |
| `~/.cursor/plugins/`, `.cursor-plugin/plugin.json` | `~/.claude/plugins/`, `.claude-plugin/plugin.json` |
| `.cursor/rules/*.mdc`、常時適用のルール | `CLAUDE.md`、`CLAUDE.md` が無い場合は `AGENTS.md`。Claude Code は `.mdc` ファイルを決して読みません。例外はモデルのルールです。「モデル」を参照。 |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>` | そのファイルが存在する場合は `<pstack>/<path>`。プラグインはスキル、`docs/guide/`、`README.md` を同梱しています。ローカルのコピーを読み、決して取得しないでください。ユーザーがリンクを必要とするときは、URL を渡します。 |
| `~/.cursor/projects/<slug>/agent-transcripts/` のトランスクリプト | `~/.claude/projects/<slug>/<session>.jsonl`。スラッグはワークスペースのパスで、`/` と `.` をそれぞれ `-` に変えたものです。たとえば `/Users/you/proj` は `-Users-you-proj` になります。そのフォルダ直下で最も新しい `.jsonl` が現在のセッションです。その `<session>/subagents/` フォルダにサブエージェントのトランスクリプトが入っています。読むのはこのワークスペースのフォルダだけにしてください。 |

## Cursor 専用の機能

Claude Code には Cursor Automations、Bugbot、Cursor のクラウドエージェント、組み込みの PR ツールはありません。手順がそのどれかを必要とするときは、返信に 1 行、`Skipped in Claude Code: <step>. <reason>.` と書いてから、次の手順に進みます。止まったり、尋ねたり、やり直したりしないでください。後の手順が、スキップした手順の成果物（URL やキーなど）を必要とするときは、プレースホルダーを置き、その行で名前を挙げます。

| Cursor | Claude Code |
| --- | --- |
| Cursor Automations: ルーティン、`update_state` のルーティン呼び出し、`api2.cursor.sh/automations` の webhook、ルーティンの起動、`SendToUser` のシークレット要求 | その 1 行を書いてスキップします。 |
| Bugbot | GitHub PR 上の Bugbot のコメントは普通のレビュースレッドなので、手順が示す forge コマンドでトリアージします。PR に Bugbot のチェックもコメントも無いときは、Bugbot を開始する、待つ、設定する手順はスキップします。 |
| Cursor のクラウドエージェント | `environment: "cloud"` は「サブエージェントのフィールド」にあるとおりワークツリーに対応します。ダッシュボードの状態や専用マシンなど、クラウドエージェントそのものを必要とする手順はスキップします。 |
| 組み込みの PR ツール | 手順が示す forge コマンド、たとえば `gh pr create` を使います。これはスキップではないので、1 行も書きません。 |
