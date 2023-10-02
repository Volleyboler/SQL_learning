CREATE TABLE IF NOT EXISTS Genres(
	id SERIAL PRIMARY KEY,
	name_genre VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS Singers(
	id SERIAL PRIMARY KEY,
	name_singer VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS Albums(
	id SERIAL PRIMARY KEY,
	name_album VARCHAR(100) NOT NULL,
	year_creation INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS Compilations(
	id SERIAL PRIMARY KEY,
	year_compilation INTEGER NOT NULL,
	name_compilation VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS Tracks(
	id SERIAL PRIMARY KEY,
	name_track VARCHAR(100) NOT NULL,
	duration TIME NOT NULL,
	album_id INTEGER NOT NULL REFERENCES Albums(id)
);


CREATE TABLE IF NOT EXISTS TrackCompilation(
	track_id INTEGER REFERENCES Tracks(id),
	compilation_id INTEGER REFERENCES Compilations(id),
	CONSTRAINT pk_track_compilation PRIMARY KEY (track_id, compilation_id)
);


CREATE TABLE IF NOT EXISTS SingerAlbum(
	singer_id INTEGER REFERENCES Singers(id),
	album_id INTEGER REFERENCES Albums(id),
	CONSTRAINT pk_singer_album PRIMARY KEY (singer_id, album_id)
);


CREATE TABLE IF NOT EXISTS SingerGenre(
	singer_id INTEGER REFERENCES Singers(id),
	genre_id INTEGER REFERENCES Genres(id),
	CONSTRAINT pk_singer_genre PRIMARY KEY (singer_id, genre_id)
);

