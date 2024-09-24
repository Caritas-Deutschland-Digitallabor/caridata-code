# This Dockerfile sets up a development environment for a full-stack application.
# It installs the necessary dependencies, including Python, Node.js, and Poetry.
# The Docker image is based on the "mcr.microsoft.com/devcontainers/base:jammy" image.

FROM mcr.microsoft.com/devcontainers/base:jammy

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode
ARG ROOT_USER=root
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.11
ARG NPM_GLOBAL=/usr/local/share/npm-global

# Set environment variables
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH=${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH
ENV PATH=${NPM_GLOBAL}/bin:${PATH}

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive \
    && echo "Installing dependencies" \
    && apt-get update \
    && apt-get install -y build-essential --no-install-recommends make \
    ca-certificates \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    pre-commit

# Install Node.js (v20.13.1) (and npm v10.5.2)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - \
    && sudo apt-get install -y nodejs

# Configure global npm install location
RUN \
    if ! cat /etc/group | grep -e "^npm:" > /dev/null 2>&1; then groupadd -r npm; fi \
    && usermod -a -G npm ${ROOT_USER} \
    && umask 0002 \
    && mkdir -p ${NPM_GLOBAL} \
    && touch /usr/local/etc/npmrc \
    && chown ${ROOT_USER}:npm ${NPM_GLOBAL} /usr/local/etc/npmrc \
    && chmod g+s ${NPM_GLOBAL} \
    && npm config -g set prefix ${NPM_GLOBAL} \
    && su ${ROOT_USER} -c "npm config -g set prefix ${NPM_GLOBAL}" \
    && su ${ROOT_USER} -c "umask 0002 && npm install -g eslint" \
    && npm cache clean --force > /dev/null 2>&1 \
    && sudo chown -R 1000:1000 "/home/vscode/.npm"

# Install Python and Poetry
USER vscode

RUN echo "Installing Python" \
    && echo "Step 1: Installing pyenv" \
    && curl https://pyenv.run | bash \
    && echo "Step 2: Installing Python ${PYTHON_VERSION}" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "Step 3: Setting global Python version to ${PYTHON_VERSION}" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "Step 4: Installing Poetry" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true
