import socket       # Get name of machine

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '^r=ow$1kg%2r3gf)5(*3m8pkc_nd2!lnkw7j63b#@+$_2e#4mr'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ibc_financeiro',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware' , 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuracoes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracoes.wsgi.application'

DATABASES = {       # Banco de dados
    'default': {
        'ENGINE': 'django.db.backends.mysql',       # Conexão com MySQL
        'NAME': 'financeiro',                       # Nome do banco de dados
        'USER': 'root',                             # Nome do usuário
        'PASSWORD': '',                             # Senha do usuário
        'HOST': 'localhost',                        # Local que está hospedado
        'PORT': '3306',                             # Porta usada para se conectar
        'OPTIONS': {                                # Opções adicionais
            'sql_mode' : 'traditional',             # Remove notificações de aviso
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Diretório para salvar arquivos dinâmicos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.kinghost.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'senhas@financeiro.ibcorrente.com.br'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'senhas@financeiro.ibcorrente.com.br'
SERVER_EMAIL = 'senhas@financeiro.ibcorrente.com.br'

# Session Time
SESSION_EXPIRE_SECONDS = 60 * (30)              # 30 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/conta/login'

# HTTPS
if socket.gethostname() == 'web36f91.kinghost.net':
    SECURE_SSL_REDIRECT = True