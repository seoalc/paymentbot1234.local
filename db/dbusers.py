import pymysql.cursors

############# проверка наличия исполнителя в базе по tg id ################
def checkUserByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkUserByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `users` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# проверка наличия исполнителя в базе по tg id ################
def getUsersCheckByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getUsersCheckByTgId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `user_check` FROM `users` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# добавление нового написавшего пользователя в базу ################
def addNewUser (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful addNewUser!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "INSERT INTO `users` (`tg_id`) VALUES (%s)"
            res = cursor.execute(sql, (tg_id))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
