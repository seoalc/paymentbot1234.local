import pymysql.cursors

############# проверка наличия исполнителя в базе по tg id ################
def checkPaymentById (id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful checkPaymentById!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `id` FROM `payments` WHERE `bill_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (id))
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# получение суммы платежа по bill_id ################
def getPaymentAmountByBillId (bill_id):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful getPaymentAmountByBillId!")
    try:
        with connection.cursor() as cursor:
            # SQL
            sql = "SELECT `pay_amount` FROM `payments` WHERE `bill_id` = %s"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, (id))
            results = cursor.fetchone()
            return results
    finally:
        # Закрыть соединение (Close connection).
        connection.close()

############# запись нового платежа в базу ################
async def addNewPayment (state):
    # Подключиться к базе данных.
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='paymentbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful addNewPayment!")
    cursor = connection.cursor()
    try:
        async with state.proxy() as data:
            # SQL
            sql = "INSERT INTO `payments` "\
            "(`user_tgid`, `pay_amount`, `bill_id`) "\
            "VALUES (%s, %s, %s)"
            # Выполнить команду запроса (Execute Query).
            # есть пользователь с этим ником в базе
            res = cursor.execute(sql, tuple(data.values()))
            connection.commit()
            return res
    finally:
        # Закрыть соединение (Close connection).
        connection.close()
