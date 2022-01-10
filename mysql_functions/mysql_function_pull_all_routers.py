import mysql.connector as connector

def pull_all_routers_mysql_connector():
    '''
    Establishes connection with MYSQL, database fdm_sky_project, table routers. Pulls values for all routers.
    :returns: A tuple for each router, contained within a list
    '''
    try:
        with connector.connect(host = 'localhost', user = 'root', password = 'root', database = "fdm_sky_project") as connect:
            cursor = connect.cursor()
            cursor.execute('''
            SELECT
                *
            FROM
                routers''')
            router_data = cursor.fetchall()
            return router_data
    except:
        return "Error"