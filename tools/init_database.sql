create table if not exists initial_player_list (
    id SERIAL,
    name varchar(128) NOT NULL,
    rating INTEGER NOT NULL
);

insert into initial_player_list (name, rating) values 
('Shiki', 2500),
('Karen', 2200),
('Frederica', 2000),
('Shuko', 1900),
('Mika', 1800),
('Rin', 1720),
('Kanade', 1700),
('Nao', 1600);