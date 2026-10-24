"""令和8年分 年末調整の金額計算（国税庁「令和8年分 年末調整のしかた」の表・算式どおり）。円の整数。依存なし。"""


def _yen(v):
    n = float(v)
    if n != n or n < 0:
        raise ValueError("金額は0以上の数値で指定してください")
    return int(n)


def kyuyo_shotoku(salary):
    """給与所得控除後の給与等の金額（令和8年分）— 47〜54ページの表・3ページの特例"""
    x = _yen(salary)
    if x > 20000000:
        raise ValueError("主たる給与が2,000万円を超える人は年末調整の対象外です")
    if x < 741000:
        return 0
    if x < 2191000:
        return x - 740000
    if x < 2193000:
        return 1451000
    if x < 2196000:
        return 1453000
    if x < 2200000:
        return 1456000
    if x < 6600000:
        l = x // 4000 * 4000
        return l * 7 // 10 - 80000 if l < 3600000 else l * 8 // 10 - 440000
    if x < 8500000:
        return x * 9 // 10 - 1100000
    return x - 1950000


def kyuyo_shotoku_kojo(salary):
    """給与所得控除額 = 給与等の金額 − 給与所得控除後の給与等の金額"""
    return _yen(salary) - kyuyo_shotoku(salary)


def kiso_kojo(gokei):
    """基礎控除額（令和8年分）— 56ページの表"""
    g = _yen(gokei)
    for limit, amount in ((4890000, 1040000), (6550000, 670000), (23500000, 620000),
                          (24000000, 480000), (24500000, 320000), (25000000, 160000)):
        if g <= limit:
            return amount
    return 0


_TOKUTEI = ((850000, 630000), (900000, 610000), (950000, 510000), (1000000, 410000), (1050000, 310000),
            (1100000, 210000), (1150000, 110000), (1200000, 60000), (1230000, 30000))


def tokutei_shinzoku_kojo(gokei):
    """特定親族特別控除額（令和8年分・19歳以上23歳未満の親族）— 56ページの表"""
    g = _yen(gokei)
    if g <= 620000:
        return 0
    for limit, amount in _TOKUTEI:
        if g <= limit:
            return amount
    return 0
