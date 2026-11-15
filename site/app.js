/* Earth Dev Defense — análogos terrestres. Site estático: lê data/dados_site.json (pipeline) e data/equipe.json.
   Sem framework: estado simples + funções de renderização. Globo 3D: globe.gl (three.js).
   As funções de cálculo (mediana, entradas, rankingAtual) não mudam no redesign: só a apresentação. */
'use strict';

const GRUPOS = { terreno: 'Terrain', cobertura: 'Ground cover', temperatura: 'Temperature', geologia: 'Geology' };
const ICONE_GRUPO = { terreno: 'mountain', cobertura: 'layers', temperatura: 'thermometer', geologia: 'gem' };
const LITO = {
  vulcanica: 'volcanic', cristalina: 'crystalline (intrusive/metamorphic)', sedimentar: 'sedimentary',
  evaporitica: 'evaporite', gelo: 'ice', impacto_terras_altas: 'impact / highlands',
  misto_indefinido: 'mixed / undefined', nao_classificado: 'unclassified',
};
const MISSOES = [
  { id: 'geral', nome: 'Overall', grupo: null, icone: 'globe',
    desc: 'All four groups (terrain, ground cover, temperature, geology) with equal weight. A good starting point to simulate a long-duration habitat.' },
  { id: 'terreno', nome: 'Landing and mobility', grupo: 'terreno', icone: 'plane-landing',
    desc: 'Terrain only (slope, roughness and relief): landing trials, rover tests and astronaut traverses on foot.' },
  { id: 'temperatura', nome: 'Cold and equipment', grupo: 'temperatura', icone: 'thermometer-snowflake',
    desc: 'Surface temperature only: endurance tests for equipment, batteries and suits, and operations in the cold.' },
  { id: 'geologia', nome: 'Field geology', grupo: 'geologia', icone: 'pickaxe',
    desc: 'Rock type only: astronaut geology training, sample collection and instrument tests.' },
  { id: 'cobertura', nome: 'Surface and dust', grupo: 'cobertura', icone: 'wind',
    desc: 'Ground cover only (bare ground, ice, vegetation, buildings): dust, instrument calibration and ice as a resource.' },
];
const USOS = {
  terreno: 'landing trials, rover mobility and traverses on foot',
  temperatura: 'thermal tests of equipment, batteries and suits',
  geologia: 'field geology training and sample collection',
  cobertura: 'dust, abrasion and instrument calibration tests',
};
const USO_CURTO = {
  terreno: ['plane-landing', 'Landing and mobility'], temperatura: ['thermometer-snowflake', 'Thermal tests'],
  geologia: ['pickaxe', 'Field geology'], cobertura: ['wind', 'Dust and instruments'],
};
// Texturas da Terra (NASA Blue Marble e topografia), servidas pelo próprio site (antes via CDN do three-globe).
const TEX = 'assets/img/terra_blue_marble.webp';
const TOPO = 'assets/img/terra_relevo.webp';
const COR = { terra: '#D42804', controle: '#6b7099', sel: '#EAFE07' };

const E = { dados: null, corpo: 'MOON', alvo: 'MOON', missao: 'geral', site: null, k: 5, controles: false, globo: null };
const $ = (s) => document.querySelector(s);
const fmt = (v, d = 1) => (v == null || Number.isNaN(v)) ? '—'
  : Number(v).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
const local = (id) => E.dados.locaisPorId[id];
const siteDoRecorte = (tile) => tile.replace(/_r\d+c\d+$/, '');
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ic = (nome, cls = '') => `<svg class="ic ${cls}" aria-hidden="true"><use href="assets/icones.svg#i-${nome}"/></svg>`;
const miniatura = (siteId) => `data/miniaturas/${siteId}.webp`;
// cor de cada corpo nos ícones: Terra azul, Lua branca, Marte vermelha
const corAlvo = () => (E.corpo === 'MOON' ? 'lua' : 'marte');
const nomeCorpoAlvo = () => (E.corpo === 'MOON' ? 'Moon' : 'Mars');
const ord = (n) => { const s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); };

/* ---------------------------------------------------------------- ranking */
function mediana(xs) {
  const s = xs.filter((x) => x != null).sort((a, b) => a - b);
  if (!s.length) return 0;
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}
function entradas() {
  const sim = E.dados.similaridade;
  return E.alvo === E.corpo ? sim.por_corpo[E.corpo] : sim.por_alvo[E.alvo];
}
/* Similaridade por grupo, na mesma escala do score: 100/(1 + d/mediana_do_grupo). */
function rankingAtual() {
  const lista = entradas();
  const med = {};
  for (const g of Object.keys(GRUPOS)) {
    let m = mediana(lista.map((e) => e.dist_grupos[g]));
    if (!(m > 0)) m = (lista.reduce((a, e) => a + (e.dist_grupos[g] || 0), 0) / lista.length) || 1;
    med[g] = m;
  }
  const missao = MISSOES.find((m) => m.id === E.missao);
  const linhas = lista.map((e) => {
    const sg = {};
    for (const g of Object.keys(GRUPOS)) sg[g] = 100 / (1 + (e.dist_grupos[g] || 0) / med[g]);
    const loc = local(e.site_id);
    return { ...e, sg, valor: missao.grupo ? sg[missao.grupo] : e.score, loc,
             controle: loc.tipo === 'controle', publicado: E.dados.publicados.has(`${e.site_id}|${E.corpo}`) };
  });
  // empates (comuns na geologia, que é discreta) desempatados pelo score geral
  linhas.sort((a, b) => (b.valor - a.valor) || (b.score - a.score));
  const visiveis = linhas.filter((l) => E.controles || !l.controle);
  visiveis.forEach((l, i) => { l.pos = i + 1; });
  return visiveis;
}
const linhasVisiveis = () => rankingAtual();

/* Empates só para exibição: linhas consecutivas com a mesma nota exibida (inteira). As notas e a ordem não mudam;
   dentro do grupo a ordem é a de sempre (nota com decimais e, em empate exato, a visão geral). */
