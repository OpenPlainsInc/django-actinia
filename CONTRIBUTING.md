# Contributing to Django Extensions

There are many ways to contribute to the project. You may improve the documentation, address a bug, add some feature to the code or do something else. All sort of contributions are welcome.

## Development

To start development on this project, fork this repository and follow the following instructions.

```bash
# clone the forked repository
$ git clone YOUR_FORKED_REPO_URL
```

 Enter the directory

```bash
cd django-actinia/
```

* Add main django-actinia repository as "upstream" (use HTTPS URL):

```bash
git remote add upstream https://github.com/openplainsinc/django-actinia.git
```

* Your remotes now should be "origin" which is your fork and "upstream" which
  is this main django-actinia repository. You can confirm that using:

```bash
git remote -v
```

* You should see something like:

```bash
origin  git@github.com:your_GH_account/django-actinia.git (fetch)
origin  git@github.com:your_GH_account/django-actinia.git (push)
```

For the following workflow, it is important that
"upstream" points to the OpenPlainsInc/django-actinia repository
and "origin" to your fork
(although generally, the naming is up to you).

### Update before creating a feature branch

* Make sure your are using the _main_ branch to create the new branch:

```bash
git checkout main
```

* Download updates from all branches from the _upstream_ remote:

```bash
git fetch upstream
```

* Update your local _main_ branch to match the _main_ branch
  in the _upstream_ repository:

```bash
git rebase upstream/main
```

Notably, you should not make commits to your local main branch,
so the above is then just a simple update (and no actual
rebase or merge happens).

### Creating a new feature branch

Now you have updated your local _main_ branch, you can create a festure branch based on it.

* Create a new feature branch and switch to it

```bash
git checkout -b new-feature
```

## Set up your python env

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Install it first:

```bash
# Install uv (macOS/Linux)
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then sync the project environment (uv creates and manages the virtual environment automatically):

```bash
$ uv sync --all-groups
```

### Pre-Commit

To improve code quality install pre-commit to perform precommit checks before push code to GitHub.
This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
# Run pre-commit install to setup the git hook scripts
$ uv run pre-commit install

# Run ruff manually
$ uv run ruff check .
$ uv run ruff format .
```

### Install Dependencies

```bash
# Install the package in development mode with all dependencies
$ uv sync --all-groups

# Run the development server
$ uv run python manage.py runserver
```

### Build Package

```bash
# Build
$ uv build

# Install locally
$ uv pip install dist/django_grass-0.0.1a0.tar.gz

# Uninstall
$ uv pip uninstall django-actinia
```

### Testing

Start the test server:

```bash
docker compose --env-file .test.env --file docker-compose-test.yml up

# or run to rebuild the images
docker compose --env-file .test.env --file docker-compose-test.yml build <container_name> --no-cache

# Run tests
docker compose --env-file .test.env --file docker-compose-test.yml exec api python manage.py test
```

To run tests against a particular `python` and `django` version installed inside your virtual environment, you may use:

```bash
$ uv run python manage.py test
# or
$ uv run pytest
```

To run tests against all supported `python` and `django` versions, you may run:

```bash
$ uv run tox
```

### Documentation

The project uses the Numpy Docstring standard to document code and is build using sphinx.
To generate documentation you may run the following commands:

```bash
# build new docs from source
$ uv run sphinx-apidoc -f -o docs/source actinia/
# Generate new site from docs
$ uv run sphinx-build -b html docs/source/ docs/build/html
