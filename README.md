# AOBP BFF Login Architecture Documentation

Architecture documents, security reviews, diagrams and supporting artifacts for AOBP SSO authentication and authorization using a Backend for Frontend (BFF).

## Start here

| Document set | Read online | Download PDF | Purpose |
| --- | --- | --- | --- |
| Centralized SSO and BFF architecture | [Markdown](docs/centralized-sso/AOBP_BFF_Centralized_SSO_Architecture.md) | [PDF](docs/centralized-sso/AOBP_BFF_Centralized_SSO_Architecture.pdf) | Generic Microservice 1/2 design, seven architecture/sequence/activity diagrams, Redis session sharing, refresh, relay, and nine attack points with mitigations |
| AWS EKS BFF architecture | [Markdown](docs/eks-bff/AOBP_BFF_Architecture_Design.md) | [PDF](docs/eks-bff/AOBP_BFF_Architecture_Design.pdf) | EKS deployment, BFF/gateway placement, login and request journeys, and security controls |
| Platform engineering specification | [Markdown](docs/platform/AOBP_Platform_Architecture_Design.md) | [PDF](docs/platform/AOBP_Platform_Architecture_Design.pdf) | Broader platform/API specification and deployment/integration guidance |
| Workflow approval example | [Step-by-step guide](docs/workflow/AODB_FLIGHT_DELAY_APPROVAL_STEP_BY_STEP_GUIDE.md) | — | AODB example with BFF authentication, backend authorization, verification steps and risk explanations |

These are separate document editions with different scope and depth. Read the diagrams with the document in the same folder; do not combine routing or policy assumptions from different editions without an architecture review. Proposed controls and verification procedures are not evidence that an implementation has passed security or runtime testing.

## Diagrams and editable sources

- [Centralized SSO PNG diagrams](docs/centralized-sso/images): seven images at 3,408 pixels wide.
- [Centralized SSO SVG diagrams](docs/centralized-sso/svg): scalable vector versions.
- [Editable Mermaid diagrams](docs/centralized-sso/diagram-source): sequence, architecture and activity sources.
- [EKS BFF diagrams](docs/eks-bff/diagrams): deployment, authentication, relay, refresh and attack points.
- [Platform diagrams](docs/platform/assets): architecture, login, requests, distributed refresh, EKS, partner integration and security boundaries.
- [Platform document generation scripts](docs/platform/scripts): source artifacts retained from the original package; environment-specific paths/dependencies may require adjustment.

## Complete packages

Original downloadable packages are retained unchanged:

- [Centralized SSO Markdown and diagrams](downloads/AOBP_BFF_Architecture_Markdown_and_Diagrams.zip)
- [EKS BFF architecture package](downloads/AOBP_BFF_Architecture_Package.zip)
- [Platform document and PNG package](downloads/AOBP_Architecture_Document_and_PNGs.zip)

For local Markdown viewing, clone/download the repository and preserve the folder structure so relative image links resolve. SVG and Mermaid sources support diagram maintenance and presentation reuse.

## Reference material

- [Original centralized SSO reference PDF](reference/AOBP_Centralized_SSO_Authentication.pdf)
- [Architecture implementation specification Word document](reference/AOBP_Architecture_Implementation_Specification.docx)

Reference files preserve earlier inputs/specifications. Review them against the relevant BFF design before implementing security-sensitive behaviour.

## Inventory and integrity

[ARTIFACTS.md](ARTIFACTS.md) lists every published artifact. [SHA256SUMS](SHA256SUMS) records content checksums, and [artifact-manifest.json](artifact-manifest.json) provides machine-readable paths, sizes and SHA-256 values.

The repository contains documentation and supporting diagram artifacts. Executable application code is maintained separately in [Auth2-BFF](https://github.com/renjithpta/Auth2-BFF).
