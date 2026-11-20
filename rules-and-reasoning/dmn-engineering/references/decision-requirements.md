# Decision requirements

## Define the graph before drawing

Identify the question answered by each decision and the information required to
answer it. Keep a decision name as a business concept, such as `Shipping lane`,
while recording the precise question in its description. Model an input fact as
input data; model derived information as a decision. This distinction makes the
responsibility for supplying versus computing a value visible.

A Decision Requirements Graph (DRG) contains the requirements relationships. A
Decision Requirements Diagram (DRD) presents a view of that graph. Several diagrams
can show different areas of one model. Layout proximity does not create a semantic
relationship. Treat a missing diagram edge separately from a missing graph link.
See [DMN 1.6, clause 6](https://www.omg.org/spec/DMN/1.6/PDF).

## Select the correct element

| Element | Responsibility | Avoid |
| --- | --- | --- |
| Input data | Supply a fact or structured value | Hiding a calculation in its label |
| Decision | Compute an output from required information | Combining unrelated questions |
| Business knowledge model (BKM) | Encapsulate parameterized reusable logic | Treating it as an automatically executed step |
| Knowledge source | Identify an authority, document, expert, or organizational source | Assuming the engine interprets its text |
| Decision service | Expose a controlled decision interface | Treating it as an authorization or transaction boundary by itself |

Use an **information requirement** when a decision requires an input or another
decision's result. Use a **knowledge requirement** to reference callable knowledge.
Use an **authority requirement** for sources of authority. These relationships have
different permitted endpoints; a visually plausible arrow is not sufficient.

## Keep dependencies meaningful

Draw dependencies toward the element that requires them. A graph does not prescribe
human work order or tell an external service to fetch information. Resolve data
acquisition and process scheduling in the host system. Describe how missing or
stale inputs are handled before invoking decisions.

Inspect the transitive dependency closure of a published decision. Remove accidental
requirements on unrelated inputs; they widen contracts and make models harder to
reuse. Conversely, declare required upstream decisions rather than depending on
an undocumented global variable injected by one engine.

Do not introduce cycles in decision evaluation dependencies. Distinguish a cyclic
business process, which can legitimately revisit a decision with new facts, from a
circular definition in a single evaluation. Use explicit state as input to successive
evaluations when implementing a repeated process.

## Review a DRD

Check names, question boundaries, arrow kinds, dependency direction, and source
identifiers. Verify that every displayed view refers to the correct underlying IDs.
Ask the business owner whether each result can be explained from its declared inputs.
An authority link supports traceability; it does not prove that the implementation
correctly represents the source or that the source applies to this case.
