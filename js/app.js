'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let currentPlotType = 'AI';
let tomSelectInstance = null;
let selectedLabels = [];
let sunburstEventsAttached = false;
let networkReady = false;

// ─── Theme maps ───────────────────────────────────────────────────────────────

// Lighter (midpoint) versions of glossary theme colors, for dropdown coloring
const THEME_DROPDOWN_COLORS = { AI: '#C95E7B', IN: '#8BBFDD', SD: '#6FBA72' };

// Returns 'AI', 'IN', or 'SD' for a DROPDOWN_OPTIONS id (e.g. "CO_Exhibition")
function themeOfId(id) {
  if (/^(IA|IDof|ODof|FT|MC|IT)/.test(id)) return 'IN';
  if (/^(TS|SP|SG)/.test(id)) return 'SD';
  return 'AI';
}

const BG_COLORS = {
  AI: 'linear-gradient(0deg, rgba(156,36,87,1) 0%, rgba(112,23,69,1) 100%)',
  IN: 'linear-gradient(0deg, rgba(24,82,164,1) 0%, rgba(6,48,107,1) 100%)',
  SD: 'linear-gradient(0deg, rgba(0,96,39,1) 0%, rgba(0,66,26,1) 100%)'
};

const COLOR_SCALE_AI = [
  [0, '#FFFFFF'],
  [0.5, '#C95E7B'],
  [1, '#671F44']
];

const COLOR_SCALE_IN = [
  [0, '#FFFFFF'],
  [0.5, '#8BBFDD'],
  [1, '#08306B']
];

const COLOR_SCALE_SD = [
  [0, '#FFFFFF'],
  [0.5, '#7BC77C'],
  [1, '#00441B']
];

const COLOR_SCALES   = { AI: COLOR_SCALE_AI,  IN: COLOR_SCALE_IN, SD: COLOR_SCALE_SD };
// Blues and Greens are defined light→dark in Plotly.js; Burg is dark→light.
// reversescale flips Blues/Greens so that high log values map to the dark end.
// const REVERSE_SCALE  = { AI: false,  IN: true,    SD: true };

// ─── Security helpers ─────────────────────────────────────────────────────────

