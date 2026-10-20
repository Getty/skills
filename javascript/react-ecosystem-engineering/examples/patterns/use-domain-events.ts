import { useEffect, useRef } from 'react';
export type DomainEvent = Readonly<{ revision: number; kind: string }>;
export type Subscribe = (listener: (event: DomainEvent) => void) => () => void;
/** Source-reviewed snippet; externally typed/installed React tests were not run. */
export function useDomainEvents(subscribe: Subscribe, onEvent: (event: DomainEvent) => void): void {
  const latest = useRef(onEvent);
  // Publish callbacks after commit, not as a render-time external side effect.
  useEffect(() => { latest.current = onEvent; }, [onEvent]);
  useEffect(() => {
    let active = true;
    const unsubscribe = subscribe(event => { if (active) latest.current(event); });
    return () => { active = false; unsubscribe(); };
  }, [subscribe]);
}
