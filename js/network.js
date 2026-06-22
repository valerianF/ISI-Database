'use strict';

// ─── Config ────────────────────────────────────────────────────────────────────
// 11 colors matching network.py's color list order
const NODE_COLORS = [
  '#e03060', '#4488cc', '#44aa66', '#cc44aa', '#22cccc',
  '#4b0082', '#8b4513', '#ff8c00', '#556b2f', '#696969', '#222222'
];
const MAX_PARENTS = 11;
const MAX_NODES   = 80;
const METADATA_KEYS = new Set(['name', 'creators', 'hyperlink', 'year', 'publication', 'fieldParts', 'naFields']);

// ─── State ─────────────────────────────────────────────────────────────────────
let cyInstance          = null;
let filterTomSelect     = null;
let linkTomSelect       = null;
let networkFilterLabels = [];
let networkLinkIDs      = [];

// ─── Theme helpers ─────────────────────────────────────────────────────────────
// THEME_DROPDOWN_COLORS and themeOfId are defined in app.js (loaded first)

function themeOfLinkID(id) {
  if (/^(IA|FT|MC)/.test(id)) return 'IN';
  if (/^(TS|SG|SP)/.test(id)) return 'SD';
  return 'AI';
}

const THEME_NAMES = {
  AI: 'Artistic Intention',
  IN: 'Interaction',
  SD: 'System Design'
};

// ─── Helpers ───────────────────────────────────────────────────────────────────
function binaryKeys(inst) {
  return Object.keys(inst).filter(k => !METADATA_KEYS.has(k));
}

// Returns true if the installation has assessable data for the given linkID.
// Returns false when all matching columns are NA (data not collected).
function hasValidDataForLink(inst, linkID) {
  if (binaryKeys(inst).some(k => k.includes(linkID))) return true;
  const naFields = inst.naFields || [];
  return !naFields.some(k => k.includes(linkID));
}

// Attempt to find a readable label for a parent group ID.
// For leaf columns (CO_Exhibition): look up in ID_LIST → LABEL_LIST.
// For TS sub-categories (TS_Ele): look up in SUNBURST SD ids → labels.
// Fall back to formatted ID string.
function parentLabel(parentID) {
  const idx = ID_LIST.indexOf(parentID);
  if (idx !== -1) return LABEL_LIST[idx].replace(/<br>/g, ' ');
  const sdIds    = SUNBURST['SD'].ids;
  const sdLabels = SUNBURST['SD'].labels;
  const sdIdx = sdIds.indexOf(parentID);
  if (sdIdx !== -1) return sdLabels[sdIdx].replace(/<br>/g, ' ');
  return parentID.replace(/_/g, ' ');
}

// ─── Core logic — mirrors network.py ──────────────────────────────────────────

// Replicate init_parents(): for each link category, find which parent groups
// are actually present among the filtered installations.
// "TS" groups columns by their 6-char intermediate sub-group (TS_Ele, TS_Mic…)
// EXCEPT for direct TS children like TS_Server which have no sub-group.
function buildParents(linkIDs, filteredInsts) {
  const parents = new Set();
  // 6-char TS intermediate nodes (e.g. TS_Ele, TS_Mic) from the sunburst hierarchy
  const tsSubgroups = new Set(
    SUNBURST['SD'].ids.filter(id => id.startsWith('TS_') && id.length === 6)
  );
  for (const linkID of linkIDs) {
    const isTS = (linkID === 'TS');
    for (const inst of filteredInsts) {
      for (const col of binaryKeys(inst)) {
        if (col.includes(linkID)) {
          if (isTS) {
            const prefix = col.substring(0, 6);
            parents.add(tsSubgroups.has(prefix) ? prefix : col);
          } else {
            parents.add(col);
          }
        }
      }
    }
  }
  return parents;
}

