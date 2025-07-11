FROM denoland/deno:debian-2.3.7

# Install necessary dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    curl \
    unzip \
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

# Warm up by downloading and caching the Python standard library and MCP package
RUN deno run --allow-net --allow-read --allow-write=node_modules --allow-env --allow-run --node-modules-dir \
    jsr:@pydantic/mcp-run-python warmup

# Expose the SSE server port
EXPOSE 8080

# Set the default command to run the MCP Run Python server with SSE transport
CMD ["deno", "run", "-N", "-R=node_modules", "-W=node_modules", "--node-modules-dir=auto", \
     "jsr:@pydantic/mcp-run-python", "sse", "--host", "0.0.0.0", "--port", "8080"]