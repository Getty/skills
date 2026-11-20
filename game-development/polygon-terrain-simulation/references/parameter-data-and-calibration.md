# Parameters, data provenance and calibration

Use this reference before populating a material database or transferring values from a paper. A formula without units, parameter meaning and applicability is incomplete.

## Contents

- [Classify every value](#classify-every-value)
- [Use the bundled examples correctly](#use-the-bundled-examples-correctly)
- [Separate properties and state](#separate-properties-and-state)
- [Record a parameter contract](#record-a-parameter-contract)
- [Convert units explicitly](#convert-units-explicitly)
- [Calibrate against behavior](#calibrate-against-behavior)
- [Avoid false precision](#avoid-false-precision)

## Classify every value

| Status | Meaning | Required evidence |
|---|---|---|
| Definition/identity | Follows from chosen quantities, such as mass = density × volume | Definition and dimensional derivation |
| Physical reference assumption | Rounded fluid property or gravity assumption | Conditions and precision |
| Source-reported measurement | Measured at a site/sample or experimental setup | Primary source, method, location/conditions, range |
| Fitted coefficient | Chosen by fitting a particular model | Equation convention, dataset, objective and uncertainty |
| Synthetic fixture | Invented for arithmetic and verification | Label as synthetic; analytic expected outcome |
| Gameplay tuning | Chosen to achieve a game response | Intended behavior, scale and acceptable approximation |

Do not silently promote the last two categories into physical measurements. A texture name, biome tag or lithology name is not enough to determine all hydraulic and mechanical coefficients.

## Use the bundled examples correctly

| Asset | Purpose | Safe interpretation |
|---|---|---|
| `assets/material-examples.json` | Contrasting toy material parameters with SI units | Synthetic parameter records; replace or calibrate for a game |
| `assets/world-state-example.json` | Four-cell consistent polygon state | Illustrates ownership, derived layers, stored water and shared faces |
| `assets/numeric-fixtures.json` | Analytical numerical examples | Expected arithmetic for the reference utilities |
| `assets/domain-transfer-example.json` | Material handoff between domains | Proposed idempotent transfer contract |

All material rows are explicitly uncalibrated. Their particle densities, porosities, rates and roughness values are convenient examples, not recommended universal soil classes. The world fixture is a small square tessellation: squares are valid polygons, and its simple orthogonal geometry makes expected results independently checkable.

Do not infer “more porosity means faster infiltration” from a toy table. Conductivity depends on connected pore geometry and fluid; infiltration additionally depends on supply, saturation, surface condition and the selected model.

Roughness appears in the example material records for convenience. In a production model, it may belong to surface cover, channel geometry and water-depth regimes rather than immutable material identity.

## Separate properties and state

### Material identity and composition

Store grain or constituent fractions with a declared basis: mass fraction, solid volume fraction, or bulk volume fraction. Sum the chosen fractions to one within tolerance. Do not mix bases in the same array.

Separate texture (particle size composition), lithology (rock/geological identity), cover (vegetation/paving), and biome (ecological/climate classification).

### Evolving state

Mass, porosity/compaction, water content, temperature if modeled, layer order and exposed material change over time. A material definition should not contain a mutable global moisture value that accidentally changes every cell using that material.

### Process parameters

Keep units and equation choices beside parameters:

- Hydraulic conductivity [m/s] versus intrinsic permeability [m²].
- Infiltration capacity [m/s] versus actual infiltrated volume [m³].
- Erosion speed [m/s] versus sediment mass rate [kg/s].
- Per-width sediment flux [m²/s] versus total mass flux [kg/s].
- Stream-power coefficient for area-based versus discharge-based models.
- Effective cohesion and friction parameters versus scour erodibility.

The same symbol \(K\) in two papers does not establish the same quantity.

## Record a parameter contract

For each important coefficient, record:

~~~json
{
  "parameter": "infiltration_capacity",
  "value": 0.00001,
  "unit": "m/s",
  "model": "bounded_bucket_constant_capacity",
  "status": "synthetic_fixture",
  "source_url": null,
  "conditions": "illustrative wet/pervious patch",
  "range_or_uncertainty": null,
  "calibration_target": null
}
~~~

Add model version, temperature, saturation range, spatial scale or grain convention when relevant. Null is preferable to an invented provenance claim. An imported dataset with missing parameters should remain incomplete until assumptions are explicitly supplied.

Store data-source attribution and license for reused datasets. Documentation being publicly readable does not by itself license redistribution of large data tables or code. Prefer small original synthetic fixtures in a reusable skill.

## Convert units explicitly

For rates, convert both time and length:

\[
1\ \mathrm{mm/h}=\frac{10^{-3}}{3600}\ \mathrm{m/s}
\approx2.7778\times10^{-7}\ \mathrm{m/s}.
\]

Across \(3600\ \mathrm{m^2}\), this supplies \(0.001\ \mathrm{m^3/s}\). A ten-minute step supplies \(0.6\ \mathrm{m^3}\), before runoff/infiltration partitioning.

For a coefficient \(D\) in \(\mathrm{m^2/year}\), divide by the declared seconds per model year to obtain \(\mathrm{m^2/s}\). Calendar-year length, game-year length and physical-time acceleration are different choices. Do not casually mix a morphology component calibrated in years with a water component stepping in seconds.

Use radians internally for trigonometric formulas or convert degrees at the boundary. A dimensionless slope \(\Delta z/\Delta x\) is the tangent of the slope angle, not the angle itself.

Use SI Manning \(n\) with its equation convention; do not mix the SI formula and unit-system coefficients from an imperial implementation.

## Calibrate against behavior

Choose observations meaningful for the game:

| Observable | Parameters/model choices it constrains |
|---|---|
| Time for a pond to drain | Outlet rule, storage geometry, infiltration |
| Maximum flood level | Inflow volume, outlet capacity, floodplain storage |
| Soil drying time | Soil capacity, evaporation/uptake, drainage |
| Material left after grading | Layer inventory, cut/fill density, suitability rules |
| Sediment deposited after a storm | Entrainment, transport, settling, source availability |
| Channel displacement over seasons | Bank law, geometry, flood forcing and morphology timescale |

Match multiple independent observations. A fast drain can be produced by high infiltration or a large outlet; fitting one curve alone may not distinguish them.

Run sensitivity experiments before increasing parameter count. Vary one mechanism at a time, then test selected interactions. Track dimensionless or scale-normalized errors so the largest absolute field does not hide the others.

Preserve a holdout scenario when calibrating. Tuning a dam model only until one favorite pond looks good does not establish general behavior.

## Avoid false precision

Report enough digits for reproducible fixtures, but use appropriate precision in interpretation. Parameter uncertainty may dominate floating-point arithmetic error.

Document the smallest resolved ditch, meaningful update interval and forecast horizon. Subgrid storage improves volume representation but does not make every unresolved flow pattern physically recoverable.

For a stylized game, make time acceleration an explicit multiplier on a named process, with corresponding budgets. Never apply a vague global speed factor to both a rate and its timestep.

### Primary references

- [USDA NRCS: bulk density, moisture and aeration](https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%20Bulk%20Density%20Moisture%20Aeration.pdf) — physical distinctions and variability.
- [Landlab: unit consistency](https://landlab.csdms.io/user_guide/units.html) — component unit assumptions.
- [USACE: erodibility coefficient conventions](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/cohesive-transport/krone-and-partheniades-methods/kd-vs-m) — coefficients change with equation form.
