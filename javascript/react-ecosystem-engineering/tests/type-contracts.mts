import { normalizeGraph, checkConnection, createHistory, type Graph, type GraphNode } from '../examples/flow-editor/src/graph-model.mjs';
const node: GraphNode = { id: 'a', type: 'source', position: { x: 0, y: 0 }, data: { label: 'A' } };
const graph: Graph = { version: 1, nodes: [node], edges: [] };
const canonical: Graph = normalizeGraph(graph);
const result = checkConnection(canonical, {});
if (!result.ok) { const code: string = result.code; void code; }
createHistory(graph).commit(graph);
// @ts-expect-error Unknown node kinds are not supported by this domain schema.
const invalidNode: GraphNode = { ...node, type: 'shell' };
// @ts-expect-error Only the current schema version is accepted in the typed contract.
const future: Graph = { ...graph, version: 2 };
void invalidNode; void future;
