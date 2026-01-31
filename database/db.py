from others.cfg import log
from .cfg import DB_HOST, DB_PASSWORD, DB_USER, DB_PORT

from aiomysql import ProgrammingError, IntegrityError, DataError, OperationalError, InterfaceError, InternalError
from aiomysql.connection import Connection
import aiomysql

async def connector_to_server() -> Connection:
    connect = await aiomysql.connect(host=DB_HOST,
                                     password=DB_PASSWORD,
                                     user=DB_USER,
                                     port=DB_PORT,
                                     autocommit=True)
    return connect
        
async def create_database(connect: Connection) -> None:
    try:
        csr = await connect.cursor()
        await csr.execute('CREATE DATABASE IF NOT EXISTS SophiaBase')
    except InternalError:
        log(f'Error creating database!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()

async def create_table(connect: Connection) -> None:
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('CREATE TABLE IF NOT EXISTS SophiaTable ('
                          'id INT PRIMARY KEY AUTO_INCREMENT, '
                          'users BIGINT, '
                          'roles TEXT, '
                          'contents TEXT)')   
    except OperationalError:
        log('Server is not available!')
    except InternalError:
        log(f'Error connecting database!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
            
async def include_in_table(connect: Connection, user: str, role: str, content: str) -> None:
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('INSERT IGNORE INTO SophiaTable (users, roles, contents) '
                          'VALUES (%s, %s, %s)', 
                          (user, 
                           role, 
                           content))
    except OperationalError:
        log('Server is not available!')
    except ProgrammingError:
        log(f'Invalid syntax')
    except DataError:
        log('Invalid length data!')
    except IntegrityError:
        log('An error was detected in the data while loading!')
    except InterfaceError:
        log('Connection to database is refused!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
        
async def select_data_from_table(connect: Connection, user: str) -> tuple | list | None:
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('SELECT users, roles, contents '
                          'FROM SophiaTable '
                          'WHERE users = %s '
                          'ORDER BY id DESC '
                          'LIMIT 30', 
                          (user, ))
        results = await csr.fetchall()
        return results
    except OperationalError:
        log('Server is not available!')
    except ProgrammingError:
        log('Incorrect a data!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
