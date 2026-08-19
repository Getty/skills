# Skills about skills

The meta group: authoring skills, keeping them lean, the library's own rules,
and the agent setup that consumes them. This is what turns the repo into a
workbench for skill editing rather than just a shelf.

| Skill | Covers |
|---|---|
| [skill-authoring](skill-authoring/SKILL.md) | Writing a new SKILL.md or reworking one — archetypes (reference, convention, workflow, concept), descriptions that actually trigger, body structure, testing with a fresh agent. |
| [skill-compressor](skill-compressor/SKILL.md) | Shrinking or merging existing skills — token efficiency without behavior loss, generalizing project-bound skills, code-example safety while compressing. |
| [getty-skill-library](getty-skill-library/SKILL.md) | Getty's library rules — where a skill lives, the `getty-` naming semantics, the hardlink/inode editing discipline, wiring projects with manage-skills, distribution duties. |
| [getty-agent-team](getty-agent-team/SKILL.md) | Installing the house multi-agent setup in a project — briefing-preloaded subagents, house-rules file with the delegation lock, the skill base, optional karr coordination. User-level only, never linked into a project. |

Working on a skill usually means two of these at once: `getty-skill-library`
answers where it lives and what it is called, `skill-authoring` answers what
goes inside.
