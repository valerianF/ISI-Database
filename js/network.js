'use strict';

// ─── Config ────────────────────────────────────────────────────────────────────
// 11 colors matching network.py's color list order
const NODE_COLORS = [
  '#e03060', '#4488cc', '#44aa66', '#cc44aa', '#22cccc',
  '#4b0082', '#8b4513', '#ff8c00', '#556b2f', '#696969', '#222222'
];
const MAX_PARENTS = 11;
const MAX_NODES   = 80;
const METADATA_KEYS = new Set(['name', 'creators', 'hyperlink', 'year', 'publication', 'fieldParts']);

// ─── State ─────────────────────────────────────────────────────────────────────
let cyInstance          = null;
let filterTomSelect     = null;
let linkTomSelect       = null;
let networkFilterLabels = [];
let networkLinkIDs      = [];

// ─── Helpers ───────────────────────────────────────────────────────────────────
function binaryKeys(inst) {
  return Object.keys(inst).filter(k => !METADATA_KEYS.has(k));
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
// "TS" uses first-6-chars grouping (TS_Ele, TS_Mic, …); all others use the
// full column name as the group key.
function buildParents(linkIDs, filteredInsts) {
  const parents = new Set();
  for (const linkID of linkIDs) {
    const isTS = (linkID === 'TS');
    for (const inst of filteredInsts) {
      for (const col of binaryKeys(inst)) {
        if (col.includes(linkID)) {
          parents.add(isTS ? col.substring(0, 6) : col);
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

  // Filter installations
  const filtered = INSTALLATIONS.filter(inst =>
    filterColIDs.every(id => inst[id] === 1)
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
  const instParents = filtered.map(inst => evaluateParents(inst, parents));

  // Determine shared_parents: parent groups shared by at least 2 installations
  const sharedParents = new Set();
  for (let i = 0; i < filtered.length; i++) {
    for (let j = i + 1; j < filtered.length; j++) {
      for (const p of instParents[i]) {
        if (instParents[j].has(p)) sharedParents.add(p);
      }
    }
  }

  // Build nodes; color isolated ones (all parents unshared) like the original
  const nodes = filtered.map((inst, i) => {
    const nodeParents = instParents[i];
    let nodeColor = '#c0c0c0';
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
  for (let i = 0; i < filtered.length; i++) {
    for (let j = i + 1; j < filtered.length; j++) {
      let edgeCount = 0;
      for (const p of instParents[i]) {
        if (!instParents[j].has(p)) continue;
        const edgeId = `${filtered[i].name}\0${filtered[j].name}\0${edgeCount}`;
        edges.push({
          group: 'edges',
          data: {
            id: edgeId,
            source: filtered[i].name,
            target: filtered[j].name,
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
          'font-size': 30,
          'font-weight': 300,
          'width': 80,
          'height': 80,
          'border-width': 0,
          'border-color': '#888888',
          'text-wrap': 'wrap',
          'text-max-width': 300,
          'color': '#222222'
        }
      },
      {
        selector: 'node:selected',
        style: { 'border-color': '#000000', 'border-width': 5 }
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
        style: { 'opacity': 1, 'border-color': '#444444', 'border-width': 2.5 }
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

  const title = networkLinkIDs
    .map(id => { const opt = LINK_OPTIONS.find(o => o.value === id); return opt ? opt.label : id; })
    .join(' | ');
  renderLegend(result.parentsArray, result.colorOf, title);
}

function hideCy() {
  const cy = document.getElementById('cy');
  if (cy) cy.style.visibility = 'hidden';
  renderLegend([], {}, '');
}

// ─── Legend ────────────────────────────────────────────────────────────────────
function renderLegend(parentsArray, colorOf, title) {
  const titleEl = document.getElementById('network-legend-title');
  if (titleEl) titleEl.textContent = title || '';

  const legend = document.getElementById('network-legend');
  if (!legend) return;
  while (legend.firstChild) legend.removeChild(legend.firstChild);
  if (!parentsArray || parentsArray.length === 0) return;

  parentsArray.forEach(p => {
    const item = document.createElement('span');
    item.className = 'legend-item';
    const dot = document.createElement('span');
    dot.className = 'legend-dot';
    dot.style.backgroundColor = colorOf[p];
    item.appendChild(dot);
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
    closeAfterSelect: false,
    onChange(values) {
      networkLinkIDs = values;
      localStorage.setItem('network_linkIDs', JSON.stringify(values));
      renderNetwork();
    }
  });

  const savedLinkIDs = JSON.parse(localStorage.getItem('network_linkIDs') || '[]');
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
    closeAfterSelect: false,
    onChange(values) {
      networkFilterLabels = values;
      localStorage.setItem('network_filterLabels', JSON.stringify(values));
      renderNetwork();
    }
  });

  const savedFilterLabels = JSON.parse(localStorage.getItem('network_filterLabels') || '[]');
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
