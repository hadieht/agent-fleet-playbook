---
name: cloud-infra-security
description: Use to review or design cloud and infrastructure configuration for security, covering IAM and identities, network exposure, storage, encryption, secrets, logging, Kubernetes and infrastructure-as-code (Terraform, Bicep, CloudFormation, Helm). Only for environments the requester owns or is authorized to assess. Don't use for application code (use secure-code-review).
---

# Cloud and infrastructure security

## Iron law
> **Least privilege, no public exposure by default, and everything as reviewed code.** If a resource was clicked together in a console, it's unreviewed.

## Procedure
1. **Inventory from code:** read the IaC (Terraform/OpenTofu, Bicep/ARM, CloudFormation/CDK, Pulumi, Helm, k8s manifests). Note anything that exists only in the console as a finding ("drift / unmanaged").
2. **Run scanners as leads:** `checkov -d .`, `trivy config .`, `kubescape scan`, `tflint`, and the cloud provider's security center or posture findings if you have access. Triage hits (skill `security-finding-triage`).
3. **Review the areas below manually.** Scanners miss intent, like "this bucket is public on purpose, but contains PII".
4. **Rank findings** by exposure × data sensitivity × privilege.

## Review areas

### Identity and access
- [ ] No wildcard actions or resources (`"Action": "*"`, `Owner`/`Contributor` at subscription scope) for workloads or CI
- [ ] Workloads use managed or workload identities (managed identity, IRSA, workload identity federation), not long-lived keys
- [ ] CI/CD authenticates via OIDC federation; no static cloud keys in CI secrets
- [ ] Human access via SSO + MFA; break-glass accounts monitored; no shared accounts
- [ ] Privilege escalation paths: can a role pass roles, create keys, or edit its own policy?
- [ ] Unused identities, keys and permissions removed (access analyzer / last-used data)

### Network exposure
- [ ] No `0.0.0.0/0` (or `*`) inbound to SSH 22, RDP 3389, databases (1433, 3306, 5432, 6379, 27017, 9200), admin panels
- [ ] Databases, caches and queues on private networks or private endpoints; public access disabled
- [ ] Ingress through a load balancer or WAF with TLS; HTTP redirected to HTTPS
- [ ] Egress restricted where feasible (limits exfiltration and SSRF impact)
- [ ] Instance metadata hardened (e.g. AWS IMDSv2 required)

### Data
- [ ] Storage buckets and containers private; no anonymous or public listing; public access blocks on
- [ ] Encryption at rest (provider-managed or customer-managed keys for sensitive data); TLS in transit, including internal
- [ ] Backups enabled, encrypted, tested for restore, and protected from deletion (immutability, soft delete)
- [ ] PII and regulated data locations known; retention policies set

### Secrets
- [ ] Secrets in a vault (Key Vault, Secrets Manager, Vault), referenced by identity, not stored in IaC variables, state files, container env in manifests, or repo
- [ ] IaC state files stored encrypted with restricted access (state often contains secrets)
- [ ] Rotation configured for keys and passwords

### Logging and detection
- [ ] Control-plane audit logs on (CloudTrail, Azure Activity Log, GCP Audit Logs) and shipped to a protected account or workspace
- [ ] Data-plane logs for sensitive stores; flow logs for critical networks
- [ ] Alerts for root/global-admin use, IAM changes, public exposure changes, disabled logging

### Kubernetes
- [ ] RBAC least privilege; no workloads bound to `cluster-admin`; service account tokens not auto-mounted unless needed
- [ ] Pod security: `runAsNonRoot`, `readOnlyRootFilesystem`, no `privileged`, no `hostPath`/`hostNetwork`/`hostPID`, capabilities dropped (Pod Security Standards "restricted")
- [ ] NetworkPolicies default-deny with explicit allows
- [ ] Images from trusted registries, pinned by digest, scanned; admission control enforcing policy
- [ ] Secrets via an external secret operator or CSI driver; etcd encryption on
- [ ] API server not public, or restricted by IP and auth

### Resilience
- [ ] Resource limits and quotas; autoscaling bounds (cost-DoS)
- [ ] Multi-zone for critical services; tested disaster recovery

## Output format
```
## Scope            # accounts/subscriptions/clusters/IaC paths reviewed
## Findings
| severity | resource (file:line) | issue | exposure | fix (IaC diff) |
## Drift / unmanaged resources
## Positive controls observed
## Not reviewed
```
