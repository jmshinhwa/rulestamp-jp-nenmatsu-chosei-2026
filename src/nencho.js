// 令和8年分 年末調整の金額計算（国税庁「令和8年分 年末調整のしかた」の表・算式どおり）。円の整数。依存なし。
'use strict';

function yen(v) {
  const n = Number(v);
  if (!Number.isFinite(n) || n < 0) throw new RangeError('金額は0以上の数値で指定してください');
  return Math.floor(n);
}

// 給与所得控除後の給与等の金額（令和8年分）— 47〜54ページの表・3ページの特例
function kyuyoShotoku(salary) {
  const x = yen(salary);
  if (x > 20000000) throw new RangeError('主たる給与が2,000万円を超える人は年末調整の対象外です');
  if (x < 741000) return 0;
  if (x < 2191000) return x - 740000;
  if (x < 2193000) return 1451000;
  if (x < 2196000) return 1453000;
  if (x < 2200000) return 1456000;
  if (x < 6600000) {
    const L = Math.floor(x / 4000) * 4000;
    return L < 3600000 ? Math.floor(L * 7 / 10) - 80000 : Math.floor(L * 8 / 10) - 440000;
  }
  if (x < 8500000) return Math.floor(x * 9 / 10) - 1100000;
  return x - 1950000;
}

// 給与所得控除額 = 給与等の金額 − 給与所得控除後の給与等の金額
function kyuyoShotokuKojo(salary) {
  return yen(salary) - kyuyoShotoku(salary);
}

// 基礎控除額（令和8年分）— 56ページの表
function kisoKojo(gokei) {
  const g = yen(gokei);
  if (g <= 4890000) return 1040000;
  if (g <= 6550000) return 670000;
  if (g <= 23500000) return 620000;
  if (g <= 24000000) return 480000;
  if (g <= 24500000) return 320000;
  if (g <= 25000000) return 160000;
  return 0;
}

// 特定親族特別控除額（令和8年分・19歳以上23歳未満の親族）— 56ページの表
const TOKUTEI = [[850000, 630000], [900000, 610000], [950000, 510000], [1000000, 410000], [1050000, 310000],
  [1100000, 210000], [1150000, 110000], [1200000, 60000], [1230000, 30000]];
function tokuteiShinzokuKojo(gokei) {
  const g = yen(gokei);
  if (g <= 620000) return 0;
  for (const [max, amount] of TOKUTEI) if (g <= max) return amount;
  return 0;
}

module.exports = { kyuyoShotoku, kyuyoShotokuKojo, kisoKojo, tokuteiShinzokuKojo };
