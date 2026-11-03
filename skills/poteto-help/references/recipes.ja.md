# コピーする価値のあるプロンプト

実際のパス、スキル、完了条件に置き換えて使ってください。くだけた言い回しで構いません。プロンプトは打ち込むものなので原文のまま残し、各行に日本語の説明を添えています。

## 理解する

- `/poteto-mode read <thread>. restate the underlying issue in your own words, in plain english.` — スレッドを読ませ、根本の問題を自分の言葉で言い直させる。
- `/in-your-own-words <long or messy ask>` — 長く乱雑な依頼を、ゴールと問題の言葉に直させる。
- `/sharpen <the prompt you're about to send>` — 送る前のプロンプトを、大きくではなく深くする。
- `/poteto-mode investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.` — 症状を調査させ、分かっていること、使ったデータ、最良の仮説を出させる。コードはまだ変えない。
- `use /how to understand <subsystem>. then use /why to find out why it broke recently.` — まず仕組みを理解し、次に最近壊れた理由を探る。
- `/recall my work on <topic> from last week, then read <issue>.` — 先週の自分の作業を思い出させてから、issue を読む。
- `/teach me why you implemented it this way and not <other way>. what did you trade off?` — この実装を選び、別案を選ばなかった理由とトレードオフを説明させる。
- `/poteto-mode take over this branch. read the decision log, find what's done, and continue. don't redo finished work.` — ブランチを引き継ぎ、決定ログから済んだ作業を把握して続行する。終わった作業をやり直さない。

## 作る

- Bug: `/poteto-mode <symptom>. repro first, then fix and verify.` — 症状を渡し、まず再現、次に修正して検証する。
- Bug in an app: `/poteto-mode repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.` — アプリの検証スキルで再現する。main でも再現するなら直し、証拠の動画を見せる。
- Bug with a cheap test: `/poteto-mode repro <bug> first. if there's a cheap test path, /tdd it. then fix and rerun.` — まず再現する。安く回せるテスト経路があればテストを先に書き、直して再実行する。
- Feature: `/poteto-mode add <behavior>. <current output> stays byte-identical. verify both.` — 振る舞いを足す。既存の出力はバイト単位で変えない。両方を検証する。
- Refactor: `/poteto-mode move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.` — コードを 1 モジュールに移す。振る舞いは変えない。先に現在の出力を記録し、後で変わっていないことを証明する。
- Perf: `/poteto-mode <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.` — 操作が特定のフィクスチャで遅い。トレースし、測って特定した原因を直し、前後を見せる。

## 設計と計画

- `/poteto-mode prototype a few options for <feature>. take screenshots or videos for me to compare.` — 機能の案をいくつか試作し、比較用のスクリーンショットか動画を撮る。
- `/poteto-mode we need <feature>. /architect it first, and answer open questions with prototypes. let me review before proceeding.` — 機能が必要。先に設計し、未決の問いは試作で答える。進む前にレビューさせる。
- `/poteto-mode write a tutorial for how i would use <new package> first. then /teach me why it beats the current one.` — 新しいパッケージの使い方のチュートリアルを先に書く。そのうえで、現行より優れている理由を説明させる。
- `ask /arena for a second opinion on this thread and our approach.` — このスレッドと自分たちの方針について、第二の意見を求める。
- `/poteto-mode turn this design into a plan. small verifiable PRs, each with its own verification steps.` — 設計を計画にする。小さく検証可能な PR に分け、それぞれに検証手順を持たせる。
- `/poteto-mode plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.` — ライブラリの移行を計画する。小さく検証可能な PR に分ける。結果はバグも含めて元と完全に一致させる。

## レビューと出荷

- `/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` — ブランチ全体を懐疑的にレビューする。まだ何も変えない。本物のバグか退行でない限り、揚げ足は取らない。Dropped の一覧も読む。
- `/create-formal-verification-skill prove <property> holds in <module>, even when <steps> interleave or retry.` — 並行やリトライが絡んでも性質が成り立つことを、形式検証で示す。そのコードのマージやリファクタの後は `/maintain-formal-verification-skill`。
- `/swarm check every package under <dir> against its check script. one worker per package. one report.` — ディレクトリ配下の各パッケージをチェックスクリプトで確認する。1 パッケージ 1 ワーカー、報告は 1 本。
- `/poteto-mode open the pr. small ordered commits, evidence in the description.` — PR を開く。小さく順序立てたコミット、説明に証拠を書く。
- `/poteto-mode babysit this pr. get it green.` — PR を見張り、グリーンにする。状態確認だけなら `/poteto-mode check on pr <number>. anything outstanding?`。
- `/poteto-mode land the stack.` — スタックを取り込む。

## 離れて戻る

- `/poteto-mode im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. /loop until done. if you're truly stuck after a few hours, stop and write up why.` — 夜間実行の契約。完了条件、隔離したワークツリー、決定ログ、コミット前の確認不要、詰まったら止まって理由を書く。
- `/show-me-your-work catch me up on what you did last night.` — 夜の作業を振り返る。まず Attention の節を読む。
- `/ketchup` — 最後のメッセージ以降のこのチャットの変化と、判断待ちの項目を一覧にする。
- `/poteto-mode full autopilot on this queue. each item is independent.` — 独立した PR のキューを、マージまで自動で回す。
- `/poteto-mode autopilot these changes, but don't merge. i'll land them.` — 変更を自動で作り検証するが、マージはしない。自分で取り込む。
- `/reflect capture what we learned so the next run doesn't repeat it.` — 学んだことを次に活かす。将来の判断を変える編集だけを承認する。
- `/bro` — 直前の返答を平易な言葉で言い直す。
