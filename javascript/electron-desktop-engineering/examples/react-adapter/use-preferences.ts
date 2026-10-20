import { useEffect, useState } from 'react';
import type {} from './desktop.js';
// Integration sketch. Include desktop.d.ts through tsconfig; no runtime import is required.
type Preferences = Readonly<{ theme: 'system' | 'light' | 'dark'; revision: number }>;
export function usePreferences() {
  const [value, setValue] = useState<Preferences | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const bridge = window.desktop;
    if (!bridge) { setError('Desktop bridge unavailable'); return; }
    let active = true;
    const apply = (next: Preferences) => {
      if (active) setValue(current => !current || next.revision >= current.revision ? next : current);
    };
    const unsubscribe = bridge.onPreferencesChanged(apply);
    bridge.getPreferences().then(apply).catch(() => { if (active) setError('Preferences unavailable'); });
    return () => { active = false; unsubscribe(); };
  }, []);
  return { value, error };
}
