#!/usr/bin/env python3
"""Build the WebSpeak 1Panel local app from its source spec (standard library only)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SPEC = Path(__file__).with_name("webspeak-appspec.json")
LANGUAGES = ("en", "es-es", "ja", "ms", "pt-br", "ru", "ko", "zh-Hant", "zh", "tr")
WEB_PORT_LABEL = {
    "en": "Web UI Port",
    "es-es": "Puerto web",
    "ja": "Web UIポート",
    "ms": "Port Web UI",
    "pt-br": "Porta da Web UI",
    "ru": "Порт веб-интерфейса",
    "ko": "웹 UI 포트",
    "zh-Hant": "Web UI 埠",
    "zh": "Web UI 端口",
    "tr": "Web UI Bağlantı Noktası",
}


def scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    safe = re.fullmatch(r"[A-Za-z0-9_./:@%+,-]+", text)
    special = text.lower() in {"true", "false", "null", "yes", "no", "on", "off"}
    if safe and not special:
        return text
    return json.dumps(text, ensure_ascii=False)


def yaml_lines(value: Any, indent: int = 0) -> list[str]:
    pad = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.extend(yaml_lines(item, indent + 2))
            else:
                lines.append(f"{pad}{key}: {scalar(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, subitem in item.items():
                    prefix = "- " if first else "  "
                    if isinstance(subitem, (dict, list)):
                        lines.append(f"{pad}{prefix}{key}:")
                        lines.extend(yaml_lines(subitem, indent + 4))
                    else:
                        lines.append(f"{pad}{prefix}{key}: {scalar(subitem)}")
                    first = False
            else:
                lines.append(f"{pad}- {scalar(item)}")
    return lines


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text("\n".join(yaml_lines(value)) + "\n", encoding="utf-8")


def description_map(description: dict[str, str]) -> dict[str, str]:
    return {lang: description.get(lang) or description["en"] for lang in LANGUAGES}


def readme(spec: dict[str, Any], lang: str) -> str:
    content = spec["readme"][lang]
    if lang == "zh":
        lines = ["## 产品介绍", "", f"**{spec['name']}** {content['introduction']}", "", "## 主要功能", ""]
        lines.extend(f"- **{feature['title']}**：{feature['description']}" for feature in content["features"])
    else:
        lines = ["## Introduction", "", f"**{spec['name']}** {content['introduction']}", "", "## Features", ""]
        lines.extend(f"- **{feature['title']}**: {feature['description']}" for feature in content["features"])
    return "\n".join(lines) + "\n"


def build(output: Path) -> tuple[Path, str, str]:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    tag = spec["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+-upstream\.\d+\.\d+\.\d+", tag):
        raise ValueError(f"version must be <fork-major.minor.patch>-upstream.<upstream-major.minor.patch>: {tag}")
    key = spec["key"]
    service = spec["services"][0]
    image = service["image"]
    if not image.endswith(f":{tag}"):
        raise ValueError(f"image tag does not match app version: {image}")
    app_dir = output / key
    version_dir = app_dir / tag
    if app_dir.exists():
        raise FileExistsError(f"refusing to overwrite {app_dir}")
    data_dir = version_dir / "data"
    scripts_dir = version_dir / "scripts"
    data_dir.mkdir(parents=True)
    scripts_dir.mkdir()
    (data_dir / ".gitkeep").touch()

    description = spec["description"]
    tags = spec["tags"]
    write_yaml(app_dir / "data.yml", {
        "name": spec["name"],
        "tags": tags,
        "title": spec["title"],
        "description": description["zh"],
        "additionalProperties": {
            "key": key,
            "name": spec["name"],
            "tags": tags,
            "shortDescZh": description["zh"],
            "shortDescEn": description["en"],
            "description": description_map(description),
            "type": spec["type"],
            "crossVersionUpdate": True,
            "limit": 0,
            "architectures": spec["architectures"],
            "website": spec["website"],
            "github": spec["github"],
            "document": spec["document"],
        },
    })
    write_yaml(version_dir / "data.yml", {
        "additionalProperties": {
            "formFields": [{
                "default": 3040,
                "envKey": "PANEL_APP_PORT_HTTP",
                "labelEn": WEB_PORT_LABEL["en"],
                "labelZh": WEB_PORT_LABEL["zh"],
                "label": WEB_PORT_LABEL,
                "required": True,
                "rule": "paramPort",
                "type": "number",
            }],
        },
    })
    write_yaml(version_dir / "docker-compose.yml", {
        "services": {
            "webspeak": {
                "image": image,
                "pull_policy": "always",
                "container_name": "${CONTAINER_NAME}",
                "restart": "always",
                "networks": ["1panel-network"],
                "ports": ["${PANEL_APP_PORT_HTTP}:3040", "40000-40099:40000-40099/udp"],
                "extra_hosts": ["host.docker.internal:host-gateway"],
                "volumes": service["volumes"],
                "labels": {"createdBy": "Apps"},
            },
        },
        "networks": {"1panel-network": {"external": True}},
    })
    for lang, filename in (("zh", "README.md"), ("en", "README_en.md")):
        (app_dir / filename).write_text(readme(spec, lang), encoding="utf-8")
    shutil.copyfile(ROOT / spec["logo"], app_dir / "logo.png")

    evidence = "\n".join(f"# - {item}" for item in spec["init_source_evidence"])
    owner = service["volume_permissions"][0]["owner"]
    if not re.fullmatch(r"\d+:\d+", owner):
        raise ValueError(f"invalid volume owner: {owner}")
    init_script = scripts_dir / "init.sh"
    init_script.write_text(
        "#!/bin/bash\n\n"
        f"# Generated from official installation evidence:\n{evidence}\n\n"
        "set -e\n"
        "if [ -d data ]; then\n"
        f"    chown -R {owner} data\n"
        "fi\n",
        encoding="utf-8",
    )
    init_script.chmod(0o755)
    return app_dir, tag, image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Directory that will receive webspeak/")
    args = parser.parse_args()
    app_dir, tag, image = build(args.output)
    print(f"package={app_dir}")
    print(f"version={tag}")
    print(f"image={image}")


if __name__ == "__main__":
    main()
