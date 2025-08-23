ARG NAUTOBOT_VERSION=2.4.2
ARG PYTHON_VER=3.11
ARG APPS
FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VERSION}-py${PYTHON_VER} as nautobot-base

USER 0

RUN sleep 10 && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    pip --no-cache-dir install --upgrade pip wheel



FROM ghcr.io/nautobot/nautobot-dev:${NAUTOBOT_VERSION}-py${PYTHON_VER} as builder

CMD ["nautobot-server", "runserver", "0.0.0.0:8080", "--insecure"]

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

# COPY ../pyproject.toml ../poetry.lock /source/
# COPY ../plugins /source/plugins
# COPY ../packages /source/packages

# Install the nautobot project to include Nautobot
# RUN cd /source && \
#     poetry install --no-interaction --no-ansi && \
#     mkdir /tmp/dist && \
#     poetry export --without-hashes -o /tmp/dist/requirements.txt

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY /command_mappers/paloalto_panos.yml /usr/local/lib/python3.11/site-packages/nautobot_device_onboarding/command_mappers/
COPY /parsers/ttp/paloalto_panos_show_system_info.ttp /usr/local/lib/python3.11/site-packages/nautobot_device_onboarding/parsers/ttp/

RUN pip install --no-cache-dir "napalm-f5 @ git+https://github.com/jdrew82/napalm-f5@feat-update_rest"

# -------------------------------------------------------------------------------------
# Build Apps in plugins folder
# -------------------------------------------------------------------------------------
# RUN for plugin in /source/plugins/*; do \
#         cd $plugin && \
#         poetry build && \
#         cp dist/*.whl /tmp/dist; \
#     done

# COPY ../jobs /opt/nautobot/jobs
# COPY ../metrics /opt/nautobot/metrics
# COPY ./configuration/nautobot_config.py /opt/nautobot/nautobot_config.py

WORKDIR /source

###################################

# -------------------------------------------------------------------------------------
# Final Image
# -------------------------------------------------------------------------------------
FROM nautobot-base as nautobot

# Accept build arguments with defaults to ensure they are set in this stage.
ARG NAUTOBOT_VERSION
ARG APPS
ARG PYTHON_VER=3.11

# Add labels for metadata
LABEL nautobot.base.version="${NAUTOBOT_VERSION}" \
      nautobot.apps="${APPS}"
LABEL org.opencontainers.image.description ""

# Copy necessary files from the builder stage
COPY --from=builder /opt/nautobot /opt/nautobot
COPY --from=builder /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN pyuwsgi --cflags | sed 's/ /\n/g' | grep -e "^-DUWSGI_SSL$"

USER nautobot
