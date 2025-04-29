FROM mundialis/actinia-core:6.0.0
# actinia-core and plugins installation
WORKDIR /build

ARG PLUGIN_VERSION=0.3.1
ARG WHEEL_NAME=actinia_statistic_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia_statistic_plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ARG PLUGIN_VERSION=0.2.1
ARG WHEEL_NAME=actinia_satellite_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia_satellite_plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ARG PLUGIN_VERSION=1.0.4
ARG WHEEL_NAME=actinia_metadata_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-metadata-plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ARG PLUGIN_VERSION=2.8.0
ARG WHEEL_NAME=actinia_module_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-module-plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ARG PLUGIN_VERSION=0.3.1
ARG WHEEL_NAME=actinia_stac_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-stac-plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ARG PLUGIN_VERSION=1.1.1
ARG WHEEL_NAME=actinia_tiling_plugin-${PLUGIN_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-tiling-plugin/releases/download/${PLUGIN_VERSION}/${WHEEL_NAME}

ENV ACTINIA_API_VERSION=3.7.0
ARG WHEEL_NAME=actinia_api-${ACTINIA_API_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-api/releases/download/${ACTINIA_API_VERSION}/${WHEEL_NAME}

# ARG WHEEL_NAME=actinia_core-${ACTINIA_CORE_VERSION}-py2.py3-none-any.whl
ENV ACTINIA_CORE_VERSION=6.0.0
ARG WHEEL_NAME=actinia_core-${ACTINIA_CORE_VERSION}-py3-none-any.whl
RUN curl -L --output /build/${WHEEL_NAME} \
    https://github.com/actinia-org/actinia-core/releases/download/${ACTINIA_CORE_VERSION}/${WHEEL_NAME}

# Install actinia-core and plugins
# Difference to `pip3 install /build/*`: Loop uses already installed
# dependencies while installing in bulk will update dependencies, even
# though older ones are already installed.
RUN for i in /build/*; do pip3 install $i; done

# Duplicate install actinia_core requirements. They are already included
# in alpine-build / alpine-runtime images, but check for updates here.
# https://raw.githubusercontent.com/actinia-org/actinia-core/4.11.0/requirements.txt
# RUN pip3 install -r https://raw.githubusercontent.com/actinia-org/actinia_core/${ACTINIA_CORE_VERSION}/requirements.txt

# Copy actinia config file and start scripts + set needed envs
COPY actinia.cfg /etc/default/actinia
