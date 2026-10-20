/** Original, deliberately small DAG model. No React or third-party dependency. */
export const LIMITS = Object.freeze({ bytes: 2_000_000, nodes: 2000, edges: 5000, label: 120 });
const ID = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;
const PORTS = Object.freeze({ source: { input: false, output: true }, transform: { input: true, output: true }, sink: { input: true, output: false } });
export class GraphError extends Error {
  constructor(code, message) { super(message); this.name = 'GraphError'; this.code = code; }
}
function fail(code, message) { throw new GraphError(code, message); }
function object(value, fields, description) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || ![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail('shape', `${description} must be a plain object`);
  const keys = Object.keys(value);
  if (keys.length !== fields.length || keys.some(k => !fields.includes(k))) fail('fields', `${description} has missing or unknown fields`);
}
function id(value) { if (typeof value !== 'string' || !ID.test(value)) fail('id', 'Invalid identifier'); return value; }
function position(value) {
  object(value, ['x', 'y'], 'Position');
  for (const axis of ['x', 'y']) if (typeof value[axis] !== 'number' || !Number.isFinite(value[axis]) || Math.abs(value[axis]) > 1e7) fail('position', 'Coordinates must be finite and bounded');
  return { x: value.x, y: value.y };
}
function edgeProblem(nodes, edge) {
  const source = nodes.get(edge.source), target = nodes.get(edge.target);
  if (!source || !target) return ['endpoint', 'Connection references a missing node'];
  if (source.id === target.id) return ['self', 'Self connections are not permitted'];
  if (!PORTS[source.type].output || edge.sourceHandle !== 'out') return ['source_port', 'Source must have the out port'];
  if (!PORTS[target.type].input || edge.targetHandle !== 'in') return ['target_port', 'Target must have the in port'];
  return null;
}
function validateEdges(nodes, edges) {
  const nodeMap = new Map(nodes.map(n => [n.id, n]));
  const occupied = new Set(), tuples = new Set(), edgeIds = new Set();
  const outgoing = new Map(nodes.map(n => [n.id, []]));
  const indegree = new Map(nodes.map(n => [n.id, 0]));
  for (const edge of edges) {
    if (edgeIds.has(edge.id)) fail('duplicate_edge_id', 'Duplicate edge identifier');
    edgeIds.add(edge.id);
    const problem = edgeProblem(nodeMap, edge); if (problem) fail(...problem);
    const tuple = JSON.stringify([edge.source, edge.sourceHandle, edge.target, edge.targetHandle]);
    if (tuples.has(tuple)) fail('duplicate_connection', 'Duplicate connection');
    tuples.add(tuple);
    const input = JSON.stringify([edge.target, edge.targetHandle]);
    if (occupied.has(input)) fail('cardinality', 'Each input accepts one connection');
    occupied.add(input);
    outgoing.get(edge.source).push(edge.target);
    indegree.set(edge.target, indegree.get(edge.target) + 1);
  }
  const queue = nodes.filter(n => indegree.get(n.id) === 0).map(n => n.id);
  let visited = 0;
  for (let i = 0; i < queue.length; i++) {
    visited++;
    for (const target of outgoing.get(queue[i])) {
      indegree.set(target, indegree.get(target) - 1);
      if (indegree.get(target) === 0) queue.push(target);
    }
  }
  if (visited !== nodes.length) fail('cycle', 'This document requires an acyclic graph');
}
/** Parse untrusted object data into a new canonical, serializable graph. */
export function normalizeGraph(value) {
  object(value, ['version', 'nodes', 'edges'], 'Graph');
  if (value.version !== 1) fail('version', 'Unsupported graph version');
  if (!Array.isArray(value.nodes) || !Array.isArray(value.edges)) fail('shape', 'Nodes and edges must be arrays');
  if (value.nodes.length > LIMITS.nodes || value.edges.length > LIMITS.edges) fail('size', 'Graph exceeds supported size');
  const ids = new Set();
  const nodes = value.nodes.map(n => {
    object(n, ['id', 'type', 'position', 'data'], 'Node');
    const nodeId = id(n.id);
    if (ids.has(nodeId)) fail('duplicate_node_id', 'Duplicate node identifier');
    ids.add(nodeId);
    if (typeof n.type !== 'string' || !Object.hasOwn(PORTS, n.type)) fail('node_type', 'Unknown node type');
    object(n.data, ['label'], 'Node data');
    if (typeof n.data.label !== 'string' || !n.data.label.trim() || (n.data.label.length > LIMITS.label * 2 || [...n.data.label].length > LIMITS.label)) fail('label', 'Label must be nonempty and bounded');
    return { id: nodeId, type: n.type, position: position(n.position), data: { label: n.data.label } };
  });
  const edges = value.edges.map(e => {
    object(e, ['id', 'source', 'target', 'sourceHandle', 'targetHandle'], 'Edge');
    return { id: id(e.id), source: id(e.source), target: id(e.target), sourceHandle: id(e.sourceHandle), targetHandle: id(e.targetHandle) };
  });
  validateEdges(nodes, edges);
  return { version: 1, nodes, edges };
}
export function parseGraph(text) {
  if (typeof text !== 'string') fail('shape', 'Import must be text');
  if (text.length > LIMITS.bytes || new TextEncoder().encode(text).byteLength > LIMITS.bytes) fail('size', 'Import is too large');
  let value;
  try { value = JSON.parse(text); } catch { fail('json', 'Import is not valid JSON'); }
  return normalizeGraph(value);
}
/** Current document must be canonical; result is still defensive about caller data. */
export function checkConnection(graph, candidate, replaceEdgeId = undefined) {
  try {
    const current = normalizeGraph(graph);
    if (!candidate || typeof candidate !== 'object') fail('shape', 'Connection must be an object');
    if (replaceEdgeId !== undefined && !current.edges.some(e => e.id === replaceEdgeId)) fail('replacement', 'Replacement edge does not exist');
    const edges = current.edges.filter(e => e.id !== replaceEdgeId);
    const used = new Set(edges.map(e => e.id));
    let suffix = 0; let candidateId = `candidate_${suffix}`; while (used.has(candidateId)) candidateId = `candidate_${++suffix}`;
    const edge = { id: candidateId, source: candidate.source, target: candidate.target, sourceHandle: candidate.sourceHandle, targetHandle: candidate.targetHandle };
    normalizeGraph({ ...current, edges: [...edges, edge] });
    return { ok: true };
  } catch (error) {
    return { ok: false, code: error instanceof GraphError ? error.code : 'invalid', message: error instanceof GraphError ? error.message : 'Invalid connection' };
  }
}
export function removeNodes(graph, nodeIds) {
  const current = normalizeGraph(graph);
  if (!Array.isArray(nodeIds) || nodeIds.length > LIMITS.nodes || nodeIds.some(v => typeof v !== 'string')) fail('shape', 'Invalid deletion set');
  const removed = new Set(nodeIds);
  return normalizeGraph({ ...current, nodes: current.nodes.filter(n => !removed.has(n.id)), edges: current.edges.filter(e => !removed.has(e.source) && !removed.has(e.target)) });
}
function freezeGraph(graph) {
  for (const n of graph.nodes) { Object.freeze(n.position); Object.freeze(n.data); Object.freeze(n); }
  graph.edges.forEach(Object.freeze); Object.freeze(graph.nodes); Object.freeze(graph.edges); return Object.freeze(graph);
}
/** Snapshot history for one local document; NOT a collaborative undo algorithm. */
export function createHistory(initial, limit = 50) {
  if (!Number.isInteger(limit) || limit < 2 || limit > 500) fail('history_limit', 'History limit must be 2..500');
  let entries = [freezeGraph(normalizeGraph(initial))], index = 0;
  const current = () => normalizeGraph(entries[index]);
  return Object.freeze({
    current,
    commit(next) {
      const canonical = normalizeGraph(next);
      if (JSON.stringify(canonical) === JSON.stringify(entries[index])) return current();
      entries = entries.slice(0, index + 1);
      entries.push(freezeGraph(canonical));
      if (entries.length > limit) entries.shift();
      index = entries.length - 1; return current();
    },
    undo() { if (index > 0) index--; return current(); },
    redo() { if (index + 1 < entries.length) index++; return current(); },
    canUndo() { return index > 0; },
    canRedo() { return index + 1 < entries.length; },
    size() { return entries.length; }
  });
}
