import mysql.connector as connector

# dry_run default set to 0
def mysql_add_router(ip_address, port, username, password):
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

def mysql_pull_all_routers():
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

def mysql_pull_one_router(router_id):
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
        return "Error"

def mysql_change_router_dry_run(router_id, dry_run):
    try:
        with connector.connect(host = 'localhost', user = 'root', password = 'root', database = "fdm_sky_project") as connect:
            cursor = connect.cursor()
            router_data = (dry_run, router_id)
            cursor.execute('''
            UPDATE
                routers
            SET
                dry_run = %s
            WHERE
                router_id = %s''', router_data)
            connect.commit()
            if dry_run == 0:
                return "dry_run = 0: Payload will be sent to router"
            if dry_run == 1:
                return "dry_run = 1: Payload will be returned to user"
    except:
        return "Error"