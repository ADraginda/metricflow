-- Aggregate Measures
-- Compute Metrics via Expressions
SELECT
  metric_time__extract_dow
  , SUM(bookings) AS bookings
FROM (
  -- Read Elements From Semantic Model 'bookings_source'
  -- Metric Time Dimension 'ds'
  -- Pass Only Elements:
  --   ['bookings', 'metric_time__extract_dow']
  SELECT
    CASE WHEN EXTRACT(dow FROM ds) = 0 THEN EXTRACT(dow FROM ds) + 7 ELSE EXTRACT(dow FROM ds) END AS metric_time__extract_dow
    , 1 AS bookings
  FROM ***************************.fct_bookings bookings_source_src_10001
) subq_6
GROUP BY
  metric_time__extract_dow
