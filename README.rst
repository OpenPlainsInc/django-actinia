# django-actinia
A Django package to utilize [Actinia](https://actinia.mundialis.de/) REST API for GRASS GIS for distributed compuational analysis and modeling.

=====
Actinia
=====

Actinia is a Django app to that allows for easy integration of ACTINIA API for GRASS GIS into an existing Django project.

## Requirments

* django (>= 4.0)
* celery (>=5.2.6)
* django-rest-framework (>=3.13)
* django-rest-framework-gis (>=0.18)
* requests (>=2.27)

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "actinia" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'channels',
        'djnago.contrib.gis',
        'rest_framework',
        'rest_framework_gis',
        'actinia'
    ]

2. Add actinia postgis data to DATABASES in settings like this::

    DATABASES = {
        ...
        'actinia': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': actinia,
            'USER': actinia,
            'PASSWORD': actinia,
            'HOST': < host >, 
            'PORT': < port > # 5432
        }
    }

3. Add ACTINIA default user configuration to settings like this::

    ACTINIA = {
        'ACTINIA_USER': actinia-gdi, # default username 
        'ACTINIA_PASSWORD': actinia-gdi, # default username 
        'ACTINIA_VERSION': v3,
        'ACTINIA_BASEURL': < host:port >,
        'ACTINIA_LOCATION': nc_spm_08,
        'ACTINIA_MAPSET': PERMANENT
    }

4. Include the polls URLconf in your project urls.py like this::

    path('actinia/', include('actina.urls')),

5. Run ``python manage.py migrate`` to create the polls models.

6. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an actinia user, location, and mapset (you'll need the Admin app enabled).) for geospatial computation and modeling with GRASS GIS.