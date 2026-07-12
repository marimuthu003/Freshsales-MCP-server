FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
# If uv is available globally, use it, else fallback to pip. We'll use pip here for standard docker deployment.
RUN pip install --no-cache-dir -e .
COPY src/ src/
EXPOSE 8080
CMD ["python", "-m", "freshsales_mcp"]
