import { memo, useCallback, useState } from 'react';
import { ReactFlow, Background, Controls, Handle, Position, applyNodeChanges, applyEdgeChanges, type Node, type Edge, type NodeProps, type Connection, type NodeChange, type EdgeChange } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './styles.css';
import { normalizeGraph, parseGraph, checkConnection, createHistory, removeNodes, type Graph } from './graph-model.mjs';
type Data = { label: string };
type AppNode = Node<Data, 'source'> | Node<Data, 'transform'> | Node<Data, 'sink'>;
type AppEdge = Edge;
const WorkflowNode = memo(function WorkflowNode({ data, type }: NodeProps<AppNode>) {
  return <div className="workflow-node">
    {type !== 'source' && <Handle id="in" type="target" position={Position.Left} />}
    <strong>{data.label}</strong><small>{type}</small>
    {type !== 'sink' && <Handle id="out" type="source" position={Position.Right} />}
  </div>;
});
const nodeTypes = { source: WorkflowNode, transform: WorkflowNode, sink: WorkflowNode };
const initial: Graph = { version: 1, nodes: [
  { id: 'input', type: 'source', position: { x: 60, y: 80 }, data: { label: 'Input' } },
  { id: 'output', type: 'sink', position: { x: 420, y: 80 }, data: { label: 'Output' } }
], edges: [] };
function documentOf(nodes: AppNode[], edges: AppEdge[]): Graph {
  return normalizeGraph({ version: 1,
    nodes: nodes.map(({ id, type, position, data }) => ({ id, type, position, data: { label: data.label } })),
    edges: edges.map(({ id, source, target, sourceHandle, targetHandle }) => ({ id, source, target, sourceHandle, targetHandle })) });
}
// Every node returned by the runtime parser has one of the declared discriminants.
function asNodes(graph: Graph): AppNode[] { return graph.nodes.map(n => ({ ...n })) as AppNode[]; }
export default function App() {
  const [history] = useState(() => createHistory(initial));
  const [nodes, setNodes] = useState<AppNode[]>(() => asNodes(initial));
  const [edges, setEdges] = useState<AppEdge[]>(initial.edges);
  const [text, setText] = useState('');
  const [status, setStatus] = useState('Connect Input to Output, or add a processing node.');
  const show = useCallback((g: Graph) => { setNodes(asNodes(g)); setEdges(g.edges); }, []);
  const commit = useCallback((g: Graph) => show(history.commit(g)), [history, show]);
  const onNodesChange = useCallback((changes: NodeChange<AppNode>[]) => setNodes(current => applyNodeChanges(changes, current)), []);
  const onEdgesChange = useCallback((changes: EdgeChange<AppEdge>[]) => setEdges(current => applyEdgeChanges(changes, current)), []);
  const connect = useCallback((connection: Connection) => {
    const graph = documentOf(nodes, edges);
    const result = checkConnection(graph, connection);
    if (!result.ok) { setStatus(result.message); return; }
    commit(normalizeGraph({ ...graph, edges: [...graph.edges, { ...connection, id: crypto.randomUUID() }] }));
    setStatus('Connection added.');
  }, [nodes, edges, commit]);
  const run = (action: () => void) => { try { action(); } catch (error) { setStatus(error instanceof Error ? error.message : 'Operation failed'); } };
  return <main>
    <h1>Validated workflow editor</h1>
    <nav aria-label="Graph commands">
      <button onClick={() => run(() => { const g=documentOf(nodes,edges); commit({ ...g, nodes: [...g.nodes, { id: crypto.randomUUID(), type: 'transform', position: { x: 220, y: 180 }, data: { label: 'Process' } }] }); })}>Add process</button>
      <button onClick={() => run(() => commit(removeNodes(documentOf(nodes,edges), nodes.filter(n => n.selected).map(n => n.id))))}>Delete selected nodes</button>
      <button disabled={!history.canUndo()} onClick={() => show(history.undo())}>Undo</button>
      <button disabled={!history.canRedo()} onClick={() => show(history.redo())}>Redo</button>
      <button onClick={() => run(() => { setText(JSON.stringify(documentOf(nodes,edges), null, 2)); setStatus('Document exported to the text area.'); })}>Export JSON</button>
      <button onClick={() => run(() => { commit(parseGraph(text)); setStatus('Validated document loaded.'); })}>Load JSON</button>
      <button onClick={() => connect({ source: 'input', sourceHandle: 'out', target: 'output', targetHandle: 'in' })}>Connect default nodes</button>
    </nav>
    <p role="status" aria-live="polite">{status}</p>
    <div className="canvas" aria-label="Workflow canvas">
      <ReactFlow<AppNode, AppEdge> nodes={nodes} edges={edges} nodeTypes={nodeTypes}
        onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={connect}
        isValidConnection={candidate => checkConnection(documentOf(nodes, edges), candidate).ok}
        onNodeDragStop={(_event, moved) => run(() => commit(documentOf(nodes.map(n => n.id === moved.id ? { ...n, position: moved.position } : n), edges)))}
        deleteKeyCode={null} fitView>
        <Background /><Controls />
      </ReactFlow>
    </div>
    <label htmlFor="document-json">Versioned graph JSON (maximum 2 MB)</label>
    <textarea id="document-json" rows={8} value={text} maxLength={2_000_000} onChange={event => setText(event.target.value)} />
  </main>;
}
