import sqlite3
import csv

import common


def get_column_specs(summary, column_name):
    n_non_numeric = summary['column_summaries'][column_name]['n_non_numeric']
    max_length = summary['column_summaries'][column_name]['max_length']
    if n_non_numeric == 0:
        column_type = 'REAL'
    else:
        column_type = 'CHAR({})'.format(str(max_length))
    column_specs = 'q{} {}'.format(column_name, column_type)

    return column_specs


def get_create_table_query(summary):
    table_query_list = [
        'CREATE TABLE project_share (',
        'ID INT PRIMARY KEY NOT NULL,'
    ]
    column_names = summary['column_names']
    for column_name in column_names:
        column_spec = get_column_specs(summary, column_name) + ','
        table_query_list.append(column_spec)
    last_entry_idx = len(table_query_list) - 1
    last_entry = table_query_list[last_entry_idx]
    table_query_list[last_entry_idx] = last_entry.replace(',', '')
    table_query_list.append(')')
    table_query = '\n'.join(table_query_list)
    return table_query


def get_to_db(summary):
    column_names = summary['column_names']
    with open('output/cleaned_project_share.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        to_db = list()
        counter = 0
        for row in reader:
            row_list = [counter]
            row_list.extend([row[key] for key in column_names])
            row_tuple = tuple(row_list)
            to_db.append(row_tuple)
            counter += 1

    return to_db


def get_insert_query(summary):
    column_names = summary['column_names']
    actual_column_names = ['ID']
    actual_column_names.extend(['q' + column_name for column_name in column_names])
    joined_column_names = ','.join(actual_column_names)
    question_marks = ','.join(['?' for _ in actual_column_names])
    insert_query = 'INSERT INTO project_share ({}) VALUES ({});'.format(joined_column_names, question_marks)

    print(insert_query)
    return insert_query


def go():
    summary = common.read_json_file('output/cleaned_project_share_summary.json')

    create_table_query = get_create_table_query(summary)
    to_db = get_to_db(summary)
    insert_query = get_insert_query(summary)

    with sqlite3.connect('output/project_share.db') as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        cursor.executemany(insert_query, to_db)
        conn.commit()


if __name__ == '__main__':
    go()
