import time
from sqlalchemy import create_engine, text
import base64
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import asyncio

# oracle+oracledb://c##wck:980714@10.0.0.198:1521/orcl
TARGET_DB = "b3JhY2xlK29yYWNsZWRiOi8vYyMjd2NrOjk4MDcxNEAxMC4wLjAuMTk4OjE1MjEvb3JjbA=="  # 198
SOURCE_DB = "b3JhY2xlK29yYWNsZWRiOi8vYyMjd2NrOjk4MDcxNEAxMC4wLjAuMTk3OjE1MjEvb3JjbA=="  # 197


# select all table names from FLEXFIN
def table_chunks() -> list:
    engine_dev = create_engine(base64.decodebytes(bytes(SOURCE_DB, 'utf-8')).decode())
    session = engine_dev.connect()
    try:
        results = session.execute(
            text("SELECT TABLE_NAME FROM all_tables WHERE OWNER = 'C##WCK'")).fetchall()
        return [f"{x[0]}" for x in results]
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()
        engine_dev.dispose()


# For Chatops DB
engine = create_engine(
    base64.decodebytes(bytes(TARGET_DB, 'utf-8')).decode(),
    pool_size=10,
    max_overflow=5  # create new session size once surpass pool_size
)


def worker(data: str):
    session = engine.connect()
    try:
        print(f"execute sql: {data}")
        session.execute(text(data))
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()  # session will be back to pool rather than terminated

async def coroutine_worker(data: str):
    session = engine.connect()
    try:
        print(f"execute sql: {data}")
        await session.execute(text(data)).fetchall()
        await session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()  # session will be back to pool rather than terminated


if __name__ == '__main__':
    start_time = time.time()  # record program start time
    source_tables = table_chunks()
    sql_chunks = []
    for t in source_tables:
        sql = f"create table FLEX_{t} as select * from {t}@ORCL197_LINK"
        sql_chunks.append(sql)

    # concurrent thredpool
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.map(worker, sql_chunks)
    print(f"concurrent thredpool - program running time: {time.time() - start_time} seconds")

    # multiprocess pool
    # with multiprocessing.Pool(processes=10) as pool:
    #     pool.map(worker, sql_chunks)
    # print(f"multiprocesses pool  - program running time: {time.time() - start_time} seconds")
    
    # coroutine
    # loop = asyncio.get_event_loop()
    # tasks = [coroutine_worker(s) for s in sql_chunks]
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    # print(f"coroutine - program running time: {time.time() - start_time} seconds")
