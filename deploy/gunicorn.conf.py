bind = "0.0.0.0:8000"    # IP и порт для Gunicorn
workers = 3             # Количество воркеров, можно менять по нагрузке
accesslog = "-"         # Лог доступа (stdout)
errorlog = "-"          # Лог ошибок (stdout)
