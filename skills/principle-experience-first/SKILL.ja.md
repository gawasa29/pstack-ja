---
name: principle-experience-first
description: "Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones."
disable-model-invocation: true
---

# Experience First

実装の都合がユーザーの喜びと衝突するときは、喜びを選びます。

- すべての機能、コントロール、オプションは正当化されなければなりません
- 出す量を減らし、質を上げます（磨かれた体験の 3 機能は、粗い 10 機能に勝ります）
- 決める前に試作します（デザインの判断は、プロダクションコードより使い捨ての HTML のほうが安く済みます）
- 細部を正しく仕上げます（トランジション、整列、余白、フィードバック、エラー状態）
- 中核のループを締めます（すべての機能は中心のワークフローに奉仕するか、道を空けるべきです）

ユーザーとは、その仕事を使う人のことです。UI ならエンドユーザーです。ライブラリや内部 API なら、それを import する同僚です。次にコードを保守するエンジニアもユーザーです。その人たちの体験も同じように重みづけし、影響をその人の視点で説明します。

土台は体験に奉仕すべきです。Foundational Thinking が仕事の*順序*を司ります。この原則は*目標*を司ります。
