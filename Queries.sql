--top 10 songs by year
select name, title, year, hotness, rownr
from
(
select a.name, s.title, s.year, s.hotness,
row_number() over(
    partition by s.year
    order by s.hotness desc) rownr
from public.songs s
inner join public.artists a on a.key_id = s.artist_key_id
where year between 2000 and 2010
) x where rownr <= 10
order by year

-- song count amorphis and similar to amorphis by year
select year, count(1) songcount
from songs
where artist_key_id in
(
select s.similarartist_key_id
from artists a
inner join similarartists s on s.artist_key_id = a.key_id
where a.name = 'Amorphis'
union
select a.key_id
from artists a
where a.name = 'Amorphis'
)
group by year

--top 10 song in uk
select *
from songs
where artist_key_id in
(
select key_id from artists
where latitude between 50.5 and 58.5
and longitude between -5.8 and 1.3
)
order by hotness desc
limit 10

--top slow songs between 1960 and 1980
select name, title, year, hotness, rownr
from
(
select a.name, s.title, s.year, s.hotness,
row_number() over(
    partition by s.year
    order by s.hotness desc) rownr
from public.songs s
inner join public.artists a on a.key_id = s.artist_key_id
where s.year <= 1980 and s.year >= 1960 and s.tempo < 100 and s.mode = 1
) x where rownr = 1
order by year

--random 10 hot songs year after 2000
with sng as
(
select a.name, s.title, s.year, s.hotness,
row_number() over(
    order by s.hotness desc) rownr
from public.songs s
inner join public.artists a on a.key_id = s.artist_key_id
where s.year >= 2000 and s.hotness > 0.6
)
select * from sng
where rownr in
(
	SELECT (y.maxrownr * random())::int + 1 r_num
	FROM generate_series(1,10)
	cross join (select max(rownr) maxrownr from sng) y
	group by 1
)