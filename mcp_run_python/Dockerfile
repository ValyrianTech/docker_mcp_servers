FROM denoland/deno:debian-1.41.3

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
RUN mkdir -p node_modules && chown -R appuser:appuser /home/appuser

# Switch to non-root user
USER appuser

# Set environment variables
ENV DENO_DIR=/home/appuser/.deno
ENV PATH="${DENO_DIR}/bin:${PATH}"

# Cache the MCP Run Python package
RUN deno cache --node-modules-dir jsr:@pydantic/mcp-run-python

# Expose port 8080 for SSE transport mode
EXPOSE 8080

# Set the default command to run the MCP Run Python server in SSE mode
# Use stdio mode instead if you plan to connect to this as a subprocess
CMD ["deno", "run", "--allow-all", "--node-modules-dir", \
     "jsr:@pydantic/mcp-run-python", "sse", "--port", "8080", "--host", "0.0.0.0"]
