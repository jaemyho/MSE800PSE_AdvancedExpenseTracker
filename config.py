class Config:
    #Connect to Remote Server
    MYSQL_HOST = 'p3nlmysql175plsk.secureserver.net'
    MYSQL_USER = 'remote_user'
    MYSQL_PASSWORD = 'ABcd!@34'
    MYSQL_DB = 'JaemyWeb'

    #Connect to Local host
    #MYSQL_HOST = 'localhost'
    #MYSQL_USER = 'root'
    #MYSQL_PASSWORD = 'abc123'
    #MYSQL_DB = 'JaemyWeb'

    MYSQL_CURSORCLASS = 'DictCursor'  # This ensures the cursor returns dictionaries
    MYSQL_CONNECT_TIMEOUT = 28800  # Increase the connect timeout (in seconds)
    MYSQL_WAIT_TIMEOUT = 28800  # Increase the wait timeout (in seconds)
    MYSQL_INTERACTIVE_TIMEOUT = 28800  # Interactive timeout (in seconds)

    # Upload folder configuration
    UPLOAD_FOLDER = 'uploads/'

    SECRET_KEY = '4@!sT&9jP$w5gR^fV#u7K$8qZ*eL3oR'