// Replicate evaluate_parents(): return which parent groups installation inst
// belongs to, given a set of parent group keys.
function evaluateParents(inst, parents) {
  const result = new Set();
  for (const parent of parents) {
    for (const col of binaryKeys(inst)) {
      if (col.includes(parent)) {
        result.add(parent);
        break;
      }
    }
  }
  return result;
}

// ─── Build Cytoscape elements ──────────────────────────────────────────────────
function buildElements(filterLabels, linkIDs) {
  // Map filter labels → binary column IDs
  const filterColIDs = filterLabels.map(lbl => {
    const idx = LABEL_LIST.indexOf(lbl);
    return idx !== -1 ? ID_LIST[idx] : null;
  }).filter(Boolean);

  // Filter installations — also exclude any with NA data for the link categories
  const filtered = INSTALLATIONS.filter(inst =>
    filterColIDs.every(id => inst[id] === 1) &&
    linkIDs.every(linkID => hasValidDataForLink(inst, linkID))
  );

  if (filtered.length === 0) return { error: 'No installations match the selected filter categories.' };
  if (filtered.length > MAX_NODES) return { error: `Too many installations (${filtered.length}). Add filter categories to narrow the results.` };

  // Build parent groups from actual data (mirrors init_parents)
  const parents = buildParents(linkIDs, filtered);

  if (parents.size === 0) return { error: 'None of the filtered installations have data for the selected link categories.' };
  if (parents.size > MAX_PARENTS) return { error: `Too many link sub-categories found (${parents.size}). Select fewer link categories or add more filters.` };

  const parentsArray = Array.from(parents);
  const colorOf = {};
  parentsArray.forEach((p, i) => { colorOf[p] = NODE_COLORS[i]; });

  // Evaluate which parent groups each installation belongs to
  // then discard installations with no data at all (all-zeros for all link categories)
  const allInstParents = filtered.map(inst => evaluateParents(inst, parents));
  const validPairs = filtered
    .map((inst, i) => ({ inst, p: allInstParents[i] }))
    .filter(({ p }) => p.size > 0);

  if (validPairs.length === 0) return { error: 'None of the filtered installations have data for the selected link categories.' };

  const withData = validPairs.map(({ inst }) => inst);
  const instParents = validPairs.map(({ p }) => p);

  // Determine shared_parents: parent groups shared by at least 2 installations
  const sharedParents = new Set();
  for (let i = 0; i < withData.length; i++) {
    for (let j = i + 1; j < withData.length; j++) {
      for (const p of instParents[i]) {
        if (instParents[j].has(p)) sharedParents.add(p);
      }
    }
  }

  // Build nodes; color isolated ones (all parents unshared) like the original
  const nodes = withData.map((inst, i) => {
    const nodeParents = instParents[i];
    let nodeColor = '#adadad';
    // Node gets colored if it has a parent that is NOT in sharedParents
    for (const p of nodeParents) {
      if (!sharedParents.has(p)) {
        nodeColor = colorOf[p];
        break;
      }
    }
    return {
      group: 'nodes',
      data: { id: inst.name, label: inst.name, inst, nodeColor }
    };
  });

  // Build edges: multiple per pair for each shared parent, with bezier offsets
  // (mirrors the n_p counter in network.py's edge loop)
  const edges = [];
  for (let i = 0; i < withData.length; i++) {
    for (let j = i + 1; j < withData.length; j++) {
      let edgeCount = 0;
      for (const p of instParents[i]) {
        if (!instParents[j].has(p)) continue;
        const edgeId = `${withData[i].name}\0${withData[j].name}\0${edgeCount}`;
        edges.push({
          group: 'edges',
          data: {
            id: edgeId,
            source: withData[i].name,
            target: withData[j].name,
            color: colorOf[p]
          },
          classes: `par${edgeCount}`
        });
        edgeCount++;
        if (edgeCount >= 4) break;
      }
    }
  }

  return { nodes, edges, parentsArray, colorOf };
}

