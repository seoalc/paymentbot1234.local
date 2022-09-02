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

############# получение имеющейся суммы у пользователя по tg id ################
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

############# получение статуса блокировки пользователя ################
def getUsersBlockStatus (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getUsersBlockStatus!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `blocked` FROM `users` WHERE `tg_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (tg_id))
            results = cursor.fetchone()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

####### получение всех пользователей #######
def getAllUsers ():
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getAllUsers!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT * FROM `users`"
            # Выполнить команду запроса (Execute Query).
            res = cursor.execute(sql)
            results = cursor.fetchall()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# получение суммы платежа по bill_id ################
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

############# обновление баланса юзера ################
async def updtUsersBalance (newBalance, tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful updtUsersBalance!")
    cursor = connection.cursor()
    try:
        a = {'newBalance': newBalance, 'tg-id': tg_id}
        # SQL
        sql = "UPDATE `users` SET "\
        "`user_check` = %s WHERE `tg_id` = %s"
        # Выполнить команду запроса (Execute Query).
        # перевожу данные в кортеж для вставки
        res = cursor.execute(sql, tuple(a.values()))
        connection.commit()
        return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# блокировка юзера ################
async def blockUserByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful blockUserByTgId!")
    cursor = connection.cursor()
    try:
        # SQL
        sql = "UPDATE `users` SET `blocked` = 1 WHERE `tg_id` = %s"
        # Выполнить команду запроса (Execute Query).
        # перевожу данные в кортеж для вставки
        res = cursor.execute(sql, (tg_id))
        connection.commit()
        return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# разблокировка юзера ################
async def unblockUserByTgId (tg_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful unblockUserByTgId!")
    cursor = connection.cursor()
    try:
        # SQL
        sql = "UPDATE `users` SET `blocked` = 0 WHERE `tg_id` = %s"
        # Выполнить команду запроса (Execute Query).
        # перевожу данные в кортеж для вставки
        res = cursor.execute(sql, (tg_id))
        connection.commit()
        return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