// Whitelist-only URL sanitizer — fixes vuln #1 (unvalidated href from CSV data)
function sanitizeUrl(raw) {
  const s = (raw || '').trim();
  if (!s) return null;
  if (/^10\./i.test(s))       return 'https://doi.org/' + s;
  if (/^doi:\s*/i.test(s))    return 'https://doi.org/' + s.replace(/^doi:\s*/i, '').trim();
  if (/^DOI:\s*/i.test(s))    return 'https://doi.org/' + s.replace(/^DOI:\s*/i, '').trim();
  if (/^https?:\/\//i.test(s)) return s;
  return null; // reject everything else (javascript:, data:, etc.)
}

// Validate a label against the known list — fixes vuln #2 (unsanitized clickData)
function validateLabel(label) {
  return (typeof label === 'string' && LABEL_LIST.includes(label)) ? label : null;
}

// ─── Filtering ────────────────────────────────────────────────────────────────
function filterInstallations(labels) {
  if (!labels.length) return [];

  const sectionIDs = labels.map(lbl => {
    const valid = validateLabel(lbl);
    if (!valid) return null;
    const idx = LABEL_LIST.indexOf(valid);
    return idx !== -1 ? ID_LIST[idx] : valid;
  }).filter(Boolean);

  if (!sectionIDs.length) return [];

  return INSTALLATIONS.filter(inst =>
    sectionIDs.every(id =>
      inst[id] === 1 ||
      (Array.isArray(inst.fieldParts) && inst.fieldParts.includes(id))
    )
  );
}

// ─── Safe DOM builders — never use innerHTML with data-origin strings ─────────
function makeRow(inst) {
  const tr = document.createElement('tr');

  // Name column — link to source (vuln #1 fixed: sanitizeUrl rejects non-http/doi)
  const tdName = document.createElement('td');
  const url = sanitizeUrl(inst.hyperlink);
  if (url) {
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.className = 'link_list';
    a.textContent = inst.name;
    tdName.appendChild(a);
  } else {
    tdName.textContent = inst.name;
  }

  const tdCreators = document.createElement('td');
  tdCreators.textContent = inst.creators;

  const tdYear = document.createElement('td');
  tdYear.textContent = inst.year;

  const tdSource = document.createElement('td');
  tdSource.textContent = inst.publication;

  tr.append(tdName, tdCreators, tdYear, tdSource);
  return tr;
}

// Shared credit data
const CREDIT_PARTS = [
  ['✍ Created by ', null],
  ['Valérian Fraisse',    'https://github.com/valerianF/ISI-Database'],
  [' with the support of ', null],
  ['Catherine Guastavino', 'https://www.mcgill.ca/sis/people/faculty/guastavino'],
  [' and ', null],
  ['Marcelo Wanderley',   'https://www.mcgill.ca/music/marcelo-m-wanderley'],
  [' with contributions from ', null],
  ['Clémentine Berger',      'https://github.com/ClementineBerger'],
  ['. Designed by ', null],
  ['Camille Magnan',      'http://camillemagnan.com/'],
  ['.', null]
];
const LICENSE_TEXT = 'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.';

function buildCreditsLinks(className = 'link_credits') {
  const p = document.createElement('p');
  CREDIT_PARTS.forEach(([text, href]) => {
    if (href) {
      const a = document.createElement('a');
      a.href = href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = className;
      a.textContent = text;
      p.appendChild(a);
    } else {
      p.appendChild(document.createTextNode(text));
    }
  });
  return p;
}

function buildCreditsHome() {
  const div = document.createElement('div');
  div.className = 'credits_home';
  div.appendChild(buildCreditsLinks('link_credits'));
  const licenseP = document.createElement('p');
  licenseP.className = 'license_text';
  licenseP.textContent = LICENSE_TEXT;
  div.appendChild(licenseP);
  return div;
}

function buildCredits() {
  const div = document.createElement('div');
  div.className = 'credits_block';
  div.appendChild(buildCreditsLinks('link_credits'));
  const license = document.createElement('p');
  license.className = 'license_text';
  license.textContent = LICENSE_TEXT;
  div.appendChild(license);
  return div;
}

function initCredits() {
  const homeContainer = document.querySelector('.credits_home');
  if (homeContainer && homeContainer.children.length === 0) {
    const credits = buildCreditsHome();
    homeContainer.parentElement.replaceChild(credits, homeContainer);
  }

  const creditsContainer = document.getElementById('credits-container');
  if (creditsContainer) {
    creditsContainer.appendChild(buildCredits());
  }
}

// ─── Credits home visibility ──────────────────────────────────────────────────
function syncCreditsHome() {
  const el = document.querySelector('.credits_home');
  if (!el) return;
  el.style.display = selectedLabels.length > 0 ? 'none' : '';
}

// ─── Results rendering ────────────────────────────────────────────────────────
function renderResults() {
  const container = document.getElementById('list_inst');
  if (!container) return;
  container.innerHTML = '';
  syncCreditsHome();

  if (!selectedLabels.length) return;

  const results = filterInstallations(selectedLabels);

  const countP = document.createElement('p');
  countP.className = 'n_results';
  countP.textContent = results.length + ' results';
  container.appendChild(countP);

  const table = document.createElement('table');
  const headerRow = document.createElement('tr');
  ['Name', 'Creator(s)', 'Year', 'Source'].forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);
  results.forEach(inst => table.appendChild(makeRow(inst)));
  container.appendChild(table);

  container.appendChild(buildCredits());
}

