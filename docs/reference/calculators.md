# 계산기

!!! spec "계산식 출처"
    거리 분해능: \(c/B\) (경로 구분), \(c/2B\) (레이더) · TWR 오차: SS-TWR \(\tfrac12 T_{reply}(e_A-e_B)\), 비대칭 DS-TWR \((R_aR_b-D_aD_b)/(R_a+R_b+D_a+D_b)\) · 링크 버짓: FCC −41.3 dBm/MHz, Friis 자유 공간 식, 열잡음 −174 dBm/Hz · 채널: IEEE 802.15.4 HRP UWB 채널 할당

!!! basic "사용법"
    값을 바꾸면 결과가 바로 갱신됩니다. 모든 계산은 브라우저에서만 이루어지며, 공식과 상수는 `tools/uwb_numbers.py`와 같은 값을 씁니다.

## 대역폭과 거리 분해능 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>대역폭 (MHz)
      <input id="rs-bw" type="number" min="1" step="0.1" value="499.2">
    </label>
  </div>
  <div class="calc-result">
    <div>시간 분해능 1/B <b id="rs-t">—</b> ns · 레이더 분해능 c/2B <b id="rs-radar">—</b> m</div>
    <div class="calc-big">경로 구분 c/B <span id="rs-out">—</span> m</div>
    <div><small>참고: 타임스탬프 단위(칩/128) 15.65 ps = 4.69 mm</small></div>
  </div>
</div>

## TWR 클럭 드리프트 오차 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>응답 지연 T<sub>reply</sub> (µs)
      <input id="tw-reply" type="number" min="1" step="1" value="1000">
    </label>
    <label>장치 A 클럭 오프셋 (ppm)
      <input id="tw-ea" type="number" step="0.1" value="10">
    </label>
    <label>장치 B 클럭 오프셋 (ppm)
      <input id="tw-eb" type="number" step="0.1" value="-10">
    </label>
    <label>실제 거리 (m)
      <input id="tw-d" type="number" min="0" step="0.1" value="5">
    </label>
  </div>
  <div class="calc-result">
    <div>SS-TWR 거리 오차 <b id="tw-ss">—</b> m (CFO 보정 전)</div>
    <div class="calc-big">DS-TWR(비대칭) 거리 오차 <span id="tw-ds">—</span> mm</div>
    <div><small id="tw-note"></small></div>
  </div>
</div>

## 링크 버짓과 도달 거리 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>채널
      <select id="lb-ch"></select>
    </label>
    <label>거리 (m)
      <input id="lb-d" type="number" min="0.1" step="0.1" value="10">
    </label>
    <label>추가 손실 (몸·벽, dB)
      <input id="lb-loss" type="number" min="0" step="1" value="0">
    </label>
    <label>안테나 이득 합 (dBi)
      <input id="lb-g" type="number" step="0.5" value="0">
    </label>
    <label>수신 잡음 지수 (dB)
      <input id="lb-nf" type="number" min="0" step="0.5" value="6">
    </label>
    <label>수신 감도 (dBm)
      <input id="lb-sens" type="number" step="1" value="-95">
    </label>
  </div>
  <div class="calc-result">
    <div>EIRP <b id="lb-eirp">—</b> dBm · 자유 공간 손실 <b id="lb-fspl">—</b> dB · 잡음 전력 <b id="lb-n">—</b> dBm</div>
    <div class="calc-big">수신 전력 <span id="lb-pr">—</span> dBm · 감도 여유 <span id="lb-margin">—</span> dB</div>
    <div>이 감도에서 자유 공간 최대 거리 <b id="lb-range">—</b> m</div>
  </div>
</div>

## 채널 ↔ 주파수 { .l2 }

<div class="calc" markdown="0">
  <div class="calc-grid">
    <label>채널 번호
      <select id="ch-no"></select>
    </label>
  </div>
  <div class="calc-result">
    <div class="calc-big"><span id="ch-fc">—</span> MHz</div>
    <div>대역폭 <b id="ch-bw">—</b> MHz · 범위 <b id="ch-range">—</b> MHz · <span id="ch-note"></span></div>
  </div>
</div>

<script src="../../javascripts/calculators.js"></script>
