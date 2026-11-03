# pstack 日本語訳（勉強用）

pstack の読み物としての日本語訳です。Cursor / Claude Code に読み込ませる実行用のプラグインではありません。

| 項目 | 内容 |
|---|---|
| 原文 | [`cursor/plugins`](https://github.com/cursor/plugins) の `pstack/` |
| 版 | 0.15.36（commit `ae5650f`） |
| 原本の場所 | `~/work/cursor-plugins/pstack/`（sparse-checkout） |
| 訳文の場所 | `~/work/pstack-ja/` |
| 規模 | 136 ファイル / 7,881 行 |
| ライセンス | MIT（[LICENSE](./LICENSE)、原文の著作権表示を保持） |

## 読み方

初めてなら、この順が素直です。

1. [README.ja.md](./README.ja.md) — pstack の思想と全体像
2. [docs/guide/README.ja.md](./docs/guide/README.ja.md) — 10 章のガイド。セットアップから夜間実行まで
3. [skills/poteto-mode/SKILL.ja.md](./skills/poteto-mode/SKILL.ja.md) — 入口スキルの本体。ルーティング規則、自律性、返答の書き方
4. [playbooks](./skills/poteto-mode/playbooks/) — 23 の手順書。まず bug-fix、feature、shipping あたり
5. [原則 24 本](./skills/principle-prove-it-works/SKILL.ja.md) — 判断の名前。`08-principles.ja.md` と併読
6. 必要になったスキル — [how](./skills/how/SKILL.ja.md)、[why](./skills/why/SKILL.ja.md)、[architect](./skills/architect/SKILL.ja.md) など

## 構成

```
pstack-ja/
├── README.ja.md                  … リポジトリ README の訳
├── docs/
│   ├── guide/                    … 01〜10 + README（images も同梱）
│   └── harness/claude-code.ja.md … Claude Code アダプタ
├── skills/
│   ├── <name>/SKILL.ja.md        … 58 スキル
│   ├── poteto-mode/playbooks/    … 23 プレイブック
│   ├── <name>/references/        … 参照ドキュメント
│   └── principle-*/              … 原則 24 本
├── agents/                       … poteto-agent / comment-sicko
├── automations/benny/            … 休眠中の Slack オートメーションパック
├── tools/                        … リンク修正と検証スクリプト
├── LICENSE
└── TRANSLATION.md                … このファイル
```

## 翻訳の方針

- **フロントマターは原文のまま**。`name` はディレクトリ名と一致する必要があり、`description` はスキルの呼び出しやメニュー表示に使われるため、訳すと壊れます。
- **識別子は訳さない**。スキル名（`poteto-mode`、`unslop` など）、コマンド（`/architect`）、プレイブック名、原則名（`principle-*`）、パス、ファイル名、モデルのスラッグ、`subagent_type` は原文のまま。
- **コード・コマンド・CLI 出力は原文のまま**。読者がそのままコピーできるようにします。
- **プロンプト例も原文のまま**。`/poteto-mode ...` のような入力例は、訳すと動かないので残しました。
- **見出し・本文・表・画像の alt・mermaid のラベルは日本語化**。mermaid の構文とノード ID は変えていません。
- **H1 は「日本語（English）」形式**。原則スキルだけは原則名そのものなので英語のまま（`# Prove It Works`）。`bro`、`in-your-own-words`、`sharpen` は原文に H1 がありません。
- **相対リンクは `.ja.md` に張り替え済み**。ただし訳文の見出しは日本語なので、原文の `#anchor` は落とし、ページ先頭へ飛ぶようにしています。
- **画像は原本からコピー**（`docs/guide/images`、`assets`）。訳文でも表示されます。
- 原文が 80 桁で折り返しているファイル（`bugbot-triage.md` など）は、日本語では折り返さないため行数が減っています。内容は欠けていません。
- **スクリプトと設定は翻訳対象外**。`skills/**/scripts/`、`automations/benny/templates/configuration.example.yaml` は原文のままです。`multi-phase-plan` の計画テンプレートも、`check-plan.mjs` が英語リテラルを検証するため原文のまま残しました。

## 用語集

| 原文 | 訳語 | 備考 |
|---|---|---|
| skill / playbook / principle | スキル / プレイブック / 原則 | 名前は原文のまま |
| subagent | サブエージェント | |
| verification / verify | 検証 / 検証する | `validation` は「バリデーション」で区別 |
| evidence / decision log | 証拠 / 決定ログ | `trail` は「証跡」 |
| finish condition / done check | 完了条件 / 合格条件 | |
| root cause | 根本原因 | |
| repro / reproduce | 再現 | `repro first` は原文のまま残す箇所あり |
| slop / unslop | slop（中身の薄い量産コード）/ unslop | スキル名は原語 |
| worktree / stack / land | ワークツリー / スタック / 取り込む（land） | |
| ship / merge / diff / commit | 出荷する / マージ / diff / コミット | |
| gate / harness / rubric | ゲート / ハーネス / ルーブリック | |
| formal verification / statechart | 形式検証 / ステートチャート | |
| finding / brief / lane / verdict | 所見 / ブリーフ / レーン / 判定 | |
| receipts / countersign / surface | 証跡 / 副署 / サーフェス | |
| fail closed / preflight | フェイルクローズ / プリフライト | benny パック |
| autonomy grant | 自律委任 | |
| flaky / spec / stub | フレーキー / 仕様 / スタブ | |
| overnight / pitfall | 夜間 / 落とし穴 | |

## 検証

`tools/` の 3 本で、原文との対応を機械的に確認できます。

```bash
python3 tools/check_coverage.py   # 原文 136 ファイルすべてに訳があるか
python3 tools/check_structure.py  # 見出し・コードフェンス・リンク先・インラインコードの一致
python3 tools/fix_links.py        # 相対リンクを .ja.md に張り替える（冪等）
```

現在の結果:

- カバレッジ: **136 / 136 ファイル**（未訳 0）
- 構造: 差分は 2 件だけ。`README.ja.md` の空行 5 本と `<your-name>-mode` の訳、`bugbot-triage.ja.md` の折り返しによる行数差。どちらも内容の欠落ではありません。
- 内部リンク: すべて解決。例外は synthesizer プロンプトの `[PR #123](url)` で、これは原文どおりのプレースホルダーです。

## 既知の注意点

- **アンカーは飛びません**。見出しを日本語化したため、原文の `#section` は訳文に対応する見出しがありません。リンクはページ単位で解決します。
- **H1 の英語併記は揺れがあります**。原則は英語のみ、一部のスキルは英語併記なしです。正式な識別子はフロントマターの `name` を見てください。
- **benny パック内で「トリアージマーカー」と「印」が混在**しています。意味は同じです。
- **原文の不備もそのまま**。たとえば `skills/why/references/sources/slack.md` の番号付きリストは 1, 3, 4 と 2 が抜けています。`principle-migrate-callers-then-delete-legacy-apis` の本文も原文どおり断片的です。
- 原文は更新が速い（1 週間で 2 版）ので、訳文は版 0.15.36 時点のスナップショットです。

## 更新するとき

```bash
cd ~/work/cursor-plugins && git pull          # 原文を更新（sparse-checkout）
cd ~/work/pstack-ja && python3 tools/fix_links.py
```

訳文は原文と別ツリーなので、上流の変更は自動では入りません。差分を見て手で反映してください。

## ライセンス

原文は MIT（Copyright (c) 2026 Lauren Tan）。この訳文も同じ条件で扱います。[LICENSE](./LICENSE) を同梱しています。
