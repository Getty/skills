# Standards and legal mapping

## Keep four layers distinct

1. Applicable functional requirements in EU/national law.
2. A technical standard and its exact published edition.
3. Official Journal citation creating a presumption of conformity for specified requirements and instrument.
4. The organization's chosen engineering or contractual target.

An edition being called a harmonised European standard by its publisher does not prove that it has already been cited for the particular law. A WAD citation is not automatically an EAA citation. Conformity presumptions cover the requirements and clauses mapped by the citation; they do not certify every aspect of a business. [A8]

## October 2026 research baseline

ETSI has published EN 301 549 V4.1.1 (2026-09). The edition updates web, document and software provisions toward WCAG 2.2 and includes EAA mapping. The Commission's AccessibleEU update of 2026-09-07 expressly distinguishes publication from subsequent OJ citation. Treat OJ citation status at the actual release date as a live verification step; this package does not assert that no citation could have appeared after that update. [A9, A10]

Do not rely on the older Bundesfachstelle explanatory page's forward-looking language as proof that V4.1.1 remains unpublished. Use the publisher for publication, EUR-Lex/OJ for legal citation and the applicable law for duties. This source reconciliation is a model for other evolving standards.

## Practical target

For new web AI interfaces, choose WCAG 2.2 AA as a practical engineering target unless the project's documented obligations require more or something different. Record why. Map the standard edition to applicable web, non-web documents, software, support and functional criteria. A WCAG-only audit can miss EN requirements beyond web content. Do not claim WCAG 3 draft compliance as a substitute for current legal obligations. [A11]

Maintain a requirements matrix with `legal_requirement`, `instrument`, `standard_edition`, `clause`, `precondition`, `applicable`, `test_method`, `evidence`, `limitation`, `owner`. Evaluate conditional requirements by actual feature, such as video, real-time text, hardware or closed functionality.

## Changing target safely

When a new edition is cited, identify transition dates, additions, removals and altered test methods. Assess the existing service rather than blindly changing a badge. Update component specifications, testing, procurement and public information. Keep historical audit target versions so an old report remains interpretable.

Avoid copying copyrighted standards wholesale into project documentation. Link the licensed or publicly available edition and write original implementation guidance. Cite exact criteria in findings so a reviewer can reproduce the mapping.