function gruposEmpate(linhas) {
  const grupos = [];
  for (const l of linhas) {
    const g = grupos[grupos.length - 1];
    if (g && Math.round(g.valor) === Math.round(l.valor)) g.linhas.push(l);
    else grupos.push({ valor: l.valor, inicio: l.pos, linhas: [l] });
  }
  return grupos;
}

/* ---------------------------------------------------------------- abertura e desafio */
function renderNumeros() {
  const d = E.dados;
  const terra = d.locais.filter((l) => l.corpo === 'EARTH').length;
  const alvos = d.locais.length - terra;
  const itens = [[terra, 'places on Earth', 'map-pin'], [alvos, 'targets on the Moon and Mars', 'crosshair'],
    [d.dados.recortes.length, '9 km tiles analyzed', 'grid-3x3'],
    [d.dados.meta.features.length, 'features per tile', 'sliders-horizontal']];
  $('#numeros').innerHTML = itens.map(([n, r, i]) => `<div class="numero">${ic(i)}<b>${n}</b><span>${r}</span></div>`).join('');
}
function renderTrio() {
  const trio = [['earth_atacama_yungay', 'Earth', 'terra'], ['moon_haworth', 'Moon', 'lua'], ['mars_jezero', 'Mars', 'marte']]
    .map(([id, corpo, cor]) => ({ l: local(id), corpo, cor })).filter((x) => x.l);
  $('#trio').innerHTML = trio.map(({ l, corpo, cor }) => `<figure class="trio-item">
      <img src="${miniatura(l.site_id)}" alt="Shaded relief of ${esc(l.nome)} (${corpo})" loading="lazy" width="240" height="240">
      <span class="corpo"><span class="ponto ${cor}"></span>${corpo}</span><span class="lugar">${esc(l.nome)}</span></figure>`).join('')
    + '<figcaption class="trio-legenda">Real relief of the analyzed tiles, at the same scale (NASADEM, LOLA and CTX data).</figcaption>';
}

/* ---------------------------------------------------------------- escolhas */
function renderAlvos() {
  $('#alvos').innerHTML = '';
  const alvos = E.dados.locais.filter((l) => l.corpo === E.corpo);
  const nomeCorpo = E.corpo === 'MOON' ? 'the Moon' : 'Mars';
  const itens = [{ id: E.corpo, nome: `All targets on ${nomeCorpo}`, info: `${alvos.length} targets combined`, todos: true },
    ...alvos.map((a) => ({ id: a.site_id, nome: a.nome,
      info: `${a.n_recortes} ${a.n_recortes === 1 ? 'tile' : 'tiles'} · ${fmt(a.lat, 2)}°, ${fmt(a.lon, 2)}°` }))];
  for (const it of itens) {
    const b = document.createElement('button');
    b.className = 'alvo'; b.type = 'button'; b.setAttribute('role', 'radio');
    b.setAttribute('aria-checked', String(it.id === E.alvo));
    b.innerHTML = (it.todos
      ? `<span class="mosaico" aria-hidden="true">${alvos.slice(0, 4).map((a) => `<img src="${miniatura(a.site_id)}" alt="" loading="lazy" width="120" height="120">`).join('')}</span>`
      : `<img class="miniatura" src="${miniatura(it.id)}" alt="Shaded relief of ${esc(it.nome)}" loading="lazy" width="240" height="240">`)
      + `<span class="alvo-nome">${esc(it.nome)}</span><span class="alvo-info">${esc(it.info)}</span>`;
    b.addEventListener('click', () => { E.alvo = it.id; E.site = null; atualizar(); });
    $('#alvos').append(b);
  }
}
function renderMissoes() {
  $('#missoes').innerHTML = '';
  for (const m of MISSOES) {
    const b = document.createElement('button');
    b.className = 'missao'; b.type = 'button'; b.setAttribute('role', 'radio');
    b.setAttribute('aria-checked', String(m.id === E.missao));
    b.innerHTML = `${ic(m.icone)}<span>${esc(m.nome)}</span>`;
    b.addEventListener('click', () => { E.missao = m.id; atualizar(); });
    $('#missoes').append(b);
  }
  $('#missao-desc').innerHTML = `${ic('info')}<span>${esc(MISSOES.find((m) => m.id === E.missao).desc)}</span>`;
}
function nomeAlvoAtual() {
  return E.alvo === E.corpo ? (E.corpo === 'MOON' ? 'the Moon (all targets)' : 'Mars (all targets)') : local(E.alvo).nome;
}
function selos(l) {
  return (l.publicado ? ' <span class="selo selo-esa" title="In ESA’s Catalogue of Planetary Analogues for this body">ESA</span>' : '')
    + (l.controle ? ' <span class="selo selo-controle" title="Control place (city or rainforest)">control</span>' : '');
}
function selecionar(id) { E.site = id; renderRanking(); renderGlobo(true); renderDetalhe(true); renderClima(); }

