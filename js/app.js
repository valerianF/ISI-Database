'use strict';

// ─── State ────────────────────────────────────────────────────────────────────
let currentPlotType = 'AI';
let tomSelectInstance = null;
let selectedLabels = [];
let sunburstEventsAttached = false;

// ─── Theme maps ───────────────────────────────────────────────────────────────
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

function buildCredits() {
  const div = document.createElement('div');

  const spacer = document.createElement('p');
  spacer.style.paddingBottom = '2cm';
  div.appendChild(spacer);

  const credits = document.createElement('p');
  credits.className = 'credits';

  const parts = [
    ['✍ Created by ', null],
    ['Valérian Fraisse',    'https://www.mcgill.ca/music/valerian-fraisse'],
    [' with the support of ', null],
    ['Catherine Guastavino', 'https://www.mcgill.ca/sis/people/faculty/guastavino'],
    [' and ', null],
    ['Marcelo Wanderley',   'https://www.mcgill.ca/music/marcelo-m-wanderley'],
    ['. Designed by ', null],
    ['Camille Magnan',      'http://camillemagnan.com/'],
    ['.', null]
  ];
  parts.forEach(([text, href]) => {
    if (href) {
      const a = document.createElement('a');
      a.href = href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'link_credits';
      a.textContent = text;
      credits.appendChild(a);
    } else {
      credits.appendChild(document.createTextNode(text));
    }
  });
  div.appendChild(credits);

  const license = document.createElement('p');
  license.style.cssText =
    'color:#AEAEAE;padding-bottom:1cm;padding-left:1cm;font-weight:500;font-size:10pt';
  license.textContent =
    'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.';
  div.appendChild(license);

  return div;
}

// ─── Results rendering ────────────────────────────────────────────────────────
function renderResults() {
  const container = document.getElementById('list_inst');
  if (!container) return;
  container.innerHTML = '';

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
    select.appendChild(option);
  });

  tomSelectInstance = new TomSelect('#dropdown_cat', {
    plugins: ['remove_button'],
    placeholder: 'Select one or more categories',
    maxItems: null,
    closeAfterSelect: false,
    onChange(values) {
      // Validate every value from the dropdown — fixes vuln #2
      selectedLabels = values.filter(v => validateLabel(v));
      localStorage.setItem('selectedLabels', JSON.stringify(selectedLabels));
      renderResults();
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
}

document.addEventListener('DOMContentLoaded', function () {
  if (document.getElementById('sunburst')) initMainPage();
  if (document.getElementById('installations-table')) renderInstallationsTable();
});
