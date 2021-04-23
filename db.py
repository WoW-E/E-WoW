import sqlite3


# ✓
def DatabaseInit(database, table, **kwargs):
    global connection
    try:
        connection = sqlite3.connect(f'database/{database}.db')
        cursor = connection.cursor()

        parameters = []

        for key, value in kwargs.items():
            param = "{} {}".format(key, value)
            parameters.append(param)

        sep = ", "
        sep = sep.join(parameters)

        cursor.execute("CREATE TABLE {} ({})".format(table, sep))

        connection.commit()
        connection.close()

        return True

    except sqlite3.OperationalError:
        connection.rollback()
        pass


# ✓
def DuplicateCheckUser(database, table, user):
    connection2 = sqlite3.connect(f'database/{database}.db')

    cursor = connection2.cursor()

    cursor.execute("SELECT user_id from {};".format(table))
    list_users = cursor.fetchall()

    list_users = [x[0] for x in list_users]

    if user in list_users:
        connection2.close()
        return False
    else:
        connection2.close()
        return True


# ✓
def ExportParameter(database, table, user, **kwargs):
    connection2 = sqlite3.connect(f'database/{database}.db')
    cursor = connection2.cursor()
    for key, value in kwargs.items():
        cursor.execute("INSERT INTO {} (user_id, {}) VALUES (:user_id, :parameter);".format(table, key),
                       {
                           'user_id': user,
                           'parameter': value
                       })

    connection2.commit()
    connection2.close()

    return True


# ✓
def UpdateParameter(database, table, user, **kwargs):
    connection2 = sqlite3.connect(f'database/{database}.db')
    cursor = connection2.cursor()

    for key, value in kwargs.items():
        cursor.execute("UPDATE {} SET {} = (:parameter) WHERE user_id = (:user_id);".format(table, key),
                       {
                           'parameter': value,
                           'user_id': user
                       })

    connection2.commit()
    connection2.close()

    return True


# ✓
def GetUserLocation(user):
    connection3 = sqlite3.connect(f'database/main.db')

    cursor = connection3.cursor()

    cursor.execute("SELECT location from location WHERE user_id = (:user)",
                   {
                       'user': user
                   })

    lists = cursor.fetchall()

    lists_ = [x[0] for x in lists]

    return lists_[0]


# ✓
def GetEverything(database, table):
    connection1 = sqlite3.connect(f'database/{database}.db')

    cursor = connection1.cursor()

    cursor.execute('SELECT * from {};'.format(table))

    lists = cursor.fetchall()

    print(lists)