/* ---------------------------------------------------------------- ranking */
function renderRanking() {
  const missao = MISSOES.find((m) => m.id === E.missao);
  $('#titulo-ranking').textContent = `Places on Earth most similar to ${nomeAlvoAtual()}`
    + (missao.grupo ? ` — ${GRUPOS[missao.grupo].toLowerCase()}` : '');
  const ol = $('#ranking'); ol.innerHTML = '';
  for (const g of gruposEmpate(linhasVisiveis())) {
    const empate = g.linhas.length > 1;
    const lugar = g.inicio;                                   // posição exibida do grupo
    if (empate) {
      const li = document.createElement('li');
      li.className = 'grupo-empate'; li.setAttribute('aria-hidden', 'true');
      li.innerHTML = `<span><b>${g.linhas.length} tied for ${ord(lugar)}</b> · score ${fmt(g.valor, 0)}</span><span>order within: score decimals</span>`;
      ol.append(li);
    }
    for (const l of g.linhas) {
      const li = document.createElement('li');
      const b = document.createElement('button');
      const podio = lugar <= 3;
      b.type = 'button';
      b.className = 'linha' + (l.controle ? ' controle' : '') + (podio ? ` podio p${lugar}` : '') + (empate ? ' empatado' : '');
      if (l.site_id === E.site) b.setAttribute('aria-current', 'true');
      b.setAttribute('aria-label', `${empate ? `tied for ${ord(lugar)}` : ord(l.pos)} ${l.loc.nome}, similarity ${fmt(l.valor, 0)} out of 100`);
      b.innerHTML = `<span class="pos">${empate ? '=' : l.pos}</span><span class="nome">${esc(l.loc.nome)}${selos(l)}</span>`
        + `<span class="valor">${fmt(l.valor, 0)}</span><span></span>`
        + `<span class="barra" aria-hidden="true"><span style="width:${Math.max(2, l.valor).toFixed(1)}%"></span></span>`;
      b.addEventListener('click', () => selecionar(l.site_id));
      li.append(b); ol.append(li);
    }
  }
}

/* ---------------------------------------------------------------- globo 3D */
const altitudeInicial = () => (window.innerWidth < 600 ? 3.1 : 2.75);
function criarGlobo() {
  const el = $('#globo');
  if (!window.Globe) {
    el.innerHTML = '<div class="globo-aviso">The 3D globe needs an internet connection and WebGL. The ranking beside it shows the same data.</div>';
    return null;
  }
  try {
    const g = Globe({ animateIn: true })(el)
      .globeImageUrl(TEX).bumpImageUrl(TOPO)
      .backgroundColor('rgba(0,0,0,0)').atmosphereColor('#9cc4f5').atmosphereAltitude(0.15)
      .width(el.clientWidth).height(el.clientHeight)
      .pointLat('lat').pointLng('lng').pointAltitude('alt').pointRadius('raio').pointColor('cor')
      .pointLabel('rotulo').pointsMerge(false).pointsTransitionDuration(500)
      .onPointClick((p) => selecionar(p.site_id))
      .ringLat('lat').ringLng('lng').ringColor(() => (t) => `rgba(234,254,7,${1 - t})`)
      .ringMaxRadius(6).ringPropagationSpeed(2.5).ringRepeatPeriod(1100);
    const reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    g.controls().autoRotate = !reduzido;
    g.controls().autoRotateSpeed = 0.35;
    g.controls().addEventListener('start', () => { g.controls().autoRotate = false; });
    g.pointOfView({ lat: 15, lng: -30, altitude: altitudeInicial() });
    new ResizeObserver(() => g.width(el.clientWidth).height(el.clientHeight)).observe(el);
    return g;
  } catch (e) {
    el.innerHTML = '<div class="globo-aviso">The 3D globe could not start in this browser (WebGL). The ranking beside it shows the same data.</div>';
    return null;
  }
}
function renderGlobo(voar) {
  if (!E.globo) E.globo = criarGlobo();
  const linhas = linhasVisiveis();
  const vals = linhas.filter((l) => !l.controle).map((l) => l.valor);
  const min = Math.min(...vals), max = Math.max(...vals);
  const pontos = linhas.map((l) => {
    const sel = l.site_id === E.site;
    const rel = max > min ? (l.valor - min) / (max - min) : 1;
    return {
      site_id: l.site_id, lat: l.loc.lat, lng: l.loc.lon,
      alt: 0.015 + 0.26 * Math.max(0, rel), raio: sel ? 0.85 : 0.5,
      cor: sel ? COR.sel : (l.controle ? COR.controle : COR.terra),
      rotulo: `<div class="rotulo-globo"><strong>${esc(l.loc.nome)}</strong><br>${ord(l.pos)} · similarity ${fmt(l.valor, 0)}`
        + `${l.publicado ? ' · ESA' : ''}${l.controle ? ' · control' : ''}</div>`,
    };
  });
  $('#legenda-globo').innerHTML = `<span>Bar height = similarity (from ${fmt(min, 0)} to ${fmt(max, 0)} in this view)</span>`
    + `<span><span class="amostra" style="background:${COR.terra}"></span>candidate place</span>`
    + (E.controles ? `<span><span class="amostra" style="background:${COR.controle}"></span>control</span>` : '')
    + `<span><span class="amostra" style="background:${COR.sel}"></span>selected</span>`
    + '<span>Drag to rotate · scroll to zoom</span>';
  if (!E.globo) return;
  E.globo.pointsData(pontos);
  const sel = pontos.find((p) => p.site_id === E.site);
  E.globo.ringsData(sel ? [sel] : []);
  if (voar && sel) {
    E.globo.controls().autoRotate = false;
    E.globo.pointOfView({ lat: sel.lat, lng: sel.lng, altitude: 2.0 }, 1200);
  }
}

