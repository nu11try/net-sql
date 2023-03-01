CREATE TABLE performers (
    id serial primary key unique,
    name varchar(20) not null
);

CREATE TABLE genres (
    id serial primary key unique,
    name varchar(20) not null
);

CREATE TABLE performers_genres (
    id serial primary key unique,
    performer_id int not null REFERENCES performers(id),
    genre_id int not null REFERENCES genres(id)
);

CREATE TABLE albums (
    id serial primary key unique,
    name varchar(50) not null,
    year date not null
);

CREATE TABLE performers_albums (
    id serial primary key unique,
    performer_id int not null REFERENCES performers(id),
    album_id int not null REFERENCES albums(id)
);

CREATE TABLE tracks (
    id serial primary key unique,
    name varchar(50) not null,
    duration int not null,
    album_id int not null references albums(id)
);

CREATE TABLE collections (
    id serial primary key unique,
    name varchar(20) not null,
    year date not null
);

CREATE TABLE collections_tracks (
    id serial primary key unique,
    collection_id int not null REFERENCES collections(id),
    track_id int not null REFERENCES tracks(id)
);