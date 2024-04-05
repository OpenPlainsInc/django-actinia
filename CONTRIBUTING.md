# Contributing to Django Extensions

There are many ways to contribute to the project. You may improve the documentation, address a bug, add some feature to the code or do something else. All sort of contributions are welcome.

## Development

To start development on this project, fork this repository and follow the following instructions.

```bash
# clone the forked repository
$ git clone YOUR_FORKED_REPO_URL
```

* Enter the directory

```bash
cd django-actinia/
```

* Add main GRASS GIS repository as "upstream" (use HTTPS URL):

```bash
git remote add upstream https://github.com/tomorrownow/django-actinia.git
```

* Your remotes now should be "origin" which is your fork and "upstream" which
  is this main GRASS GIS repository. You can confirm that using:

```bash
git remote -v
```

* You should see something like:

```bash
origin  git@github.com:your_GH_account/django-actinia.git (fetch)
origin  git@github.com:your_GH_account/django-actinia.git (push)
```

For the following workflow, it is important that
"upstream" points to the OSGeo/grass repository
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

```bash
# create a virtual environment
$ python3 -m venv venv
# activate the virtual environment
$ source venv/bin/activate
```

### Pre-Commit

To improve code quality install pre-commit to perform precommit checks before push code to GitHub.

```bash
# Install pre-commit
(venv) $ pip install pre-commit
# Run pre-commit install to setup the git hook scripts
(venv) $ pre-commit install
```

### Install Dependencies

```bash
# install django-extensions in development mode
(venv) $ pip install -e .
# install dependencies
(venv) $ pip install Django -r requirements-dev.txt

(venv) $ python manage.py runserver
```

### Build Package

```bash
# Build
python setup.py sdist

# Install
python -m pip install --user django-actinia/dist/django-grass-0.0.1a0.tar.gz

# Uninstall
python -m pip uninstall django-actinia
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
# install pytest
(venv) $ pip install pytest-django # `python manage.py test` or `make test` also work
(venv) $ pytest # `python manage.py test` or `make test` also
```

To run tests against all supported `python` and `django` versions, you may run:

```bash
# install dependency
(venv) $ pip install tox
# run tests
(venv) $ tox
```

### Documentation

The project uses the Numpy Docstring standard to document code and is build using sphinx.
To generate documentation you may run the following commands:

```bash
# install dependency
(venv) $ pip install sphinx
# build new docs from source
(venv) $ sphinx-apidoc -f -o docs/source actina/
# Generate new site from docs
(venv) $ sphinx-build -b html docs/source/ docs/build/html
