# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **reusable Django app** (package `grass/`, project name `django_grass`) that models actinia
objects in the Django ORM (`grass/models/`: `Location`, `Mapset`, `Layer`, `ActiniaUser`,
`Permission`) and talks to an [actinia](https://actinia.mundialis.de/) instance through
`actinia-python-client`. Django + DRF + Celery + Channels, drf-spectacular for the schema.

It is a library meant to be consumed by an application layer; it does not implement a product
API itself. Current working branch: `upgrade-to-actinia-6.0.0`.

## State of the views

`grass/views/general/` (locations, mapsets) and the user viewset are implemented.
`grass/views/raster/`, `grass/views/vector/`, and `grass/views/imagery/` are placeholders
(license-header `__init__.py` only), not yet implemented. New views should use
`permission_classes = [IsAuthenticated]`.

## Commands

CI (`.github/workflows/django_tests.yml`) runs Django's test runner on Python 3.10 against
Postgres with GDAL installed:

```bash
pip install -r requirements.txt && pip install GDAL==$(gdal-config --version)
python manage.py migrate
python manage.py test
```

Tests that hit actinia expect the compose stack: `docker compose -f docker-compose-test.yml up`
(PostGIS + actinia-core built from `actinia/`). `tox.ini` also defines pytest-style envs
(`testpaths = ./tests`, settings `test_api/settings`) plus flake8/precommit envs. Lint CI
(`pylint_black.yml`) runs flake8 and black; run `black .` and `flake8` before committing.

Test environment variables are documented in `.test.env.example`; copy to `.test.env` locally
(git-ignored) and fill in values.

## Conventions

- GPL license headers on source files; keep them on new files.
- The `venv/`, `build/`, `dist/`, `actinia-core-data/`, and `valkey_data/` dirs are local
  artifacts, not source.
