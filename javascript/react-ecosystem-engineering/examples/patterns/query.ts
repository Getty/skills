import { useQuery } from '@tanstack/react-query';
type Item = Readonly<{ id: string; label: string }>;
function parseItems(value: unknown): Item[] {
  if (!Array.isArray(value) || value.length > 1000) throw new Error('Invalid item response');
  return value.map(row => {
    if (!row || typeof row !== 'object' || typeof row.id !== 'string' || typeof row.label !== 'string' || row.id.length > 100 || row.label.length > 500) throw new Error('Invalid item');
    return { id: row.id, label: row.label };
  });
}
/** TanStack Query integration sketch: verify the installed major and provider first. */
export function useItems(tenantId: string) {
  return useQuery({
    queryKey: ['tenant', tenantId, 'items'],
    enabled: tenantId.length > 0,
    queryFn: async ({ signal }) => {
      const response = await fetch(`/api/tenants/${encodeURIComponent(tenantId)}/items`, { signal });
      if (!response.ok) throw new Error(`Request failed (${response.status})`);
      // The service/proxy must additionally enforce a transport-level response-byte limit.
      return parseItems(await response.json());
    },
    staleTime: 30_000,
    retry: false
  });
}
