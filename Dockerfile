FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-editable

FROM gcr.io/distroless/python3-debian12
WORKDIR /app
# This doesn't work yet fyi - gotta fix dep copying
COPY --from=builder /app/.venv/lib/python3.11/site-packages /app/site-packages
ENV PYTHONPATH=/app/site-packages
COPY . .

# --- Required ---
ENV HOVER_USERNAME=""
ENV HOVER_PASSWORD=""
ENV HOVER_TOTP_SECRET=""
ENV HOVER_DNS_ID=""
ENV HOVER_ROOT_DOMAIN=""

# --- Optional ---
ENV HOVER_GET_DNSIDS="false"
ENV HOVER_DISCOVER_IP="true"
ENV HOVER_IP_ADDRESS=""
ENV HOVER_SRC_DOMAIN=""
ENV HOVER_USER_AGENT="Chromium"
ENV HOVER_LOG_LEVEL="INFO"
ENV HOVER_LOG_RETENTION_DAYS="7"
ENV HOVER_RUN_INTERVAL="300"

CMD ["/app/main.py"]
