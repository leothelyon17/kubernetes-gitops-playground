# GitHub MCP Server Chart (Work in progress 🚧)

## Introduction

[Helm](https://helm.sh) chart for deploying [`github-mcp-server`](https://github.com/github/github-mcp-server) on Kubernetes.

## Overview

This chart provides a simple way to deploy GitHub's MCP server on Kubernetes.
It's intended as a minimal starting point. You may need to customize configuration (environment variables,
secrets, volumes, etc.) for your use case or production needs.

## Prerequisites

- Kubernetes cluster (v1.19+ recommended)
- [Helm 3](https://helm.sh/docs/intro/install/) installed

## Disclaimer

This chart is community-maintained and not officially supported by GitHub.
Use in production at your own risk!
