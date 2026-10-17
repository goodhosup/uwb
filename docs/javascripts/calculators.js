// 레퍼런스 > 계산기 페이지 전용 스크립트
// 상수와 공식은 tools/uwb_numbers.py와 같은 값을 쓴다 (본문 수치의 단일 출처).
(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  if (!$("rs-bw")) return;
  const num = (id) => parseFloat($(id).value);
  const fmt = (x, d = 1) => Number.isFinite(x) ? x.toLocaleString("ko-KR", { maximumFractionDigits: d, minimumFractionDigits: d }) : "—";

  const C = 299792458;
  const PSD = -41.3; // dBm/MHz (FCC 실내)
  // 채널: [중심 MHz, 대역폭 MHz, 대역]
  const CH = {
    0: [499.2, 499.2, "sub-GHz"], 1: [3494.4, 499.2, "low"], 2: [3993.6, 499.2, "low"], 3: [4492.8, 499.2, "low"],
    4: [3993.6, 1331.2, "low"], 5: [6489.6, 499.2, "high"], 6: [6988.8, 499.2, "high"], 7: [6489.6, 1081.6, "high"],
    8: [7488.0, 499.2, "high"], 9: [7987.2, 499.2, "high"], 10: [8486.4, 499.2, "high"], 11: [7987.2, 1331.2, "high"],
    12: [8985.6, 499.2, "high"], 13: [9484.8, 499.2, "high"], 14: [9984.0, 499.2, "high"], 15: [9484.8, 1354.97, "high"],
  };
  const MANDATORY = { 0: true, 3: true, 9: true };
  const fspl = (d, fHz) => 20 * Math.log10(4 * Math.PI * d * fHz / C);

  function resolution() {
    const bw = num("rs-bw") * 1e6;
    $("rs-t").textContent = fmt(1e9 / bw, 3);
    $("rs-radar").textContent = fmt(C / (2 * bw), 3);
    $("rs-out").textContent = fmt(C / bw, 3);
  }

  function twr() {
    const tr = num("tw-reply") * 1e-6;
    const ea = num("tw-ea") * 1e-6;
    const eb = num("tw-eb") * 1e-6;
    const tof = num("tw-d") / C;
    $("tw-ss").textContent = fmt(C * 0.5 * tr * (ea - eb), 3);
    // 비대칭 DS-TWR: A가 측정하는 Ra, Da와 B가 측정하는 Rb, Db (각자 자기 클럭으로)
    const db = tr, da = 1.5 * tr; // B의 응답 지연, A의 두 번째 지연 (비대칭 예)
    const Ra = (2 * tof + db) * (1 + ea), Da = da * (1 + ea);
    const Rb = (2 * tof + da) * (1 + eb), Db = db * (1 + eb);
    const est = (Ra * Rb - Da * Db) / (Ra + Rb + Da + Db);
    $("tw-ds").textContent = fmt((est - tof) * C * 1000, 3);
    $("tw-note").textContent = `DS-TWR 예시는 B의 응답 지연 ${fmt(db * 1e6, 0)} µs, A의 두 번째 지연 ${fmt(da * 1e6, 0)} µs인 비대칭 교환으로 계산했습니다.`;
  }

  function linkBudget() {
    const [fc, bw] = CH[$("lb-ch").value];
    const eirp = PSD + 10 * Math.log10(bw);
    const L = fspl(num("lb-d"), fc * 1e6);
    const pr = eirp + num("lb-g") - L - num("lb-loss");
    const n = -174 + 10 * Math.log10(bw * 1e6) + num("lb-nf");
    const allowed = eirp + num("lb-g") - num("lb-loss") - num("lb-sens");
    const range = Math.pow(10, (allowed - 20 * Math.log10(4 * Math.PI * fc * 1e6 / C)) / 20);
    $("lb-eirp").textContent = fmt(eirp);
    $("lb-fspl").textContent = fmt(L);
    $("lb-n").textContent = fmt(n);
    $("lb-pr").textContent = fmt(pr);
    $("lb-margin").textContent = fmt(pr - num("lb-sens"));
    $("lb-range").textContent = fmt(range);
  }

  function channel() {
    const k = $("ch-no").value;
    const [fc, bw, band] = CH[k];
    $("ch-fc").textContent = fmt(fc, 1);
    $("ch-bw").textContent = fmt(bw, 2);
    $("ch-range").textContent = `${fmt(fc - bw / 2, 1)} – ${fmt(fc + bw / 2, 1)}`;
    const notes = [`${band} 대역`];
    if (MANDATORY[k]) notes.push("대역별 필수 채널");
    if (k === "5" || k === "9") notes.push("스마트폰·디지털 키에서 주로 사용");
    $("ch-note").textContent = notes.join(" · ");
  }

  const opts = Object.entries(CH).map(([k, [fc]]) => `<option value="${k}">Ch${k} (${fc} MHz)</option>`).join("");
  $("lb-ch").innerHTML = opts;
  $("lb-ch").value = "9";
  $("ch-no").innerHTML = opts;
  $("ch-no").value = "9";

  const bind = (ids, fn) => { ids.forEach((id) => $(id).addEventListener("input", fn)); fn(); };
  bind(["rs-bw"], resolution);
  bind(["tw-reply", "tw-ea", "tw-eb", "tw-d"], twr);
  bind(["lb-ch", "lb-d", "lb-loss", "lb-g", "lb-nf", "lb-sens"], linkBudget);
  bind(["ch-no"], channel);
})();
