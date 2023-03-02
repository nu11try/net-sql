SELECT genres.name, COUNT(performers.name)
FROM genres
         INNER JOIN performers_genres ON genres.id = performers_genres.genre_id
         INNER JOIN performers ON performers_genres.performer_id = performers.id
GROUP BY genres.name;

SELECT COUNT(tracks.name)
FROM tracks
         INNER JOIN albums ON tracks.album_id = albums.id
WHERE albums.year BETWEEN '2019-01-01' AND '2020-12-31';

SELECT albums.name, AVG(tracks.duration)
FROM albums
         INNER JOIN tracks ON tracks.album_id = albums.id
GROUP BY albums.name;

SELECT performers.name
FROM performers
WHERE performers.name not in (SELECT performers.name
                              FROM performers
                                       INNER JOIN performers_albums ON performers.id = performers_albums.performer_id
                                       INNER JOIN albums ON albums.id = performers_albums.album_id
                              WHERE albums.year BETWEEN '2020-01-01' and '2020-12-31');

SELECT collections.name
FROM collections
         INNER JOIN collections_tracks ON collections.id = collections_tracks.collection_id
         INNER JOIN tracks ON tracks.id = collections_tracks.track_id
         INNER JOIN albums ON albums.id = tracks.album_id
         INNER JOIN performers_albums ON performers_albums.album_id = albums.id
         INNER JOIN performers ON performers.id = performers_albums.performer_id
WHERE performers.name = 'Сплин'
GROUP BY collections.name;

SELECT albums.name
FROM albums
         INNER JOIN performers_albums ON albums.id = performers_albums.album_id
         INNER JOIN performers ON performers.id = performers_albums.performer_id
         INNER JOIN performers_genres ON performers.id = performers_genres.performer_id
         INNER JOIN genres ON genres.id = performers_genres.genre_id
GROUP BY albums.name
HAVING COUNT(distinct genres.name) > 1;

SELECT tracks.name
FROM tracks
         INNER JOIN collections_tracks ON tracks.id = collections_tracks.track_id
WHERE collections_tracks.collection_id IS NULL;

SELECT performers.name
FROM tracks
         INNER JOIN albums ON albums.id = tracks.album_id
         INNER JOIN performers_albums ON performers_albums.album_id = albums.id
         INNER JOIN performers ON performers.id = performers_albums.performer_id
GROUP BY performers.name, tracks.duration
HAVING tracks.duration = (SELECT min(duration) FROM tracks);

SELECT albums.name
FROM albums
         INNER JOIN tracks ON tracks.album_id = albums.id
WHERE tracks.album_id IN (SELECT album_id
                          FROM tracks
                          GROUP BY album_id
                          HAVING count(id) = (SELECT count(id)
                                              FROM tracks
                                              GROUP BY album_id
                                              ORDER BY count(tracks)
                                              LIMIT 1));
