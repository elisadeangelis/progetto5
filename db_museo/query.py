create_table_artisti = '''

CREATE TABLE artisti (
    Artist_ID int PRIMARY KEY,
    Name varchar(80),
    Nationality varchar(80),
    Gender varchar(10),
    Birth_Year YEAR,
    Death_Year YEAR    
);
'''


create_table_artworks = '''

CREATE TABLE artworks (
    Artwork_ID int PRIMARY KEY,
    Title varchar(100),
    Date YEAR 
);


'''