// ─── Full installations table (list.html) ─────────────────────────────────────
function renderInstallationsTable() {
  const container = document.getElementById('installations-table');
  if (!container) return;

  const countP = document.createElement('p');
  countP.className = 'n_results_page';
  countP.textContent = INSTALLATIONS.length + ' Installations';
  container.appendChild(countP);

  const table = document.createElement('table');
  const headerRow = document.createElement('tr');
  ['Name', 'Creator(s)', 'Year', 'Source'].forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);
  INSTALLATIONS.forEach(inst => table.appendChild(makeRow(inst)));
  container.appendChild(table);
}

// ─── Sunburst ─────────────────────────────────────────────────────────────────
function renderSunburst(type) {
  const el = document.getElementById('sunburst');
  if (!el) return;

  const data = SUNBURST[type];
  const logValues = data.values.map(v => Math.log(Math.max(v, 1)));

  const trace = {
    type: 'sunburst',
    ids: data.ids,
    labels: data.labels,
    parents: data.parents,
    values: data.values,
    branchvalues: 'total',
    hoverinfo: 'skip',
    maxdepth: 3,
    name: '',
    marker: {
      colors: logValues,
      colorscale: COLOR_SCALES[type],
      // autocolorscale: true,
      line: { color: 'white', width: 1.2 }
    }
  };

  const layout = {
    margin: { t: 0, l: 50, r: 0, b: 0 },
    font: { family: 'Roboto', size: 16, weight: 300 },
    autosize: true,
    height: 600,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'white'
  };

  const config = { responsive: true, displayModeBar: false };

  const plotPromise = el._hasPlotly
    ? Plotly.react(el, [trace], layout, config)
    : Plotly.newPlot(el, [trace], layout, config);
  plotPromise.then(() => {
    el._hasPlotly = true;
    if (!sunburstEventsAttached) {
      sunburstEventsAttached = true;
      el.on('plotly_click', handleSunburstClick);
    }
  });
}

// Parent nodes have ID length ≤ 6 (e.g. "AI", "CO", "SyD", "TS_Ele")
function isParentNode(id) {
  return typeof id === 'string' && id.length <= 6;
}

function handleSunburstClick(eventData) {
  if (!eventData || !eventData.points.length) return;
  const pt = eventData.points[0];
  if (isParentNode(pt.id)) return;

  // Validate label before using it — fixes vuln #2
  const label = validateLabel(pt.label);
  if (!label) return;

  if (!selectedLabels.includes(label)) {
    selectedLabels.push(label);
    localStorage.setItem('selectedLabels', JSON.stringify(selectedLabels));
    if (tomSelectInstance) {
      tomSelectInstance.addItem(label, true); // silent — won't re-trigger onChange
    }
  }
  renderResults();
}

// ─── Background ───────────────────────────────────────────────────────────────
function updateBackground(type) {
  const el = document.getElementById('page_content');
  if (el) el.style.background = BG_COLORS[type];
}

// ─── Dropdown ─────────────────────────────────────────────────────────────────
function initDropdown() {
  const select = document.getElementById('dropdown_cat');
  if (!select) return;

  DROPDOWN_OPTIONS.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.label;
    option.setAttribute('data-theme', themeOfId(opt.id));
    select.appendChild(option);
  });

  tomSelectInstance = new TomSelect('#dropdown_cat', {
    plugins: ['remove_button'],
    placeholder: 'Select one or more categories',
    maxItems: null,
    maxOptions: false,
    closeAfterSelect: false,
    onChange(values) {
      // Validate every value from the dropdown — fixes vuln #2
      selectedLabels = values.filter(v => validateLabel(v));
      localStorage.setItem('selectedLabels', JSON.stringify(selectedLabels));
      renderResults();
    },
    render: {
      option: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || 'white';
        return `<div class="option" style="border-left:6px solid ${color};padding-left:10px">${escape(data.text)}</div>`;
      },
      item: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || 'white';
        return `<div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color};margin-right:5px;vertical-align:middle;flex-shrink:0"></span>${escape(data.text)}</div>`;
      }
    }
  });

  // Restore saved selections after Tom Select is initialized
  const savedLabels = localStorage.getItem('selectedLabels');
  if (savedLabels) {
    try {
      const restored = JSON.parse(savedLabels);
      if (Array.isArray(restored)) {
        selectedLabels = restored;
        tomSelectInstance.setValue(restored);
      }
    } catch (e) {
      // Ignore parse errors
    }
  }
}

