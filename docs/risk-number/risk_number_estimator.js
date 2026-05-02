function cagrForTotalReturn(totalReturn, years) {
  return Math.pow(1 + totalReturn, 1 / years) - 1;
}

function periodReturnForTotalReturn(totalReturn, years, periodYears) {
  return Math.pow(1 + totalReturn, periodYears / years) - 1;
}

const anchors = [
  { downside: 0.02, riskNumber: 22 },
  { downside: 0.05, riskNumber: 32 },
  { downside: 0.07, riskNumber: 42 },
  { downside: 0.12, riskNumber: 62 },
  { downside: 0.18, riskNumber: 82 },
  { downside: 0.2742, riskNumber: 91 }
];

function approximateRiskNumberFromDownside(downsideMagnitude) {
  if (downsideMagnitude <= anchors[0].downside) return Math.max(1, Math.round(anchors[0].riskNumber * downsideMagnitude / anchors[0].downside));
  for (let i = 1; i < anchors.length; i++) {
    const a = anchors[i - 1];
    const b = anchors[i];
    if (downsideMagnitude <= b.downside) {
      const weight = (downsideMagnitude - a.downside) / (b.downside - a.downside);
      return Math.round(a.riskNumber + weight * (b.riskNumber - a.riskNumber));
    }
  }
  const last = anchors[anchors.length - 1];
  const prev = anchors[anchors.length - 2];
  const slope = (last.riskNumber - prev.riskNumber) / (last.downside - prev.downside);
  return Math.min(99, Math.round(last.riskNumber + slope * (downsideMagnitude - last.downside)));
}

function downsideFromReturnAndVol(sixMonthReturn, annualVolatility) {
  const sixMonthVol = annualVolatility / Math.sqrt(2);
  return sixMonthReturn - 1.64 * sixMonthVol;
}

function volForDownside(sixMonthReturn, downsideMagnitude) {
  const sixMonthVol = (sixMonthReturn + downsideMagnitude) / 1.64;
  return { sixMonthVol, annualVol: sixMonthVol * Math.sqrt(2) };
}

function pct(x) {
  return `${(100 * x).toFixed(2)}%`;
}

const targetTotalReturn = 1.0;
const years = 3;
const annualReturn = cagrForTotalReturn(targetTotalReturn, years);
const sixMonthReturn = periodReturnForTotalReturn(targetTotalReturn, years, 0.5);

console.log(`Target total return: ${pct(targetTotalReturn)} in ${years} years`);
console.log(`Required CAGR: ${pct(annualReturn)}`);
console.log(`Required 6-month compound return: ${pct(sixMonthReturn)}`);
console.log('');
console.log('Volatility implied by chosen Nitrogen-style downside:');
for (const row of [
  { label: 'RN ~45 public example', downside: 0.0821 },
  { label: 'Low 60s', downside: 0.12 },
  { label: 'Low 80s', downside: 0.18 },
  { label: 'RN ~91 public example', downside: 0.2742 }
]) {
  const vol = volForDownside(sixMonthReturn, row.downside);
  console.log(`${row.label}: downside -${pct(row.downside)}, 6m vol ${pct(vol.sixMonthVol)}, annual vol ${pct(vol.annualVol)}`);
}
console.log('');
console.log('Risk Number implied by annual volatility assumptions:');
for (const annualVol of [0.18, 0.25, 0.35, 0.50, 0.56]) {
  const downside = downsideFromReturnAndVol(sixMonthReturn, annualVol);
  const downsideMagnitude = Math.max(0, -downside);
  console.log(`Annual vol ${pct(annualVol)} -> downside ${pct(downside)} -> approx RN ${approximateRiskNumberFromDownside(downsideMagnitude)}`);
}
