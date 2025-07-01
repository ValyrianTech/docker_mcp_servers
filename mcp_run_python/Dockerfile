FROM denoland/deno:debian-2.3.7

# Install necessary dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    curl \
    unzip \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for running the application
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

# Create node_modules directory and set permissions
RUN mkdir -p /home/appuser/app/node_modules && chown -R appuser:appuser /home/appuser

# Switch to non-root user
USER appuser

# Set environment variables
ENV DENO_DIR=/home/appuser/.deno
ENV PATH="${DENO_DIR}/bin:${PATH}"
ENV DOCKER_CONTAINER=true

# Create Python virtual environment and install dependencies
RUN python3 -m venv /home/appuser/venv
ENV PATH="/home/appuser/venv/bin:${PATH}"
RUN pip install --no-cache-dir mcp-python-client fastmcp

# Warm up by downloading and caching the Python standard library and MCP package
RUN deno run --allow-net --allow-read --allow-write=node_modules --allow-env --allow-run --node-modules-dir \
    jsr:@pydantic/mcp-run-python warmup

# Copy the proxy server script
COPY --chown=appuser:appuser proxy_server.py /home/appuser/app/

# Expose the proxy server port
EXPOSE 8080

# Set the default command to run the proxy server
CMD ["python3", "proxy_server.py"]