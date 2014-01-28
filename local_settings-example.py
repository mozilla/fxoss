ALLOWED_HOSTS = ["*"]
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "568eaad6-2a5c-4c14-9732-bc03f7efe1378471373b-8fc5-4cf3-990d-721f4f3ead65d3b4cf5c-bff2-4999-b1cd-0098cfd91c5c"
NEVERCACHE_KEY = "a381f1f5-04fb-462e-9f7c-62814eb2c2cc46900db9-aacc-41a0-a797-5d3e39dd48137826efc2-7330-488b-8c20-0598c109c4ef"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "fxoss",
        # Not used with sqlite3.
        "USER": "daaray",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}
