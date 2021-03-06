#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Django settings for cblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9)yrf^)*4dv#4r16x5t!^lw(!%38$e1@zsd+of--b%q+cf3q^gm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'blog',
    'DjangoUeditor',
    'mcaptcha',
    'chat',
    'photo',
    'interest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cblog.urls'

WSGI_APPLICATION = 'cblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )
else:
    # Make `python manage.py syncdb` works happy!
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'admin'
    MYSQL_DB = 'dq_blog3'


#2014-7-3 13:22  by cheer
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
    }
}
#************************************************************
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''

STATIC_URL = '/static/'



TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, './upload/media/'),
    os.path.join(BASE_DIR, './static/'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MEDIA_ROOT = './upload/media/'
MEDIA_URL = '/media/'


# 邮件配置
# EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST          = 'smtp.sina.com'
# EMAIL_PORT          = 25
# EMAIL_HOST_USER     = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS       = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# session
SESSION_COOKIE_AGE = 60*60*24*3 #1天
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True   #浏览器关闭删除cookies
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.request',
# )

# DEBUG = False
# ALLOWED_HOSTS = ['*']
# STATIC_ROOT = os.path.join(BASE_DIR,  'static')