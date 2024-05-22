from funzioni_db import *
from query import *



DB_NAME = "museo"

connection = create_server_connection("localhost","root","")
execute_query(connection, f"drop database {DB_NAME}")
create_database(connection, DB_NAME)
connection = create_db_connection("localhost", "root","", DB_NAME) 


execute_query(connection, create_table_artisti)
execute_query(connection, create_table_artworks)
inserisci_dati_artisti(connection, 'artisti', 'artists_cleaned.csv')