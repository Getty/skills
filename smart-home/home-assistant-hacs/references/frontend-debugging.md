# Frontend resources and debugging

## Locate the failure

Check backend entity state first, then reproduce with a native card, then compare the custom card in a duplicate dashboard. Identify the exact browser/Companion WebView, HA frontend version, card version, theme, and dependencies. A Python integration failure is not repaired by clearing a browser cache.

HACS repository state distinguishes downloaded code, pending updates, and pending restart. Follow the project's activation requirement rather than assuming a download immediately changes every browser. [HACS dashboard](https://www.hacs.xyz/docs/use/repositories/dashboard/).

## Resource checklist

Confirm the loaded JavaScript URL and type, one intended version, HTTP response, browser console error, and cache version. Avoid duplicate manual and HACS-managed resource entries. Storage-mode versus YAML resources have different ownership; inspect actual dashboard settings. Do not edit an unrelated dashboard file because a tutorial uses a different mode.

card-mod may use a frontend module for particular functionality/performance, and its documented resource path depends on installation. Use the actual resource URL, not an example cache tag. [card-mod](https://github.com/thomasloven/lovelace-card-mod).

## Keep CSS and templates maintainable

Prefer supported card options to selectors reaching into another project's internal DOM. Record any CSS selector/version coupling. JavaScript templates in button-card and Jinja templates elsewhere are not interchangeable languages. A template that renders a correct label may still misconfigure an action.

Mushroom's Template Card redesign is a concrete example of layout/theme compatibility changing. Follow its installed-version documentation and migration notes, rather than applying old CSS blindly. [Mushroom migration record](https://github.com/piitaya/lovelace-mushroom/issues/1771).

## Performance and behavior

Limit graph point counts, simultaneous cards, expensive dynamic filters, and per-second updates on tablets. ApexCharts documents experimental features and possible rendering/performance limitations; enable them for a specific requirement with a native fallback. [ApexCharts](https://github.com/RomRider/apexcharts-card).

Test tap, hold, double-tap, navigation, confirmation dialogs, and touch targets on the actual client. Display hiding and confirmation UI are not backend authorization. For consequential operations, place enforcement in the action path as well.

## Recovery

Use a duplicate dashboard or saved raw configuration for experiments. If necessary switch to a native-card view while retaining backend entities. Remove stale resource references after deliberate uninstall. A working incognito/second-browser control case helps distinguish cache and local browser state from server code.
