# Patchright vs SeleniumBase

These tools solve different engineering problems. Neither is a universal CAPTCHA verification service.

| Dimension | Patchright | SeleniumBase |
|---|---|---|
| Primary abstraction | Playwright-compatible Chromium automation | Python browser testing/automation framework |
| Language/API | Python and Node.js Playwright-style APIs | Python |
| Browser scope | Chromium only | Chromium CDP modes plus regular Selenium browser support |
| Existing Playwright migration | Usually straightforward | Requires adapting to SeleniumBase APIs |
| Test framework features | Playwright ecosystem | SeleniumBase fixtures, assertions, reports and test helpers |
| CAPTCHA provider verification | Not included | Not a substitute for provider Siteverify APIs |
| `solve_captcha()` | No matching built-in SeleniumBase method | Documented method in SeleniumBase CDP interfaces |

## Practical choice for this repository

For this Python Server 2 codebase, SeleniumBase is already installed and is the least disruptive choice for browser diagnostics and QA. Patchright is a fit when a project already uses Playwright and needs to preserve that programming model. It is a separate Chromium automation driver, not a drop-in implementation of SeleniumBase's `solve_captcha()`.

Do not select either library on the assumption that it guarantees successful verification with every CAPTCHA provider. For websites you administer, use the provider's documented verification API and validate its response server-side.

## References

- SeleniumBase CDP docs: https://seleniumbase.io/help_docs/cdp_mode_methods/
- SeleniumBase CDP examples: https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode
- Patchright Python package: https://pypi.org/project/patchright/
- Patchright npm package: https://www.npmjs.com/package/patchright