// ─── Radio buttons ────────────────────────────────────────────────────────────
function initRadioButtons() {
  document.querySelectorAll('input[name="select_plot"]').forEach(radio => {
    radio.addEventListener('change', function () {
      currentPlotType = this.value;
      localStorage.setItem('selectedPlotType', currentPlotType);
      const container = document.getElementById('list_inst');
      if (container) container.innerHTML = '';
      renderSunburst(currentPlotType);
      updateBackground(currentPlotType);
      if (selectedLabels.length) renderResults();
    });
  });
}

// ─── Chart view switcher ──────────────────────────────────────────────────────
function applyNetworkLayout() {
  const pageContent = document.getElementById('page_content');
  const sunburstSection = document.getElementById('sunburst-section');
  const networkSection = document.getElementById('network-section');
  const listInst = document.getElementById('list_inst');
  const creditsHome = document.querySelector('.credits_home');

  if (sunburstSection) sunburstSection.style.display = 'none';
  if (listInst) listInst.style.display = 'none';
  if (creditsHome) creditsHome.style.display = 'none';
  if (networkSection) networkSection.style.display = '';
  if (pageContent) {
    pageContent.classList.add('network-active');
    pageContent.style.background = '#F6F6F6';
  }
}

function applySunburstLayout() {
  const pageContent = document.getElementById('page_content');
  const sunburstSection = document.getElementById('sunburst-section');
  const networkSection = document.getElementById('network-section');
  const listInst = document.getElementById('list_inst');
  const creditsHome = document.querySelector('.credits_home');

  if (networkSection) networkSection.style.display = 'none';
  if (sunburstSection) sunburstSection.style.display = '';
  if (listInst) listInst.style.display = '';
  if (pageContent) pageContent.classList.remove('network-active');
  updateBackground(currentPlotType);
  syncCreditsHome();
}

function initChartSwitcher() {
  if (!document.getElementById('network-section')) return;

  const savedView = localStorage.getItem('chartView') || 'sunburst';
  const viewRadio = document.getElementById('view-' + savedView);
  if (viewRadio) viewRadio.checked = true;
  if (savedView === 'network') applyNetworkLayout();

  document.querySelectorAll('input[name="chart_view"]').forEach(radio => {
    radio.addEventListener('change', function () {
      localStorage.setItem('chartView', this.value);
      if (this.value === 'network') {
        applyNetworkLayout();
        if (!networkReady && typeof renderNetwork === 'function') {
          networkReady = true;
          renderNetwork();
        }
      } else {
        applySunburstLayout();
      }
    });
  });
}

// ─── Entry points ─────────────────────────────────────────────────────────────
function initMainPage() {
  const savedPlotType = localStorage.getItem('selectedPlotType');
  if (savedPlotType && ['AI', 'IN', 'SD'].includes(savedPlotType)) {
    currentPlotType = savedPlotType;
    document.querySelector(`input[name="select_plot"][value="${currentPlotType}"]`).checked = true;
  }
  renderSunburst(currentPlotType);
  updateBackground(currentPlotType);
  initDropdown();
  initRadioButtons();
  initChartSwitcher();
}

document.addEventListener('DOMContentLoaded', function () {
  initCredits();
  if (document.getElementById('sunburst')) {
    initMainPage();
    if (typeof initNetworkPage === 'function') {
      initNetworkPage();
      if (localStorage.getItem('chartView') === 'network') {
        networkReady = true;
        if (typeof renderNetwork === 'function') renderNetwork();
      }
    }
  }
  if (document.getElementById('installations-table')) renderInstallationsTable();
});
