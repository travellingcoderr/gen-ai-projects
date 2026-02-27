#!/usr/bin/env python3
"""Generate a root-level Postman collection from FastAPI routes in all projects.

Outputs:
- postman/postman-template.json
- postman/gen-ai-projects.postman_collection.json
"""

from __future__ import annotations

import argparse
import ast
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


def _base_url_var(project: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in project)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return f"{cleaned.strip('_')}_base_url"


@dataclass
class Endpoint:
    project: str
    route_module: str
    route_file: Path
    function_name: str
    method: str
    prefix: str
    path: str
    full_path: str
    tags: list[str]


def _normalize_path(prefix: str, path: str) -> str:
    left = (prefix or "").strip()
    right = (path or "").strip()

    if not left.startswith("/"):
        left = "/" + left if left else ""
    if right and not right.startswith("/"):
        right = "/" + right

    combined = f"{left}{right}" or "/"
    while "//" in combined:
        combined = combined.replace("//", "/")
    if len(combined) > 1 and combined.endswith("/"):
        combined = combined[:-1]
    return combined


def _parse_main(main_file: Path) -> list[tuple[str, str, list[str]]]:
    text = main_file.read_text(encoding="utf-8")
    tree = ast.parse(text)

    route_alias_to_module: dict[str, str] = {}
    includes: list[tuple[str, str, list[str]]] = []

    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("app.api.routes."):
                module = node.module.split(".")[-1]
                for alias in node.names:
                    if alias.name == "router":
                        route_alias_to_module[alias.asname or alias.name] = module

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "include_router":
            continue

        if not node.args:
            continue
        first = node.args[0]
        if not isinstance(first, ast.Name):
            continue

        prefix = ""
        tags: list[str] = []
        for kw in node.keywords:
            if kw.arg == "prefix" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                prefix = kw.value.value
            if kw.arg == "tags" and isinstance(kw.value, ast.List):
                tags = [elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant) and isinstance(elt.value, str)]

        alias_name = first.id
        module = route_alias_to_module.get(alias_name)
        if module:
            includes.append((module, prefix, tags))

    return includes


def _parse_route_file(
    project: str,
    route_module: str,
    route_file: Path,
    prefix: str,
    tags: list[str],
) -> list[Endpoint]:
    text = route_file.read_text(encoding="utf-8")
    tree = ast.parse(text)
    endpoints: list[Endpoint] = []

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Attribute):
                continue
            if not isinstance(decorator.func.value, ast.Name):
                continue
            if decorator.func.value.id != "router":
                continue

            method = decorator.func.attr.lower()
            if method not in HTTP_METHODS:
                continue

            path = ""
            if decorator.args and isinstance(decorator.args[0], ast.Constant) and isinstance(decorator.args[0].value, str):
                path = decorator.args[0].value

            endpoints.append(
                Endpoint(
                    project=project,
                    route_module=route_module,
                    route_file=route_file,
                    function_name=node.name,
                    method=method.upper(),
                    prefix=prefix,
                    path=path,
                    full_path=_normalize_path(prefix, path),
                    tags=tags,
                )
            )

    return endpoints


def discover_endpoints(root: Path) -> list[Endpoint]:
    endpoints: list[Endpoint] = []

    for main_file in sorted(root.glob("*/backend/app/main.py")):
        project = main_file.parts[-4]
        includes = _parse_main(main_file)
        for module, prefix, tags in includes:
            route_file = main_file.parent / "api" / "routes" / f"{module}.py"
            if route_file.exists():
                endpoints.extend(_parse_route_file(project, module, route_file, prefix, tags))

    endpoints.sort(key=lambda e: (e.project, e.route_module, e.full_path, e.method))
    return endpoints


def build_template(root: Path, endpoints: list[Endpoint]) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    for ep in endpoints:
        project = grouped.setdefault(
            ep.project,
            {
                "project": ep.project,
                "base_url_variable": _base_url_var(ep.project),
                "endpoints": [],
            },
        )
        project["endpoints"].append(
            {
                "method": ep.method,
                "path": ep.full_path,
                "prefix": ep.prefix,
                "route_module": ep.route_module,
                "route_file": str(ep.route_file.relative_to(root)),
                "function": ep.function_name,
                "tags": ep.tags,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": root.name,
        "projects": [grouped[key] for key in sorted(grouped.keys())],
    }


def _add_folder(items: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for item in items:
        if item.get("name") == name and "item" in item:
            return item
    folder: dict[str, Any] = {"name": name, "item": []}
    items.append(folder)
    return folder


def _request_item(base_url_var: str, ep: Endpoint, root: Path) -> dict[str, Any]:
    raw_url = f"{{{{{base_url_var}}}}}{ep.full_path}"
    path_parts = [p for p in ep.full_path.strip("/").split("/") if p]
    request: dict[str, Any] = {
        "method": ep.method,
        "header": [{"key": "Content-Type", "value": "application/json"}] if ep.method != "GET" else [],
        "url": {
            "raw": raw_url,
            "host": [f"{{{{{base_url_var}}}}}"],
            "path": path_parts,
        },
        "description": f"Source: {ep.route_file.relative_to(root)}::{ep.function_name}",
    }

    if ep.method in {"POST", "PUT", "PATCH"}:
        request["body"] = {
            "mode": "raw",
            "raw": "{\n  \"query\": \"replace me\"\n}",
            "options": {"raw": {"language": "json"}},
        }

    return {
        "name": f"{ep.method} {ep.full_path}",
        "request": request,
        "response": [],
    }


def build_collection(root: Path, endpoints: list[Endpoint]) -> dict[str, Any]:
    collection_items: list[dict[str, Any]] = []
    project_names = sorted({ep.project for ep in endpoints})

    for project in project_names:
        project_folder = _add_folder(collection_items, project)
        project_eps = [ep for ep in endpoints if ep.project == project]

        for ep in project_eps:
            # Mirror folder structure under each project for API route ownership clarity.
            current = project_folder
            for part in ["backend", "app", "api", "routes", ep.route_module]:
                current = _add_folder(current["item"], part)
            current["item"].append(_request_item(_base_url_var(project), ep, root))

    variables = [
        {"key": _base_url_var(project), "value": "http://localhost:8000", "type": "string"}
        for project in project_names
    ]

    return {
        "info": {
            "name": f"{root.name} - Auto Generated APIs",
            "_postman_id": str(uuid.uuid5(uuid.NAMESPACE_URL, str(root))),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "description": "Auto-generated from FastAPI route files. Do not edit manually.",
        },
        "item": collection_items,
        "variable": variables,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--template", type=Path, default=Path("postman/postman-template.json"))
    parser.add_argument(
        "--collection",
        type=Path,
        default=Path("postman/gen-ai-projects.postman_collection.json"),
    )
    args = parser.parse_args()

    root = args.root.resolve()
    endpoints = discover_endpoints(root)

    template = build_template(root, endpoints)
    collection = build_collection(root, endpoints)

    template_path = (root / args.template).resolve() if not args.template.is_absolute() else args.template
    collection_path = (
        (root / args.collection).resolve() if not args.collection.is_absolute() else args.collection
    )

    write_json(template_path, template)
    write_json(collection_path, collection)

    print(f"Generated template: {template_path}")
    print(f"Generated collection: {collection_path}")
    print(f"Discovered endpoints: {len(endpoints)}")


if __name__ == "__main__":
    main()
