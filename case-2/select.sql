SELECT name, year FROM albums WHERE year BETWEEN '2018-01-01' and '2018-12-31';

-- Долгая выборка
SELECT name, duration FROM tracks WHERE duration = (SELECT MAX(duration) FROM tracks);

-- Быстрая выборка
SELECT name, duration FROM tracks ORDER BY duration DESC limit 1;

SELECT name, duration FROM tracks WHERE duration >= 210;

SELECT name FROM collections WHERE year BETWEEN '2018-01-01' and '2020-12-31';

SELECT name FROM performers WHERE NOT name LIKE '%% %%';

SELECT name FROM tracks WHERE name LIKE '%%Мой%%' OR name LIKE '%%мой%%';
