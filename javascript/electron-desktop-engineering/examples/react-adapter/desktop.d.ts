export {};
type Theme = 'system' | 'light' | 'dark';
type Preferences = Readonly<{ theme: Theme; revision: number }>;
declare global {
  interface Window {
    desktop?: Readonly<{
      getPreferences(): Promise<Preferences>;
      setTheme(theme: Theme): Promise<Preferences>;
      openDocumentation(): Promise<void>;
      onPreferencesChanged(listener: (value: Preferences) => void): () => void;
    }>;
  }
}
