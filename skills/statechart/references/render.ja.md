# チャートを描画する

ユーザーに見せる `.mmd` ファイルはそれぞれ、npm パッケージ `pele@1.9.0` で描画し、SVG をユーザーに渡してください。Pele はリポジトリの外に一度だけインストールします。各 SVG は、対応する `.mmd` ファイルと同じ名前で、その隣に書いてください。API は https://pele.run/api です。`render` のオプションには `{ limit: 1_000_000, outputLimit: 8_000_000, maxEdges: 10_000 }` を渡してください。Pele の既定値は、500 状態のチャートが収まるより小さいためです。Pele が `PeleError` を投げたら、Mermaid のテキストとエラーをユーザーに見せてください。

## 色

Pele は Mermaid の `theme` と `themeVariables` を無視します。`--pele-*` の CSS 変数を `.pele` に設定してください。一覧は https://pele.run/theming にあります。コマンドは各状態に、そのグループの色クラス（`class sN teal` など）を付けます。壊れた状態には `class sN breaks` か `class sN mayBreak`、バグへの最短経路上の状態には `class sN bugPath`、PROPERTY の反例が永遠に繰り返す状態には `class sN repeats` を付けます。Pele はこれらのクラスを状態のノードに置きます。クラスは CSS で色付けしてください。

`.mmd` ファイルには `breaks` と `mayBreak` の `classDef` 行があるので、どの Mermaid ビューアでもバグの印が表示されます。グループの色、`bugPath`、`repeats` の `classDef` はありません。Pele は各 `classDef` の色をノードの `style` 属性として書き出し、`style` 属性は通常の CSS ルールに優先します。そのため、下の印のルールは `!important` を使います。これがないと、ダークテーマでも明るい印の色のままになります。バグの印は塗りとテキストを設定し、`bugPath` と `repeats` は枠線を設定します。印がグループの色の上に出るよう、印のルールはグループの色の後に置いてください。

この色は提案です。旧スキルの色です。各 SVG の先頭の `<style>` 要素に入れてください。そうすれば各 SVG は、ビューアのライト／ダーク設定に従います。

```css
.pele {
  --pele-bg: #ffffff;
  --pele-fg: #1c1c1c;
  --pele-muted: #656565;
  --pele-line: #808080;
  --pele-surface: #fcfcfc;
  --pele-surface-alt: #f1f1f1;
  --pele-border: #c9c9c9;
}
.pele .blue rect { fill: #c3e0ff; }
.pele .orange rect { fill: #f0d3bf; }
.pele .purple rect { fill: #e3d5ff; }
.pele .yellow rect { fill: #f0dcbf; }
.pele .teal rect { fill: #bfe3df; }
.pele .tan rect { fill: #e5d9ce; }
.pele .pink rect { fill: #ffcbe6; }
.pele .breaks rect {
  fill: #ffecee !important;
  stroke: #e72e3b !important;
  stroke-width: 2.5px !important;
}
.pele .breaks text {
  fill: #cd2834 !important;
}
.pele .mayBreak rect {
  fill: #fff3e6 !important;
  stroke: #e8730c !important;
  stroke-width: 2.5px !important;
}
.pele .mayBreak text {
  fill: #b85a06 !important;
}
.pele .bugPath rect {
  stroke: #1680f3 !important;
  stroke-width: 2.5px !important;
}
.pele .repeats rect {
  stroke: #9b35d6 !important;
  stroke-width: 2.5px !important;
  stroke-dasharray: 6 3;
}
@media (prefers-color-scheme: dark) {
  .pele {
    --pele-bg: #1f1f1f;
    --pele-fg: #f5f5f5;
    --pele-muted: #acacac;
    --pele-line: #939393;
    --pele-surface: #121212;
    --pele-surface-alt: #2c2c2c;
    --pele-border: #4e4e4e;
  }
  .pele .blue rect { fill: #1b3857; }
  .pele .orange rect { fill: #573117; }
  .pele .purple rect { fill: #3c2e57; }
  .pele .yellow rect { fill: #573d17; }
  .pele .teal rect { fill: #174641; }
  .pele .tan rect { fill: #3d3127; }
  .pele .pink rect { fill: #57233e; }
  .pele .breaks rect {
    fill: #2e2021 !important;
    stroke: #cf2b35 !important;
  }
  .pele .breaks text {
    fill: #ff6463 !important;
  }
  .pele .mayBreak rect {
    fill: #2e2619 !important;
    stroke: #d0700f !important;
  }
  .pele .mayBreak text {
    fill: #ffa257 !important;
  }
  .pele .bugPath rect {
    stroke: #116dd2 !important;
  }
  .pele .repeats rect {
    stroke: #9a3fcf !important;
  }
}
```
