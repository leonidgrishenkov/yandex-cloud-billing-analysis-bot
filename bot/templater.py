from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def render_template(name: str, values: dict | None = None) -> str:
    if not values:
        values = {}

    template = _create_templater().get_template(name=name)

    return template.render(**values)


def _create_templater() -> Environment:
    if not getattr(_create_templater, "_env", None):
        _create_templater._env = Environment(
            loader=FileSystemLoader(
                searchpath=Path(__file__).parents[0] / "templates",
            )
        )
    return _create_templater._env
