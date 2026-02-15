# kubernetes-gitops-playground

GitOps repository for managing multi-environment Kubernetes infrastructure and applications, with Argo CD as the deployment controller and a mix of Helm, Kustomize overlays, and raw manifests.

## Overview

This repo currently manages:

- Base cluster lifecycle inputs for `lab` and `prod` environments (`clusters/`).
- Argo CD application definitions (`argocd-app-manifests/`).
- Application configs, Helm values, and Kustomize overlays (`apps/`).
- Platform add-ons and storage tooling (Traefik, MetalLB, cert-manager, Rook Ceph, External Secrets).
- MCP-related services (GitHub, GitLab, Plane, Vault MCP, MCP Inspector).
- Supporting automation with GitHub Actions and Ansible playbooks.

## Environment Model

Two primary environments are defined in-repo:

- `lab`: inventory and group vars in `clusters/lab/`, Argo project `home-lab`.
- `prod`: inventory and group vars in `clusters/prod/`, Argo project `prod-home`.

Primary environment/project files:

- `clusters/lab/hosts.yml`
- `clusters/prod/hosts.yml`
- `apps/argocd/lab/app-project.yml`
- `apps/argocd/prod/app-project.yml`

## Repository Layout

```text
.
├── apps/                          # App configs, overlays, values files
│   ├── argocd/                    # Argo CD AppProject + repo list per env
│   ├── <app>/values-*.yml         # Helm values for env-specific chart deploys
│   └── <app>/overlays/<env>/      # Kustomize overlays for app-specific resources
├── argocd-app-manifests/          # Argo CD Application manifests
│   ├── prod/*.yml                 # Prod app definitions
│   └── *-lab.yml                  # Existing lab app definitions
├── clusters/                      # Kubespray inventory/group vars per env
├── ansible/                       # Operational playbooks (restart, cleanup, certs)
├── helm-charts/                   # Local charts (for example slurpit, github-mcp-server)
├── images/                        # Docker build contexts for custom images
├── k8s-addons/                    # Add-on inventory/config
├── microceph/                     # MicroCeph inventory + vars
├── snapshots/                     # Snapshot create/restore var files
└── .github/workflows/             # Ops and provisioning workflows
```

## GitOps Delivery Pattern

This repo uses a hybrid Argo CD model:

- Helm chart source for upstream software.
- Git source in this repo for values files and overlays.
- Argo CD multi-source applications when chart + in-repo config are combined.

Examples:

- `argocd-app-manifests/prod/traefik.yml` uses Helm chart source + this repo as `$values`.
- `argocd-app-manifests/prod/vault-mcp-server.yml` deploys from in-repo Kustomize path only.

## Application Conventions

Most applications follow one of these patterns:

- Helm values only: values in `apps/<app>/values-<env>.yml`.
- Helm + overlay: values plus additional manifests in `apps/<app>/overlays/<env>/`.
- Overlay only (raw manifests): `apps/<app>/overlays/<env>/kustomization.yml` with Deployment/Service/IngressRoute/ExternalSecret resources.

Common overlay resources:

- `deployment.yml`
- `service.yml`
- `ingress-route.yml` (Traefik CRD)
- `external-secret*.yml` / `external-secrets*.yml`
- `kustomization.yml`

## MCP Services Managed Here

Current MCP-related deployments and ingress hosts:

| Service | Path | Ingress Host |
|---|---|---|
| GitHub MCP | `apps/github-mcp-server/overlays/prod` | `github-mcp.home.nerdylyonsden.io` |
| GitLab MCP | `apps/gitlab-mcp-server/overlays/prod` | `gitlab-mcp.home.nerdylyonsden.io` |
| Plane MCP | `apps/plane-mcp-server/overlays/prod` | `plane-mcp.home.nerdylyonsden.io` |
| Vault MCP | `apps/vault-mcp-server/overlays/prod` | `vault-mcp.home.nerdylyonsden.io` |
| Wiki.js MCP | `apps/wikijs-mcp-server/overlays/prod` | `wikijs-mcp.home.nerdylyonsden.io` |
| MCP Inspector UI | `apps/mcp-inspector/overlays/prod` | `mcp-inspector.home.nerdylyonsden.io` |
| MCP Inspector Proxy | `apps/mcp-inspector/overlays/prod` | `mcp-inspector-proxy.home.nerdylyonsden.io` |

