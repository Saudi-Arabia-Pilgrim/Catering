from corsheaders.defaults import default_headers, default_methods

# ===================== CORS ORIGINS configurations =====================
CSRF_TRUSTED_ORIGINS = [
    "https://maqom360.com",
    "http://api.maqom360.com",
    "https://maqom360.com",
    "http://api.maqom360.com",
    r"^http://localhost:\d+$",  # Allow localhost with any port
    r"^http://127\.0\.0\.1:\d+$",  # Allow 127.0.0.1 with any port
]

CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE: int = 10 * 60  # 10 minutes
CORS_ALLOWED_ORIGIN_REGEXES = [
    "https://maqom360.com",
    "http://api.maqom360.com",
    "https://maqom360.com",
    "http://api.maqom360.com",
    r"^http://localhost:\d+$",  # Allow localhost with any port
    r"^http://127\.0\.0\.1:\d+$",  # Allow 127.0.0.1 with any port
]

CORS_ALLOW_METHODS = (
    *default_methods,
)

CORS_ALLOW_HEADERS = (
    *default_headers,
)

# ngrok http --url=collie-refined-amazingly.ngrok-free.app 8000
