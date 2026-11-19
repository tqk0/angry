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
    padding: 18px;
    background: rgba(14, 19, 29, 0.78);
    border-radius: 12px;
  }
  .card {
    width: 100%;
    max-width: 310px;
    background: #161B26;
    border: 2px solid #F59E0B;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }
  .card h2 { margin: 6px 0 8px; font-size: 21px; line-height: 1.35; color: #FFFFFF; }
  .card p { margin: 10px 0 0; font-size: 12px; color: #CBD5E1; line-height: 1.6; }
  .kicker { font-size: 12px; color: #FDE073; }
  .mode-tabs {
    margin-top: 12px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    padding: 4px;
    background: #0F131C;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
  }
  .mode-tab {
    padding: 8px 6px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: #CBD5E1;
    font-family: 'DotGothic16', sans-serif;
    font-size: 13px;
    cursor: pointer;
  }
  .mode-tab.active {
    background: #FF6B1A;
    color: #FFFFFF;
  }
  .mode-meta { margin-top: 10px; font-size: 12px; color: #F8FAFC; }
  .mode-sub { margin-top: 3px; font-size: 11px; color: #94A3B8; }
  .start-btn {
    margin-top: 14px;
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
  .secondary-btn {
    margin-top: 8px;
    width: 100%;
    padding: 10px 14px;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    background: #1E2536;
    color: #E2E8F0;
    font-family: 'DotGothic16', sans-serif;
    font-size: 13px;
    cursor: pointer;
  }
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
      <span class="hud-label" id="midLabel">STAGE 1/8 平原</span>
      <span class="hud-val" id="timeVal">45s</span>
      <span class="hud-sub" id="levelVal">速度 1.0x · かけだし</span>
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
        <div class="kicker">3レーン・ランゲーム</div>
        <h2>怒りのレトリーバー！<br/>にんじんダッシュ</h2>
        <div class="mode-tabs">
          <button class="mode-tab active" data-mode="standard">スタンダード</button>
          <button class="mode-tab" data-mode="endless">エンドレス</button>
        </div>
        <div class="mode-meta" id="modeTitle">スタンダード（全8ステージ）</div>
        <div class="mode-sub" id="modeSub">各45秒 · ステージごとにスピードUP · BEST 0</div>
        <p id="modeDesc">平原から溶岩城まで全8ステージ（各45秒）！ステージが進むほどスピードが上がります。</p>
        <button id="startBtn" class="start-btn">ゲームスタート</button>
      </div>
    </div>

    <div id="stageClearOverlay" class="overlay" style="display:none;">
      <div class="card">
        <div class="kicker" id="scKicker">STAGE 1/8 平原 45秒完走！</div>
        <h2 id="scTitle">ステージ1 クリア！</h2>
        <p id="scDesc" style="margin-top:6px;">スコアを引き継いで、ライフ全回復で次のステージへ！</p>
        <div class="stats-box">
          <div class="stat-row"><span>現在のスコア</span><strong id="scScore" style="color:#FDE073;">0</strong></div>
          <div class="stat-row"><span>状況</span><span id="scDetail">0本 · ライフ ♥♥♥ 回復</span></div>
        </div>
        <button id="nextStageBtn" class="start-btn">STAGE 2：砂漠へすすむ</button>
        <button id="scMenuBtn" class="secondary-btn">モード選択へもどる</button>
      </div>
    </div>

    <div id="endOverlay" class="overlay" style="display:none;">
      <div class="card">
        <div class="kicker" id="endKicker">STAGE 8 溶岩城も突破！</div>
        <h2 id="endTitle">全8ステージ制覇！</h2>
        <div class="stats-box">
          <div class="stat-row"><span>スコア</span><strong id="endScore" style="color:#FDE073;">0</strong></div>
          <div class="stat-row"><span>ハイスコア</span><strong id="endBest">0</strong></div>
          <div class="stat-row"><span>結果</span><span id="endDetail">0本 · 1.0x</span></div>
        </div>
        <button id="restartBtn" class="start-btn">STAGE 1からもういちど</button>
        <button id="menuBtn" class="secondary-btn">モード選択へもどる</button>
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
  const DURATION = 45, TOTAL_STAGES = 8, MAX_LIVES = 3, BASE_SPEED = 235;
  const BEST_KEYS = {
    standard: 'golden_carrot_dash_best_st',
    endless: 'golden_carrot_dash_best_st_endless'
  };

  const MODE_INFO = {
    standard: {
      title: 'スタンダード（全8ステージ）',
      sub: '各45秒 · ステージごとにスピードUP',
      desc: '平原から溶岩城まで全8ステージ（各45秒）！ステージが進むほどスピードが上がります。'
    },
    endless: {
      title: 'エンドレス（草原・無限）',
      sub: 'Lv.5まで5秒ごと · 以降10秒ごと加速',
      desc: '時間制限なしの草原ステージ！Lv.5まで5秒ごと、以降は10秒ごとにスピードが上がり続けます。'
    }
  };

  const STAGES = [
    { stage: 1, theme: 'meadow', name: '平原', baseSpeed: 235, step: 30, interval: 800, dbl: 0.08, obs: ['brick', 'pipe', 'chestnut'] },
    { stage: 2, theme: 'desert', name: '砂漠', baseSpeed: 260, step: 30, interval: 740, dbl: 0.14, obs: ['cactus', 'sandstone', 'sand_spike'] },
    { stage: 3, theme: 'island', name: '海島', baseSpeed: 285, step: 30, interval: 685, dbl: 0.18, obs: ['coral', 'palm_log', 'urchin'] },
    { stage: 4, theme: 'snow', name: '雪山', baseSpeed: 310, step: 30, interval: 635, dbl: 0.22, obs: ['ice_block', 'snowman', 'frost_spike'] },
    { stage: 5, theme: 'jungle', name: 'ジャングル', baseSpeed: 335, step: 30, interval: 590, dbl: 0.27, obs: ['vine_log', 'piranha', 'totem'] },
    { stage: 6, theme: 'mountain', name: '山脈', baseSpeed: 360, step: 30, interval: 550, dbl: 0.32, obs: ['boulder', 'iron_fence', 'rock_crab'] },
    { stage: 7, theme: 'cloud', name: '雲海', baseSpeed: 385, step: 30, interval: 515, dbl: 0.36, obs: ['thunder_cloud', 'wing_block', 'sky_spike'] },
    { stage: 8, theme: 'castle', name: '溶岩城', baseSpeed: 415, step: 35, interval: 475, dbl: 0.42, obs: ['castle_brick', 'lava_fire', 'spiky_ball'] }
  ];

  const PAL = {
    K:'#1A120E', k:'#6B4E35', e:'#1E1614', g:'#DFBE97', l:'#F0DAC0', d:'#BA9268',
    w:'#FFFFFF', p:'#E8998D', r:'#EF4444', y:'#FDE047',
    G:'#F59E0B', L:'#FDE073', D:'#C2670A', W:'#FFFFFF', R:'#E63946',
    P:'#FCA5A5', O:'#FF6B1A', Y:'#FFA834', C:'#B44309', V:'#22C55E', F:'#15803D', I:'#0D5229',
    B:'#C84C0C', H:'#FC9838', N:'#00A800', S:'#80D010', E:'#005800', T:'#9E4718',
    U:'#D97724', Z:'#FDE68A', A:'#F59E0B', X:'#B45309',
    j:'#F3B36C', m:'#D97736', n:'#8C4216', s:'#C26D3A', t:'#E69F66',
    a:'#FB7185', b:'#2563EB', c:'#38BDF8', f:'#0284C7', h:'#BAE6FD',
    i:'#334155', o:'#94A3B8', q:'#CBD5E1', u:'#6D28D9', v:'#A78BFA',
    x:'#64748B', z:'#78350F', J:'#166534'
  };

  function mkSprite(rows, sc) {
    const c = document.createElement('canvas');
    c.width = rows[0].length * sc;
    c.height = rows.length * sc;
    const ctx = c.getContext('2d');
    ctx.imageSmoothingEnabled = false;
    for (let r = 0; r < rows.length; r++) {
      for (let col = 0; col < rows[r].length; col++) {
        const ch = rows[r][col];
        if (ch !== '.' && PAL[ch]) {
          ctx.fillStyle = PAL[ch];
          ctx.fillRect(col * sc, r * sc, sc, sc);
        }
      }
    }
    return c;
  }

  const SPRITES = {
    run1: mkSprite([
      '........................','.......kkkkkkkkkk.......','.....kkllllllllllkk.....','....kllggggggggggllk....',
      '...kggggggggggggggggk...','..kddggggkggggggkggddk..','.kddgggwekkggggkkewggddk','.kdddggeeelllllleeeedddk',
      '.kddgggllleeeelllgggdddk','.kddgggllleeeelllgggdddk','..kddkgglllkklllggkddk..','...kkgggllllllllgggkk...',
      '....kkggggllllggggkk....','....kggggllllllggggk....','....kggggllllllggggkggk.','....kggggllllllggggkllk.',
      '....kgggggllllgggggkkk..','....kllggggddggggllk....','....kllkgggddgggkllk....','....keek.kdkkdk.keek....',
      '.....kk...kkkk...kk.....','........................','........................','........................'
    ], 3),
    run2: mkSprite([
      '.......kkkkkkkkkk.......','.....kkllllllllllkk.....','....kllggggggggggllk....','..kkggggggggggggggggkk..',
      '.kddggggkggggggkggggddk.','kdddgggwekkggggkkewggddk','kddddggeeelllllleeeedddk','.kddgggllleeeelllgggdddk',
      '.kddgggllleeeelllgggdddk','..kddkgglllkklllggkddk..','...kkgggllllllllgggkk...','....kkggggllllggggkk....',
      '....kggggllllllggggk....','.kggkggggllllllggggk....','.kllkggggllllllggggk....','..kkkgggggllllgggggk....',
      '....kggggggddggggggk....','.....kllkggddggkllk.....','.....keek.kkkk.keek.....','......kk........kk......',
      '........................','........................','........................','........................'
    ], 3),
    hurt: mkSprite([
      '........................','.......kkkkkkkkkk.......','.....kkllllllllllkk.....','....kllggggggggggllk....',
      '...kggggggggggggggggk...','..kddggggkggggggkggddk..','.kddggggkggggggggkgggddk','.kdddggggkllllllkggggddk',
      '.kddgggllleeeelllgggdddk','.kddgggllleeeelllgggdddk','..kddkgglllpplllggkddk..','...kkgggllllllllgggkk...',
      '....kkggggllllggggkk....','....kggggllllllggggk....','...kllggggggggggggllk...','...keekggggggggggkeek...',
      '....kk.kggggggggk.kk....','.......kdk....kdk.......','.......kee....eek.......','........kk....kk........',
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
    ], 3),
    cactus: mkSprite([
      '......KKKK......','.....KVFFIK.....','.KKK.KVFFWK.KKK.','KVFIKKVFFIKKVFIK',
      'KVFIKKWFFIKKVFIK','KVFIKKVFFIKKVFIK','KVFKKKKFFIKKVFIK','.KKVFFFVFFIKKKK.',
      '...KKKKVFFIK....','.....KVFFIK.....','.....KWFFIK.....','.....KVFFIK.....',
      '.....KVFFWK.....','.....KVFFIK.....','....KKVFFIKK....','...KKKKKKKKKK...'
    ], 3),
    sandstone: mkSprite([
      'KKKKKKKKKKKKKKKK','KjjjjjjjKjjjjjjK','KjmmmmmmKjmmnmmK','KjmjmmmmKjmnmmmK',
      'KKKKKKKKKKKKKKKK','KjjjKjjjjjjjKjjK','KmmmKmmmnmmmKmmK','KmmnKmmmmmmmKmmK',
      'KKKKKKKKKKKKKKKK','KjjjjjjjKjjjjjjK','KjmmmmmmKjmmmmnK','KjmmnmmmKjmmmmmK',
      'KKKKKKKKKKKKKKKK','KjjjKjjjjjjjKjjK','KmmmKmmmmmmmKmmK','KKKKKKKKKKKKKKKK'
    ], 3),
    sand_spike: mkSprite([
      '.......KK.......','......KWWK......','....KKttttKK....','..KKttssssssKK..',
      '.KWtssssssssstWK','KKtKKssssssKKtKK','KtKWKKssssKKWKtK','KssWWKssssKWWssK',
      'KssssssssssssssK','KsssnnnnnnnnsssK','.KssnnKKKKnnssK.','..KKnnnnnnnnKK..',
      '...KKKKKKKKKK...','..KnnK....KnnK..','..KKKK....KKKK..','................'
    ], 3),
    coral: mkSprite([
      '...KK......KK...','..KOOOK..KaaWK..','..KOaaK..KaaaK..','...KaaKKKKaaK...',
      '.KKKaaaaOaaaKK..','KOOaaaaaaaWaaOK.','KOaaaaaaaaaaaRK.','.KKKaaRRRRaaKK..',
      '...KaaRRRRaaK...','...KaaRRRRaaK...','..KaaRRRRRRaaK..','..KaaRRRRRRaaK..',
      '..KRRRRRRRRRRK..','.KKRRRRRRRRRRKK.','KZZZZRRRRRRZZZZK','KKKKKKKKKKKKKKKK'
    ], 3),
    palm_log: mkSprite([
      '..KKKK....KKKK..','.KSSNNKKKKNNSSK.','KSNNNNKKKKNNNNSK','.KKKKzUUUUzKKKK.',
      '....KzZZUUUzK...','....KzUUzzUzK...','....KzZZZZzzK...','....KzUUUzzUK...',
      '....KzZZUUzzK...','....KzUUzzUzK...','....KzZZZZzzK...','....KzUUUzzUK...',
      '....KzZZUUzzK...','...KKzUUUUzzKK..','..KZZZZZZZZZZZK.','..KKKKKKKKKKKKK.'
    ], 3),
    urchin: mkSprite([
      '.......KK.......','..KK..KWWK..KK..','.KvvK.KvvK.KvvK.','..KuvKKuuKKvuK..',
      'KK.KuuuuuuuuK.KK','KWvuuuuuuuuuuvWK','.KKuuKWKKWKuuKK.','...uuKWWKWWuu...',
      '.KKuuKKKKKKuuKK.','KvvuuuuuuuuuuvvK','KK.KuuuuuuuuK.KK','..KuvKKuuKKvuK..',
      '.KvvK.KvvK.KvvK.','..KK..KWWK..KK..','.......KK.......','................'
    ], 3),
    ice_block: mkSprite([
      'KKKKKKKKKKKKKKKK','KWWWWWWWWWWWhhhK','KWhhhccccccchhfK','KWhccccccccchffK',
      'KWccWWcccccchffK','KWcWccchcccchffK','KWhccccchccchffK','KWhccccccchcbffK',
      'KWhccWWccccbbffK','KWhcWccchccbbffK','KWhccccchccbbffK','KWhhhhhhhhhbbbfK',
      'KffccccccbbbbbfK','KffffffffbbbbbfK','KbbbbbbbbbbbbbfK','KKKKKKKKKKKKKKKK'
    ], 3),
    snowman: mkSprite([
      '.....KKKKKK.....','....KiiiiiiK....','....KiiiiiiK....','..KKKKKKKKKKKK..',
      '...KWWWWWWWWK...','..KWWKKWWKKWWK..','..KWWKeWWKeWWK..','..KWWWWOOOWWWK..',
      '..KqqWWWWWWqqK..','...KKRRRRRRKK...','..KWWWWeeWWWWK..','.KWWWWWWWWWWWWK.',
      '.KWWqqWeeWWqqWK.','..KqqqqqqqqqqK..','...KKKKKKKKKK...','................'
    ], 3),
    frost_spike: mkSprite([
      '.......KK.......','......KWWK......','.....KWhhWK.....','....KWhcchfK....',
      '..KKKWhcchfKKK..','.KWhKWccchfKhfK.','.KWhccchccchffK.','.KWhKWcKKcfKhfK.',
      'KWhcKWWKKWWKchfK','KWhcchccccchbbfK','KWhccccccccbbffK','KfffccccccbbbffK',
      '.KfffbbbbbbfffK.','..KKbbbbbbbbKK..','...KKKKKKKKKK...','................'
    ], 3),
    vine_log: mkSprite([
      'KKKKKKKKKKKKKKKK','KTUUUTTTTTSSSTTK','KTTzzTTTSSJJSzTK','KUUUUzTTJJSSTUTK',
      'KTzzUUUTSSJzzTTK','KTTTTzTSJJzTTTUK','KSSTTUUJJTTTzzTK','KJJSSzTTTTTTTTTK',
      'KTJJSSUUUTzzUTTK','KTTJJSSzTTTUUUTK','KUUUTJJSSzzTTTTK','KTzzTTTJJSSUUUTK',
      'KTTTTzTTTJJSSzTK','KUUUUUzzTTTJJSSK','KzzzzzzzzzTTTJJK','KKKKKKKKKKKKKKKK'
    ], 3),
    piranha: mkSprite([
      '....KKKKKKKK....','..KKRRRRWRRRKK..','.KRRWRRRRRRWRRK.','KRRRRRRRWWWRRRRK',
      'KRRWRRKWWWKRRRRK','KRRRRKPPPPPKRRRK','.KRRKWWKKKWWKRK.','..KKK.KJJJK.KKK.',
      '......KNNNK.....','..KKKKKNNNKKKKK.','.KSSSSKNNNKSSSSK','KSSJJJKKKKKJJJSS',
      '.KKKK.KNNNK.KKKK','......KJJJK.....','.....KKJJJKK....','....KKKKKKKKK...'
    ], 3),
    totem: mkSprite([
      '..KKKKKKKKKKKK..','.KoooxxxxxJxxxK.','.KoxxxxxxxxxJJK.','.KoxKKKxxKKKxJK.',
      '.KoxKyyxxKyyxJK.','.KoxKKKxxKKKxxK.','.KoxxxxxxxxxxxK.','.KoxxKKKKKKKxxK.',
      '.KoxKWWKWKWWKxK.','.KoxKKKKKKKKKxK.','.KoxxxxxJxxxxxK.','.KJxxxxJJJxxxxK.',
      '.KJJxxiiiiixxxK.','.KiiiiiiiiiJJxK.','KiiiiiiiiiiiiiiK','KKKKKKKKKKKKKKKK'
    ], 3),
    boulder: mkSprite([
      '....KKKKKKKK....','..KKqqqooooiKK..','.KqqooooooiiiiK.','KqqoooKKooooiiiK',
      'KqoooKooKoooiiiK','KoooqqqqooooKKiK','KoooKoooooooKiiK','KooiKooqqqooKiiK',
      'KiiiKKooooooKiiK','KiiiiiooKKiiiiiK','.KiiiiKiiiiiiiK.','.KiiiiiiKiiiiKK.',
      '..KiiiiiiiiiiK..','..KKiiiiiiiiKK..','....KKKKKKKK....','................'
    ], 3),
    iron_fence: mkSprite([
      '..KK...KK...KK..','.KWWK.KWWK.KWWK.','.KqqK.KqqK.KqqK.','KKKKKKKKKKKKKKKK',
      'KyyyyiiiiyyyyiiK','KiiyyyyiiiiyyyyK','KKKKKKKKKKKKKKKK','.KqqK.KqqK.KqqK.',
      '.KoiK.KoiK.KoiK.','KKKKKKKKKKKKKKKK','KoooooooKooooooK','KiiiiiiiKiiiiiiK',
      'KKKKKKKKKKKKKKKK','.KoiK......KoiK.','.KiiK......KiiK.','.KKKK......KKKK.'
    ], 3),
    rock_crab: mkSprite([
      '.......KK.......','.....KKooKK.....','...KKqqooooKK...','..KqqooooooooK..',
      '.KqqooiiiiiooiK.','KqqoKKiiiiiiKKiK','KooKWKKiiiiKKWKi','KooKWWKiiiiKWWKi',
      'KiiiiiiiiiiiiiiK','KOOKiiiiiiiiKOOK','KOOoKiiiiiiKoOOK','.KK.KKKKKKKK.KK.',
      '...KiiK..KiiK...','..KiiK....KiiK..','..KKKK....KKKK..','................'
    ], 3),
    thunder_cloud: mkSprite([
      '....KKKKKKKK....','..KKqqqqooooKK..','.KqqqqooooooiiK.','KqqKKooooKKoooiK',
      'KqKWWRooKWWKooiK','KqooooooioooooiK','KooiiiiiiiiiiiK.','.KKKKKKKKKKKKKK.',
      '.....KKyyKK.....','....KyyyyK......','...KyyyyAAK.....','.....KyyAAK.....',
      '....KyyAAK......','...KyyAK........','...KAK..........','...KK...........'
    ], 3),
    wing_block: mkSprite([
      '................','................','....KKKKKKKK....','KK..KZZZZZZK..KK',
      'KWKKKZAAAAZK.KWK','KWWWKZAWWAZKKWWK','KWqWKZAAWAZKKWqK','.KKqKZAAZZZKKqK.',
      '..KKKZAAWAZKKK..','....KZAAAAZK....','....KZAXXAXK....','....KXXXXXXK....',
      '....KKKKKKKK....','................','................','................'
    ], 3),
    sky_spike: mkSprite([
      '.......KK.......','......KRRK......','....KKWWWWKK....','..KKWWWWWWqqKK..',
      '.KRWqqWWWWqqWRK.','KKRKKWWWWWWKKRKK','KqKWKKWWWWKKWKqK','KqKWWKWWWWKWWKqK',
      'KqqqqqqqqqqqqqqK','KqqcccccccccqqqK','.KqqccKKKKccqqK.','..KKccccccccKK..',
      '...KKKKKKKKKK...','..KccK....KccK..','..KKKK....KKKK..','................'
    ], 3),
    castle_brick: mkSprite([
      'KKKKKKKKKKKKKKKK','KoooooooKooooooK','KoiiiiiiKoiiiiiK','KoiiiiiiKoiiiiiK',
      'KKKKKKKKKKKKKKKK','KoooKoooooooKooK','KiiiKiiiiiiiKiiK','KiiiKiiiiiiiKiiK',
      'KKKKKKKKKKKKKKKK','KoooooooKooooooK','KoiiiiiiKoiiiiiK','KoiiiiiiKoiiiiiK',
      'KKKKKKKKKKKKKKKK','KoooKoooooooKooK','KiiiKiiiiiiiKiiK','KKKKKKKKKKKKKKKK'
    ], 3),
    lava_fire: mkSprite([
      '.......KK.......','......KRRK......','.....KROORK.....','....KROyyORK....',
      '...KROyyyyORK...','..KROyyWWyyORK..','..KRyyWWWWyyRK..','.KROyyWWWWyyORK.',
      '.KROyyyyyyyyORK.','.KROyyKKKKyyORK.','..KROyyyyyyORK..','..KRROyyyyORRK..',
      '...KRRROORRRK...','....KKRRRRKK....','......KKKK......','................'
    ], 3),
    spiky_ball: mkSprite([
      '.......KK.......','..KK..KWWK..KK..','.KqqK.KqqK.KqqK.','..KiqKKiiKKqiK..',
      'KK.KiiiiiiiiK.KK','KWqiiiiiiiiiiqWK','.KKiiKRRKKRRiKK.','...iiKRyKiyRK...',
      '.KKiiKKKKKKiiKK.','KqqiiiiiiiiiiqqK','KK.KiiiiiiiiK.KK','..KiqKKiiKKqiK..',
      '.KqqK.KqqK.KqqK.','..KK..KWWK..KK..','.......KK.......','................'
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

  let mode = 'standard', stage = 1;
  function getBest(m) { return Number(localStorage.getItem(BEST_KEYS[m]) || '0'); }
  function setBest(m, val) { localStorage.setItem(BEST_KEYS[m], String(val)); }
  function getStageCfg(s) { return STAGES[s - 1] || STAGES[0]; }
  function getTheme() { return mode === 'endless' ? 'meadow' : getStageCfg(stage).theme; }

  let state = 'TITLE';
  let lane = 1, playerX = laneX(1), tilt = 0;
  let invuln = 0, hurt = 0, anger = 1, runT = 0, scroll = 0, cloudX = 0;
  let elapsed = 0, timeLeft = DURATION, score = 0, carrots = 0, combo = 0, maxCombo = 0, lives = MAX_LIVES, level = 1;
  let spawnMs = 250, lastSafeLane = 1, entities = [], texts = [], banner = '', bannerT = 0;

  function getStreakMult(c) {
    return Math.min(2.0, Math.round((1 + Math.floor(Math.max(0, c) / 5) * 0.2) * 10) / 10);
  }

  function getDiff() {
    if (mode === 'endless') {
      const t = Math.max(0, elapsed);
      const lv = t < 20 ? 1 + Math.floor(t / 5) : 5 + Math.floor((t - 20) / 10);
      const speed = 250 + (lv - 1) * 28;
      const interval = Math.max(270, 780 - (lv - 1) * 42);
      const dbl = Math.min(0.54, 0.08 + (lv - 1) * 0.045);
      const labels = ['おさんぽ', 'かけあし', 'リズム走', '本気ダッシュ', 'ぷんぷん猛走', '爆走モード', '限界突破'];
      return { level: lv, label: labels[Math.min(labels.length - 1, lv - 1)], speed, interval, dbl, carrot: 0.64 };
    }
    const cfg = getStageCfg(stage);
    const phase = Math.min(2, Math.floor(Math.max(0, elapsed) / 15));
    const phaseLabels = ['かけだし', '加速中', 'ラストスパート'];
    return {
      level: phase + 1,
      label: phaseLabels[phase],
      speed: cfg.baseSpeed + phase * cfg.step,
      interval: Math.max(275, cfg.interval - phase * 70),
      dbl: Math.min(0.62, cfg.dbl + phase * 0.1),
      carrot: Math.max(0.46, 0.62 - (stage - 1) * 0.015 - phase * 0.02)
    };
  }

  function syncModeCard() {
    const info = MODE_INFO[mode];
    document.querySelectorAll('.mode-tab').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    document.getElementById('modeTitle').textContent = info.title;
    document.getElementById('modeSub').textContent = info.sub + ' · BEST ' + getBest(mode).toLocaleString();
    document.getElementById('modeDesc').textContent = info.desc;
    syncHud();
  }

  function syncHud() {
    const tier = getDiff();
    const mult = (tier.speed / BASE_SPEED).toFixed(1);
    const cfg = getStageCfg(stage);
    document.getElementById('scoreVal').textContent = score.toLocaleString();
    document.getElementById('bestVal').textContent = 'BEST ' + getBest(mode).toLocaleString();
    if (mode === 'endless') {
      document.getElementById('midLabel').textContent = 'スピード';
      document.getElementById('timeVal').textContent = mult + 'x';
      document.getElementById('levelVal').textContent = 'LV.' + tier.level + ' · ' + Math.floor(elapsed) + 's';
    } else {
      document.getElementById('midLabel').textContent = 'STAGE ' + stage + '/' + TOTAL_STAGES + ' ' + cfg.name;
      document.getElementById('timeVal').textContent = Math.ceil(timeLeft) + 's';
      document.getElementById('levelVal').textContent = '速度 ' + mult + 'x · ' + tier.label;
    }
    document.getElementById('livesVal').textContent = '♥'.repeat(Math.max(0, lives)) + '♡'.repeat(Math.max(0, MAX_LIVES - lives));
    const sm = getStreakMult(combo);
    document.getElementById('carrotVal').textContent = carrots + '本' + (sm > 1 ? ' · x' + sm.toFixed(1) : '');
  }

  function startFreshGame() {
    state = 'PLAYING'; stage = 1;
    lane = 1; playerX = laneX(1); tilt = 0;
    invuln = 0; hurt = 0; anger = 1.1; elapsed = 0; timeLeft = DURATION;
    score = 0; carrots = 0; combo = 0; maxCombo = 0; lives = MAX_LIVES; level = 1;
    spawnMs = 250; lastSafeLane = 1; entities = []; texts = [];
    banner = mode === 'endless' ? 'エンドレス！Lv.5まで5秒ごと加速！' : 'STAGE 1 平原スタート！';
    bannerT = 1.5;
    document.getElementById('titleOverlay').style.display = 'none';
    document.getElementById('stageClearOverlay').style.display = 'none';
    document.getElementById('endOverlay').style.display = 'none';
    document.getElementById('touchControls').style.display = 'grid';
    [523,659,784,1046].forEach((n,i)=>tone(n,0.07,'square',0.07,i*0.06));
    syncHud();
  }

  function advanceToNextStage() {
    stage = Math.min(TOTAL_STAGES, stage + 1);
    const cfg = getStageCfg(stage);
    state = 'PLAYING';
    lane = 1; playerX = laneX(1); tilt = 0;
    invuln = 0; hurt = 0; anger = 1.2; elapsed = 0; timeLeft = DURATION;
    lives = MAX_LIVES; level = 1;
    spawnMs = 250; lastSafeLane = 1; entities = []; texts = [];
    banner = 'STAGE ' + stage + ' ' + cfg.name + 'スタート！';
    bannerT = 1.6;
    document.getElementById('stageClearOverlay').style.display = 'none';
    document.getElementById('touchControls').style.display = 'grid';
    [523,659,784,1046].forEach((n,i)=>tone(n,0.07,'square',0.07,i*0.06));
    syncHud();
  }

  function showStageClear() {
    state = 'STAGE_CLEAR';
    const curCfg = getStageCfg(stage);
    const nxtCfg = getStageCfg(stage + 1);
    const nxtSpeed = (nxtCfg.baseSpeed / BASE_SPEED).toFixed(1);
    document.getElementById('touchControls').style.display = 'none';
    document.getElementById('scKicker').textContent = 'STAGE ' + stage + '/' + TOTAL_STAGES + ' ' + curCfg.name + ' 45秒完走！';
    document.getElementById('scTitle').textContent = 'ステージ' + stage + ' クリア！';
    document.getElementById('scDesc').textContent = 'スコアを引き継いで、ライフ全回復で次は「' + nxtCfg.name + '」（初速 ' + nxtSpeed + 'x）へ！';
    document.getElementById('scScore').textContent = score.toLocaleString();
    document.getElementById('scDetail').textContent = carrots + '本 · ライフ ♥♥♥ 回復';
    document.getElementById('nextStageBtn').textContent = 'STAGE ' + (stage + 1) + '：' + nxtCfg.name + 'へすすむ';
    document.getElementById('stageClearOverlay').style.display = 'flex';
    [523,659,784,1046,784,1046].forEach((n,i)=>tone(n,0.1,'square',0.08,i*0.08));
    syncHud();
  }

  function endGame(allCleared) {
    state = allCleared ? 'ALL_CLEAR' : 'OVER';
    const tier = getDiff();
    const mult = (tier.speed / BASE_SPEED).toFixed(1);
    const cfg = getStageCfg(stage);
    document.getElementById('touchControls').style.display = 'none';
    document.getElementById('endKicker').textContent = allCleared ? 'STAGE 8 溶岩城も突破！おめでとう！' : (mode === 'standard' ? 'STAGE ' + stage + '/' + TOTAL_STAGES + ' ' + cfg.name + ' · 障害物にぶつかった！' : 'エンドレス · 障害物にぶつかった！');
    document.getElementById('endTitle').textContent = allCleared ? '全8ステージ制覇！' : 'ゲームオーバー';
    document.getElementById('endScore').textContent = score.toLocaleString();
    document.getElementById('endBest').textContent = getBest(mode).toLocaleString();
    document.getElementById('endDetail').textContent = carrots + '本 · 速度 ' + mult + 'x · 最大' + maxCombo + '連続';
    document.getElementById('restartBtn').textContent = mode === 'standard' ? 'STAGE 1からもういちど' : 'もういちどあそぶ';
    document.getElementById('endOverlay').style.display = 'flex';
    if (allCleared) [523,659,784,1046,784,1046].forEach((n,i)=>tone(n,0.1,'square',0.08,i*0.08));
    else [392,349,311,261].forEach((n,i)=>tone(n,0.14,'sawtooth',0.08,i*0.11));
    syncHud();
  }

  function returnToMenu() {
    state = 'TITLE'; stage = 1;
    score = 0; carrots = 0; combo = 0; lives = MAX_LIVES; elapsed = 0; timeLeft = DURATION;
    document.getElementById('stageClearOverlay').style.display = 'none';
    document.getElementById('endOverlay').style.display = 'none';
    document.getElementById('titleOverlay').style.display = 'flex';
    syncModeCard();
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

  document.querySelectorAll('.mode-tab').forEach(btn => {
    btn.onclick = () => { mode = btn.dataset.mode; stage = 1; syncModeCard(); };
  });
  document.getElementById('startBtn').onclick = startFreshGame;
  document.getElementById('nextStageBtn').onclick = advanceToNextStage;
  document.getElementById('restartBtn').onclick = startFreshGame;
  document.getElementById('scMenuBtn').onclick = returnToMenu;
  document.getElementById('menuBtn').onclick = returnToMenu;
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
    else if (e.key === ' ' || e.key === 'Enter') {
      if (state === 'STAGE_CLEAR') { e.preventDefault(); advanceToNextStage(); }
      else if (state !== 'PLAYING') { e.preventDefault(); startFreshGame(); }
    }
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
    const obs = mode === 'endless' ? ['brick', 'pipe', 'chestnut'] : getStageCfg(stage).obs;
    const lanes = [0, 1, 2];
    const reachable = lanes.filter(l => Math.abs(l - lastSafeLane) <= 1);
    const safe = reachable[Math.floor(Math.random() * reachable.length)];
    lastSafeLane = safe;
    const blocked = lanes.filter(l => l !== safe);
    if (Math.random() < tier.dbl) {
      blocked.forEach(bl => entities.push({ kind: obs[Math.floor(Math.random()*3)], lane: bl, y: SKY_H - 36, bob: Math.random()*6 }));
      if (Math.random() < 0.8) entities.push({ kind: Math.random() < 0.14 ? 'gold' : 'carrot', lane: safe, y: SKY_H - 64, bob: Math.random()*6 });
    } else {
      let obLane = null;
      if (Math.random() < 0.78) {
        obLane = blocked[Math.floor(Math.random()*blocked.length)];
        entities.push({ kind: obs[Math.floor(Math.random()*3)], lane: obLane, y: SKY_H - 36, bob: Math.random()*6 });
      }
      if (Math.random() < tier.carrot + 0.2) {
        const free = lanes.filter(l => l !== obLane);
        const cl = free[Math.floor(Math.random()*free.length)];
        entities.push({ kind: Math.random() < 0.12 ? 'gold' : 'carrot', lane: cl, y: obLane !== null ? SKY_H - 64 : SKY_H - 36, bob: Math.random()*6 });
      }
    }
  }

  function drawPyramid(x, baseY, w, h) {
    for (let row = 0; row < h; row += 4) {
      const inset = Math.floor((row / h) * (w * 0.5));
      const rw = Math.max(4, w - inset * 2);
      const half = Math.ceil(rw * 0.55);
      ctx.fillStyle = '#E09F4B';
      ctx.fillRect(x + inset, baseY - row - 4, half, 4);
      ctx.fillStyle = '#A86424';
      ctx.fillRect(x + inset + half, baseY - row - 4, Math.max(0, rw - half), 4);
    }
    ctx.fillStyle = '#F5C478';
    ctx.fillRect(x + Math.floor(w * 0.46), baseY - h + 4, 6, 4);
  }

  function drawPeak(x, baseY, w, h, bodyCol, capCol, ratio) {
    for (let row = 0; row < h; row += 4) {
      const inset = Math.floor((row / h) * (w * 0.48));
      ctx.fillStyle = row >= h * (1 - ratio) ? capCol : bodyCol;
      ctx.fillRect(x + inset, baseY - row - 4, Math.max(4, w - inset * 2), 4);
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
      timeLeft = mode === 'endless' ? DURATION : Math.max(0, DURATION - elapsed);
      const tier = getDiff();
      if (tier.level > level) {
        level = tier.level;
        banner = mode === 'endless'
          ? 'SPEED UP! LV.' + tier.level + ' (' + (tier.speed/BASE_SPEED).toFixed(1) + 'x)'
          : 'SPEED UP! (' + (tier.speed/BASE_SPEED).toFixed(1) + 'x) ' + tier.label;
        bannerT = 1.5; anger = 1.2;
        [440,554,659,880].forEach((n,i)=>tone(n,0.08,'square',0.07,i*0.065));
      }
      scroll = (scroll + dt * tier.speed) % 64;
      runT += dt * (8 + Math.min(12, tier.speed / 35));
      if (invuln > 0) invuln = Math.max(0, invuln - dt);
      if (hurt > 0) hurt = Math.max(0, hurt - dt);
      if (anger > 0) anger = Math.max(0, anger - dt);
      if (bannerT > 0) bannerT = Math.max(0, bannerT - dt);

      playerX += (laneX(lane) - playerX) * Math.min(1, dt * 19);
      tilt *= Math.pow(0.001, dt);

      spawnMs -= dt * 1000;
      if (spawnMs <= 0) { spawnWave(tier); spawnMs = tier.interval; }

      for (const ent of entities) {
        ent.y += tier.speed * dt;
        ent.bob += dt * 7;
        if (ent.dead) continue;
        const ex = laneX(ent.lane);
        const isCarrot = ent.kind === 'carrot' || ent.kind === 'gold';
        const hitX = isCarrot ? 38 : 20;
        const hitTop = isCarrot ? PLAYER_Y - 22 : PLAYER_Y - 12;
        const hitBot = isCarrot ? PLAYER_Y + 24 : PLAYER_Y + 14;
        const halfH = isCarrot ? 20 : 12;
        if (Math.abs(playerX - ex) < hitX && ent.y + halfH >= hitTop && ent.y - halfH <= hitBot) {
          if (isCarrot) {
            ent.dead = true;
            const prevMult = getStreakMult(combo);
            combo++; maxCombo = Math.max(maxCombo, combo);
            carrots++;
            const mult = getStreakMult(combo);
            const pts = Math.round((ent.kind === 'gold' ? 300 : 100) * mult);
            score += pts;
            if (score > getBest(mode)) setBest(mode, score);
            if (ent.kind === 'gold') [587,784,1046,1318].forEach((n,i)=>tone(n,0.07,'square',0.08,i*0.055));
            else { tone(659+combo*25,0.06,'square',0.07,0); tone(988+combo*25,0.1,'square',0.07,0.05); }
            const label = ent.kind === 'gold'
              ? (mult > 1 ? '+' + pts + ' GOLD x' + mult.toFixed(1) : '+' + pts + ' GOLD!')
              : (mult > prevMult ? '+' + pts + ' x' + mult.toFixed(1) + ' UP!' : (mult > 1 ? '+' + pts + ' x' + mult.toFixed(1) : '+' + pts));
            texts.push({ x: ex, y: PLAYER_Y - 32, t: label, c: (ent.kind === 'gold' || mult > prevMult) ? '#FDE047' : '#FFF', l: 0.7 });
          } else if (invuln <= 0) {
            ent.dead = true; lives--; combo = 0; invuln = 1.25; hurt = 0.45; anger = 1.5;
            tone(200,0.1,'sawtooth',0.09,0,100); tone(130,0.16,'square',0.09,0.06,65);
            texts.push({ x: playerX, y: PLAYER_Y - 36, t: 'イテッ！', c: '#FCA5A5', l: 0.7 });
            if (lives <= 0) { endGame(false); break; }
          }
        }
      }
      for (const ent of entities) {
        if ((ent.kind === 'carrot' || ent.kind === 'gold') && !ent.dead && ent.y >= CANVAS_H + 20) {
          if (combo > 0) {
            combo = 0;
            texts.push({ x: laneX(ent.lane), y: CANVAS_H - 22, t: '取り逃し x1.0', c: '#CBD5E1', l: 0.7 });
          }
        }
      }
      entities = entities.filter(e => !e.dead && e.y < CANVAS_H + 20);
      texts = texts.filter(t => { t.y -= 38 * dt; t.l -= dt; return t.l > 0; });

      if (mode === 'standard' && timeLeft <= 0 && state === 'PLAYING') {
        score += lives * 500;
        if (score > getBest(mode)) setBest(mode, score);
        if (stage < TOTAL_STAGES) showStageClear();
        else endGame(true);
      }
      hudT += dt;
      if (hudT >= 0.08) { hudT = 0; syncHud(); }
    }

    const theme = getTheme();
    ctx.imageSmoothingEnabled = false;
    let sideC = '#248A24', roadC = '#D9A75A', centerC = '#CE9A4D', dashC = '#F8E6BE', horC = '#1B1410';

    if (theme === 'desert') {
      ctx.fillStyle = '#F2A65A'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 22);
      ctx.fillStyle = '#F9C97E'; ctx.fillRect(0, SKY_H - 22, CANVAS_W, 22);
      ctx.fillStyle = '#FFF3B0'; ctx.fillRect(296, 12, 24, 24);
      ctx.fillStyle = '#FDE047'; ctx.fillRect(300, 16, 16, 16);
      drawPyramid(14, SKY_H, 108, 46); drawPyramid(144, SKY_H, 76, 32); drawPyramid(228, SKY_H, 116, 52);
      sideC = '#C97B36'; roadC = '#EAD09A'; centerC = '#DFC182'; dashC = '#FFF5DC'; horC = '#4A2B13';
    } else if (theme === 'island') {
      ctx.fillStyle = '#38BDF8'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 26);
      ctx.fillStyle = '#0284C7'; ctx.fillRect(0, SKY_H - 26, CANVAS_W, 26);
      ctx.fillStyle = '#FACC15'; ctx.fillRect(236, SKY_H - 32, 76, 10);
      ctx.fillStyle = '#78350F'; ctx.fillRect(268, SKY_H - 54, 6, 24);
      ctx.fillStyle = '#16A34A'; ctx.fillRect(252, SKY_H - 60, 38, 8);
      sideC = '#0284C7'; roadC = '#FDE68A'; centerC = '#FCD34D'; dashC = '#FFFFFF'; horC = '#0369A1';
    } else if (theme === 'snow') {
      ctx.fillStyle = '#60A5FA'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 24);
      ctx.fillStyle = '#93C5FD'; ctx.fillRect(0, SKY_H - 24, CANVAS_W, 24);
      drawPeak(8, SKY_H, 110, 48, '#64748B', '#F8FAFC', 0.42);
      drawPeak(124, SKY_H, 128, 56, '#475569', '#FFFFFF', 0.45);
      drawPeak(246, SKY_H, 108, 44, '#64748B', '#F8FAFC', 0.40);
      sideC = '#64748B'; roadC = '#EFF6FF'; centerC = '#DBEAFE'; dashC = '#3B82F6'; horC = '#1E3A8A';
    } else if (theme === 'jungle') {
      ctx.fillStyle = '#0F766E'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 22);
      ctx.fillStyle = '#115E59'; ctx.fillRect(0, SKY_H - 22, CANVAS_W, 22);
      ctx.fillStyle = '#064E3B'; ctx.fillRect(16, SKY_H - 44, 64, 44); ctx.fillRect(28, SKY_H - 56, 40, 12);
      ctx.fillStyle = '#15803D'; ctx.fillRect(120, SKY_H - 36, 92, 36); ctx.fillRect(240, SKY_H - 48, 104, 48);
      sideC = '#14532D'; roadC = '#7C5A3B'; centerC = '#694A2E'; dashC = '#BEF264'; horC = '#052E16';
    } else if (theme === 'mountain') {
      ctx.fillStyle = '#9A3412'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 24);
      ctx.fillStyle = '#EA580C'; ctx.fillRect(0, SKY_H - 24, CANVAS_W, 24);
      drawPeak(0, SKY_H, 130, 52, '#44403C', '#78716C', 0.30);
      drawPeak(115, SKY_H, 136, 62, '#292524', '#57534E', 0.32);
      drawPeak(230, SKY_H, 130, 48, '#44403C', '#78716C', 0.28);
      sideC = '#44403C'; roadC = '#A8A29E'; centerC = '#8E8883'; dashC = '#FDE68A'; horC = '#1C1917';
    } else if (theme === 'cloud') {
      ctx.fillStyle = '#2563EB'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 20);
      ctx.fillStyle = '#60A5FA'; ctx.fillRect(0, SKY_H - 20, CANVAS_W, 20);
      ['#EF4444','#F97316','#FACC15','#22C55E','#38BDF8'].forEach((c, i) => {
        ctx.fillStyle = c; ctx.fillRect(190 + i * 4, 14 + i * 4, 90 - i * 8, 4);
      });
      ctx.fillStyle = '#FFFFFF';
      for (let cx = 0; cx < CANVAS_W; cx += 48) { ctx.fillRect(cx + 4, SKY_H - 16, 40, 16); ctx.fillRect(cx + 12, SKY_H - 22, 24, 6); }
      sideC = '#93C5FD'; roadC = '#FFFFFF'; centerC = '#E0F2FE'; dashC = '#38BDF8'; horC = '#1D4ED8';
    } else if (theme === 'castle') {
      ctx.fillStyle = '#1C1917'; ctx.fillRect(0, 0, CANVAS_W, SKY_H - 18);
      ctx.fillStyle = '#DC2626'; ctx.fillRect(0, SKY_H - 18, CANVAS_W, 18);
      ctx.fillStyle = '#F97316'; ctx.fillRect(0, SKY_H - 10, CANVAS_W, 10);
      ctx.fillStyle = '#292524';
      for (let bx = 12; bx < CANVAS_W; bx += 64) {
        ctx.fillRect(bx, SKY_H - 54, 40, 36);
        ctx.fillRect(bx, SKY_H - 62, 10, 8); ctx.fillRect(bx+15, SKY_H - 62, 10, 8); ctx.fillRect(bx+30, SKY_H - 62, 10, 8);
      }
      sideC = '#991B1B'; roadC = '#57534E'; centerC = '#44403C'; dashC = '#FBBF24'; horC = '#0C0A09';
    } else {
      ctx.fillStyle = '#5C94FC'; ctx.fillRect(0, 0, CANVAS_W, SKY_H);
      ctx.fillStyle = '#198E19'; ctx.fillRect(28, SKY_H - 22, 64, 22); ctx.fillRect(240, SKY_H - 28, 76, 28);
      ctx.fillStyle = '#FFF';
      ctx.fillRect(((60+cloudX)%(CANVAS_W+60))-50, 20, 36, 12);
      ctx.fillRect(((230+cloudX*0.7)%(CANVAS_W+60))-50, 34, 40, 12);
    }

    ctx.fillStyle = horC; ctx.fillRect(0, SKY_H - 4, CANVAS_W, 4);
    ctx.fillStyle = sideC; ctx.fillRect(0, SKY_H, GRASS_W, CANVAS_H - SKY_H); ctx.fillRect(CANVAS_W - GRASS_W, SKY_H, GRASS_W, CANVAS_H - SKY_H);
    ctx.fillStyle = roadC; ctx.fillRect(GRASS_W, SKY_H, ROAD_W, CANVAS_H - SKY_H);
    ctx.fillStyle = centerC; ctx.fillRect(GRASS_W + LANE_W, SKY_H, LANE_W, CANVAS_H - SKY_H);

    if (state === 'PLAYING') {
      ctx.fillStyle = theme === 'castle' ? 'rgba(253,224,71,0.14)' : ((theme === 'snow' || theme === 'cloud') ? 'rgba(59,130,246,0.15)' : 'rgba(255,255,255,0.18)');
      ctx.fillRect(GRASS_W + lane * LANE_W + 4, PLAYER_Y - 34, LANE_W - 8, 68);
    }

    const off = Math.floor(scroll);
    for (let y = SKY_H - 64 + off; y < CANVAS_H + 32; y += 64) {
      if (y >= SKY_H) {
        ctx.fillStyle = dashC;
        ctx.fillRect(GRASS_W + LANE_W - 2, y, 4, 28);
        ctx.fillRect(GRASS_W + LANE_W * 2 - 2, y, 4, 28);
        ctx.fillStyle = theme === 'castle' ? '#F97316' : (theme === 'snow' || theme === 'cloud' ? '#FFF' : (theme === 'desert' ? '#E69F58' : '#4CE04C'));
        ctx.fillRect(12, y + 10, 14, 6);
        ctx.fillRect(CANVAS_W - 26, y + 26, 14, 6);
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
      ctx.fillRect(24, 120, CANVAS_W - 48, 42);
      ctx.strokeStyle = '#FACC15'; ctx.lineWidth = 3;
      ctx.strokeRect(24, 120, CANVAS_W - 48, 42);
      ctx.font = '15px "DotGothic16", monospace';
      ctx.fillStyle = '#FACC15';
      ctx.fillText(banner, CANVAS_W / 2, 147);
    }

    requestAnimationFrame(loop);
  }
  syncModeCard();
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=740, scrolling=False)
