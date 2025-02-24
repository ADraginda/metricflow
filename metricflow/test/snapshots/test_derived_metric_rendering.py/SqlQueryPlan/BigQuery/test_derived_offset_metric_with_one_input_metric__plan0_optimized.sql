-- Compute Metrics via Expressions
SELECT
  metric_time__day
  , bookings_5_days_ago AS bookings_5_day_lag
FROM (
  -- Join to Time Spine Dataset
  -- Pass Only Elements:
  --   ['bookings', 'metric_time__day']
  -- Aggregate Measures
  -- Compute Metrics via Expressions
  SELECT
    subq_11.ds AS metric_time__day
    , SUM(subq_9.bookings) AS bookings_5_days_ago
  FROM ***************************.mf_time_spine subq_11
  INNER JOIN (
    -- Read Elements From Semantic Model 'bookings_source'
    -- Metric Time Dimension 'ds'
    SELECT
      DATE_TRUNC(ds, day) AS metric_time__day
      , 1 AS bookings
    FROM ***************************.fct_bookings bookings_source_src_10001
  ) subq_9
  ON
    DATE_SUB(CAST(subq_11.ds AS DATETIME), INTERVAL 5 day) = subq_9.metric_time__day
  GROUP BY
    metric_time__day
) subq_15
