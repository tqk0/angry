
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="怒りのレトリーバー！にんじんダッシュ",
    page_icon="🥕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 520px;
      }
      header[data-testid="stHeader"] {
        background: transparent;
      }
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DotGothic16&family=Press+Start+2P&display=swap" rel="stylesheet" />
<style>
  * { box-sizing: border-box; user-select: none; -webkit-user-select: none; }
  body {
    margin: 0;
    padding: 8px;
    background: #121620;
    color: #F8FAFC;
    font-family: 'DotGothic16', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .hud {
    width: 100%;
    max-width: 380px;
    background: #181E2B;
    border: 2px solid #2A3347;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .hud-col { display: flex; flex-direction: column; }
  .hud-label { font-size: 11px; color: #94A3B8; }
  .hud-val { font-family: 'Press Start 2P', monospace; font-size: 13px; color: #FDE073; margin-top: 2px; }
  .hud-sub { font-size: 12px; color: #F8FAFC; margin-top: 2px; }
  .stage-wrap {
    position: relative;
    width: 100%;
    max-width: 380px;
  }
  canvas {
    width: 100%;
    height: auto;
    display: block;
    border: 4px solid #273043;
    border-radius: 12px;
    background: #5C94FC;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    touch-action: none;
    cursor: grab;
  }
  .controls {
    width: 100%;
    max-width: 380px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 8px;
  }
  .ctrl-btn {
    height: 44px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    background: #1E2433;
    color: #F8FAFC;
    font-family: 'DotGothic16', sans-serif;
    font-size: 14px;
    cursor: pointer;
  }
  .ctrl-btn:active { transform: translateY(1px); background: #2A3347; }
  .overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(14, 19, 29, 0.8);
    border-radius: 12px;
  }
  .card {
    width: 100%;
    max-width: 295px;
    background: #161B26;
    border: 2px solid #F59E0B;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }
  .card h2 { margin: 6px 0 8px; font-size: 21px; line-height: 1.35; color: #FFFFFF; }
  .card p { margin: 0; font-size: 12px; color: #CBD5E1; line-height: 1.6; }
  .kicker { font-size: 12px; color: #FDE073; }
  .start-btn {
    margin-top: 16px;
    width: 100%;
    padding: 12px 16px;
    border: none;
    border-radius: 8px;
    background: #FF6B1A;
    color: #FFFFFF;
    font-family: 'DotGothic16', sans-serif;
    font-size: 16px;
    cursor: pointer;
  }
  .start-btn:hover { background: #FF7F38; }
  .stats-box {
    margin-top: 12px;
    padding: 10px 0;
    border-top: 1px solid rgba(255,255,255,0.12);
    border-bottom: 1px solid rgba(255,255,255,0.12);
    font-size: 13px;
  }
  .stat-row { display: flex; justify-content: space-between; margin: 4px 0; }
  .top-actions {
    width: 100%;
    max-width: 380px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    font-size: 12px;
    color: #94A3B8;
  }
  .mute-btn {
    background: #1E2433;
    border: 1px solid rgba(255,255,255,0.12);
    color: #F8FAFC;
    border-radius: 6px;
    padding: 4px 10px;
    font-family: 'DotGothic16', sans-serif;
    font-size: 12px;
    cursor: pointer;
  }
</style>
</head>
<body>
  <div class="top-actions">
    <span>スワイプ / 矢印キーで3レーン移動</span>
    <button id="muteBtn" class="mute-btn">音: ON</button>
  </div>

  <div class="hud">
    <div class="hud-col">
      <span class="hud-label">スコア / BEST</span>
      <span class="hud-val" id="scoreVal">0</span>
      <span class="hud-sub" id="bestVal">BEST 0</span>
    </div>
    <div class="hud-col" style="text-align:center;">
      <span class="hud-label">のこり時間</span>
      <span class="hud-val" id="timeVal">60s</span>
      <span class="hud-sub" id="levelVal">LV.1 おさんぽ</span>
    </div>
    <div class="hud-col" style="text-align:right;">
      <span class="hud-label">ライフ / 🥕</span>
      <span class="hud-val" id="livesVal">♥♥♥</span>
      <span class="hud-sub" id="carrotVal">0本</span>
    </div>
  </div>

  <div class="stage-wrap">
    <canvas id="gameCanvas" width="360" height="560"></canvas>

    <div id="titleOverlay" class="overlay">
      <div class="card">
        <div class="kicker">1分間 3レーン・ランゲーム</div>
        <h2>怒りのレトリーバー！<br/>にんじんダッシュ</h2>
        <p>指で左右にスライド（または矢印キー）して障害物をよけ、60秒間にんじんを集めよう！</p>
        <button id="startBtn" class="start-btn">ゲームスタート</button>
      </div>
    </div>

    <div id="endOverlay" class="overlay" style="display:none;">
      <div class="card">
        <div class="kicker" id="endKicker">60秒完走！</div>
        <h2 id="endTitle">ステージクリア！</h2>
        <div class="stats-box">
          <div class="stat-row"><span>スコア</span><strong id="endScore" style="color:#FDE073;">0</strong></div>
          <div class="stat-row"><span>ハイスコア</span><strong id="endBest">0</strong></div>
          <div class="stat-row"><span>にんじん / 最大コンボ</span><span id="endDetail">0本 · 0</span></div>
        </div>
        <button id="restartBtn" class="start-btn">もういちどあそぶ</button>
      </div>
    </div>
  </div>

  <div id="touchControls" class="controls" style="display:none;">
    <button class="ctrl-btn" id="leftBtn">◀ ひだり</button>
    <button class="ctrl-btn" id="centerBtn">まんなか</button>
    <button class="ctrl-btn" id="rightBtn">みぎ ▶</button>
  </div>

<script>
(() => {
  const CANVAS_W = 360, CANVAS_H = 560, SKY_H = 76, GRASS_W = 48;
  const ROAD_W = CANVAS_W - GRASS_W * 2, LANE_W = ROAD_W / 3, PLAYER_Y = 456;
  const DURATION = 60, MAX_LIVES = 3;
  const BEST_KEY = 'golden_carrot_dash_best_st';

  const TIERS = [
    { level: 1, label: 'おさんぽ', speed: 235, interval: 820, dbl: 0.08, carrot: 0.62 },
    { level: 2, label: 'かけあし', speed: 295, interval: 690, dbl: 0.22, carrot: 0.56 },
    { level: 3, label: '本気ダッシュ', speed: 360, interval: 575, dbl: 0.36, carrot: 0.52 },
    { level: 4, label: 'ぷんぷん猛走', speed: 430, interval: 475, dbl: 0.48, carrot: 0.48 },
    { level: 5, label: '鬼ごっこMAX', speed: 505, interval: 395, dbl: 0.60, carrot: 0.45 },
  ];

  const PAL = {
    K:'#1A120E', k:'#4A2810', e:'#1E1410', g:'#F8B43C', l:'#FFE8A3', d:'#D9821E',
    w:'#FFFFFF', p:'#FF8FA3', r:'#EF4444', y:'#FDE047',
    G:'#F59E0B', L:'#FDE073', D:'#C2670A', W:'#FFFFFF', R:'#E63946',
    P:'#FCA5A5', O:'#FF6B1A', Y:'#FFA834', C:'#B44309', V:'#22C55E', F:'#15803D',
    B:'#C84C0C', H:'#FC9838', N:'#00A800', S:'#80D010', E:'#005800', T:'#9E4718',
    U:'#D97724', Z:'#FDE68A', A:'#F59E0B', X:'#B45309'
  };

  function mkSprite(rows, sc) {
    const c = document.createElement('canvas');
    c.width = rows[0].length * sc;
    c.height = rows.length * sc;
    const x = c.getContext('2d');
    x.imageSmoothingEnabled = false;
    for (let r = 0; r < rows.length; r++) {
      for (let col = 0; col < rows[r].length; col++) {
        const ch = rows[r][col];
        if (ch !== '.' && PAL[ch]) {
          x.fillStyle = PAL[ch];
          x.fillRect(col * sc, r * sc, sc, sc);
        }
      }
    }
    return c;
  }

  const SPRITES = {
    run1: mkSprite([
      '........................','.......kkkkkkkkkk.......','.....kkggggggggggkk.....','....kggggggggggggggk....',
      '...kddggggggggggggddk...','..kdddggkggggggkggdddk..','..kdddgggkggggkgggdddk..','.kddddggweggggweggddddk.',
      '.kddddggeegllgeeggddddk.','.kdddggpplleellppggdddk.','..kddkgglllkklllggkddk..','...kkgggllkllkllgggkk...',
      '.....krrrrryyrrrrrk.....','.....kggggllllggggk.....','....kggggllllllggggk....','....kggggllllllggggkggk.',
      '....kggggllllllggggkllk.','....kgggggllllgggggkkk..','....klllgggggggglllk....','....klllkggkkggklllk....',
      '.....kkk.kdkkdk.kkk.....','.........kk..kk.........','........................','........................'
    ], 3),
    run2: mkSprite([
      '.......kkkkkkkkkk.......','.....kkggggggggggkk.....','....kggggggggggggggk....','..kkddggggggggggggddkk..',
      '.kddddggkggggggkggddddk.','kddddggggkggggkggggddddk','kddddgggweggggwegggddddk','.kdddgggeegllgeegggdddk.',
      '.kdddggpplleellppggdddk.','..kddkgglllkklllggkddk..','...kkgggllkllkllgggkk...','.....krrrrryyrrrrrk.....',
      '.....kggggllllggggk.....','....kggggllllllggggk....','.kggkggggllllllggggk....','.kllkggggllllllggggk....',
      '..kkkgggggllllgggggk....','....kggggggggggggggk....','.....klllkggggklllk.....','......kkk.kkkk.kkk......',
      '........................','........................','........................','........................'
    ], 3),
    hurt: mkSprite([
      '........................','.......kkkkkkkkkk.......','.....kkggggggggggkk.....','....kggggggggggggggk....',
      '...kddggggggggggggddk...','..kdddggkggggggkggdddk..','.kddddggkggggggkggddddk.','.kddddgggkgllgkgggddddk.',
      '.kddddggkggllggkggddddk.','.kdddggpplleellppggdddk.','..kddkgglllpplllggkddk..','...kkgggllllllllgggkk...',
      '.....krrrrryyrrrrrk.....','.....kggggllllggggk.....','....kggggllllllggggk....','...kllggggggggggggllk...',
      '...kkkggggggggggggkkk...','.....kggggggggggggk.....','......kddk....kddk......','......kkkk....kkkk......',
      '........................','........................','........................','........................'
    ], 3),
    anger: mkSprite([
      '.RR..RR.','RWR..RWR','.RR..RR.','........','.RR..RR.','RWR..RWR','.RR..RR.','........'
    ], 3),
    carrot: mkSprite([
      '.......KK.KK....','......KVVKKVK...','......KVVFVVVK..','.......KFVVFK...',
      '......KKFFKK....','.....KYYYYOOK...','....KYYYOOOOOK..','....KYYOOCCOOOK.',
      '....KYYOOOOCCOK.','.....KOOOOOOCK..','.....KYOOOOCK...','......KOOOCK....',
      '......KOOOCK....','.......KOCK.....','.......KCK......','........K.......'
    ], 3),
    gold: mkSprite([
      '.......KK.KK....','......KWWKKWK...','......KWZZZWWK..','.......KZZZWK...',
      '......KKZZKK....','.....KZZZZAAK...','....KZZZAAAAAK..','....KZZAAXXAAAK.',
      '....KZZAAAAXXAK.','.....KAAAAAAXK..','.....KZAAAAXK...','......KAAAXK....',
      '......KAAAXK....','.......KAXK.....','.......KXK......','........K.......'
    ], 3),
    brick: mkSprite([
      'KKKKKKKKKKKKKKKK','KHHHHHHHKHHHHHHK','KHBBBBBBKHBBBBBK','KHBBBBBBKHBBBBBK',
      'KKKKKKKKKKKKKKKK','KHHHKHHHHHHHKHHK','KBBBKBBBBBBBKBBK','KBBBKBBBBBBBKBBK',
      'KKKKKKKKKKKKKKKK','KHHHHHHHKHHHHHHK','KHBBBBBBKHBBBBBK','KHBBBBBBKHBBBBBK',
      'KKKKKKKKKKKKKKKK','KHHHKHHHHHHHKHHK','KBBBKBBBBBBBKBBK','KKKKKKKKKKKKKKKK'
    ], 3),
    pipe: mkSprite([
      'KKKKKKKKKKKKKKKK','KSSNNNNNNNNNNEEK','KSWSSNNNNNNNNEEK','KSSNNNNNNNNNNEEK',
      'KSSNNNNNNNNNNEEK','KKKKKKKKKKKKKKKK','.KSSNNNNNNNNEEK.','.KSWSSNNNNNNEEK.',
      '.KSSNNNNNNNNEEK.','.KSSNNNNNNNNEEK.','.KSSNNNNNNNNEEK.','.KSSNNNNNNNNEEK.',
      '.KSSNNNNNNNNEEK.','.KSSNNNNNNNNEEK.','.KSSNNNNNNNNEEK.','.KKKKKKKKKKKKKK.'
    ], 3),
    chestnut: mkSprite([
      '.......KK.......','......KTTK......','....KKTTTTKK....','..KKTUUUTTTTKK..',
      '.KTUUUTTTTTTTTK.','KTUTKKTTTTKKTUTK','KTTKWKKTTKKWKTTK','KTTTWWKTTKWWTTTK',
      'KTTTTTKTTKTTTTTK','KTTTTTTTTTTTTTTK','.KTTTLLLLLLTTTK.','..KKLLLLLLLLKK..',
      '...KKKKKKKKKK...','..KDDK....KDDK..','..KKKK....KKKK..','................'
    ], 3)
  };

  let audioCtx = null, muted = false;
  function tone(freq, dur, type='square', vol=0.07, delay=0, slide=0) {
    if (muted) return;
    if (!audioCtx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (Ctx) audioCtx = new Ctx();
    }
    if (!audioCtx) return;
    if (audioCtx.state === 'suspended') audioCtx.resume().catch(()=>{});
    const t = audioCtx.currentTime + delay;
    const o = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, t);
    if (slide) o.frequency.exponentialRampToValueAtTime(slide, t + dur);
    g.gain.setValueAtTime(0.001, t);
    g.gain.linearRampToValueAtTime(vol, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, t + dur);
    o.connect(g); g.connect(audioCtx.destination);
    o.start(t); o.stop(t + dur + 0.02);
  }

  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const laneX = (l) => GRASS_W + LANE_W * l + LANE_W / 2;

  let bestScore = Number(localStorage.getItem(BEST_KEY) || '0');
  let state = 'TITLE';
  let lane = 1, playerX = laneX(1), tilt = 0;
  let invuln = 0, hurt = 0, anger = 1, runT = 0, scroll = 0, cloudX = 0;
  let elapsed = 0, timeLeft = DURATION, score = 0, carrots = 0, combo = 0, maxCombo = 0, lives = MAX_LIVES, level = 1;
  let spawnMs = 250, entities = [], particles = [], texts = [], banner = '', bannerT = 0;

  function syncHud() {
    const tier = TIERS[Math.min(TIERS.length - 1, Math.floor(elapsed / 12))];
    document.getElementById('scoreVal').textContent = score.toLocaleString();
    document.getElementById('bestVal').textContent = 'BEST ' + bestScore.toLocaleString();
    document.getElementById('timeVal').textContent = Math.ceil(timeLeft) + 's';
    document.getElementById('levelVal').textContent = 'LV.' + tier.level + ' ' + tier.label;
    document.getElementById('livesVal').textContent = '♥'.repeat(Math.max(0, lives)) + '♡'.repeat(Math.max(0, MAX_LIVES - lives));
    document.getElementById('carrotVal').textContent = carrots + '本';
  }

  function startGame() {
    state = 'PLAYING';
    lane = 1; playerX = laneX(1); tilt = 0;
    invuln = 0; hurt = 0; anger = 1.1; elapsed = 0; timeLeft = DURATION;
    score = 0; carrots = 0; combo = 0; maxCombo = 0; lives = MAX_LIVES; level = 1;
    spawnMs = 250; entities = []; particles = []; texts = [];
    banner = 'ダッシュ！にんじんを集めろ！'; bannerT = 1.4;
    document.getElementById('titleOverlay').style.display = 'none';
    document.getElementById('endOverlay').style.display = 'none';
    document.getElementById('touchControls').style.display = 'grid';
    [523,659,784,1046].forEach((n,i)=>tone(n,0.07,'square',0.07,i*0.06));
    syncHud();
  }

  function endGame(cleared) {
    state = cleared ? 'CLEAR' : 'OVER';
    document.getElementById('touchControls').style.display = 'none';
    document.getElementById('endKicker').textContent = cleared ? '60秒完走！お疲れさま！' : '障害物にぶつかった！';
    document.getElementById('endTitle').textContent = cleared ? 'ステージクリア！' : 'ゲームオーバー';
    document.getElementById('endScore').textContent = score.toLocaleString();
    document.getElementById('endBest').textContent = bestScore.toLocaleString();
    document.getElementById('endDetail').textContent = carrots + '本 · 最大' + maxCombo + 'コンボ';
    document.getElementById('endOverlay').style.display = 'flex';
    if (cleared) [523,659,784,1046,784,1046].forEach((n,i)=>tone(n,0.1,'square',0.08,i*0.08));
    else [392,349,311,261].forEach((n,i)=>tone(n,0.14,'sawtooth',0.08,i*0.11));
    syncHud();
  }

  function moveLane(delta) {
    if (state !== 'PLAYING') return;
    const next = Math.max(0, Math.min(2, lane + delta));
    if (next !== lane) {
      lane = next;
      tilt = delta * 0.22;
      tone(280, 0.07, 'triangle', 0.06, 0, 420);
    }
  }

  function jumpLane(target) {
    if (state !== 'PLAYING' || target === lane) return;
    tilt = (target > lane ? 1 : -1) * 0.22;
    lane = target;
    tone(280, 0.07, 'triangle', 0.06, 0, 420);
  }

  document.getElementById('startBtn').onclick = startGame;
  document.getElementById('restartBtn').onclick = startGame;
  document.getElementById('leftBtn').onclick = () => moveLane(-1);
  document.getElementById('centerBtn').onclick = () => jumpLane(1);
  document.getElementById('rightBtn').onclick = () => moveLane(1);
  document.getElementById('muteBtn').onclick = () => {
    muted = !muted;
    document.getElementById('muteBtn').textContent = muted ? '音: OFF' : '音: ON';
  };

  window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'a') { e.preventDefault(); moveLane(-1); }
    else if (e.key === 'ArrowRight' || e.key === 'd') { e.preventDefault(); moveLane(1); }
    else if ((e.key === ' ' || e.key === 'Enter') && state !== 'PLAYING') { e.preventDefault(); startGame(); }
  });

  let swActive = false, swId = -1, swStart = 0, swStep = 0, swMoved = 0;
  canvas.addEventListener('pointerdown', (e) => {
    if (state !== 'PLAYING') return;
    canvas.setPointerCapture(e.pointerId);
    swActive = true; swId = e.pointerId; swStart = e.clientX; swStep = e.clientX; swMoved = 0;
  });
  canvas.addEventListener('pointermove', (e) => {
    if (!swActive || e.pointerId !== swId || state !== 'PLAYING') return;
    const dx = e.clientX - swStep;
    swMoved = Math.max(swMoved, Math.abs(e.clientX - swStart));
    if (dx >= 28) { moveLane(1); swStep = e.clientX; }
    else if (dx <= -28) { moveLane(-1); swStep = e.clientX; }
  });
  canvas.addEventListener('pointerup', (e) => {
    if (!swActive || e.pointerId !== swId) return;
    swActive = false;
    if (state === 'PLAYING' && swMoved < 12) {
      const r = canvas.getBoundingClientRect();
      const rx = ((e.clientX - r.left) / r.width) * CANVAS_W;
      if (rx < GRASS_W + LANE_W) jumpLane(0);
      else if (rx < GRASS_W + LANE_W * 2) jumpLane(1);
      else jumpLane(2);
    }
  });

  function spawnWave(tier) {
    const obs = ['brick', 'pipe', 'chestnut'];
    const lanes = [0, 1, 2];
    const safe = lanes[Math.floor(Math.random() * 3)];
    const blocked = lanes.filter(l => l !== safe);
    if (Math.random() < tier.dbl) {
      blocked.forEach(bl => entities.push({ kind: obs[Math.floor(Math.random()*3)], lane: bl, y: SKY_H - 36, bob: Math.random()*6 }));
      if (Math.random() < 0.78) entities.push({ kind: Math.random() < 0.14 ? 'gold' : 'carrot', lane: safe, y: SKY_H - 36, bob: Math.random()*6 });
    } else {
      let obLane = null;
      if (Math.random() < 0.78) {
        obLane = blocked[Math.floor(Math.random()*blocked.length)];
        entities.push({ kind: obs[Math.floor(Math.random()*3)], lane: obLane, y: SKY_H - 36, bob: Math.random()*6 });
      }
      if (Math.random() < tier.carrot + 0.2) {
        const free = lanes.filter(l => l !== obLane);
        const cl = free[Math.floor(Math.random()*free.length)];
        entities.push({ kind: Math.random() < 0.12 ? 'gold' : 'carrot', lane: cl, y: SKY_H - 36, bob: Math.random()*6 });
      }
    }
  }

  let last = performance.now(), hudT = 0;
  function loop(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    cloudX = (cloudX + dt * 16) % CANVAS_W;

    if (state === 'TITLE') {
      runT += dt * 7; scroll = (scroll + dt * 150) % 64;
    } else if (state === 'PLAYING') {
      elapsed += dt;
      timeLeft = Math.max(0, DURATION - elapsed);
      const tier = TIERS[Math.min(TIERS.length - 1, Math.floor(elapsed / 12))];
      if (tier.level > level) {
        level = tier.level;
        banner = 'LV.' + tier.level + ' ' + tier.label + '！';
        bannerT = 1.6; anger = 1.3;
        [440,554,659,880].forEach((n,i)=>tone(n,0.08,'square',0.07,i*0.065));
      }
      scroll = (scroll + dt * tier.speed) % 64;
      runT += dt * (8 + level * 1.8);
      if (invuln > 0) invuln = Math.max(0, invuln - dt);
      if (hurt > 0) hurt = Math.max(0, hurt - dt);
      if (anger > 0) anger = Math.max(0, anger - dt);
      if (bannerT > 0) bannerT = Math.max(0, bannerT - dt);

      playerX += (laneX(lane) - playerX) * Math.min(1, dt * 18);
      tilt *= Math.pow(0.001, dt);

      spawnMs -= dt * 1000;
      if (spawnMs <= 0) { spawnWave(tier); spawnMs = tier.interval; }

      for (const ent of entities) {
        ent.y += tier.speed * dt;
        ent.bob += dt * 7;
        if (ent.dead) continue;
        const ex = laneX(ent.lane);
        if (Math.abs(playerX - ex) < 34 && ent.y + 18 >= PLAYER_Y - 20 && ent.y - 18 <= PLAYER_Y + 22) {
          if (ent.kind === 'carrot' || ent.kind === 'gold') {
            ent.dead = true;
            combo++; maxCombo = Math.max(maxCombo, combo);
            carrots++;
            const mult = Math.min(4, 1 + Math.floor(combo / 5));
            const pts = (ent.kind === 'gold' ? 300 : 100) * mult;
            score += pts;
            if (score > bestScore) { bestScore = score; localStorage.setItem(BEST_KEY, String(bestScore)); }
            if (ent.kind === 'gold') [587,784,1046,1318].forEach((n,i)=>tone(n,0.07,'square',0.08,i*0.055));
            else { tone(659+combo*25,0.06,'square',0.07,0); tone(988+combo*25,0.1,'square',0.07,0.05); }
            texts.push({ x: ex, y: PLAYER_Y - 32, t: '+' + pts, c: ent.kind === 'gold' ? '#FDE047' : '#FFF', l: 0.7 });
          } else if (invuln <= 0) {
            ent.dead = true; lives--; combo = 0; invuln = 1.25; hurt = 0.45; anger = 1.5;
            tone(200,0.1,'sawtooth',0.09,0,100); tone(130,0.16,'square',0.09,0.06,65);
            texts.push({ x: playerX, y: PLAYER_Y - 36, t: 'イテッ！', c: '#FCA5A5', l: 0.7 });
            if (lives <= 0) { endGame(false); break; }
          }
        }
      }
      entities = entities.filter(e => !e.dead && e.y < CANVAS_H + 50);
      texts = texts.filter(t => { t.y -= 38 * dt; t.l -= dt; return t.l > 0; });

      if (timeLeft <= 0 && state === 'PLAYING') {
        score += lives * 500;
        if (score > bestScore) { bestScore = score; localStorage.setItem(BEST_KEY, String(bestScore)); }
        endGame(true);
      }
      hudT += dt;
      if (hudT >= 0.08) { hudT = 0; syncHud(); }
    }

    // Draw
    ctx.imageSmoothingEnabled = false;
    ctx.fillStyle = '#5C94FC'; ctx.fillRect(0, 0, CANVAS_W, SKY_H);
    ctx.fillStyle = '#198E19'; ctx.fillRect(28, SKY_H - 22, 64, 22); ctx.fillRect(240, SKY_H - 28, 76, 28);
    ctx.fillStyle = '#FFF';
    ctx.fillRect(((60+cloudX)%(CANVAS_W+60))-50, 20, 36, 12);
    ctx.fillRect(((230+cloudX*0.7)%(CANVAS_W+60))-50, 34, 40, 12);
    ctx.fillStyle = '#1B1410'; ctx.fillRect(0, SKY_H - 4, CANVAS_W, 4);

    ctx.fillStyle = '#248A24';
    ctx.fillRect(0, SKY_H, GRASS_W, CANVAS_H - SKY_H);
    ctx.fillRect(CANVAS_W - GRASS_W, SKY_H, GRASS_W, CANVAS_H - SKY_H);
    ctx.fillStyle = '#D9A75A'; ctx.fillRect(GRASS_W, SKY_H, ROAD_W, CANVAS_H - SKY_H);
    ctx.fillStyle = '#CE9A4D'; ctx.fillRect(GRASS_W + LANE_W, SKY_H, LANE_W, CANVAS_H - SKY_H);

    if (state === 'PLAYING') {
      ctx.fillStyle = 'rgba(255,255,255,0.14)';
      ctx.fillRect(GRASS_W + lane * LANE_W + 4, PLAYER_Y - 34, LANE_W - 8, 68);
    }

    const off = Math.floor(scroll);
    for (let y = SKY_H - 64 + off; y < CANVAS_H + 32; y += 64) {
      if (y >= SKY_H) {
        ctx.fillStyle = '#F8E6BE';
        ctx.fillRect(GRASS_W + LANE_W - 2, y, 4, 28);
        ctx.fillRect(GRASS_W + LANE_W * 2 - 2, y, 4, 28);
        ctx.fillStyle = '#4CE04C';
        ctx.fillRect(12, y + 10, 12, 6);
        ctx.fillRect(CANVAS_W - 24, y + 24, 12, 6);
      }
    }

    for (const ent of entities) {
      const cx = laneX(ent.lane);
      const bob = (ent.kind === 'carrot' || ent.kind === 'gold') ? Math.round(Math.sin(ent.bob)*3) : 0;
      ctx.fillStyle = 'rgba(27,20,16,0.28)';
      ctx.fillRect(Math.round(cx - 16), Math.round(ent.y + 18), 32, 6);
      const sp = SPRITES[ent.kind];
      ctx.drawImage(sp, Math.round(cx - sp.width/2), Math.round(ent.y - sp.height/2 + bob));
    }

    if (!(invuln > 0 && Math.floor(invuln * 16) % 2 === 0)) {
      const f = Math.floor(runT) % 2 === 0;
      const sp = hurt > 0 ? SPRITES.hurt : (f ? SPRITES.run1 : SPRITES.run2);
      ctx.fillStyle = 'rgba(27,20,16,0.34)';
      ctx.fillRect(Math.round(playerX - 20), PLAYER_Y + 24, 40, 8);
      ctx.save();
      ctx.translate(Math.round(playerX), Math.round(PLAYER_Y + (f ? 0 : -3)));
      ctx.rotate(tilt);
      ctx.drawImage(sp, -Math.round(sp.width / 2), -Math.round(sp.height / 2));
      if ((anger > 0 || Math.floor(runT * 0.4) % 4 === 0) && hurt <= 0) {
        ctx.drawImage(SPRITES.anger, 22, -38);
      }
      ctx.restore();
    }

    ctx.font = 'bold 14px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    for (const t of texts) {
      ctx.globalAlpha = Math.max(0, t.l / 0.7);
      ctx.fillStyle = t.c;
      ctx.fillText(t.t, Math.round(t.x), Math.round(t.y));
    }
    ctx.globalAlpha = 1;

    if (bannerT > 0 && state === 'PLAYING') {
      ctx.fillStyle = 'rgba(18,22,32,0.85)';
      ctx.fillRect(36, 120, CANVAS_W - 72, 42);
      ctx.strokeStyle = '#FACC15'; ctx.lineWidth = 3;
      ctx.strokeRect(36, 120, CANVAS_W - 72, 42);
      ctx.font = '16px "DotGothic16", monospace';
      ctx.fillStyle = '#FACC15';
      ctx.fillText(banner, CANVAS_W / 2, 147);
    }

    requestAnimationFrame(loop);
  }
  syncHud();
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=740, scrolling=False)
