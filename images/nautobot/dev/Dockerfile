# Accept args used in FROM (must be before any FROM)
ARG BASE_VERSION
ARG PYTHON_VER=3.11
ARG APPS

# Base stage
FROM ghcr.io/nautobot/nautobot:${BASE_VERSION}-py${PYTHON_VER} AS nautobot-base

USER 0

RUN sleep 10 && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    pip --no-cache-dir install --upgrade pip wheel

# Builder stage
FROM ghcr.io/nautobot/nautobot-dev:${BASE_VERSION}-py${PYTHON_VER} AS builder

CMD ["nautobot-server", "runserver", "0.0.0.0:8080", "--insecure"]

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

# If present in the build context, this will be copied
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# These COPY sources must exist relative to the build context directory
# (remove or adjust if they don't live under this folder)
COPY command_mappers/paloalto_panos.yml \
     /usr/local/lib/python${PYTHON_VER}/site-packages/nautobot_device_onboarding/command_mappers/
COPY command_mappers/bigip_f5.yml \
     /usr/local/lib/python${PYTHON_VER}/site-packages/nautobot_device_onboarding/command_mappers/

COPY parsers/ttp/paloalto_panos_show_system_info.ttp \
     /usr/local/lib/python${PYTHON_VER}/site-packages/nautobot_device_onboarding/parsers/ttp/
COPY parsers/ttp/bigip_f5_get_facts.ttp \
     /usr/local/lib/python${PYTHON_VER}/site-packages/nautobot_device_onboarding/parsers/ttp/

RUN pip install --no-cache-dir "napalm-f5 @ git+https://github.com/jdrew82/napalm-f5@feat-update_rest"

WORKDIR /source

# Final image
FROM nautobot-base AS nautobot

# Re-declare args for use in this stage
ARG BASE_VERSION
ARG APPS
ARG PYTHON_VER=3.11

# Metadata
LABEL nautobot.base.version="${BASE_VERSION}" \
      nautobot.apps="${APPS}"
LABEL org.opencontainers.image.description="Nautobot image with optional plugins and tools"

# Bring artifacts from builder
COPY --from=builder /opt/nautobot /opt/nautobot
COPY --from=builder /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN pyuwsgi --cflags | sed 's/ /\n/g' | grep -e "^-DUWSGI_SSL$"

USER nautobot
