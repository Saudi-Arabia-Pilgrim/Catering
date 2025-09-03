AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'authentication:token_obtain_pair'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = 'authentication:token_obtain_pair'

# Password validation settings
# ===================== Password validators =====================

AUTH_PASSWORD_VALIDATORS = [
    {
        # ======== Prevents weak/common passwords like '123456' or 'password' ========
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # ======== Prevents too short passwords (default: 8 chars) ========
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        # ======== Prevents passwords too similar to username, email, etc. ========
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # ======== Prevents passwords that are entirely numeric (e.g. 12345678) ========
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Password reset token timeout (in seconds)
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
