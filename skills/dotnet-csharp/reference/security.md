# .NET security: sinks, safe patterns, review checks

Use with skill `secure-code-review`. For each sink, ask: **can untrusted input reach it?**

| Risk (CWE) | Dangerous in .NET | Safe pattern |
|---|---|---|
| SQL injection (CWE-89) | `new SqlCommand("… " + input)`, `FromSqlRaw($"… {input}")`, `ExecuteSqlRaw` with concatenation, Dapper with string-built SQL | Parameters (`@id`), EF LINQ, `FromSql($"…{id}")` / `ExecuteSql($"…")` (parameterized), Dapper with anonymous params |
| Command injection (CWE-78) | `Process.Start("cmd", "/c " + input)`, `UseShellExecute = true` with user data | Avoid the shell; `ProcessStartInfo` with `ArgumentList.Add(...)`; allow-list commands and arguments |
| Path traversal (CWE-22) | `Path.Combine(root, userPath)`. **Note: if `userPath` is absolute, `Path.Combine` returns `userPath` and ignores `root`** | `var full = Path.GetFullPath(Path.Combine(root, name)); if (!full.StartsWith(Path.GetFullPath(root) + Path.DirectorySeparatorChar, StringComparison.Ordinal)) reject;` Prefer generated file names; never trust uploaded names |
| Insecure deserialization (CWE-502) | `BinaryFormatter` (removed in .NET 9; flag any use in older code), `NetDataContractSerializer`, `SoapFormatter`, `LosFormatter`, Newtonsoft `TypeNameHandling` ≠ `None`, `JavaScriptSerializer` with type resolvers | `System.Text.Json` with concrete types; for polymorphism, `[JsonDerivedType]` allow-lists |
| XXE (CWE-611) | `XmlDocument` / `XmlTextReader` with `XmlResolver` set, `DtdProcessing.Parse` on untrusted XML | Defaults in modern .NET are safe; keep `XmlResolver = null` and `DtdProcessing = Prohibit` |
| XSS (CWE-79) | `Html.Raw(userInput)`, `MarkupString` in Blazor, building HTML strings, unencoded JSON inside `<script>` | Razor auto-encoding; `HtmlEncoder.Default.Encode`; a sanitizer (e.g. HtmlSanitizer) for rich text; Content-Security-Policy header |
| Open redirect (CWE-601) | `Redirect(returnUrl)` | `LocalRedirect(returnUrl)` or `Url.IsLocalUrl(returnUrl)` check |
| SSRF (CWE-918) | `httpClient.GetAsync(userSuppliedUrl)` | Allow-list hosts and schemes; resolve and block private, loopback and link-local IP ranges (including after redirects); disable auto-redirect or re-validate |
| ReDoS (CWE-1333) | `new Regex(pattern)` on untrusted input with backtracking | Timeout (`TimeSpan.FromMilliseconds(100)`) or `RegexOptions.NonBacktracking`; never let users supply patterns |
| Mass assignment (CWE-915) | Binding request bodies directly to EF entities | Input DTOs with only allowed fields; map explicitly |
| IDOR / BOLA (CWE-639) | `db.Orders.FindAsync(id)` without an owner check | Filter by owner/tenant in the query (`Where(o => o.Id == id && o.TenantId == tenant)`) or resource-based authorization |
| Missing authz (CWE-862) | New endpoint without `[Authorize]` / `RequireAuthorization` | Fallback policy requiring an authenticated user; explicit `AllowAnonymous` |
| Weak crypto (CWE-327/328) | `MD5`, `SHA1`, `DES`, `TripleDES`, `RC2`, AES-ECB, custom crypto, `System.Random` for tokens | `RandomNumberGenerator.GetBytes` / `GetInt32`; `AesGcm`; SHA-256+ for integrity; HMAC for signatures |
| Password storage (CWE-916) | Plain hashes (`SHA256(password)`) | `PasswordHasher<TUser>` (ASP.NET Core Identity) or `Rfc2898DeriveBytes.Pbkdf2` with SHA-256 and a high iteration count, or Argon2 via a vetted library |
| Timing attacks (CWE-208) | `==` comparing MACs or tokens | `CryptographicOperations.FixedTimeEquals` |
| Secrets in code (CWE-798) | Connection strings and keys in `appsettings.json`, source, tests | User Secrets (dev), Azure Key Vault / AWS Secrets Manager (prod), managed identities |
| Sensitive logging (CWE-532) | Logging tokens, passwords, full request bodies, PII | Log IDs, not payloads; redaction (`Microsoft.Extensions.Compliance.Redaction`) |
| Info exposure (CWE-209) | `UseDeveloperExceptionPage` in prod; returning `ex.Message` | Problem Details with generic text; details only in logs |
| CSRF (CWE-352) | Cookie auth + state-changing endpoints without antiforgery | Antiforgery tokens; `SameSite` cookies; token auth for APIs |
| JWT misconfig (CWE-347) | `ValidateLifetime = false`, `ValidateIssuerSigningKey = false`, accepting `alg: none` | Keep validation flags on; pin algorithms; short lifetimes; rotate keys |
| CORS misconfig | `AllowAnyOrigin()` + `AllowCredentials()`, reflecting any `Origin` | Explicit origin list |
| Dependency confusion | Multiple NuGet sources without mapping | `packageSourceMapping` in `nuget.config`; reserved package-ID prefixes |

## Tooling
- Enable the .NET analyzers with security rules (`<AnalysisLevel>latest-recommended</AnalysisLevel>`) and review CA2100, the CA3xxx injection rules and the CA5xxx crypto/config rules.
- SAST: CodeQL (C#) or Semgrep rulesets for C#; treat findings with skill `security-finding-triage`.
- Dependencies: `dotnet list package --vulnerable --include-transitive`; NuGet Audit in restore (`<NuGetAudit>true</NuGetAudit>`, `<NuGetAuditMode>all</NuGetAuditMode>`).
- Secrets: `gitleaks` in CI and pre-commit.
- Headers: HSTS, CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, frame-ancestors via CSP.
