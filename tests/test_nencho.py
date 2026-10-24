import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import nencho  # noqa: E402

ROWS = json.load(open(os.path.join(HERE, "official_table_rows.json"), encoding="utf-8"))["rows"]
DATA = json.load(open(os.path.join(HERE, "..", "data", "2026.json"), encoding="utf-8"))


class OfficialTable(unittest.TestCase):
    def test_every_official_row(self):
        self.assertEqual(len(ROWS), 1103)
        for r in ROWS:
            for x in (r["from"], r["below"] - 1):
                self.assertEqual(nencho.kyuyo_shotoku(x), r["income"], x)

    def test_special_rows_page3(self):
        self.assertEqual(nencho.kyuyo_shotoku(740999), 0)
        self.assertEqual(nencho.kyuyo_shotoku(741000), 1000)
        self.assertEqual(nencho.kyuyo_shotoku(2190999), 1450999)
        self.assertEqual(nencho.kyuyo_shotoku_kojo(1500000), 740000)   # 最低保障額 74万円

    def test_formula_rows_page54(self):
        self.assertEqual(nencho.kyuyo_shotoku(7000000), 5200000)   # 7,000,000 × 90% − 1,100,000
        self.assertEqual(nencho.kyuyo_shotoku(10000000), 8050000)  # 10,000,000 − 1,950,000
        with self.assertRaises(ValueError):
            nencho.kyuyo_shotoku(20000001)


class DataFile(unittest.TestCase):
    def test_basic_deduction_matches_data(self):
        for b in DATA["basic_deduction"]["bands"]:
            if b["gokei_max"]:
                self.assertEqual(nencho.kiso_kojo(b["gokei_max"]), b["deduction"])
            self.assertEqual(nencho.kiso_kojo(b["gokei_over"] + 1), b["deduction"])

    def test_specified_relative_matches_data(self):
        self.assertEqual(nencho.tokutei_shinzoku_kojo(620000), 0)
        for b in DATA["specified_relative_deduction"]["bands"]:
            self.assertEqual(nencho.tokutei_shinzoku_kojo(b["gokei_max"]), b["deduction"])
            self.assertEqual(nencho.tokutei_shinzoku_kojo(b["gokei_over"] + 1), b["deduction"])
        self.assertEqual(nencho.tokutei_shinzoku_kojo(1230001), 0)

    def test_every_number_has_a_source(self):
        """Every number in data/2026.json sits under an object (itself or a parent) that carries an nta.go.jp source."""
        missing = []

        def has_src(o):
            src = o.get("source") if isinstance(o, dict) else None
            return bool(src and str(src.get("url", "")).startswith("https://www.nta.go.jp/") and src.get("read"))

        def walk(o, path, covered):
            if isinstance(o, dict):
                covered = covered or has_src(o)
                for k, v in o.items():
                    if k in ("source", "official_index", "tax_year"):
                        continue
                    if isinstance(v, (int, float)) and not isinstance(v, bool) and not covered:
                        missing.append(path + "." + k)
                    walk(v, path + "." + k, covered)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, "%s[%d]" % (path, i), covered)

        walk(DATA, "", False)
        self.assertEqual(missing, [])

    def test_source_check_can_fail(self):
        bad = {"x": {"amount": 1}}
        self.assertFalse(isinstance(bad["x"].get("source"), dict))


if __name__ == "__main__":
    unittest.main()
