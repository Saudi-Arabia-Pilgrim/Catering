from corsheaders.defaults import default_methods, default_headers

# ===================== CORS ORIGINS configurations =====================
CSRF_TRUSTED_ORIGINS = [
    "https://collie-refined-amazingly.ngrok-free.app",
    "http://collie-refined-amazingly.ngrok-free.app",
    "http://localhost",
    "http://127.0.0.1",
    "https://wider-app.vercel.app"
]

CSRF_TRUSTED_ORIGINS = [
    "https://collie-refined-amazingly.ngrok-free.app",
]


CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE: int = 10 * 60  # 10 minutes
CORS_ALLOWED_ORIGIN_REGEXES = [
    "https://collie-refined-amazingly.ngrok-free.app",
    "http://collie-refined-amazingly.ngrok-free.app",
    r"^http://localhost:\d+$",  # Allow localhost with any port
    r"^http://127\.0\.0\.1:\d+$",  # Allow 127.0.0.1 with any port
    "https://wider-app.vercel.app"
]

CORS_ALLOW_METHODS = (
    *default_methods,
)

CORS_ALLOW_HEADERS = (
    *default_headers,
)