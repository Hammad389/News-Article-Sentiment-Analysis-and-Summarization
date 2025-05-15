import pandas as pd
import mysql.connector

class CSV_TO_SQL:
    def __init__(self, file_path, table_name="csv_to_sql"):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database="module2_db"
        )
        self.cursor = self.conn.cursor()
        self.df = pd.read_csv(file_path)
        self.table_name = table_name
        self.df.columns = [col.replace(' ', '_') for col in self.df.columns]
        self.create_table()
        self.insert_into_db()

    def get_columns(self):
        columns = []
        for col in self.df.columns:
            dtype = self.df[col].dtype
            if dtype in ['int64', 'int32']:
                col_type = 'INT'
            elif dtype in ['float64', 'float32']:
                col_type = 'FLOAT'
            elif dtype == 'bool':
                col_type = 'BOOLEAN'
            elif dtype == 'datetime64[ns]':
                col_type = 'DATETIME'
            else:
                col_type = 'TEXT'
            columns.append(f"{col} {col_type}")
        must_have_columns = [
            'id INT AUTO_INCREMENT PRIMARY KEY',
            'created DATETIME DEFAULT CURRENT_TIMESTAMP',
            'updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        ]
        return must_have_columns + columns

    def create_table(self):
        columns_list = ", ".join(self.get_columns())
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_list});"
        self.cursor.execute(query)
        # find and add index on date column
        for col in self.df.columns:
            if 'date' in col.lower() or self.df[col].dtype == 'datetime64[ns]':
                self.cursor.execute(f"CREATE INDEX idx_{col} ON {self.table_name}({col});")

    def insert_into_db(self):
        cols = ', '.join(self.df.columns)
        values_to_place = ', '.join(['%s'] * len(self.df.columns))
        query = f"INSERT IGNORE INTO {self.table_name} ({cols}) VALUES ({values_to_place})"

        for _, row in self.df.iterrows():
            # clean the row for any missing value
            clean_row = [None if pd.isna(val) else val for val in row]
            self.cursor.execute(query, tuple(clean_row))

        self.conn.commit()


if __name__ == "__main__":
    # name the csv_file to "sample_file.csv"
    CSV_TO_SQL('sample_file.csv')
