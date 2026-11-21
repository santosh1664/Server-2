# Patchright vs SeleniumBase

These tools solve different engineering problems. Neither is a universal CAPTCHA verification service.

| Dimension | Patchright | SeleniumBase |
|---|---|---|
| Primary abstraction | Playwright-compatible Chromium automation | Python browser testing/automation framework |
| Language/API | Python and Node.js Playwright-style APIs | Python |
| Browser scope | Chromium only | Chromium CDP modes plus regular Selenium browser support |
| Existing Playwright migration | Usually straightforward | Requires adapting to SeleniumBase APIs |
| Test framework features | Playwright ecosystem | SeleniumBase fixtures, assertions, reports and test helpers |
| Provider token verification | Not included | Not a substitute for provider Siteverify APIs |
| `solve_captcha()` method | No equivalent built-in SeleniumBase method | Documented method in SeleniumBase CDP interfaces |

## Which is better?

There is no universal winner.

- **Patchright** is a better fit when your codebase already uses Playwright and you want to retain its API and ecosystem. It is Chromium-only and changes aspects of Playwright's browser-driver behavior. Its own documentation notes trade-offs, including Console API limitations and compatibility differences.
- **SeleniumBase** is a better fit for this repository's Python testing/diagnostics foundation because it is already installed and offers browser fixtures, assertions, reporting, and multiple browser-control interfaces.
- **SeleniumBase's `sb.solve_captcha()`** is a documented challenge-handling method in its CDP interfaces. It is not the same thing as a provider verification API and does not guarantee that every provider challenge will be accepted.
- Neither tool can independently validate a provider token. For sites you administer, the server must use the provider's documented verification API and validate hostname/action/expiry and other provider-specific fields.

## Recommendation for Server 2

Keep SeleniumBase as the current browser diagnostics framework. Do not add Patchright as a second browser engine yet; doing so increases dependency and debugging overhead without adding provider verification.

If a future part of the product is already based on Playwright, evaluate Patchright separately for that workload. Do not choose a browser framework based on claims that it will reliably defeat anti-bot systems.

## References

- SeleniumBase CDP docs: https://seleniumbase.io/help_docs/cdp_mode_methods/
- SeleniumBase CDP examples: https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode
- Patchright Python package: https://pypi.org/project/patchright/
- Patchright npm package: https://www.npmjs.com/package/patchright
