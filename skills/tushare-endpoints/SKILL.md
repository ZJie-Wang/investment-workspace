---
name: tushare-endpoints
description: Technical guide for using bundled Tushare A-share data endpoints. Use whenever working with Tushare endpoints.
---

# Tushare Endpoints

Use this skill as a technical endpoint guide. It explains local coverage, environment checks, input normalization, and endpoint-selection heuristics.

Treat this skill as a Tushare interface guide, not an analysis framework.

## Quick Workflow

1. Identify the object type before touching an endpoint: stock, index, industry classification, ETF, public fund, convertible bond, or domestic macro series.
2. Check if the environment is ready: 
   - Python version 3.7+
   - `tushare` package
   - `TUSHARE_TOKEN`
4. If the user asks for live data, locate candidate endpoints in`references/endpoint-catalog.md` - a document provided by Tushare official.
5. Open the endpoint's official Tushare doc link before assuming parameter names, field names, row limits, or permission requirements.
6. Normalize dates and codes before calling the API. Resolve parameter conflicts before making the request.
7. If the local bundle does not cover an endpoint or the official page is unavailable, fall back to web search to recover the endpoint details.

## Core Rules

- Prefer the bundled endpoint index for discovery and the official doc link for authoritative parameter and output details.
- Warn early about missing `TUSHARE_TOKEN`, missing `tushare`, or unsupported Python version.
- Normalize all dates to `YYYYMMDD`.
- Do not pass conflicting date selectors such as `trade_date` together with `start_date` and `end_date`.
- If the user gives a future date and requires data, clip to the most recent plausible available date and say that you did so.
- Convert naked security codes to exchange-suffixed codes when the exchange can be inferred confidently. Otherwise ask for clarification.
- Default to A-shares unless the user explicitly asks for another market.
- Distinguish stock, index, ETF, fund, bond, and macro requests before selecting an endpoint. Do not mix their APIs.
- If a critical error prevents the workflow from continuing, stop and report.
- **Before Pulling data**: Check the environment first.
- **While Pulling Data**:
  - Verify actual endpoint schemas from returned data; do not trust guessed field names.
  - If a query looks wrong or empty, inspect the raw output before concluding the data is unavailable.
  - **Always** remember that Tushare provides scheduled updated data, most of which are **EOD** data, not real-time updates.

- **Before Analysis**:
  - Run a quick data audit: row counts, date coverage, missing values, and obvious outliers.
  - Validate the exact fields and rows used in the analysis.
  - Handle sparse or missing values

## Bundled Resources

- `references/endpoint-catalog.md`: human-readable endpoint catalog grouped by family, including curl-able links to the official docs for each endpoint.

