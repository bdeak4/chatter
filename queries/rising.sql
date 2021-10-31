SELECT data.*, percent_change_by_day,
	(percent_change_week / MAX(percent_change_week) OVER()) +
	(1.0 * sum_week / MAX(sum_week) OVER()) AS score
FROM (
	SELECT ticker,
		SUM(percent_change_day) AS percent_change_week,
		SUM(sum_day) AS sum_week,
		GROUP_CONCAT(CAST(percent_change_day AS INT)) AS percent_change_by_day
	FROM (
		SELECT ticker,
			CASE LAG(ticker, 1) OVER (ORDER BY ticker, date)
				WHEN ticker THEN (
					100.0 * (SUM(count) -
					LAG(SUM(count), 1) OVER (ORDER BY ticker, date)) /
					LAG(SUM(count), 1) OVER (ORDER BY ticker, date)
				)
			END AS percent_change_day,
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
		WHERE date >= DATE("now", "-7 days") AND type = 'crypto'
		GROUP BY date, ticker
		ORDER BY ticker, date
	)
	WHERE sum_day > avg_sum_day
	GROUP BY ticker
) AS rising INNER JOIN (
	SELECT ticker,
		SUM(CASE polarity WHEN 1 THEN count ELSE 0 END) AS polarity_positive_count,
		SUM(CASE polarity WHEN 0 THEN count ELSE 0 END) AS polarity_neutral_count,
		SUM(CASE polarity WHEN -1 THEN count ELSE 0 END) AS polarity_negative_count,
		SUM(CASE subjectivity WHEN 1 THEN count ELSE 0 END) AS subjectivity_subjective_count,
		SUM(CASE subjectivity WHEN 0 THEN count ELSE 0 END) AS subjectivity_objective_count,
		SUM(CASE source WHEN "post" THEN count ELSE 0 END) AS source_post_count,
		SUM(CASE source WHEN "comment" THEN count ELSE 0 END) AS source_comment_count
	FROM tickers
	WHERE date >= DATE("now", "-7 days") AND type = 'crypto'
	GROUP BY ticker
) AS data ON rising.ticker = data.ticker
ORDER BY score DESC
LIMIT 15;
