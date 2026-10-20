# React ecosystem and component routing catalog

**Read when:** selecting a dependency, recognizing an existing package, or routing an unfamiliar integration.

## Coverage contract

This is a broad task-oriented catalog, not a claim to enumerate every React package or rank popularity. **D** means a dedicated engineering workflow is provided; it does not mean every upstream API was tested. **C** means a reviewed comparison/integration guide. **P** means a discovery pointer: current API, maintenance, license, and compatibility must be researched before use. A reviewed core project's source does not independently verify every listed third-party React wrapper.

Package names include recognition aliases and older generations; they are **not** a command to install every entry. Read the lockfile first. Check exact versions, peer dependencies, advisory status, license/paid-feature boundary, rendering environment, accessibility, and removal cost. Fetch targeted official documentation when a task goes beyond the chapter's verified scope.

| Category | Library / component ecosystem | Recognize packages | Depth | Load |
|---|---|---|---|---|
| Routing | [React Router](https://reactrouter.com/start/modes) | `react-router`, `react-router-dom` | D | [12-routing-and-url-state](12-routing-and-url-state.md) |
| Routing | [TanStack Router / Start](https://tanstack.com/router/latest/docs/overview) | `@tanstack/react-router`, `@tanstack/react-start` | C | [11-frameworks-and-deployment](11-frameworks-and-deployment.md) |
| Framework | [Next.js](https://nextjs.org/docs/app) | `next` | D | [09-ssr-hydration-rsc](09-ssr-hydration-rsc.md) |
| Build | [Vite](https://vite.dev/guide/) | `vite`, `@vitejs/plugin-react` | D | [45-build-monorepos-packaging-ci](45-build-monorepos-packaging-ci.md) |
| Server state | [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults) | `@tanstack/react-query` | D | [13-server-state-query-swr](13-server-state-query-swr.md) |
| Server state | [SWR](https://swr.vercel.app/docs/getting-started) | `swr` | C | [13-server-state-query-swr](13-server-state-query-swr.md) |
| State | [Redux Toolkit / RTK Query](https://redux.js.org/toolkit/introduction/getting-started) | `@reduxjs/toolkit`, `react-redux` | D | [14-redux-toolkit-rtk-query](14-redux-toolkit-rtk-query.md) |
| State | [Zustand](https://github.com/pmndrs/zustand) | `zustand` | D | [15-zustand-jotai-and-reactive-stores](15-zustand-jotai-and-reactive-stores.md) |
| State | [Jotai](https://jotai.org/docs) | `jotai` | C | [15-zustand-jotai-and-reactive-stores](15-zustand-jotai-and-reactive-stores.md) |
| State | [XState](https://stately.ai/docs/xstate-react) | `xstate`, `@xstate/react` | D | [16-state-machines-and-streams](16-state-machines-and-streams.md) |
| State | [MobX](https://mobx.js.org/README.html) | `mobx`, `mobx-react-lite` | P | [15-zustand-jotai-and-reactive-stores](15-zustand-jotai-and-reactive-stores.md) |
| State | [Valtio](https://valtio.dev/) | `valtio` | P | [15-zustand-jotai-and-reactive-stores](15-zustand-jotai-and-reactive-stores.md) |
| Streams | [RxJS](https://rxjs.dev/) | `rxjs` | P | [16-state-machines-and-streams](16-state-machines-and-streams.md) |
| Forms | [React Hook Form](https://github.com/react-hook-form/react-hook-form) | `react-hook-form`, `@hookform/resolvers` | D | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| Forms | [TanStack Form](https://tanstack.com/form/latest/docs/overview) | `@tanstack/react-form` | C | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| Schemas | [Zod](https://zod.dev/) | `zod` | D | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| Schemas | [Valibot](https://valibot.dev/) | `valibot` | P | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| Schemas | [Yup](https://github.com/jquense/yup) | `yup` | P | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| Forms legacy | [Formik](https://formik.org/) | `formik` | P | [18-forms-and-runtime-schemas](18-forms-and-runtime-schemas.md) |
| API | [Apollo Client](https://www.apollographql.com/docs/react) | `@apollo/client` | C | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| API | [Relay](https://relay.dev/docs/) | `react-relay`, `relay-runtime` | C | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| API | [tRPC](https://trpc.io/docs/) | `@trpc/client`, `@trpc/react-query`, `@trpc/tanstack-react-query` | C | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| API | [urql](https://urql.dev/) | `urql`, `@urql/core` | P | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| API | [GraphQL Code Generator](https://the-guild.dev/graphql/codegen) | `@graphql-codegen/cli` | P | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| API | [OpenAPI TypeScript](https://openapi-ts.dev/) | `openapi-typescript`, `openapi-fetch` | P | [17-api-graphql-trpc-openapi](17-api-graphql-trpc-openapi.md) |
| CSS | [Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite) | `tailwindcss`, `@tailwindcss/vite` | C | [19-styling-design-tokens](19-styling-design-tokens.md) |
| CSS | [CSS Modules](https://vite.dev/guide/) | `postcss` | C | [19-styling-design-tokens](19-styling-design-tokens.md) |
| CSS | [Emotion](https://emotion.sh/docs/introduction) | `@emotion/react`, `@emotion/styled` | P | [19-styling-design-tokens](19-styling-design-tokens.md) |
| CSS | [styled-components](https://styled-components.com/docs) | `styled-components` | P | [19-styling-design-tokens](19-styling-design-tokens.md) |
| CSS | [vanilla-extract](https://vanilla-extract.style/) | `@vanilla-extract/css` | P | [19-styling-design-tokens](19-styling-design-tokens.md) |
| CSS | [Panda CSS](https://panda-css.com/) | `@pandacss/dev` | P | [19-styling-design-tokens](19-styling-design-tokens.md) |
| Primitives | [Radix UI](https://www.radix-ui.com/primitives/docs/overview/introduction) | `radix-ui`, `@radix-ui/react-dialog` | D | [20-headless-primitives](20-headless-primitives.md) |
| Primitives | [Base UI](https://base-ui.com/react/overview/quick-start) | `@base-ui/react` | C | [20-headless-primitives](20-headless-primitives.md) |
| Primitives | [React Aria Components](https://react-aria.adobe.com/getting-started) | `react-aria-components`, `react-aria` | D | [20-headless-primitives](20-headless-primitives.md) |
| Primitives | [Headless UI](https://headlessui.com/) | `@headlessui/react` | P | [20-headless-primitives](20-headless-primitives.md) |
| Components | [shadcn/ui](https://ui.shadcn.com/docs) | `shadcn` | D | [21-shadcn-component-registries](21-shadcn-component-registries.md) |
| Components | [Material UI / MUI X](https://mui.com/material-ui/getting-started/) | `@mui/material`, `@mui/x-data-grid`, `@mui/x-date-pickers` | C | [22-component-suites](22-component-suites.md) |
| Components | [Mantine](https://mantine.dev/getting-started/) | `@mantine/core`, `@mantine/hooks` | C | [22-component-suites](22-component-suites.md) |
| Components | [Chakra UI](https://chakra-ui.com/docs/get-started/installation) | `@chakra-ui/react` | C | [22-component-suites](22-component-suites.md) |
| Components | [Ant Design](https://ant.design/docs/react/introduce/) | `antd` | C | [22-component-suites](22-component-suites.md) |
| Components | [Fluent UI](https://react.fluentui.dev/) | `@fluentui/react-components` | P | [22-component-suites](22-component-suites.md) |
| Components | [PrimeReact](https://primereact.org/) | `primereact` | P | [22-component-suites](22-component-suites.md) |
| Components | [HeroUI](https://www.heroui.com/) | `@heroui/react` | P | [22-component-suites](22-component-suites.md) |
| Components | [React Bootstrap](https://react-bootstrap.github.io/) | `react-bootstrap` | P | [22-component-suites](22-component-suites.md) |
| Widgets | [Downshift](https://www.downshift-js.com/) | `downshift` | P | [20-headless-primitives](20-headless-primitives.md) |
| Widgets | [React Select](https://react-select.com/) | `react-select` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Widgets | [Floating UI](https://floating-ui.com/docs/react) | `@floating-ui/react` | P | [20-headless-primitives](20-headless-primitives.md) |
| Widgets | [cmdk](https://cmdk.paco.me/) | `cmdk` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Widgets | [Sonner](https://sonner.emilkowal.ski/) | `sonner` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Widgets | [Embla Carousel](https://www.embla-carousel.com/) | `embla-carousel-react` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Widgets | [React Resizable Panels](https://github.com/bvaughn/react-resizable-panels) | `react-resizable-panels` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Tables | [TanStack Table](https://tanstack.com/table/latest) | `@tanstack/react-table` | D | [24-tables-and-data-grids](24-tables-and-data-grids.md) |
| Tables | [AG Grid](https://www.ag-grid.com/react-data-grid/getting-started/) | `ag-grid-react`, `ag-grid-community`, `ag-grid-enterprise` | C | [24-tables-and-data-grids](24-tables-and-data-grids.md) |
| Virtualization | [TanStack Virtual](https://tanstack.com/virtual/latest) | `@tanstack/react-virtual` | C | [25-virtualization-large-lists](25-virtualization-large-lists.md) |
| Virtualization | [React Virtuoso](https://virtuoso.dev/) | `react-virtuoso` | C | [25-virtualization-large-lists](25-virtualization-large-lists.md) |
| Virtualization | [react-window](https://github.com/bvaughn/react-window) | `react-window` | P | [25-virtualization-large-lists](25-virtualization-large-lists.md) |
| Charts | [Recharts](https://recharts.github.io/en-US/) | `recharts` | C | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [Chart.js / react-chartjs-2](https://www.chartjs.org/docs/latest/) | `chart.js`, `react-chartjs-2` | C | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [Apache ECharts](https://echarts.apache.org/en/index.html) | `echarts`, `echarts-for-react` | C | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [Nivo](https://nivo.rocks/) | `@nivo/core`, `@nivo/line` | P | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [visx](https://visx.airbnb.tech/) | `@visx/visx`, `@visx/shape` | P | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [Victory](https://commerce.nearform.com/open-source/victory/) | `victory` | P | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Charts | [D3](https://d3js.org/) | `d3` | P | [26-charts-and-data-visualization](26-charts-and-data-visualization.md) |
| Motion | [Motion](https://motion.dev/docs/react) | `motion`, `framer-motion` | D | [27-animation-motion](27-animation-motion.md) |
| Motion | [React Spring](https://www.react-spring.dev/) | `@react-spring/web` | P | [27-animation-motion](27-animation-motion.md) |
| Gestures | [use-gesture](https://use-gesture.netlify.app/) | `@use-gesture/react` | P | [27-animation-motion](27-animation-motion.md) |
| Drag/drop | [dnd kit generations](https://dndkit.com/) | `@dnd-kit/react`, `@dnd-kit/core`, `@dnd-kit/sortable` | D | [28-drag-and-drop](28-drag-and-drop.md) |
| Drag/drop | [Pragmatic drag and drop](https://atlassian.design/components/pragmatic-drag-and-drop/) | `@atlaskit/pragmatic-drag-and-drop` | P | [28-drag-and-drop](28-drag-and-drop.md) |
| Drag/drop | [React DnD](https://react-dnd.github.io/react-dnd/) | `react-dnd` | P | [28-drag-and-drop](28-drag-and-drop.md) |
| Graphs | [React Flow](https://reactflow.dev/learn) | `@xyflow/react`, `reactflow` | D | [29-react-flow-foundations](29-react-flow-foundations.md) |
| Layout | [Dagre](https://github.com/dagrejs/dagre) | `@dagrejs/dagre` | P | [31-react-flow-layout-subflows](31-react-flow-layout-subflows.md) |
| Layout | [ELK.js](https://github.com/kieler/elkjs) | `elkjs` | P | [31-react-flow-layout-subflows](31-react-flow-layout-subflows.md) |
| Editors | [Tiptap](https://tiptap.dev/docs/editor/getting-started/install/react) | `@tiptap/react`, `@tiptap/core` | D | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Editors | [Lexical](https://lexical.dev/docs/getting-started/react) | `lexical`, `@lexical/react` | C | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Editors | [ProseMirror](https://prosemirror.net/) | `prosemirror-state`, `prosemirror-view` | P | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Editors | [Slate](https://docs.slatejs.org/) | `slate`, `slate-react` | P | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Editors | [Plate](https://platejs.org/) | `platejs`, `@udecode/plate` | P | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Markdown | [React Markdown / unified](https://github.com/remarkjs/react-markdown) | `react-markdown`, `unified`, `remark-gfm`, `rehype-sanitize` | P | [35-rich-text-markdown](35-rich-text-markdown.md) |
| Collaboration | [Yjs](https://docs.yjs.dev/) | `yjs`, `y-websocket` | D | [33-react-flow-persistence-history-collaboration](33-react-flow-persistence-history-collaboration.md) |
| Collaboration | [Automerge](https://automerge.org/) | `@automerge/automerge` | P | [40-realtime-offline-localfirst](40-realtime-offline-localfirst.md) |
| Code | [Monaco](https://microsoft.github.io/monaco-editor/) | `monaco-editor`, `@monaco-editor/react` | P | [36-code-editors-terminals](36-code-editors-terminals.md) |
| Code | [CodeMirror](https://codemirror.net/) | `codemirror`, `@codemirror/view` | P | [36-code-editors-terminals](36-code-editors-terminals.md) |
| Terminal | [xterm.js](https://xtermjs.org/) | `@xterm/xterm`, `xterm` | P | [36-code-editors-terminals](36-code-editors-terminals.md) |
| 3D | [React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/introduction) | `@react-three/fiber` | C | [37-maps-canvas-three](37-maps-canvas-three.md) |
| 3D | [Drei](https://drei.docs.pmnd.rs/) | `@react-three/drei` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Canvas | [Konva](https://konvajs.org/docs/react/) | `konva`, `react-konva` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Canvas | [PixiJS](https://pixijs.com/) | `pixi.js`, `@pixi/react` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Maps | [MapLibre GL / react-map-gl](https://maplibre.org/maplibre-gl-js/docs/) | `maplibre-gl`, `react-map-gl` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Maps | [React Leaflet](https://react-leaflet.js.org/) | `leaflet`, `react-leaflet` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Maps | [deck.gl](https://deck.gl/) | `@deck.gl/react` | P | [37-maps-canvas-three](37-maps-canvas-three.md) |
| Dates | [React DayPicker](https://daypicker.dev/) | `react-day-picker` | P | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| Dates | [FullCalendar](https://fullcalendar.io/docs/react) | `@fullcalendar/react` | P | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| Dates | [date-fns](https://date-fns.org/) | `date-fns` | P | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| Dates | [Day.js](https://day.js.org/) | `dayjs` | P | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| Dates | [Luxon](https://moment.github.io/luxon/) | `luxon` | P | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| i18n | [react-i18next](https://react.i18next.com/) | `react-i18next`, `i18next` | C | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| i18n | [React Intl](https://formatjs.github.io/docs/react-intl/) | `react-intl` | C | [38-dates-calendars-i18n](38-dates-calendars-i18n.md) |
| Files | [Uppy](https://uppy.io/) | `@uppy/react`, `@uppy/core` | P | [39-files-media-pdf](39-files-media-pdf.md) |
| Files | [React Dropzone](https://react-dropzone.js.org/) | `react-dropzone` | P | [39-files-media-pdf](39-files-media-pdf.md) |
| PDF viewing | [React-PDF](https://github.com/wojtekmaj/react-pdf) | `react-pdf` | P | [39-files-media-pdf](39-files-media-pdf.md) |
| PDF generation | [React-pdf renderer](https://react-pdf.org/) | `@react-pdf/renderer` | P | [39-files-media-pdf](39-files-media-pdf.md) |
| Local DB | [Dexie](https://dexie.org/) | `dexie`, `dexie-react-hooks` | P | [40-realtime-offline-localfirst](40-realtime-offline-localfirst.md) |
| Local DB | [RxDB](https://rxdb.info/) | `rxdb` | P | [40-realtime-offline-localfirst](40-realtime-offline-localfirst.md) |
| Network | [Socket.IO](https://socket.io/docs/v4/) | `socket.io-client` | P | [40-realtime-offline-localfirst](40-realtime-offline-localfirst.md) |
| Security | [DOMPurify](https://github.com/cure53/DOMPurify) | `dompurify` | C | [41-auth-security-trust](41-auth-security-trust.md) |
| Testing | [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) | `@testing-library/react`, `@testing-library/user-event` | D | [42-unit-component-network-tests](42-unit-component-network-tests.md) |
| Testing | [Vitest](https://vitest.dev/guide/) | `vitest` | D | [42-unit-component-network-tests](42-unit-component-network-tests.md) |
| Testing | [MSW](https://mswjs.io/docs/) | `msw` | C | [42-unit-component-network-tests](42-unit-component-network-tests.md) |
| Testing | [Playwright](https://playwright.dev/docs/intro) | `@playwright/test`, `playwright` | D | [43-browser-storybook-accessibility](43-browser-storybook-accessibility.md) |
| Testing | [Storybook](https://storybook.js.org/docs) | `storybook`, `@storybook/react-vite` | D | [43-browser-storybook-accessibility](43-browser-storybook-accessibility.md) |
| Testing | [Jest](https://jestjs.io/) | `jest` | P | [42-unit-component-network-tests](42-unit-component-network-tests.md) |
| Testing | [Cypress](https://docs.cypress.io/) | `cypress` | P | [43-browser-storybook-accessibility](43-browser-storybook-accessibility.md) |
| Accessibility | [axe-core](https://github.com/dequelabs/axe-core) | `axe-core`, `@axe-core/playwright` | P | [43-browser-storybook-accessibility](43-browser-storybook-accessibility.md) |
| Icons | [Lucide](https://lucide.dev/) | `lucide-react` | P | [23-component-contracts-accessibility](23-component-contracts-accessibility.md) |
| Mobile | [React Native / Expo](https://reactnative.dev/) | `react-native`, `expo` | P | [49-native-and-other-renderers](49-native-and-other-renderers.md) |
| CLI renderer | [Ink](https://github.com/vadimdemedes/ink) | `ink` | P | [49-native-and-other-renderers](49-native-and-other-renderers.md) |
| Observability | [Sentry React](https://docs.sentry.io/platforms/javascript/guides/react/) | `@sentry/react` | P | [44-debugging-observability](44-debugging-observability.md) |

## Selection experiment

Take the hardest representative requirement, implement a small fixture, and measure correctness, accessibility behavior, bundle/runtime impact, integration effort, and upgrade/removal cost. Verify the license for the actual feature/edition shipped. Treat popularity claims as unmeasured unless a dated primary metric is supplied. Prefer an existing coherent dependency over installing a second tool that owns the same state or interaction layer.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R50: React Flow learning index](https://reactflow.dev/learn)
- [R32: shadcn/ui documentation](https://ui.shadcn.com/docs)
- [R40: TanStack Table](https://tanstack.com/table/latest)
- [R48: dnd kit](https://dndkit.com/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
