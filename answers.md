# Answer

## A1.1

### How is the data table actually loaded?

The data table is loaded dynamically through an AJAX/XHR request to an endpoint that returns data in JSON format.

### Is it present in the HTML that `requests.get()` returns, or does it arrive some other way?

No. The HTML returned by `requests.get()` only contains the page structure and the table layout. The actual table data is not embedded in the HTML. Instead, it is retrieved from a separate JSON response after the page has finished loading.

### Evidence

- Viewing the page source does not show the table data.
- In **Developer Tools → Network → XHR/Fetch**, there is a request to a data endpoint.
- The response from this request is a JSON object containing the table records.
- Parameters such as `draw`, `start`, and `length` indicate that the website uses **server-side processing**, where only the required rows are requested from the server.

---

## A1.3 Metadata Standard

The machine-readable metadata was successfully extracted from a `<script type="application/ld+json">` tag embedded in the dataset page. Based on the extracted JSON, the **data.bkpm.go.id** portal uses the **Schema.org** metadata standard, as indicated by:

```json
"@context": "https://schema.org"
```

---

## Ethical and Technical Considerations for Scraping

Based on my observations, the website functions as a public data portal that provides information through a web interface. The data displayed on the page is not entirely embedded in the HTML. Instead, after the page loads, the browser sends requests to the server and receives the required data for display.

The form shown before accessing the dataset may serve several purposes, such as collecting user profile information, tracking how many people use the dataset, sending updates to users, or understanding how the dataset is being used.

In my opinion, using the discovered JSON endpoint without submitting the form can be acceptable under certain conditions. The dataset is publicly available and licensed under **CC BY 4.0**, which allows reuse as long as proper attribution is provided. In addition, the endpoint does not require authentication, login credentials, or bypassing any security mechanism. However, I would still respect the publisher's intended workflow. Even if the endpoint can technically be accessed directly, users should follow the provider's guidelines whenever possible. If the endpoint is only used to retrieve public data more efficiently while respecting the license and terms of use, I believe this approach is acceptable.

During the scraping process, there are situations where I would stop and ask for human guidance instead of attempting to bypass restrictions. One example is when the website introduces a CAPTCHA, which clearly indicates that the publisher intends to prevent automated access. Likewise, if authentication, permission-based access, or terms of use explicitly prohibit scraping, I would not attempt to bypass those controls because such decisions involve organizational policy rather than technical implementation.

If the portal introduces technical barriers, I would handle them in order from the simplest solution to the most restrictive. If I receive an HTTP 403 response because of an invalid User-Agent, I would use a standard browser User-Agent. If the server returns HTTP 429 due to rate limits, I would implement rate limiting and add delays between requests. If the website uses rotating CSRF tokens, I would follow the normal workflow by retrieving a fresh token before each request. Finally, if a CAPTCHA appears, I would stop the automation and escalate the issue to a human because CAPTCHA is an intentional security mechanism rather than a normal technical problem.

In my opinion, a developer should not independently decide to bypass CAPTCHA, circumvent security mechanisms, ignore access restrictions, or scrape protected data without permission. Such decisions should involve the data owner or the responsible organization to ensure that data collection remains ethical and compliant with applicable policies.

---

# Part E - Orchestration & Design

## E1. Scheduling without daily polling

Instead of downloading the entire dataset every day, I would create a lightweight script that periodically checks the dataset metadata, such as the **Last-Modified** HTTP header or another metadata field provided by the endpoint. The main scraping pipeline would only run when a change in the dataset is detected. This approach minimizes unnecessary requests while ensuring that newly published data is collected as soon as it becomes available.

## E2. Idempotency and warehouse safety

An idempotent pipeline means that running the same job once or multiple times always produces the same final result in the database without creating duplicate records. A simple and reliable approach is to delete the records for the target quarter before inserting the refreshed data. For example, the pipeline first executes `DELETE FROM fakta_investasi WHERE periode = '2026 - Quarter 2'`, and then inserts the latest data for that quarter. This ensures that even if the job is executed multiple times, the warehouse remains consistent and free of duplicate records.

## E3. Handling data revisions (restatements)

If BKPM revises previously published data, directly overwriting the old records would remove the original version and eliminate the audit trail. A simple solution is to add two columns: `updated_at`, which stores the timestamp of the latest update, and `data_status`, which indicates whether the record is **preliminary** or **final**. During analysis, users can simply query the latest version or select only records where `data_status = 'final'`. This approach preserves historical information while ensuring that reports use the latest official data.

## E4. Schema changes and pipeline resilience

I would design the pipeline to **fail loudly**. The Python script would validate the expected schema by checking both the column names and the number of columns before processing the data. For example, a simple validation using `assert` can detect unexpected schema changes. If the portal changes the schema in a future release, the pipeline should stop immediately and notify the data team. Allowing the pipeline to continue while ignoring unexpected schema changes could silently introduce incorrect data into the warehouse and lead to inaccurate analysis.