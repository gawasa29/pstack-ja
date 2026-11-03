---
name: unslop
description: Cut AI tells from any writing.
disable-model-invocation: true
---

# unslop（AI っぽさを取り除く）

AI らしいパターンを取り除くために文章を編集します。下のパターンを走査してから書き直します。意味は保ち、意図したトーンに合わせます。

## 検出して直すパターン

ルール番号は、他のスキルが引用する安定した id です。ルールを削除しても、番号の欠番はそのまま残ります。

### 内容

3. **表面的な -ing 句。** "highlighting..."、"ensuring..."、"reflecting..."、"showcasing..."、"fostering..."。削除するか、実際の根拠を添えて展開します。
5. **曖昧な出典。** "Experts believe"、"Industry reports suggest"、"Some critics argue"。出典を名指しするか、削除します。

### 言葉づかい

7. **AI 語彙。** Additionally、crucial、delve、enduring、enhance、fostering、garner、interplay、intricate、landscape（抽象的な用法）、pivotal、showcase、tapestry（抽象的な用法）、testament、underscore、vibrant。平易な言葉に置き換えます。
8. **「is」の気取った言い方。** "serves as"、"stands as"、"boasts"、"features"。"is" か "has" と言います。
9. **「Not just X, but Y」。** 代わりに要点をまっすぐ述べます。
10. **3 つ組の法則。** 考えを無理に 3 つ組にまとめません。自然な数を使います。
11. **類語の巡回。** 1 段落の中に Protagonist、main character、central figure、hero が全部出てくるような書き方です。1 つ選び、それを繰り返します。
12. **偽の範囲。** X と Y が意味のある尺度に乗っていないのに "from X to Y" と書くことです。トピックを直接列挙します。

### スタイル

13. **em ダッシュの使いすぎ。** em ダッシュは全面的に避けます。使うのはピリオドかカンマだけです（括弧、en ダッシュ、ダッシュ代わりのハイフンも使いません）。考えを切り離す必要があるなら、文を終えるかカンマを使います。
14. **コロンの使いすぎ。** コロンはリストや例の前なら問題ありませんが、文中をつなぐ記号としては使いません。"If you're coming from traditional automation: instead of registering event handlers, you describe conditions" は、コロンを付けても何も加わりません。比較の枠組みなしで要点が単独で立つように書き直します。"Describing when the scheduler should fire works best as plain English." 意味は同じで、頼りの記号はありません。
15. **太字の使いすぎ。** 固有名詞や頭字語をすべて太字にしません。
16. **インライン見出しのリスト。** 兆候は、その行を言い換えるだけの太字ラベルとコロンです。"**Performance:** Performance improved..."。そういうものは文章に直します。ピリオドで終わり、項目を名指しし、そのあとに本当に新しい詳細が続く太字の導入（"**Schema in TypeScript.** Tables live in one file."）は問題なく、兆候ではありません。
17. **タイトルケースの見出し。** センテンスケースを使います。
18. **飾りの絵文字。** 見出しや箇条書きから取り除きます。
19. **カーリークォート。** ストレートクォートを使います。

### コミュニケーションの痕跡

20. **チャットボットの決まり文句。** "I hope this helps!"、"Let me know if..."、"Of course!"、"Certainly!"、"Found the smoking gun!"。削除します。
22. **追従的な口調。** "Great question! You're absolutely right!"。まっすぐ応答します。

### 埋め草

23. **埋め草のフレーズ。** "In order to" は "To" に、"Due to the fact that" は "Because" になります。"It is important to note that" は削除します。
24. **過剰なヘッジ。** "could potentially possibly be argued that it might" は "may" になります。
25. **ありきたりな結論。** "The future looks bright."。具体的な計画や事実を述べます。

### 専門用語

26. **抽象的な比喩の名詞。** Substrate（base）、wedge、wedge in（add）、vector（way、method）、locus、vantage、nexus、名詞としての primitive、比喩としての harness、"API surface" の surface、bedrock、比喩としての scaffolding、modality、paradigm、gold-plating（仕事に必要以上のもの）、比喩としての ratchet（機構の本当の名前か、締まる一方の上限）、コードを移すときの evacuate（move out）、endgame（最後のフェーズ）、north star、flywheel。技術的に見えますが、たいていはもっと平易で具体的な言葉があります。具体的な言葉を選びます。

### 平易な言葉

27. **どう感じるかではなく、何をするかを書く。** "the database stays close at hand"、"SQL you can read"、"types that follow your schema" は感覚を名指ししています。直し方は、仕組みか数字を名指しすることです。"`.toSQL()` returns the exact string sent to the database"、"a column rename fails the build"。その文が読者に何をしてほしいのか、何を知ってほしいのかを問い、それを書きます。具体的な指示、事実、数字として言い直せないなら、削ります。もう 1 つ確認します。その文が他のプロジェクトのドキュメントにそのまま置けても違和感がないなら、このプロジェクトについては何も言っていません。削ります。
28. **密な文は短くするか分割する。** 読者が文を解析するのに戻らないといけないなら、2 つに分けるか、節を落とします。1 文に 1 つの考えです。
29. **能動態。** 能動態を優先します。"is/are/was/were + 過去分詞" を見つけ、行為者を名指しします。"queries are validated" は "the compiler validates queries" に、"the file is parsed by the loader" は "the loader parses the file" になります。受動態が許されるのは、行為者が不明なとき、または本当にどうでもよいときだけです。
30. **副詞を削るか、より強い動詞を使う。** "runs quickly" は "is fast" か数字になり、"significantly improves" は計測された差分になります。弱い動詞を支えている副詞があるなら、その動詞が間違っています。
31. **平易な言葉を優先する。** "utilize" と "leverage" は "use" に、"facilitate" は "help" に、"numerous" は "many" に、"in the event that" は "if" になります。気取った類語がより明確なことはまれです。
32. **気取った文章。** 文字どおりの言い方があるのに比喩や飾りを使うことです。格言（"wire it or delete it"）、効果のための修辞的な断片、コードの擬人化（"the plan holds it"）、比喩的な動詞（"rides along"、"stands on"）、決まり切った枠組みのフレーズ。"A dial worth turning" は "a parameter worth varying" になります。言いたいことを言います。比喩の名詞はルール 26 が扱っています。
33. **圧縮しすぎ。** 冠詞の脱落、動詞のない断片、記号語法、略語は、読者に読むのではなく解読させることになります。"Parser rejects bad date → exit 2, no write" は "The parser rejects a bad date, exits with code 2, and writes nothing." になります。冠詞と動詞を備えた完全な文を書き、矢印や略語は書き下します。
