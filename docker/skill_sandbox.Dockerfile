FROM python:3.11-slim
RUN useradd -u 1000 -m sandboxuser
USER 1000
WORKDIR /tmp/sandbox
# No pip installs in Dockerfile — skills get only stdlib
# Additional packages can be installed per-skill in a requirements step
# that runs inside the container before the skill code