/* ---------------------------------------------------------------- comparação */
function valorAlvo(col) {
  if (E.alvo !== E.corpo) return local(E.alvo).media[col];
  const alvos = E.dados.locais.filter((l) => l.corpo === E.corpo);
  return alvos.reduce((a, l) => a + l.media[col], 0) / alvos.length;
}
function fmtUnid(v, u) {
  if (u === 'K') return `${fmt(v, 0)} K (${fmt(v - 273.15, 0)} °C)`;
  if (u === 'fraction') return `${fmt(100 * v, 0)}%`;
  return `${fmt(v, v >= 100 ? 0 : 1)} ${u}`;
}
/* Halteres: alvo (círculo azul) × lugar da Terra (losango vermelho), agrupados por categoria, cada linha na própria escala. */
function halteres(site) {
  const feats = E.dados.dados.meta.features.filter((f) => f.grupo !== 'geologia');
  const W = 300, pad = 10;
  let html = `<div class="legenda" aria-hidden="true"><span><span class="ponto ${corAlvo()}"></span>Target (${nomeCorpoAlvo()})</span>`
    + '<span><span class="ponto terra"></span>Place on Earth</span>'
    + '<span>Each row has its own scale: from the lowest to the highest value among all places.</span></div><div class="halteres">';
  let tabela = '<table><thead><tr><th>Feature</th><th class="num">Target</th><th class="num">Earth</th></tr></thead><tbody>';
  let grupoAtual = null;
  for (const f of feats) {
    if (f.grupo !== grupoAtual) {
      grupoAtual = f.grupo;
      html += `<p class="halteres-grupo">${ic(ICONE_GRUPO[f.grupo] || 'info')}${esc(GRUPOS[f.grupo] || f.grupo)}</p>`;
    }
    const vals = E.dados.locais.map((l) => l.media[f.coluna]);
    const min = Math.min(...vals), max = Math.max(...vals);
    // posição em % da trilha (mesma escala de antes: do menor ao maior valor entre todos os locais)
    const x = (v) => 100 * (pad + (W - 2 * pad) * (max > min ? (v - min) / (max - min) : 0.5)) / W;
    const va = valorAlvo(f.coluna), vt = site.media[f.coluna];
    const xa = x(va), xt = x(vt);
    const dica = `${f.nome}: target ${fmtUnid(va, f.unidade)}; ${site.nome} ${fmtUnid(vt, f.unidade)}`;
    html += `<div class="haltere"><span class="rot">${esc(f.nome)}</span>`
      + `<div class="trilha" role="img" aria-label="${esc(dica)}" data-dica="${esc(dica)}" tabindex="0">`
      + `<span class="trilha-ligacao" style="left:${Math.min(xa, xt).toFixed(2)}%;width:${Math.abs(xa - xt).toFixed(2)}%"></span>`
      + `<span class="marca-terra" style="left:${xt.toFixed(2)}%"></span><span class="marca-alvo ${corAlvo()}" style="left:${xa.toFixed(2)}%"></span>`
      + '</div></div>';
    tabela += `<tr><td>${esc(f.nome)}</td><td class="num">${fmtUnid(va, f.unidade)}</td><td class="num">${fmtUnid(vt, f.unidade)}</td></tr>`;
  }
  tabela += '</tbody></table>';
  return html + `</div><details class="saiba"><summary>See the table of values</summary><div class="tabela-wrap">${tabela}</div></details>`;
}
/* Leitura absoluta da distância de um grupo (a barra é relativa aos outros lugares da Terra). */
function absoluto(g, d) {
  if (g === 'geologia') {
    return d < 0.25 ? 'same rock type' : d < 0.75 ? 'target rock type undefined' : 'different rock type';
  }
  const rot = d < 0.5 ? 'very similar' : d < 1 ? 'similar' : d < 1.5 ? 'different' : 'very different';
  return `${rot} (${fmt(d, 1)} standard deviation${d >= 1.95 ? 's' : ''})`;
}
/* Rótulo curto (uma ou duas palavras) da mesma leitura absoluta, para os mini-cards. */
function rotuloCurto(g, d) {
  if (g === 'geologia') return d < 0.25 ? ['same rock', 'bom'] : d < 0.75 ? ['undefined', 'medio'] : ['different rock', 'ruim'];
  return d < 0.5 ? ['very similar', 'bom'] : d < 1 ? ['similar', 'bom'] : d < 1.5 ? ['different', 'medio'] : ['very different', 'ruim'];
}
function renderDetalhe(rolar) {
  const linhas = linhasVisiveis();
  if (!linhas.length) { $('#detalhe').innerHTML = ''; return; }
  if (!E.site || !linhas.some((l) => l.site_id === E.site)) E.site = linhas[0].site_id;
  const l = linhas.find((x) => x.site_id === E.site);
  const site = l.loc;
  const alvoImg = local(siteDoRecorte(l.recorte_alvo));
  $('#titulo-detalhe').textContent = `${site.nome} × ${nomeAlvoAtual()}`;
  // um uso só é sugerido se o grupo é parecido em termos absolutos (< 1 desvio-padrão; geologia: mesma classe)
  const parecidos = Object.keys(GRUPOS).filter((g) => (g === 'geologia' ? l.dist_grupos[g] < 0.25 : l.dist_grupos[g] < 1));
  const geoAlvo = alvoImg.geologia ? LITO[alvoImg.geologia.classe_predominante] : '—';
  const geoTerra = site.geologia ? LITO[site.geologia.classe_predominante] : '—';
  $('#detalhe').innerHTML = `
    <div class="comparacao">
      <figure class="figura"><img src="data/${esc(alvoImg.imagem_relevo)}" alt="Shaded relief of ${esc(alvoImg.nome)}" width="480" height="480">
        <figcaption><span class="ponto ${corAlvo()}"></span><strong>${esc(alvoImg.nome)}</strong> — 27 km window; yellow squares = analyzed tiles</figcaption></figure>
      <figure class="figura"><img src="data/${esc(site.imagem_relevo)}" alt="Shaded relief of ${esc(site.nome)}" width="480" height="480">
        <figcaption><span class="ponto terra"></span><strong>${esc(site.nome)}</strong> (${fmt(site.lat, 2)}°, ${fmt(site.lon, 2)}°)${l.publicado ? ' · <span class="selo selo-esa">ESA</span>' : ''}</figcaption></figure>
      <div class="cartao placar">
        <div class="resumo-score"><span class="grande">${fmt(l.score, 0)}</span><span class="de">out of 100</span>
          <span class="contexto">overall · ${ord(l.pos)} with the current filter</span></div>
        <div class="mini-grupos">${Object.keys(GRUPOS).map((g) => {
          const [rot, cls] = rotuloCurto(g, l.dist_grupos[g]);
          return `<div class="mini-grupo" title="${esc(GRUPOS[g])}: ${esc(absoluto(g, l.dist_grupos[g]))}">${ic(ICONE_GRUPO[g])}
            <span class="g-nome">${GRUPOS[g]}</span><span class="g-nota" aria-label="${GRUPOS[g]}: ${fmt(l.sg[g], 0)} out of 100">${fmt(l.sg[g], 0)}</span>
            <span class="g-rot ${cls}">${rot}</span></div>`;
        }).join('')}</div>
        <p class="rotulo">Good for</p>
        ${parecidos.length ? `<ul class="usos">${parecidos.map((g) => `<li class="uso" title="${esc(USOS[g])}">${ic(USO_CURTO[g][0])}${USO_CURTO[g][1]}</li>`).join('')}</ul>`
          : '<p class="nota" style="margin:0">No group is really similar: a weak analog for this target.</p>'}
        ${site.tipo === 'controle' ? '<p class="nota" style="margin:0">This is a <strong>control place</strong> (city or rainforest), included to check the method.</p>' : ''}
        <details class="saiba"><summary>See details</summary>
          <p>Similarity per group (same scale; 50 = typical pair). The score compares with the other places on Earth; the text says how similar the place is in absolute terms:</p>
          <ul class="lista">${Object.keys(GRUPOS).map((g) => `<li><strong>${GRUPOS[g]} ${fmt(l.sg[g], 0)}:</strong> ${absoluto(g, l.dist_grupos[g])}</li>`).join('')}</ul>
          <p><strong>Geology:</strong> target ${esc(geoAlvo)} · Earth ${esc(geoTerra)}${site.geologia ? `<br><span title="${esc(site.geologia.fonte)}">Unit: ${esc(Object.keys(site.geologia.unidades)[0])}</span>` : ''}</p>
          ${parecidos.length ? `<p><strong>Good for</strong> (similar groups: less than 1 standard deviation, or the same rock type):</p>
            <ul class="lista">${parecidos.map((g) => `<li><strong>${GRUPOS[g]}:</strong> ${USOS[g]}</li>`).join('')}</ul>` : ''}
          <p>Elevation: ${esc(site.fonte_dem)}. Most similar tiles: ${esc(l.recorte_alvo)} × ${esc(l.recorte_terra)}.</p>
        </details>
      </div>
    </div>
    <div class="cartao">${halteres(site)}</div>`;
  ligarDicas($('#detalhe'));
  if (rolar && window.innerWidth < 960) $('#detalhe-sec').scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function ligarDicas(raiz) {
  const tip = $('#tooltip');
  raiz.querySelectorAll('[data-dica]').forEach((el) => {
    const mostrar = (x, y) => { tip.textContent = el.dataset.dica; tip.hidden = false;
      tip.style.left = `${Math.min(x + 12, innerWidth - 270)}px`; tip.style.top = `${y + 12}px`; };
    el.addEventListener('mousemove', (ev) => mostrar(ev.clientX, ev.clientY));
    el.addEventListener('mouseleave', () => { tip.hidden = true; });
    el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); mostrar(r.left, r.bottom); });
    el.addEventListener('blur', () => { tip.hidden = true; });
  });
}

