import mysql.connector as connector

def change_router_dry_run_mysql_connector(router_id, dry_run):
    '''
    Establishes connection with MYSQL, database fdm_sky_project, table routers. Changes dry_run value from 0 to 1 or 1 to 0
    :param router_id: primary key of router to be changed
    :param dry_run: new value of dry_run to be set
    :returns: new dry_run value
    '''
    
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
        return "Error: Unable to configure dry_run"