### ワークツリーとシミュレータの片付け（Worktree and simulator cleanup）

1. スナップショットを取って監査します。`df -h /` を記録し、`scripts/worktree-audit.sh [-b <pr-base-ref>] [repo-path]` を実行します（principle-build-the-lever）。`-b` を付けないと `origin/HEAD` に対して `MERGED` を判定するので、PR の向き先が別ブランチなら `-b origin/<branch>` を渡します。パスは `git worktree list` から読むもので、手で打った `myrepo-worktrees/x` は `.cursor/worktrees/myrepo/x` にあるものを取りこぼすため、決して手入力しません（principle-encode-lessons-in-structure）。各ワークツリーをサイズ、経過、マージ状態、未コミットの作業、PR の状態、最後に触った最新のチャットで分類し、バケットを提案します。トランスクリプトの走査は遅いので、バックグラウンドで回します。
2. バケットは助言であって許可ではありません。ピン留めされたチャットと稼働中のチャットが本物のアーティファクトです（principle-prove-it-works）。その集合をユーザーかサイドバーから取得し、候補すべてと突き合わせます。この道具は、ユーザーがピン留めしていたワークツリーに `safe` と印を付けたことがあるので、ピン留め集合のほうを優先します。
3. 削除の前に使用状況を確かめます。`verify-recent-chat` の行すべてと、疑わしいものについては、サブエージェントをファンアウトしてトランスクリプトを読ませ、そのチャットがピン留めか稼働中か、どのワークツリーに触っているかを報告させます（principle-guard-the-context-window、トランスクリプトは量が膨大です）。ピン留めされたチャットは、バックグラウンドのサブエージェント経由で arena や再現用のツリーを兄弟ワークツリーに作ることがあり、名前がサイドバーに出ていなくても使用中です。サブエージェントごとに、その作業に合った推論レベルと、fast か standard の速度を選んでください（Subagents セクション参照）。
4. 取り返しのつかない喪失の前で止まります。`wip:N` は追跡対象の未コミット編集が N 個あるという意味です。diff を見せて先に判断を得てください。きれいなワークツリーの削除はブランチから戻せますが、未コミットの作業は消えます。`scratch:N` は追跡外の使い捨てで、捨てて安全ですが、ファイル名は示します。Autonomy に従い、きれいでマージ済みで使用中でないものは進めます。`wip` と使用中は止まります。
5. 確認済みの集合を剪定します。パスごとに `git worktree remove --force <path>` を実行します。無視対象のビルド成果物が残ってディレクトリが消えないなら、`rm -rf` してから `git worktree prune` を実行します。ブランチの ref は残るので、コミットは失われません。`df -h /` で確認し、一覧を取り直します。
6. シミュレータとその他の回収対象。次に大きく空くのはたいていシミュレータです。`xcrun simctl --set testing delete all`（XCTestDevices のクローン）、`xcrun simctl delete unavailable`、そして `xcrun simctl runtime list` の後に古いランタイムへ `runtime delete <id>` を実行します。必要ならさらに、Xcode の `DerivedData` と `iOS DeviceSupport`、`~/Library/Application Support/Cursor`（`state.vscdb.backup` や、ワークスペースとして開いたフォルダ名を持つ `<root>` が膨らむ `snapshots/roots/<root>`）、パッケージのキャッシュ（pnpm、uv、brew、yarn）。消してよいのは、ユーザーが残せと言っていないキャッシュだけです。

ユーザーの状態を削除するのに、滑りを捕まえるコードレビューが無い唯一のプレイブックです。だから上のゲートがレビューの代わりです。

**返信内容：** 前後の `df -h /` と空いた容量、剪定したワークツリー、残したものそれぞれの1行の理由（どのチャットが使用中か、未コミットの作業があるか）。
