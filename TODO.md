# TODO — Übergabe

## Update 18. August 2026 (spätere Session): Claude-Setup + Restructure

- **Gruppen liegen jetzt unter `skills/`** (`git mv`, Inodes erhalten — Link-Count
  stichprobenartig verifiziert). Das ist der Zielzustand aus Punkt 2 unten; drei der
  vier registrierten Sources (`~/dev/skills/skills/{perl,k8s,tools}`) lösen dadurch
  wieder auf. `dbio` fehlt weiterhin (eigene Quelle geplant, siehe unten).
- **Neue Gruppe `skills/skills/`** (skills über skills): `skill-authoring` (neu),
  `skill-compressor` (überarbeitet aus ~/tmp), `getty-skill-library` (neu),
  `getty-agent-team` (aus ~/tmp `setup-agent-team`, umbenannt + Referenzen aktualisiert),
  Ursprünglich hier: `claude-headless`, jetzt in eigener Gruppe (nächster Punkt).
- **Neue Gruppe `skills/development/`**: `feedback-loop-debugging` (aus
  `p5-www-forgejo/.claude/skills/diagnose` übernommen, Frontmatter umgeschrieben —
  description als Trigger statt Workflow-Summary, Heading umbenannt).
- **Neue Gruppe `skills/claude/`**: `claude-headless` (claude ruft claude, Fakten gegen
  claude 2.1.234 verifiziert) und `model-routing` (Task-/Rollen-Einsortierung auf
  Fable/Opus/Sonnet/Haiku, inkl. Agenten-Bauer-Perspektive; Modell-Leiter ist als
  Cache 2026-08 markiert).
- **Neue Gruppe `skills/software/`**: `getty-create-software` (Rewrite aus ~/tmp).
- **`skills/perl/getty-perl-distribution`** (aus ~/tmp `create-perl-distribution`,
  umbenannt; Perl-Templates jetzt selbst-enthalten unter `templates/`).
- **CLAUDE.md** (Inode-Regel!), **`.claude/skills/`** mit relativen Symlinks auf die
  Repo-Dateien, **Plugin-Manifeste** (`.claude-plugin/`, `.codex-plugin/`) via
  `manage-skills package`, README-Kette aktualisiert.
- **Gruppe `tools/` aufgelöst** → `skills/system-and-network-administration/`
  (`getty-rex` per `git mv` umgezogen, Inode erhalten). Die Sources-Config wurde
  zwischenzeitlich extern auf **eine** Root-Quelle (`~/dev/skills`) umgestellt und
  löst alle 21 Skills auf — Punkt 2/3 unten sind damit offenbar erledigt; nur das
  Label habe ich auf "(grouped)" ohne Gruppen-Aufzählung gekürzt.
- **Gruppe `k8s/` aufgelöst** → `kubernetes-concepts` liegt jetzt in
  `system-and-network-administration/`, dazu neu: `kubernetes-cilium-concepts`
  (generisch extrahiert aus `kubernetes-ocp/.claude/skills/cilium`, das dort als
  Site-Skill bleibt) und `docker` (Docker+Compose in einem, generisch —
  `getty-docker` macht Getty später selbst).
- Offen: Marketplace-Eintrag für `Getty/skills` in `Getty/marketplace` (Snippets
  liefert `manage-skills package`), ~/tmp-Originale löschen, committen.
- Punkt 3 unten (discover_skills-Bug) bleibt offen — betrifft nur `sources add`
  auf das Repo-Root; die Gruppen-Sources funktionieren.

---

Stand: 18. August 2026, Ende der Session. **Der Umbau ist mittendrin und nichts ist
committet.** Diese Datei ist der Einstieg für die nächste Session.
(Anmerkung der späteren Session: der Initial-Commit existiert inzwischen.)

## Zustand jetzt

**Getty/skills** (dieses Repo, noch kein einziger Commit):

```
skills/git/getty-git-commit-style      skills/perl/getty-perl-core
skills/git/getty-git-usage      (neu)  skills/perl/perl-www-crawl4ai
skills/k8s/getty-kubernetes-concepts   skills/perl/getty-perl-io-async-future
skills/tools/getty-rex                 skills/perl/getty-perl-kubernetes-classes
                                       skills/perl/getty-perl-mcp
                                       skills/perl/getty-perl-moo
                                       skills/perl/getty-perl-moose
                                       skills/perl/getty-perl-release-author-getty
                                       skills/perl/getty-perl-release-dist-ini
```

13 Skills. Regel dahinter: **hier liegt nur, was in keinem Projekt zuhause ist.**
Alles mit einem Heimat-Repo (`karr`, `dbio-*`, `www-paypal-core` …) bleibt dort.

