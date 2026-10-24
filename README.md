# 令和8年分（2026年分）年末調整の金額データ

令和8年分の年末調整で使う主な金額（基礎控除・給与所得控除後の給与等の金額・扶養親族等の所得要件・特定親族特別控除・納期限）を、国税庁「令和8年分 年末調整のしかた」から写した JSON / CSV と、小さな計算関数（JavaScript・Python）です。すべての数字に出典ページと確認日を付けています。

直接計算する → https://getreadystack.com/ja/for/kaishain-nenmatsu-chosei-2026?ref=gh_nenmatsu

## 令和8年分で変わったこと（国税庁の資料より）

- **基礎控除**：合計所得金額 489万円以下は 104万円、489万円超655万円以下は 67万円、655万円超2,350万円以下は 62万円（改正前は 58万円が基本）。2,350万円超の区分は変わらず、2,500万円超は 0円。
- **給与所得控除の最低保障額**：65万円 → 74万円（令和8・9年分）。給与等の金額 74万1,000円未満なら給与所得は 0円。
- **扶養親族・同一生計配偶者の所得要件**：合計所得金額 58万円以下 → 62万円以下（給与だけなら 136万円以下）。
- **特定親族特別控除**（19歳以上23歳未満の親族）：合計所得金額 62万円超123万円以下で、控除額は最大 63万円（85万円以下）から 3万円まで。
- **23歳未満の扶養親族がいる人の一般生命保険料控除**：上限 4万円 → 6万円（令和8・9年分）。
- **使い始め**：改正後の金額は令和8年12月に行う年末調整から。11月までの源泉徴収事務は変わりません。
- **納期限**：年末調整分の所得税は令和9年1月12日（火）（納期の特例は1月20日（水））。
- **様式**：基礎控除申告書 兼 配偶者控除等申告書 兼 特定親族特別控除申告書 兼 所得金額調整控除申告書の「控除額の計算」等、保険料控除申告書の生命保険料控除欄が改正されています。

## ファイル

| ファイル | 中身 |
|---|---|
| `data/2026.json` | 上の金額すべて。各項目に `source`（国税庁 PDF の URL・ページ・確認日） |
| `data/2026.csv` | 基礎控除・特定親族特別控除・給与所得の特例の表（同じ出典列付き） |
| `src/nencho.js` / `src/nencho.py` | `kyuyoShotoku` / `kyuyo_shotoku`（給与所得控除後の金額）、`kyuyoShotokuKojo`（給与所得控除額）、`kisoKojo`（基礎控除額）、`tokuteiShinzokuKojo`（特定親族特別控除額） |
| `tests/official_table_rows.json` | 国税庁の「給与所得控除後の給与等の金額の表」47〜54ページの全 1,103 行 |

```js
const n = require('./src/nencho.js');
n.kyuyoShotoku(3000000);        // 2020000
n.kisoKojo(2020000);            // 1040000
n.tokuteiShinzokuKojo(900000);  // 610000
```

```python
from nencho import kyuyo_shotoku, kiso_kojo
kyuyo_shotoku(3000000)  # 2020000
kiso_kojo(2020000)      # 1040000
```

テストは表の全行（各行の下限と上限 −1 円）と、データファイルの各区分の境目を確かめます。`python3 -m unittest discover -s tests` · `node --test tests/`

## 出典（2026-10-24 確認）

- 国税庁「令和8年分 年末調整のしかた」 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/01.htm （一括 PDF：https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/nencho_all.pdf ・3〜5、47〜56ページ）
- 国税庁「変更を予定している年末調整関係書類」 https://www.nta.go.jp/users/gensen/nencho_shorui/index.htm

法令が変わったら更新します（[CHANGELOG](CHANGELOG.md)）。これは国税庁の資料を写したもので、個別の判断は国税庁の資料・税理士にご確認ください。

## English summary

Japan's 2026 (令和8年分) year-end tax adjustment amounts — basic deduction (¥1,040,000 up to ¥4.89M total income), the employment-income table with the new ¥740,000 minimum deduction, dependant income lines (¥620,000 / salary ¥1.36M), the specified-relative deduction for ages 19–22, and the January 2027 payment deadlines — as JSON/CSV with the National Tax Agency source page and read date on every number, plus small pure functions in JS and Python tested against all 1,103 rows of the official table.

Code: MIT. Data: CC BY 4.0 (source: 国税庁).
