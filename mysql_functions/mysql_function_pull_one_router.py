import mysql.connector as connector

def pull_one_router_mysql_connector(router_id):
    '''
    Establishes connection with MYSQL, database fdm_sky_project, table routers. Pulls all values for one router.
    :param router_id: primary key of router to be pulled
    :returns: all data as single tuple within a list
    '''
    try:
        with connector.connect(host = 'localhost', user = 'root', password = 'root', database = "fdm_sky_project") as connect:
            cursor = connect.cursor()
            cursor.execute('''
            SELECT
                *
            FROM
                routers
            WHERE
                router_id = %s''' % router_id)
            router_data = cursor.fetchall()
            return router_data
    except:
        return "Error: Unable to pull router %s data." % router_id