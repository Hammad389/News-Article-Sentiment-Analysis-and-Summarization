import pandas as pd
import mysql.connector

class CSV_TO_SQL:
    def __init__(self, file_path, table_name="csv_to_sql"):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='centre879149',
            database="generic_csv"
        )
        self.cursor = self.conn.cursor()
        self.chunk_size = 100
        self.df = pd.read_csv(file_path, chunksize=self.chunk_size)
        self.table_name = table_name
        self.df.columns = [col.replace(' ', '_') for col in next(self.df)]
        self.create_table()
        self.insert_into_db()

    def get_columns(self):
        columns = []
        for col in self.df.columns:
            columns.append(f"{col} TEXT")
        must_have_columns = [
            'id INT AUTO_INCREMENT PRIMARY KEY',
            'created DATETIME DEFAULT CURRENT_TIMESTAMP',
            'updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        ]
        return must_have_columns + columns

    def index_exist(self, index_name):
        self.cursor.execute("""
        SELECT COUNT(1)
        FROM INFORMATION_SCHEMA.STATISTICS
        WHERE table_schema = DATABASE()
            AND table_name = %s
            AND index_name = %s
        """, (self.table_name, index_name))
        return self.cursor.fetchone()[0]>0

    def create_table(self):
        columns_list = ", ".join(self.get_columns())
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_list});"
        self.cursor.execute(query)
        if not self.index_exist('idx_created'):
            self.cursor.execute(f"CREATE INDEX idx_created ON {self.table_name}(created);")
        if not self.index_exist('idx_updated'):
            self.cursor.execute(f"CREATE INDEX idx_updated ON {self.table_name}(updated);")

    def insert_into_db(self):
        cols = ', '.join(self.df.columns)
        values_to_place = ', '.join(['%s'] * len(self.df.columns))
        query = f"INSERT IGNORE INTO {self.table_name} ({cols}) VALUES ({values_to_place})"

        for chunk in self.df:
            for _, row in chunk.iterrows():
                # clean the row for any missing value
                clean_row = [None if pd.isna(val) else val for val in row]
                self.cursor.execute(query, tuple(clean_row))
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    # name the csv_file to "sample_file.csv"
    CSV_TO_SQL('sample_file.csv')
