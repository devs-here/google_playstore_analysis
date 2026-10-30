CREATE DATABASE IF NOT EXISTS google_play_analysis;
USE google_play_analysis;

-- 1. Apps and rated apps per category
SELECT
    category,
    COUNT(*)      AS total_apps,
    COUNT(rating) AS rated_apps,
    ROUND(100 * COUNT(rating) / COUNT(*), 1) AS pct_rated
FROM apps
GROUP BY category
ORDER BY total_apps DESC;

-- 2. Rating vs number of apps per category
SELECT
    category,
    COUNT(*)              AS total_apps,
    COUNT(rating)         AS rated_apps,
    ROUND(AVG(rating), 2) AS avg_rating
FROM apps
GROUP BY category
HAVING COUNT(rating) >= 50
ORDER BY avg_rating DESC;

-- 3. Free vs paid apps
SELECT
    type,
    COUNT(*)              AS total_apps,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(reviews))   AS avg_reviews,
    ROUND(AVG(installs))  AS avg_installs
FROM apps
WHERE type IS NOT NULL
GROUP BY type;

-- 4. Install ranges vs rating and reviews
SELECT
    CASE
        WHEN installs < 1000       THEN '1. Under 1K'
        WHEN installs < 100000     THEN '2. 1K - 100K'
        WHEN installs < 10000000   THEN '3. 100K - 10M'
        ELSE                            '4. 10M+'
    END AS install_range,
    COUNT(*)              AS total_apps,
    COUNT(rating)         AS rated_apps,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(reviews))   AS avg_reviews
FROM apps
GROUP BY install_range
ORDER BY install_range;

-- 5a. Top 10 apps by reviews
SELECT app, category, reviews, rating
FROM apps
ORDER BY reviews DESC
LIMIT 10;

-- 5b. Top 10 apps by installs (ties ordered by reviews)
SELECT app, category, installs, reviews, rating
FROM apps
ORDER BY installs DESC, reviews DESC
LIMIT 10;

-- 6. Ratings by last update year
SELECT
    YEAR(last_updated)    AS update_year,
    COUNT(*)              AS total_apps,
    COUNT(rating)         AS rated_apps,
    ROUND(AVG(rating), 2) AS avg_rating
FROM apps
WHERE last_updated IS NOT NULL
GROUP BY update_year
ORDER BY update_year;

-- 7. Content rating vs rating and installs
SELECT
    content_rating,
    COUNT(*)              AS total_apps,
    COUNT(rating)         AS rated_apps,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(installs))  AS avg_installs
FROM apps
GROUP BY content_rating
ORDER BY total_apps DESC;

-- 8. App size vs rating and installs
SELECT
    CASE
        WHEN size_mb < 5   THEN '1. Under 5 MB'
        WHEN size_mb < 20  THEN '2. 5 - 20 MB'
        WHEN size_mb < 50  THEN '3. 20 - 50 MB'
        ELSE                    '4. 50 MB+'
    END AS size_range,
    COUNT(*)              AS total_apps,
    COUNT(rating)         AS rated_apps,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(installs))  AS avg_installs
FROM apps
WHERE size_mb IS NOT NULL
GROUP BY size_range
ORDER BY size_range;

-- 9. Heatmap data: rating by category and install range
SELECT category,
       CASE
           WHEN installs < 1000     THEN '1. Under 1K'
           WHEN installs < 100000   THEN '2. 1K - 100K'
           WHEN installs < 10000000 THEN '3. 100K - 10M'
           ELSE                          '4. 10M+'
       END AS install_range,
       COUNT(rating) AS rated_apps,
       ROUND(AVG(rating), 2) AS avg_rating
FROM apps
GROUP BY category, install_range
HAVING COUNT(rating) >= 10
ORDER BY category, install_range;