/* ---------------------------------------------------------------- ZEUS */
function renderZeus() {
  $('#k').value = E.k; $('#k-valor').textContent = E.k;
  const chave = `k${E.k}`;
  const lista = linhasVisiveis().filter((l) => l.cocluster[chave] > 0).sort((a, b) => b.cocluster[chave] - a.cocluster[chave]);
  const q = E.dados.dados.meta.qualidade_k.find((x) => x.k === E.k);
  // em quantos dos k grupos caem os quadrados do alvo (só leitura dos clusters já calculados)
  const alvosIds = E.alvo === E.corpo ? E.dados.locais.filter((l) => l.corpo === E.corpo).map((l) => l.site_id) : [E.alvo];
  const tilesAlvo = E.dados.dados.recortes.filter((r) => alvosIds.includes(r.site_id));
  const contagem = {};
  for (const r of tilesAlvo) contagem[r.clusters[chave]] = (contagem[r.clusters[chave]] || 0) + 1;
  const nGrupos = Object.keys(contagem).length;
  const resumo = `<p class="k-resumo">The AI splits all tiles into <b>k = ${E.k}</b> groups. The tiles of ${esc(nomeAlvoAtual())} fall into `
    + `<b>${nGrupos}</b> of them; the places below share a group with part of those tiles.</p>`;
  // agrupa pela fração dos quadrados do alvo (o texto repetido aparece uma vez, como legenda)
  const faixas = [];
  for (const l of lista) {
    const f = faixas[faixas.length - 1];
    if (f && Math.abs(f.v - l.cocluster[chave]) < 1e-9) f.linhas.push(l); else faixas.push({ v: l.cocluster[chave], linhas: [l] });
  }
  $('#zeus').innerHTML = resumo + (lista.length
    ? '<p class="zeus-legenda">Percentage = share of the target’s tiles that fall in the same group as the place.</p>'
      + faixas.map((f) => `<div class="zeus-grupo"><div class="zeus-faixa"><b>${fmt(100 * f.v, 0)}%</b>
          <span class="barra" aria-hidden="true"><span style="width:${(100 * f.v).toFixed(1)}%"></span></span></div>
          <div class="zeus-chips">${f.linhas.map((l) => `<button type="button" class="chip${l.controle ? ' controle' : ''}" data-site="${l.site_id}"
            aria-label="${esc(l.loc.nome)}, ${fmt(100 * f.v, 0)}% of the target’s tiles${l.controle ? ', control place' : ''}">${l.controle ? ic('building-2') : ''}${esc(l.loc.nome)}${l.controle ? ' <small>control</small>' : ''}</button>`).join('')}</div></div>`).join('')
    : '<p class="nota">With this k, no place on Earth falls in the same group as the target: ZEUS sees it as unique.</p>');
  $('#zeus-qualidade').textContent = q ? `Clustering quality with k = ${E.k}: silhouette ${fmt(q.silhueta_embedding, 2)} (0 to 1, higher = better separated groups); suggested k = ${E.dados.dados.meta.k_sugerido}.` : '';
  $('#zeus').querySelectorAll('.chip').forEach((c) => c.addEventListener('click', () => selecionar(c.dataset.site)));
}