Argo CD app manifests for MCP servers:

- `argocd-app-manifests/prod/vault-mcp-server.yml`
- `argocd-app-manifests/prod/wikijs-mcp-server.yml`

## Secrets and Configuration

Secret handling in app overlays is centered on External Secrets + Vault-backed stores.

- ExternalSecret resources are defined in each app overlay when needed.
- Example SecretStore reference: `mcp-servers-vault-backend` in MCP server manifests.
- Utility script `scripts/encrypt-secret.py` is used in workflows to encrypt GitHub environment secrets with repository public keys.

## Infrastructure and Ops Automation

Key GitHub Actions workflows (manual `workflow_dispatch` heavy):

- Cluster provisioning and Kubespray orchestration:
  - `.github/workflows/kubespray-cluster-create.yml`
  - `.github/workflows/kubespray-cluster-reset.yml`
  - `.github/workflows/kubespray-addon-pre.yml`
  - `.github/workflows/kubespray-addon-post.yml`
- Argo CD setup and repo registration:
  - `.github/workflows/install-argocd.yml`
  - `.github/workflows/add-argocd-repos.yml`
- Kubeconfig setup and access checks:
  - `.github/workflows/setup-kubectl-test-k8s-access.yml`
- Custom image build/push:
  - `.github/workflows/build-image-plane-mcp.yml`
  - `.github/workflows/build-image-nautobot.yml`
  - `.github/workflows/build-image-netbox.yml`

Operational Ansible playbooks:

- `ansible/restart-kube-services.yml`
- `ansible/cluster-cleanup-pb.yml`
- `ansible/update-k8s-certs-pb.yml`

## Common Workflows

### Add a New App Overlay

1. Create `apps/<app>/overlays/<env>/` with a `kustomization.yml` and required resources.
2. Add ingress and external secret resources if needed.
3. Add or update an Argo CD `Application` manifest under `argocd-app-manifests/`.
4. Commit and open PR.

### Add a Helm-Based App

1. Add `apps/<app>/values-<env>.yml`.
2. Create/update Argo CD `Application` manifest with Helm source and `$values` reference to this repo.
3. Add overlay resources only if extra K8s objects are required.

## Validation Commands

Use these commands locally before opening PRs:

```bash
# Kustomize render
kubectl kustomize apps/<app>/overlays/<env>

# Client-side validation
kubectl apply --dry-run=client -f apps/<app>/overlays/<env>

# Server-side validation against cluster
kubectl apply --dry-run=server -f apps/<app>/overlays/<env>

# YAML lint (repo has .yamllint config)
yamllint .
```

## Storage and Snapshot Notes

Snapshot var files are maintained in `snapshots/`:

- `snapshots/snapshot-creation-vars.yml`
- `snapshots/snapshot-restore-vars.yml`

Baseline snapshot names currently referenced:

- `baseline_kubernetes`
- `baseline_os`

MicroCeph inventory/vars live in `microceph/` for lab/prod.

## Current State and Cleanup Opportunities

This repo contains both newer and legacy patterns. You will see:

- Multi-source Argo applications and single-source applications.
- App manifests split between `argocd-app-manifests/prod/` and top-level `*-lab.yml`.
- Some manifests that still include inline template comments from initial scaffolding.

Recommended follow-up improvements:

- Standardize all Argo app manifests into per-environment subfolders.
- Normalize labels and naming across app overlays.
- Pin mutable container tags (`latest`) where still present.