// ─── Message helper ────────────────────────────────────────────────────────────
function setMessage(msg) {
  const el = document.getElementById('network-message');
  if (!el) return;
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
}

// ─── Render ────────────────────────────────────────────────────────────────────
function renderNetwork() {
  clearDetail();

  if (networkLinkIDs.length === 0) {
    setMessage('Select at least one link category to build the network.');
    hideCy();
    return;
  }

  const result = buildElements(networkFilterLabels, networkLinkIDs);

  if (result.error) {
    setMessage(result.error);
    hideCy();
    return;
  }

  setMessage('');
  const cyEl = document.getElementById('cy');
  if (cyEl) cyEl.style.visibility = 'visible';

  const { nodes, edges } = result;

  if (cyInstance) cyInstance.destroy();

  cyInstance = cytoscape({
    container: cyEl,
    elements: [...nodes, ...edges],
    style: [
      {
        selector: 'node',
        style: {
          'background-color': 'data(nodeColor)',
          'label': 'data(label)',
          'font-family': 'Roboto, sans-serif',
          'font-size': 40,
          'font-weight': 300,
          'width': 60,
          'height': 60,
          'border-width': 0,
          'text-wrap': 'wrap',
          'text-max-width': 300,
          'color': '#000000'
        }
      },
      {
        selector: 'node:selected',
        style: { 'border-color': '#0c0c0c', 'border-width': 8 }
      },
      {
        selector: 'edge',
        style: {
          'line-color': 'data(color)',
          'width': 5,
          'opacity': 0.6,
          'curve-style': 'bezier'
        }
      },
      {
        selector: 'edge.par1',
        style: {
          'curve-style': 'unbundled-bezier',
          'control-point-distances': 20,
          'control-point-weights': 0.5
        }
      },
      {
        selector: 'edge.par2',
        style: {
          'curve-style': 'unbundled-bezier',
          'control-point-distances': -20,
          'control-point-weights': 0.5
        }
      },
      {
        selector: 'edge.par3',
        style: {
          'curve-style': 'unbundled-bezier',
          'control-point-distances': 40,
          'control-point-weights': 0.5
        }
      },
      {
        selector: '.faded',
        style: { 'opacity': 0.3 }
      },
      {
        selector: 'node.highlighted',
        style: { 'opacity': 1, 'border-color': '#0c0c0c', 'border-width': 2.5 }
      },
      {
        selector: 'edge.highlighted',
        style: { 'opacity': 0.9, 'width': 7 }
      }
    ],
    layout: {
      name: 'cose',
      animate: true,
      animationDuration: 800,
      nodeDimensionsIncludeLabels: true,
      padding: 60,
      nodeRepulsion: function () { return 8192; },
      nodeOverlap: 40,
      idealEdgeLength: function () { return 100; },
      edgeElasticity: function () { return 32; },
      nestingFactor: 1.2,
      gravity: 1,
      numIter: 1000,
      initialTemp: 1000,
      coolingFactor: 0.99,
      minTemp: 1.0,
      componentSpacing: 80,
      fit: true
    }
  });

  cyInstance.on('mouseover', 'node', function (evt) {
    const n = evt.target;
    cyInstance.elements().addClass('faded');
    n.removeClass('faded').addClass('highlighted');
    n.connectedEdges().removeClass('faded').addClass('highlighted');
    n.connectedEdges().connectedNodes().removeClass('faded').addClass('highlighted');
  });

  cyInstance.on('mouseout', 'node', function () {
    cyInstance.elements().removeClass('faded highlighted');
  });

  cyInstance.on('tap', 'node', function (evt) {
    showDetail(evt.target.data('inst'));
  });
  cyInstance.on('tap', function (evt) {
    if (evt.target === cyInstance) clearDetail();
  });

  // Group link IDs by parent theme and build "Theme | Cat1 | Cat2 | ..." title
  const themeGroups = {};
  networkLinkIDs.forEach(id => {
    const theme = themeOfLinkID(id);
    if (!themeGroups[theme]) themeGroups[theme] = [];
    const opt = LINK_OPTIONS.find(o => o.value === id);
    themeGroups[theme].push(opt ? opt.label : id);
  });
  const titleParts = [];
  Object.entries(themeGroups).forEach(([theme, cats]) => {
    titleParts.push(THEME_NAMES[theme]);
    cats.forEach(c => titleParts.push(c));
  });
  renderLegend(result.parentsArray, result.colorOf, themeGroups);
}

