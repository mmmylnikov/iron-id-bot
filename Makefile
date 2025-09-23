# DEV

style_wps:
	flake8 . --select=WPS

style_ruff:
	ruff check .

format_ruff:
	ruff format .

style:
	make format_ruff style_ruff style_wps

types:
	mypy .

check:
	make style types

test:
	pytest


# CI/CD (dev)

actci:
	act -W ".github/workflows/ci.yml"


# CORE

VERSION := $(shell grep -m1 '^version *= *' pyproject.toml | sed -E 's/version *= *["'\'']([^"'\'']+)["'\'']/\1/')

bot:
	uv run bot.py

build:
	docker build . --tag ghcr.io/mmmylnikov/iron-id-bot:$(VERSION) --platform linux/amd64

push:
	docker push ghcr.io/mmmylnikov/iron-id-bot:$(VERSION)
