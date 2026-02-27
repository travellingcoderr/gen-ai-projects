# gen-ai-projects
All generative AI projects

This will host different projects catering to various use cases.

** Use Cases ** 

Customer Support Agent
project: [customer-support-agent](customer-support-agent/README.md)

## Postman Auto-Generation

This repo includes a root-level Postman generator that scans all FastAPI route files and creates:

- Template metadata: `postman/postman-template.json`
- Single merged Postman collection: `postman/gen-ai-projects.postman_collection.json`

Run locally:

```bash
python3 tools/postman/generate_postman_collection.py
```

Automation:

- Workflow: `.github/workflows/postman-autogen.yml`
- Triggered when `backend/app/main.py` or `backend/app/api/routes/**/*.py` changes
- On `push`: regenerates and auto-commits updated Postman JSON files
- On `pull_request`: regenerates and fails if checked-in JSON is stale
