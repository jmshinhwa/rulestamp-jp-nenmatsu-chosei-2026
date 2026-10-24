'use strict';
const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const n = require('../src/nencho.js');
const ROWS = require(path.join(__dirname, 'official_table_rows.json')).rows;
const DATA = require(path.join(__dirname, '..', 'data', '2026.json'));

test('every official table row (pages 47-54)', () => {
  assert.strictEqual(ROWS.length, 1103);
  for (const r of ROWS) for (const x of [r.from, r.below - 1]) assert.strictEqual(n.kyuyoShotoku(x), r.income, String(x));
});

test('special rows and formulas', () => {
  assert.strictEqual(n.kyuyoShotoku(740999), 0);
  assert.strictEqual(n.kyuyoShotoku(741000), 1000);
  assert.strictEqual(n.kyuyoShotokuKojo(1500000), 740000);
  assert.strictEqual(n.kyuyoShotoku(7000000), 5200000);
  assert.strictEqual(n.kyuyoShotoku(10000000), 8050000);
  assert.throws(() => n.kyuyoShotoku(20000001));
});

test('basic deduction and specified relative deduction match data/2026.json', () => {
  for (const b of DATA.basic_deduction.bands) {
    if (b.gokei_max) assert.strictEqual(n.kisoKojo(b.gokei_max), b.deduction);
    assert.strictEqual(n.kisoKojo(b.gokei_over + 1), b.deduction);
  }
  for (const b of DATA.specified_relative_deduction.bands) {
    assert.strictEqual(n.tokuteiShinzokuKojo(b.gokei_max), b.deduction);
    assert.strictEqual(n.tokuteiShinzokuKojo(b.gokei_over + 1), b.deduction);
  }
  assert.strictEqual(n.tokuteiShinzokuKojo(620000), 0);
  assert.strictEqual(n.tokuteiShinzokuKojo(1230001), 0);
});
