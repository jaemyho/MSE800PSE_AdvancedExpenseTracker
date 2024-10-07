class Config:
    MYSQL_HOST = 'p3nlmysql175plsk.secureserver.net'
    MYSQL_USER = 'remote_user'
    MYSQL_PASSWORD = 'ABcd!@34'
    MYSQL_DB = 'JaemyWeb'
    MYSQL_CURSORCLASS = 'DictCursor'  # This ensures the cursor returns dictionaries
    MYSQL_CONNECT_TIMEOUT = 28800  # Increase the connect timeout (in seconds)
    MYSQL_WAIT_TIMEOUT = 28800  # Increase the wait timeout (in seconds)
    MYSQL_INTERACTIVE_TIMEOUT = 28800  # Interactive timeout (in seconds)

    # Upload folder configuration
    UPLOAD_FOLDER = 'uploads/'