function hideCy() {
  const cy = document.getElementById('cy');
  if (cy) cy.style.visibility = 'hidden';
  renderLegend([], {}, {});
}

// ─── Legend ────────────────────────────────────────────────────────────────────
// themeGroups: { AI: ['Category'], SD: ['Cat1', 'Cat2'] } — used for title with colored dots
function renderLegend(parentsArray, colorOf, themeGroups) {
  const titleEl = document.getElementById('network-legend-title');
  if (titleEl) {
    while (titleEl.firstChild) titleEl.removeChild(titleEl.firstChild);
    Object.entries(themeGroups).forEach(([theme, cats], i) => {
      if (i > 0) titleEl.appendChild(document.createTextNode('  '));
      const dot = document.createElement('span');
      dot.className = 'legend-dot legend-dot-title';
      dot.style.backgroundColor = THEME_DROPDOWN_COLORS[theme] || '#888';
      titleEl.appendChild(dot);
      titleEl.appendChild(document.createTextNode(' ' + THEME_NAMES[theme] + ' | ' + cats));
    });
  }

  const legend = document.getElementById('network-legend');
  if (!legend) return;
  while (legend.firstChild) legend.removeChild(legend.firstChild);
  if (!parentsArray || parentsArray.length === 0) return;

  parentsArray.forEach(p => {
    const item = document.createElement('span');
    item.className = 'legend-item';
    const bar = document.createElement('span');
    bar.className = 'legend-bar';
    bar.style.backgroundColor = colorOf[p];
    item.appendChild(bar);
    item.appendChild(document.createTextNode(parentLabel(p)));
    legend.appendChild(item);
  });
}

// ─── Detail panel ──────────────────────────────────────────────────────────────
function showDetail(inst) {
  const panel = document.getElementById('node-detail');
  if (!panel) return;
  while (panel.firstChild) panel.removeChild(panel.firstChild);

  const nameP = document.createElement('p');
  nameP.className = 'detail-name';
  const url = sanitizeUrl(inst.hyperlink);
  if (url) {
    const a = document.createElement('a');
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
    a.textContent = inst.name;
    nameP.appendChild(a);
  } else {
    nameP.textContent = inst.name;
  }
  panel.appendChild(nameP);

  [['Creators', inst.creators], ['Year', inst.year], ['Source', inst.publication]].forEach(([lbl, val]) => {
    if (!val) return;
    const p = document.createElement('p');
    p.className = 'detail-field';
    const b = document.createElement('b');
    b.textContent = lbl + ': ';
    p.appendChild(b);
    p.appendChild(document.createTextNode(val));
    panel.appendChild(p);
  });

  panel.style.display = 'block';
}

function clearDetail() {
  const panel = document.getElementById('node-detail');
  if (panel) panel.style.display = 'none';
}

