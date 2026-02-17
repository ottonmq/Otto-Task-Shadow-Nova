"""
⚙️ DJANGO SETTINGS FOR OTTO-TASK ECOSYSTEM
🧬 ARCHITECT: OTTO NAPOLEÓN MENDOZA
🛡️ SECURITY PROTOCOL: SHADOW ARCHITECT ACTIVE
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚡ SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ottonqq-shadow-architect-protocol-2026'

# ⚡ SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# --- INSTALLED APPS: OTTO-TASK CORE ---
INSTALLED_APPS = [
    'django.contrib.admin',
        'django.contrib.auth',
            'django.contrib.contenttypes',
                'django.contrib.sessions',
                    'django.contrib.messages',
                        'django.contrib.staticfiles',
                            # Third party security modules
                                'allauth',
                                    'allauth.account',
                                        'allauth.socialaccount',
                                        ]

                                        # --- DATABASE CONFIGURATION ---
                                        DATABASES = {
                                            'default': {
                                                    'ENGINE': 'django.db.backends.sqlite3',
                                                            'NAME': BASE_DIR / 'db.sqlite3',
                                                                }
                                                                }

                                                                # ==========================================================
                                                                # 🚨 CRITICAL SECURITY CONFIGURATION (AUDIT TARGET)
                                                                # ==========================================================
                                                                # The Shadow Architect has flagged the following line:
                                                                # Risk: CSRF Vulnerability via Social Auth GET requests.

                                                                SOCIALACCOUNT_LOGIN_ON_GET = True  # <- [AUDIT_ALERT]: Vulnerability point

                                                                # ==========================================================

                                                                # --- INTERNATIONALIZATION ---
                                                                LANGUAGE_CODE = 'es-es'
                                                                TIME_ZONE = 'UTC'
                                                                USE_I18N = True
                                                                USE_TZ = True

                                                                STATIC_URL = 'static/'

                                                                # 🏮 POWERED BY OTTONQQ
                                                                