from others.cfg import log
from .cfg import DB_HOST, DB_PASSWORD, DB_USER, DB_PORT

from aiomysql import (
    ProgrammingError, 
    IntegrityError, 
    DataError, 
    OperationalError, 
    InterfaceError, 
    InternalError
    )

from aiomysql.pool import Pool

import aiomysql

async def sql_create_pool() -> Pool:
    pool = await aiomysql.create_pool(host=DB_HOST,
                                      password=DB_PASSWORD,
                                      user=DB_USER,
                                      port=DB_PORT,
                                      autocommit=True)
    return pool

async def sql_create_database(pool: Pool) -> None:
    try:
        cnn = await pool.acquire()
        csr = await cnn.cursor()
        
        await csr.execute('CREATE DATABASE IF NOT EXISTS SophiaBase')
    except InternalError:
        log(f'Error creating database!')
    finally:
        if csr != None:
            await csr.close()
        if cnn != None:
            pool.release(cnn)
        else:
            return

async def sql_create_table(pool: Pool) -> None:
    try:
        cnn = await pool.acquire()
        csr = await cnn.cursor()
        
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
        if csr != None:
            await csr.close()
        if cnn != None:
            pool.release(cnn)
        else:
            return
            
async def sql_include_table(pool: Pool, user: str, role: str, content: str) -> None:
    try:
        cnn = await pool.acquire()
        csr = await cnn.cursor()
        
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
        if csr != None:
            await csr.close()
        if cnn != None:
            pool.release(cnn)
        else:
            return
        
async def sql_get_table(pool: Pool, user: str) -> tuple | None:
    try:
        cnn = await pool.acquire()
        csr = await cnn.cursor()
        
        await csr.execute('USE SophiaBase')
        await csr.execute('SELECT roles, contents '
                          'FROM SophiaTable '
                          'WHERE users = %s '
                          'ORDER BY id DESC '
                          'LIMIT 50', 
                          (user, ))
        results = await csr.fetchall()
        return results
    except OperationalError:
        log('Server is not available!')
    except ProgrammingError:
        log('Incorrect a data!')
    finally:
        if csr != None:
            await csr.close()
        if cnn != None:
            pool.release(cnn)
        else:
            return
