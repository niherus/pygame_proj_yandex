def strr(text):
    return f"'{text}'"


def create_table(cur, table_name, fields):
    request = f'CREATE TABLE IF NOT EXISTS {table_name}({",".join(fields)});'
    cur.execute(request)


def drop_table(cur, table_name):
    request = f'DROP TABLE IF EXISTS {table_name}'
    cur.execute(request)


def insert_row(cur, table_name, row):
    if isinstance(row, dict):
        collumns = []
        values = []
        for key, val in row.items():
            collumns.append(str(key))
            if isinstance(val, str):
                val = strr(val)
            else:
                val = str(val)
            values.append(str(val))
        row = f'({", ".join(collumns)}) VALUES({", ".join(values)})'
    elif isinstance(row, list):
        row = [strr(val) if isinstance(val, str) else str(val) for val in row]
        row = f'VALUES({", ".join(row)})'
    else:
        raise Exception

    request = f'INSERT INTO {table_name} {row}'
    cur.execute(request)


def get_data(cur, table_name):
    request = f'SELECT * FROM {table_name}'
    return cur.execute(request).fetchall()
