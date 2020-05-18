DROP TABLE IF EXISTS songs;
CREATE TABLE songs
 (
    key_id int NOT NULL PRIMARY KEY,
    song_id varchar,
    title varchar NOT NULL,
    artist_id varchar NOT NULL,
    artist_key_id int NOT NULL,
    year int,
    duration numeric NOT NULL,
    danceability numeric,
    energy numeric,
    hotness numeric,
    mode int,
    tempo numeric
    );

create index ix1_songs on songs (artist_key_id);

DROP TABLE IF EXISTS artists;
CREATE TABLE  artists
 (
    key_id int NOT NULL PRIMARY KEY,
    artist_id varchar NOT NULL,
    name varchar NOT NULL,
    location varchar,
    latitude numeric,
    longitude numeric,
    hotness numeric,
    familiarity numeric
 );

DROP TABLE IF EXISTS similarartists;
CREATE TABLE IF NOT EXISTS similarartists
 (
    key_id int not null PRIMARY KEY,
    artist_key_id int NOT NULL,
    similarartist_key_id int NOT NULL,
    artist_id varchar NOT NULL,
    similarartist_id varchar NOT NULL
 );

create index ix1_similarartists on similarartists (artist_key_id, similarartist_key_id);


COPY artists FROM '/Users/murat.turkoglu/OneDrive - LC WAIKIKI MAGAZACILIK HIZMETLERI TIC.A.S/MEF/ApplicationsDataManagement/MillionSongDB/MillionSongSubset/csv/artists.csv' DELIMITER ',' CSV HEADER;
COPY similarartists FROM '/Users/murat.turkoglu/OneDrive - LC WAIKIKI MAGAZACILIK HIZMETLERI TIC.A.S/MEF/ApplicationsDataManagement/MillionSongDB/MillionSongSubset/csv/similarartists.csv' DELIMITER ',' CSV HEADER;
COPY songs FROM '/Users/murat.turkoglu/OneDrive - LC WAIKIKI MAGAZACILIK HIZMETLERI TIC.A.S/MEF/ApplicationsDataManagement/MillionSongDB/MillionSongSubset/csv/songs.csv' DELIMITER ',' CSV HEADER;

update songs s
set artist_key_id = a.key_id
from artists a
where s.artist_id = a.artist_id;

update similarartists s
set artist_key_id = a1.key_id
from artists a1
where s.artist_id = a1.artist_id;

update similarartists s
set similarartist_key_id = a2.key_id
from artists a2
where s.similarartist_id = a2.artist_id;

delete from similarartists
where artist_key_id = 0 or similarartist_key_id = 0;