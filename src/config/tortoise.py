TORTOISE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": "db.sqlite3"},
        }
    },
    "apps": {
        "backend": {
            "models": ["src.api.models.db", "aerich.models"],
            "default_connection": "default"
        }
    }
}
