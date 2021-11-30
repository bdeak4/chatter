SELECT data.*, percent_change_by_day, days_with_change,
	(percent_change_week / MAX(percent_change_week) OVER()) +
	(1.0 * sum_week / MAX(sum_week) OVER()) AS score
FROM (
	SELECT ticker, type,
		SUM(percent_change_day) AS percent_change_week,
		SUM(sum_day) AS sum_week,
		GROUP_CONCAT(percent_change_day) AS percent_change_by_day,
		GROUP_CONCAT(day_with_change) AS days_with_change
	FROM (
		SELECT ticker, type,
			CASE LAG(ticker, 1) OVER (ORDER BY ticker, date)
				WHEN ticker THEN CAST(
					100.0 * (SUM(count) -
					LAG(SUM(count), 1) OVER (ORDER BY ticker, date)) /
					LAG(SUM(count), 1) OVER (ORDER BY ticker, date)
				AS INT)
			END AS percent_change_day,
			CASE LAG(ticker, 1) OVER (ORDER BY ticker, date)
				WHEN ticker THEN CAST(
					JULIANDAY(DATE()) - JULIANDAY(date)
				AS INT)
			END AS day_with_change,
			SUM(count) AS sum_day,
			(
				SELECT AVG(sum_day)
				FROM (
					SELECT SUM(count) AS sum_day
					FROM tickers
					GROUP BY ticker
				)
			) AS avg_sum_day
		FROM (
			SELECT ticker, date, type,
				CASE source
					WHEN "post" THEN count * 5
					ELSE count
				END AS count
			FROM tickers
		)
		WHERE date >= DATE("now", "-7 days") AND type = ?
		GROUP BY date, ticker
		ORDER BY ticker, date
	)
	WHERE sum_day > avg_sum_day AND percent_change_day != ""
	GROUP BY ticker
) AS rising
INNER JOIN (
	SELECT ticker, type,
		SUM(CASE polarity WHEN 1 THEN count ELSE 0 END) AS polarity_positive_count,
		SUM(CASE polarity WHEN 0 THEN count ELSE 0 END) AS polarity_neutral_count,
		SUM(CASE polarity WHEN -1 THEN count ELSE 0 END) AS polarity_negative_count,
		SUM(CASE subjectivity WHEN 1 THEN count ELSE 0 END) AS subjectivity_subjective_count,
		SUM(CASE subjectivity WHEN 0 THEN count ELSE 0 END) AS subjectivity_objective_count,
		SUM(CASE source WHEN "post" THEN count ELSE 0 END) AS source_post_count,
		SUM(CASE source WHEN "comment" THEN count ELSE 0 END) AS source_comment_count
	FROM tickers
	WHERE date >= DATE("now", "-7 days")
	GROUP BY ticker
) AS data
ON rising.ticker = data.ticker AND rising.type = data.type
ORDER BY score DESC
LIMIT 25;
