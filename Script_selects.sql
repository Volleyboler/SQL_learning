SELECT name_track, duration FROM Tracks
WHERE duration = (SELECT MAX(duration) FROM Tracks);


SELECT name_track FROM Tracks 
WHERE duration >= "00:03:30";


SELECT name_compilation FROM Compilations 
WHERE year_compilation BETWEEN 2018 AND 2020;


--SELECT name_singer  FROM Singers 
--WHERE (LENGTH (name_singer)-LENGTH (replace(name_singer,' ','')))=0;


SELECT name_singer FROM Singers 
WHERE name_singer not LIKE '% %';


SELECT name_track FROM Tracks 
WHERE name_track LIKE '%my%' OR name_track LIKE '%Мой%' OR name_track LIKE '%мой%';


SELECT Genres.name_genre, COUNT(*) AS count
FROM Genres
JOIN SingerGenre ON Genres.id = SingerGenre.genre_id
JOIN Singers ON SingerGenre.singer_id = Singers.id 
GROUP BY Genres.name_genre;



SELECT COUNT(Tracks.id) AS tracks_count
FROM Albums
JOIN Tracks ON Albums.id  = Tracks.album_id 
WHERE Albums.year_creation BETWEEN 2019 AND 2020;



--Видимо нужно перевести время в секунды и обратно, но SQLIte эту функцию не поддерживает
SELECT name_album, AVG(Tracks.duration) 
FROM Albums
JOIN Tracks ON Albums.id = Tracks.album_id
GROUP BY name_album;



SELECT name_singer 
FROM Singers s
JOIN SingerAlbum sa ON s.id = sa.singer_id  
JOIN Albums a ON sa.album_id = a.id 
WHERE a.year_creation != 2020


SELECT name_singer FROM Singers
WHERE name_singer NOT IN 
(SELECT DISTINCT name_singer FROM Singers s 
JOIN SingerAlbum sa ON s.id = sa.singer_id  
JOIN Albums a ON sa.album_id = a.id
WHERE a.year_creation = 2020)


SELECT DISTINCT name_compilation FROM Compilations c 
JOIN TrackCompilation tc ON c.id = tc.compilation_id 
JOIN Tracks t ON tc.track_id = t.id 
JOIN Albums a ON t.album_id = a.id 
JOIN SingerAlbum sa ON a.id = sa.album_id 
JOIN Singers s ON sa.singer_id = s.id 
WHERE name_singer = "Rammstein"; 