/* ---------------------------------------------------------------- clima (Marte) */
function fmtClima(v, u) {
  if (u === 'K') return `${fmt(v, 0)} K`;
  if (u === 'Pa') return `${fmt(v, 0)} Pa`;
  if (u === 'mm/day') return `${fmt(v, 2)} mm/day`;
  return fmt(v, v < 0.1 ? 3 : 2);
}
function renderClima() {
  const el = $('#clima');
  const C = E.dados.dados.clima_marte;
  if (!C) { el.innerHTML = '<p class="nota">Climate layer not computed in this data version.</p>'; return; }
  if (E.corpo !== 'MARS') {
    el.innerHTML = '<p class="nota">The climate comparison exists only for Mars (the Moon has no atmosphere). '
      + 'Choose the <strong>Mars</strong> tab in step 1 to see it.</p>';
    return;
  }
  const bloco = C.por_alvo[E.alvo];
  const linhas = linhasVisiveis().filter((l) => bloco.locais[l.site_id]);
  const porClima = [...linhas].sort((a, b) => bloco.locais[b.site_id].sim - bloco.locais[a.site_id].sim);
  const posClima = Object.fromEntries(porClima.map((l, i) => [l.site_id, i + 1]));
  const n = linhas.length;
  const sel = linhas.find((l) => l.site_id === E.site) || linhas[0];
  const c = bloco.locais[sel.site_id];
  const pc = posClima[sel.site_id];
  const terco = (p) => (p <= n / 3 ? 'alto' : p <= (2 * n) / 3 ? 'meio' : 'baixo');
  const frase = {
    'alto|alto': 'is similar to the target <strong>in terrain and also in climate</strong>: a good candidate for full tests.',
    'alto|meio': 'is similar in terrain; in climate it sits mid-list.',
    'alto|baixo': 'is similar in <strong>terrain</strong>, but among the <strong>least similar in climate</strong>: good for terrain, rock and mobility tests, not for climate tests.',
    'meio|alto': 'is among the most similar in <strong>climate</strong>, but not in terrain: useful for testing equipment in cold, dry conditions.',
    'baixo|alto': 'is a <strong>climate</strong> analog, but not a terrain one: useful for testing equipment in that environment, not terrain or rock.',
  }[`${terco(sel.pos)}|${terco(pc)}`] || 'sits mid-list or lower on both criteria.';
  const val = bloco.validacao;
  const tabela = bloco.marte ? `<details class="saiba"><summary>See the ${C.grandezas.length} compared quantities</summary><div class="tabela-wrap"><table>
      <thead><tr><th>Quantity</th><th class="num">Mars (model cell)</th><th class="num">${esc(sel.loc.nome)}</th><th class="num">Similarity</th></tr></thead><tbody>
      ${C.grandezas.map((g) => `<tr><td>${esc(g.nome)}${g.peso < 1 ? ' <small>(weight ½)</small>' : ''}</td>`
        + `<td class="num">${fmtClima(bloco.marte[g.id], g.unidade)}</td><td class="num">${fmtClima(c.terra[g.id], g.unidade)}</td>`
        + `<td class="num">${fmt(c.grandezas[g.id], 0)}</td></tr>`).join('')}
      </tbody></table></div>
      <p class="nota">Mars model cell used: ${fmt(bloco.celula[0], 0)}°, ${fmt(bloco.celula[1], 0)}° E (2° × 2°, ~120 km).
        Pressure and rain enter on a log scale.</p></details>` : '';
  const dica = E.alvo === E.corpo
    ? `<p class="dica-clima">${ic('info')}<span>Showing the average of the 6 Mars sites. <a href="#passo-1">Pick one Mars landing site in step 1</a> to see the full comparison of the ${C.grandezas.length} climate quantities.</span></p>` : '';
  el.innerHTML = `
    <p class="intro-bloco">How much the climate of each place on Earth resembles that of Mars, independent of the ranking above.</p>
    ${dica}
    <div class="clima-grade">
      <div class="cartao">
        <div class="resumo-score"><span class="grande">${fmt(c.sim, 0)}</span><span class="de">out of 100 in climate</span>
          <span class="contexto">${esc(sel.loc.nome)}: ${ord(pc)} of ${n} in climate · ${ord(sel.pos)} of ${n} in the ranking above</span></div>
        <p style="margin:var(--e-3) 0 0;color:var(--tinta)"><strong>${esc(sel.loc.nome)}</strong> ${frase}</p>
        ${tabela}
      </div>
      <div class="cartao">
        <h4 class="rotulo" style="margin:0 0 var(--e-2);font-size:var(--t-s);color:var(--branco)">Most similar in climate to ${esc(nomeAlvoAtual())}</h4>
        <ol class="mini-ranking">${porClima.slice(0, 6).map((l, i) => `<li><button type="button" data-site="${l.site_id}"
            aria-label="${ord(i + 1)} in climate: ${esc(l.loc.nome)}, ${fmt(bloco.locais[l.site_id].sim, 0)} out of 100">
            <span class="pos">${i + 1}</span><span class="nome">${esc(l.loc.nome)}</span><span class="valor">${fmt(bloco.locais[l.site_id].sim, 0)}</span>
            <span></span><span class="barra" aria-hidden="true"><span style="width:${bloco.locais[l.site_id].sim.toFixed(1)}%"></span></span></button></li>`).join('')}</ol>
        <details class="saiba"><summary>Learn more and limitations</summary>
          <p>Work by team member <strong>Luís Gustavo de Oliveira Miranda</strong>: it compares nine climate quantities
            (air and surface temperature, change over the year and between day and night, pressure, rain and dust) of each place
            on Earth with the NASA Ames Mars climate model. It is independent of the ranking above, which measures terrain, ground cover,
            surface temperature and geology${val ? ` (correlation between the two: ${fmt(val.spearman_com_score_v1_7, 2)}, i.e. almost none)` : ''}.</p>
          <p>Scale: 100 = equal in every quantity; 0 = as different as the extremes of Earth and Mars combined.
            ${val ? `It separates analogs from cities and rainforest with AUC ${fmt(val.auc_analogo_x_controle, 2)}.` : ''}</p>
          <ul class="lista">${C.avisos.map((a) => `<li>${esc(a)}</li>`).join('')}</ul>
        </details>
      </div>
    </div>`;
  el.querySelectorAll('.mini-ranking button').forEach((b) => b.addEventListener('click', () => selecionar(b.dataset.site)));
}

