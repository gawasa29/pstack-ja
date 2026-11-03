# ルーティングマップの例

このファイルを `.cursor/automations/benny/` の外、たとえば `.cursor/benny/routing.md` にコピーし、すべてのプレースホルダーを置き換えてください。`routing.map_path` はそのコピーを指すようにします。パックのリフレッシュがそれを上書きしてはなりません。

トリアージのスキルは、これをデータとして扱います。ルートには、報告か原因追跡からの証拠（evidence）が必要です。キーワードの一致だけでは足りません。

```yaml
routes:
  - name: "billing-example"
    match:
      product_areas:
        - "billing-area-placeholder"
      code_paths:
        - "billing-code-path-placeholder"
      error_signatures:
        - "billing-error-placeholder"
    destination:
      slack_channel: "billing-channel-placeholder"
      tracker_team: "billing-team-placeholder"
    owners:
      - "billing-owner-placeholder"
    allow_feature_owner_ping: false

  - name: "desktop-example"
    match:
      product_areas:
        - "desktop-area-placeholder"
      code_paths:
        - "desktop-code-path-placeholder"
      error_signatures:
        - "desktop-error-placeholder"
    destination:
      slack_channel: "desktop-channel-placeholder"
      tracker_team: "desktop-team-placeholder"
    owners:
      - "desktop-owner-placeholder"
    allow_feature_owner_ping: false

fallback:
  destination: ""
  owners: []
  allow_feature_owner_ping: false

ping_policy:
  default: "off"
  allow:
    - "configured-feature-owner"
    - "confirmed-regression-author"
  deny:
    - "broad-on-call-group"
    - "unverified-owner"
```

## ルール

- 1 つのチームが一致しないすべての報告を受け入れる場合を除き、`fallback.destination` は空のままにしてください。
- 安定したプロダクト領域、コードパス、エラーの署名を使ってください。
- 公開するコピーに、非公開のデータを含めないでください。
- 公開する例に、生のユーザー ID やチャンネル ID を貼り付けないでください。
- 対象チームが同意するまで、機能オーナーへの ping はオフのままにしてください。
- 別ルートへの転送は、報告者にどこへ行けばよいかを伝えるものです。オートメーションはクロスポストを決してしません。
