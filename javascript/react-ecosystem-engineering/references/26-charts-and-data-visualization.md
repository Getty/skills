# Charts and data visualization

**Read when:** creating dashboards, time-series views, or interactive graphics.

## Choose the rendering model

Recharts, Chart.js, and ECharts have different integration and rendering tradeoffs. Compare declarative React composition, canvas/SVG requirements, interaction complexity, dataset size, responsive measurement, export, and accessibility needs. The reviewed Recharts site exposes the v3 generation; confirm installed APIs and migration requirements rather than copying v2 internals. Nivo, visx, Victory, and direct D3 are catalog alternatives requiring targeted review.

## Data semantics first

Document units, timezone, aggregation interval, missing versus zero, outliers, categorical order, and axis domains. Never let a styling decision silently change the interpretation of data. A truncated axis or stacked percentage chart needs a deliberate analytical justification. Preserve raw observations separately from downsampled display data.

Build a typed transformation from domain records to chart series and test it without React. Define stable series IDs and colors through the product design system, with non-color distinctions where useful. Treat tooltip content as user-facing formatted data, not raw HTML from a response. Control animation for live updates and reduced-motion users.

## Interaction and accessibility

Provide a textual summary or data table when the chart conveys essential information. Tooltips must not be the sole way to obtain a value. Support keyboard interaction for actionable data points and expose filtering state clearly. Coordinate legends, brushing, and linked views through explicit state rather than incidental internal chart state.

## Acceptance

Test empty/single-point/all-null series, negative values, daylight-saving transitions, many categories, long labels, resized containers, export, and hidden-then-revealed charts. Inspect production bundle impact and dispose imperative chart instances/listeners. Measure update cost under the expected live event rate; aggregate or throttle upstream rather than scheduling a full redraw for every insignificant event.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R44: Recharts](https://recharts.github.io/en-US/)
- [R45: Chart.js](https://www.chartjs.org/docs/latest/)
- [R46: Apache ECharts](https://echarts.apache.org/en/index.html)
- [R39: WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