// ─── Dropdowns ─────────────────────────────────────────────────────────────────
function initDropdowns() {
  const controlsContainer = document.getElementById('network-controls');
  if (!controlsContainer) return;

  // Link category group
  const linkGroup = document.createElement('div');
  linkGroup.className = 'network-control-group';

  const linkLabel = document.createElement('label');
  linkLabel.className = 'network-control-label';
  linkLabel.textContent = 'Link by category';

  const linkContainer = document.createElement('div');
  linkContainer.className = 'dropdown_container';

  const linkSelect = document.createElement('select');
  linkSelect.id = 'dropdown_link';
  linkSelect.multiple = true;
  linkSelect.placeholder = 'Select link categories';

  LINK_OPTIONS.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt.value;
    o.textContent = opt.label;
    o.setAttribute('data-theme', themeOfLinkID(opt.value));
    linkSelect.appendChild(o);
  });

  linkContainer.appendChild(linkSelect);
  linkGroup.appendChild(linkLabel);
  linkGroup.appendChild(linkContainer);
  controlsContainer.appendChild(linkGroup);

  linkTomSelect = new TomSelect('#dropdown_link', {
    plugins: ['remove_button'],
    placeholder: 'Select link categories',
    maxItems: null,
    maxOptions: false,
    closeAfterSelect: false,
    onChange(values) {
      networkLinkIDs = values;
      localStorage.setItem('network_linkIDs', JSON.stringify(values));
      renderNetwork();
    },
    render: {
      option: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || '#888';
        return `<div class="option" style="border-left:6px solid ${color};padding-left:10px">${escape(data.text)}</div>`;
      },
      item: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || '#888';
        return `<div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color};margin-right:5px;vertical-align:middle;flex-shrink:0"></span>${escape(data.text)}</div>`;
      }
    }
  });

  const rawLinkIDs = localStorage.getItem('network_linkIDs');
  const savedLinkIDs = rawLinkIDs !== null ? JSON.parse(rawLinkIDs) : ['TS'];
  if (savedLinkIDs.length) {
    linkTomSelect.setValue(savedLinkIDs, true);
    networkLinkIDs = savedLinkIDs;
  }

  // Filter group
  const filterGroup = document.createElement('div');
  filterGroup.className = 'network-control-group';

  const filterLabel = document.createElement('label');
  filterLabel.className = 'network-control-label';
  filterLabel.textContent = 'Filter installations';

  const filterContainer = document.createElement('div');
  filterContainer.className = 'dropdown_container';

  const filterSelect = document.createElement('select');
  filterSelect.id = 'dropdown_filter';
  filterSelect.multiple = true;
  filterSelect.placeholder = 'Filter installations';

  DROPDOWN_OPTIONS.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt.value;
    o.textContent = opt.label;
    o.setAttribute('data-theme', themeOfId(opt.id));
    filterSelect.appendChild(o);
  });

  filterContainer.appendChild(filterSelect);
  filterGroup.appendChild(filterLabel);
  filterGroup.appendChild(filterContainer);
  controlsContainer.appendChild(filterGroup);

  filterTomSelect = new TomSelect('#dropdown_filter', {
    plugins: ['remove_button'],
    placeholder: 'Filter installations',
    maxItems: null,
    maxOptions: false,
    closeAfterSelect: false,
    onChange(values) {
      networkFilterLabels = values;
      localStorage.setItem('network_filterLabels', JSON.stringify(values));
      renderNetwork();
    },
    render: {
      option: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || '#888';
        return `<div class="option" style="border-left:6px solid ${color};padding-left:10px">${escape(data.text)}</div>`;
      },
      item: function (data, escape) {
        const color = THEME_DROPDOWN_COLORS[data.theme] || '#888';
        return `<div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color};margin-right:5px;vertical-align:middle;flex-shrink:0"></span>${escape(data.text)}</div>`;
      }
    }
  });

  const rawFilterLabels = localStorage.getItem('network_filterLabels');
  const savedFilterLabels = rawFilterLabels !== null ? JSON.parse(rawFilterLabels) : ['Semi-Permanent'];
  if (savedFilterLabels.length) {
    filterTomSelect.setValue(savedFilterLabels, true);
    networkFilterLabels = savedFilterLabels;
  }
}

// ─── Init (called by app.js after DOM is ready) ────────────────────────────────
function initNetworkPage() {
  initDropdowns();
  if (networkLinkIDs.length === 0) {
    setMessage('Select at least one link category to build the network.');
    hideCy();
  }
}