/* ---------------------------------------------------------------- resultados em destaque */
function topGeral(corpo, n) {
  return E.dados.similaridade.por_corpo[corpo].filter((e) => local(e.site_id).tipo !== 'controle')
    .sort((a, b) => b.score - a.score).slice(0, n).map((e) => `${local(e.site_id).nome} (${fmt(e.score, 0)})`);
}
function renderResultados() {
  const m = topGeral('MARS', 3), l = topGeral('MOON', 3);
  $('#resultado-analise').innerHTML = `${ic('arrow-right')}<span><strong>Main result:</strong> for <strong>Mars</strong>,
    ${esc(m.slice(0, 2).join(', '))} and ${esc(m[2])} lead. For the <strong>Moon</strong>, nothing comes close: the least different
    are ${esc(l.slice(0, 2).join(', '))} and ${esc(l[2])}, so the Moon calls for combining analogs by mission type.</span>`;
  const v = (t, c) => E.dados.dados.meta.validacao.find((x) => x.teste === t && x.corpo === c);
  const a = v('candidatos_vs_controles', 'MOON'), b = v('candidatos_vs_controles', 'MARS'), c = v('publicados_vs_demais', 'MOON');
  if (a && b && c) {
    $('#resultado-metodologia').innerHTML = `${ic('shield-check')}<span><strong>Validation result:</strong> the method separates
      analogs from cities and rainforest (AUC ${fmt(a.auc, 2)} on the Moon and ${fmt(b.auc, 2)} on Mars) and puts the ESA catalogue
      places on top for the Moon (AUC ${fmt(c.auc, 2)}).</span>`;
  }
}

/* ---------------------------------------------------------------- metodologia */
const NOMES_GRUPO_FONTE = { terra: 'Earth', lua: 'Moon', marte: 'Mars', ia_clima: 'AI and climate', imagens: 'Images and interface' };
const AVISOS_PRINCIPAIS = [6, 7, 1];   // viés de seleção, análogos de terreno (não mineralógicos), fontes de temperatura
function renderSobre() {
  const meta = E.dados.dados.meta;
  const v = (teste, corpo) => meta.validacao.find((x) => x.teste === teste && x.corpo === corpo);
  const tiles = [
    ['Moon', v('publicados_vs_demais', 'MOON'), 'ESA catalogue places ranked above the rest'],
    ['Mars', v('publicados_vs_demais', 'MARS'), 'ESA catalogue places ranked above the rest'],
    ['Moon', v('candidatos_vs_controles', 'MOON'), 'analogs ranked above cities and rainforest'],
    ['Mars', v('candidatos_vs_controles', 'MARS'), 'analogs ranked above cities and rainforest'],
  ].filter((t) => t[1]);
  $('#validacao').innerHTML = tiles.map(([c, x, r]) => `<div class="tile"><div class="corpo-t">${c}</div><div class="num">${fmt(x.auc, 2)}</div>`
    + `<div class="rot">${r} (AUC; p = ${fmt(x.p, 3)})</div></div>`).join('')
    + '<p class="nota" style="grid-column:1/-1;margin:0">The places on Earth were chosen by the team (selection bias).</p>';
  const principais = AVISOS_PRINCIPAIS.filter((i) => meta.avisos[i]);
  const resto = meta.avisos.filter((_, i) => !principais.includes(i));
  $('#avisos').innerHTML = principais.map((i) => `<li>${esc(meta.avisos[i])}</li>`).join('');
  $('#avisos-resto').innerHTML = resto.map((a) => `<li>${esc(a)}</li>`).join('');
  $('#avisos-mais').hidden = !resto.length;
  const grupos = {};
  for (const f of meta.fontes) (grupos[f.grupo || 'terra'] ||= []).push(f);
  $('#fontes').innerHTML = Object.keys(NOMES_GRUPO_FONTE).filter((g) => grupos[g]).map((g) => `<details class="saiba fonte-grupo" open>
      <summary>${NOMES_GRUPO_FONTE[g]} (${grupos[g].length})</summary><ul>${grupos[g].map((f) => `<li><a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.nome)}</a> — ${esc(f.uso)}`
      + (f.credito ? `. ${esc(f.credito)}` : '') + (f.licenca ? ` (${esc(f.licenca)})` : '') + '</li>').join('')}</ul></details>`).join('');
  $('#protocolo').textContent = meta.protocolo;
}

