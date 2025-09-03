from corsheaders.defaults import default_headers, default_methods

# ===================== CORS ORIGINS configurations =====================
CSRF_TRUSTED_ORIGINS = [
    "http://catering.mukhsin.space",
    "https://collie-refined-amazingly.ngrok-free.app",
    "http://collie-refined-amazingly.ngrok-free.app",
    "https://catering.mukhsin.space",
    "http://frontend.mukhsin.space",
    "https://frontend.mukhsin.space",
    r"^http://localhost:\d+$",  # Allow localhost with any port
    r"^http://127\.0\.0\.1:\d+$",  # Allow 127.0.0.1 with any port
]

CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE: int = 10 * 60  # 10 minutes
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"https://catering.mukhsin.space",
    r"http://catering.mukhsin.space",
    r"http://frontend.mukhsin.space",
    r"https://frontend.mukhsin.space",
    r"https://collie-refined-amazingly.ngrok-free.app",
    r"http://collie-refined-amazingly.ngrok-free.app",
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
