export type GraphNode = { id: string; type: 'source' | 'transform' | 'sink'; position: { x: number; y: number }; data: { label: string } };
export type GraphEdge = { id: string; source: string; target: string; sourceHandle: string; targetHandle: string };
export type Graph = { version: 1; nodes: GraphNode[]; edges: GraphEdge[] };
export declare const LIMITS: Readonly<{ bytes: number; nodes: number; edges: number; label: number }>;
export declare class GraphError extends Error { readonly code: string; constructor(code: string, message: string); }
export declare function normalizeGraph(value: unknown): Graph;
export declare function parseGraph(text: string): Graph;
export declare function checkConnection(graph: unknown, candidate: unknown, replaceEdgeId?: string): { ok: true } | { ok: false; code: string; message: string };
export declare function removeNodes(graph: unknown, nodeIds: string[]): Graph;
export declare function createHistory(initial: unknown, limit?: number): Readonly<{ current(): Graph; commit(next: unknown): Graph; undo(): Graph; redo(): Graph; canUndo(): boolean; canRedo(): boolean; size(): number }>;