/* ---------------------------------------------------------------- equipe */
function iniciais(nome) {
  const p = nome.replace(/[’']/g, '').split(/\s+/).filter((x) => x.length > 2 || /^[A-ZÀ-Ú]/.test(x));
  return (p[0][0] + p[p.length - 1][0]).toUpperCase();
}
/* Contato com ícone. Vazio ("", ainda não informado) ou null (a pessoa não tem) não aparece para o público. */
function contato(valor, tipo, nome) {
  if (!valor) return '';
  const href = tipo === 'email' ? `mailto:${valor}` : valor;
  const [icone, rot] = { email: ['mail', `Email ${nome}: ${valor}`], lattes: ['graduation-cap', `${nome}’s Lattes CV`],
    linkedin: ['linkedin', `${nome} on LinkedIn`] }[tipo];
  return `<li><a href="${esc(href)}" target="_blank" rel="noopener" aria-label="${esc(rot)}" title="${esc(rot)}">${ic(icone)}</a></li>`;
}
async function renderEquipe() {
  let eq;
  try { eq = await (await fetch('data/equipe.json', { cache: 'no-cache' })).json(); } catch (_) { return; }
  const fotos = eq.fotos || [];
  $('#equipe-conteudo').innerHTML = `
    <div class="equipe-topo">
      <div>
        <div class="equipe-marca">
          ${eq.logo ? `<img class="logo-equipe" src="${esc(eq.logo)}" alt="Earth Dev Defense team logo" loading="lazy" width="96" height="96">` : ''}
          <h3 class="nome-equipe">Earth <span>Dev</span> Defense</h3>
        </div>
        <p>${esc(eq.descricao)}</p>
        <p class="nota">Local event: <strong>${esc(eq.evento_local)}</strong> ·
          <a href="${esc(eq.pagina_oficial)}" target="_blank" rel="noopener">official team page</a></p>
      </div>
      <div class="fotos">${fotos.slice(0, 2).map((f) => `<img src="${esc(f.arquivo)}" alt="${esc(f.legenda)}" loading="lazy" width="800" height="600">`).join('')}</div>
    </div>
    <div class="integrantes">${eq.integrantes.map((p) => {
      const cs = contato(p.email, 'email', p.nome) + contato(p.lattes, 'lattes', p.nome) + contato(p.linkedin, 'linkedin', p.nome);
      return `<article class="pessoa">
        ${p.foto ? `<img class="avatar" src="${esc(p.foto)}" alt="Photo of ${esc(p.nome)}" loading="lazy" width="72" height="72">`
          : `<span class="iniciais" aria-hidden="true">${esc(iniciais(p.nome))}</span>`}
        <div><h3>${esc(p.nome)}</h3>
          ${p.funcao ? `<p class="funcao">${esc(p.funcao)}</p>` : ''}
          ${cs ? `<ul class="contatos">${cs}</ul>` : ''}</div>
      </article>`;
    }).join('')}
    </div>`;
}

/* ---------------------------------------------------------------- navegação */
function ligarNavegacao() {
  const btn = $('.menu-btn'), menu = $('#menu');
  const fechar = () => { menu.classList.remove('aberto'); btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-label', 'Open menu');
    btn.querySelector('use').setAttribute('href', 'assets/icones.svg#i-menu'); };
  btn.addEventListener('click', () => {
    const abrir = !menu.classList.contains('aberto');
    if (!abrir) return fechar();
    menu.classList.add('aberto'); btn.setAttribute('aria-expanded', 'true'); btn.setAttribute('aria-label', 'Close menu');
    btn.querySelector('use').setAttribute('href', 'assets/icones.svg#i-x');
  });
  menu.querySelectorAll('a').forEach((a) => a.addEventListener('click', fechar));
  document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') fechar(); });

  // seção atual no menu e passo atual da análise (a última seção cujo topo passou da linha de leitura)
  const secoes = ['inicio', 'desafio', 'analise', 'metodologia', 'equipe'].map((id) => document.getElementById(id));
  const passos = [...document.querySelectorAll('.passos-nav a')].map((a) => [a, document.querySelector(a.getAttribute('href'))]);
  let pedido = false;
  const marcar = () => {
    pedido = false;
    const linha = 140;
    let atual = secoes[0];
    for (const s of secoes) if (s.getBoundingClientRect().top <= linha) atual = s;
    menu.querySelectorAll('a').forEach((a) => a.setAttribute('aria-current', String(a.getAttribute('href') === `#${atual.id}`)));
    let passoAtual = null;
    for (const [a, alvo] of passos) if (alvo && alvo.getBoundingClientRect().top <= linha + 40) passoAtual = a;
    passos.forEach(([a]) => {
      a.classList.toggle('feito', passoAtual && passos.findIndex(([x]) => x === a) < passos.findIndex(([x]) => x === passoAtual));
      if (a === passoAtual) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
    });
  };
  addEventListener('scroll', () => { if (!pedido) { pedido = true; requestAnimationFrame(marcar); } }, { passive: true });
  marcar();
}

/* ---------------------------------------------------------------- início */
function atualizar() {
  document.querySelectorAll('.aba').forEach((a) => a.setAttribute('aria-selected', String(a.dataset.corpo === E.corpo)));
  renderAlvos(); renderMissoes(); renderRanking(); renderDetalhe(false); renderGlobo(false); renderZeus(); renderClima();
}
async function iniciar() {
  ligarNavegacao();
  renderEquipe();
  let dados;
  try {
    dados = await (await fetch('data/dados_site.json', { cache: 'no-cache' })).json();
  } catch (e) {
    $('#analise').insertAdjacentHTML('beforeend', '<p class="nota">The data could not be loaded. Open the site through a web server '
      + '(e.g. <code>python -m http.server</code> inside the <code>site/</code> folder).</p>');
    return;
  }
  E.dados = { dados, locais: dados.locais, locaisPorId: Object.fromEntries(dados.locais.map((l) => [l.site_id, l])),
              similaridade: dados.similaridade,
              publicados: new Set((dados.meta.analogos_publicados || []).map((p) => `${p.site_id}|${p.corpo}`)) };
  E.k = dados.meta.k_sugerido;
  document.querySelectorAll('.aba').forEach((a) => a.addEventListener('click', () => {
    E.corpo = a.dataset.corpo; E.alvo = E.corpo; E.site = null; atualizar();
  }));
  $('#mostrar-controles').addEventListener('change', (ev) => { E.controles = ev.target.checked; atualizar(); });
  $('#k').addEventListener('input', (ev) => { E.k = Number(ev.target.value); renderZeus(); });
  renderNumeros(); renderTrio(); renderSobre(); renderResultados(); atualizar();
}
iniciar();
