import mysql.connector as connector

# dry_run default set to 0
def add_router_mysql_connector(ip_address, port, username, password):
    '''
    Establishes connection with MYSQL, database fdm_sky_project, table routers. Adds one router to the table, with dry_run set to 0.
    :param ip_address: ip address through which the router is accessed
    :param port: port through which router is accessed
    :param username: router ssh username
    :param password: router ssh password
    :returns: String stating router has (not) been added to mysql table.
    '''
    try:
        with connector.connect(host = 'localhost', user = 'root', password = 'root', database = "fdm_sky_project") as connect:
            cursor = connect.cursor()
            router_data = (ip_address, port, username, password)
            cursor.execute('''
            INSERT INTO
                routers(ip_address, port, username, password)
            VALUES
                (%s, %s, %s, %s)''', router_data)

            connect.commit()

            return "Router added to MYSQL"
    except:
        return "Error adding router to MYSQL"