**Was in den Projekten passiert ist:** 191 Skill-Verzeichnisse in 50 Projekten umbenannt
(`perl-moo` → `getty-perl-moo`) und auf die Quelle hardlinked. 9 davon inhaltlich
ersetzt — veraltete `perl-core`-Varianten durch die jüngste. Referenzen in 179 Dateien
nachgezogen (CLAUDE.md, `.claude/agents/*.md`, ADRs).

**59 von 67 Top-Level-Repos und 3 von 21 dbio-Repos haben jetzt uncommittete Änderungen.**

## Zuerst

1. **Verifizieren, bevor irgendetwas committet wird.** Trockenlauf über alle
   `.claude/agents/*.md`: löst jeder in `briefing.skills` deklarierte Name noch auf?
   Ein übersehener alter Name lässt `briefing` den Spawn verweigern — laut, aber
   überall. Danach stichprobenartig `manage-skills check` in ein paar Projekten.
2. **Sources reparieren.** Registriert sind noch vier Verzeichnisse aus dem
   Zwischenstand, zwei davon zeigen ins Leere (`dbio` 0 skills, `tools` 1). Ziel ist
   **eine** Quelle: `~/dev/skills/skills` — geht erst nach Punkt 3.
3. **`discover_skills`-Bug in manage-skills.** `sources add <lokales Verzeichnis>`
   kennt die Gruppen-Ebene nicht: die Funktion iteriert stur `"$source_dir"/*/`, ohne
   `skill_dirs_in`. Bei Remote-Quellen fällt das nicht auf, weil `remote_materialise`
   vorher flach nach `sources.d/` materialisiert. Fix gehört in `discover_skills` —
   Achtung, das Ausgabeformat ist `dir:name`, bei Gruppen braucht es den vollen Pfad,
   also ziehen die Aufrufer mit.
4. **Dann committen**, repo für repo. Nichts davon ist bisher gepusht.

## Entscheidungen, die offen sind

- **`dbio-*` Skills** (6 Stück, je ~20 Projekte): eigene Quelle aus `~/dev/dbio-dev/dbio`
  statt zentral. Noch nicht gemacht.
- **`karr`-Skills**: dito aus `~/dev/karr`. Bei `karr` selbst sind 3 Altersstände im
  Umlauf; die 17.08.-Fassung (mit `karr metrics`) ist die jüngste und steckt in nur 5
  von 41 Repos.
- **`dbio-coordination`**: in `dbio-dev/dbio` liegt eine **uncommittete** Änderung, die
  `claude --permission-mode bypassPermissions` durch den `claude_with_ollama`-Wrapper
  ersetzt. Die 20 anderen Projekte tragen noch die `bypassPermissions`-Variante. Das ist
  eine Berechtigungsentscheidung, keine Aufräumarbeit — bewusst nicht angefasst.
- **`kanban-issues-karr-cli`**: 2 Varianten, die aus `karr` ist neuer.
- **Die tool-eigenen Skills** (`manage-skills`, `manage-skills-drift-triage`) hatte der
  erste Worker in die Quelle gezogen und zurückverlinkt; ich habe sie beim Rückbau
  wieder entfernt, sie leben im manage-skills-Repo. Prüfen, ob dort alles stimmt.

## Angefangen, nicht fertig

- **`our-codex`** (`~/dev/our-codex`, geklont): Umbau vom AGENTS.md-Bündler zum
  Übersetzer. **Tests stehen** (`test/smoke-test.sh`, 21 Tests, 14 rot),
  **Implementierung nicht begonnen**. Das Design ist abgestimmt: Skills per Hardlink
  nach `.agents/skills/`, Agents umgeformt nach `.codex/agents/<name>.toml` (Bindestrich
  → Unterstrich, `briefing.skills` → `[briefing] skills`), `CLAUDE.md` → `AGENTS.md`,
  `.gitignore` automatisch, `our-codex clean` räumt auf. Das alte Bündeln entfällt
  ersatzlos — war nur ein Workaround aus der Zeit, als Codex nur AGENTS.md konnte.
- **Bilder für GitHub**: Prompts für manage-skills, skills, karr, briefing und our-codex
  sind formuliert (Riso-Look, Llama, Name als Headline, 1280×640). Bilder noch nicht
  erzeugt. Achtung: Das Social-Preview-Bild muss in den Repo-Settings hochgeladen
  werden, ein `assets/`-Bild allein bewirkt nichts.

## Heute fertig geworden (Kontext, nichts zu tun)

- **manage-skills v0.8.0** — Gruppen-Erkennung eine Ebene tiefer, `sync` behält
  inhaltlich abweichende Kopien (`--force` überschreibt), Codex-Plugin, 117 Tests.
- **briefing v0.3.0** — Codex-Unterstützung über `SubagentStart`, end-to-end verifiziert.
- **Getty/marketplace** — Katalog für beide Welten, beide Plugins in beiden Manifesten.
  `Getty/claude-code` ist gelöscht.
