-- Compute Metrics via Expressions
SELECT
  subq_6.metric_time
  , delayed_bookings * 2 AS double_counted_delayed_bookings
FROM (
  -- Aggregate Measures
  SELECT
    subq_5.metric_time
    , SUM(subq_5.bookings) AS delayed_bookings
  FROM (
    -- Pass Only Elements:
    --   ['bookings', 'metric_time']
    SELECT
      subq_4.metric_time
      , subq_4.bookings
    FROM (
      -- Constrain Output with WHERE
      SELECT
        subq_3.metric_time
        , subq_3.is_instant
        , subq_3.bookings
      FROM (
        -- Pass Only Elements:
        --   ['bookings', 'is_instant', 'metric_time']
        SELECT
          subq_2.metric_time
          , subq_2.is_instant
          , subq_2.bookings
        FROM (
          -- Metric Time Dimension 'ds'
          SELECT
            subq_1.ds
            , subq_1.ds__week
            , subq_1.ds__month
            , subq_1.ds__quarter
            , subq_1.ds__year
            , subq_1.ds_partitioned
            , subq_1.ds_partitioned__week
            , subq_1.ds_partitioned__month
            , subq_1.ds_partitioned__quarter
            , subq_1.ds_partitioned__year
            , subq_1.booking_paid_at
            , subq_1.booking_paid_at__week
            , subq_1.booking_paid_at__month
            , subq_1.booking_paid_at__quarter
            , subq_1.booking_paid_at__year
            , subq_1.create_a_cycle_in_the_join_graph__ds
            , subq_1.create_a_cycle_in_the_join_graph__ds__week
            , subq_1.create_a_cycle_in_the_join_graph__ds__month
            , subq_1.create_a_cycle_in_the_join_graph__ds__quarter
            , subq_1.create_a_cycle_in_the_join_graph__ds__year
            , subq_1.create_a_cycle_in_the_join_graph__ds_partitioned
            , subq_1.create_a_cycle_in_the_join_graph__ds_partitioned__week
            , subq_1.create_a_cycle_in_the_join_graph__ds_partitioned__month
            , subq_1.create_a_cycle_in_the_join_graph__ds_partitioned__quarter
            , subq_1.create_a_cycle_in_the_join_graph__ds_partitioned__year
            , subq_1.create_a_cycle_in_the_join_graph__booking_paid_at
            , subq_1.create_a_cycle_in_the_join_graph__booking_paid_at__week
            , subq_1.create_a_cycle_in_the_join_graph__booking_paid_at__month
            , subq_1.create_a_cycle_in_the_join_graph__booking_paid_at__quarter
            , subq_1.create_a_cycle_in_the_join_graph__booking_paid_at__year
            , subq_1.ds AS metric_time
            , subq_1.ds__week AS metric_time__week
            , subq_1.ds__month AS metric_time__month
            , subq_1.ds__quarter AS metric_time__quarter
            , subq_1.ds__year AS metric_time__year
            , subq_1.listing
            , subq_1.guest
            , subq_1.host
            , subq_1.create_a_cycle_in_the_join_graph
            , subq_1.create_a_cycle_in_the_join_graph__listing
            , subq_1.create_a_cycle_in_the_join_graph__guest
            , subq_1.create_a_cycle_in_the_join_graph__host
            , subq_1.is_instant
            , subq_1.create_a_cycle_in_the_join_graph__is_instant
            , subq_1.bookings
            , subq_1.instant_bookings
            , subq_1.booking_value
            , subq_1.max_booking_value
            , subq_1.min_booking_value
            , subq_1.bookers
            , subq_1.average_booking_value
          FROM (
            -- Pass Only Additive Measures
            SELECT
              subq_0.ds
              , subq_0.ds__week
              , subq_0.ds__month
              , subq_0.ds__quarter
              , subq_0.ds__year
              , subq_0.ds_partitioned
              , subq_0.ds_partitioned__week
              , subq_0.ds_partitioned__month
              , subq_0.ds_partitioned__quarter
              , subq_0.ds_partitioned__year
              , subq_0.booking_paid_at
              , subq_0.booking_paid_at__week
              , subq_0.booking_paid_at__month
              , subq_0.booking_paid_at__quarter
              , subq_0.booking_paid_at__year
              , subq_0.create_a_cycle_in_the_join_graph__ds
              , subq_0.create_a_cycle_in_the_join_graph__ds__week
              , subq_0.create_a_cycle_in_the_join_graph__ds__month
              , subq_0.create_a_cycle_in_the_join_graph__ds__quarter
              , subq_0.create_a_cycle_in_the_join_graph__ds__year
              , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned
              , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__week
              , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__month
              , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__quarter
              , subq_0.create_a_cycle_in_the_join_graph__ds_partitioned__year
              , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at
              , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__week
              , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__month
              , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__quarter
              , subq_0.create_a_cycle_in_the_join_graph__booking_paid_at__year
              , subq_0.listing
              , subq_0.guest
              , subq_0.host
              , subq_0.create_a_cycle_in_the_join_graph
              , subq_0.create_a_cycle_in_the_join_graph__listing
              , subq_0.create_a_cycle_in_the_join_graph__guest
              , subq_0.create_a_cycle_in_the_join_graph__host
              , subq_0.is_instant
              , subq_0.create_a_cycle_in_the_join_graph__is_instant
              , subq_0.bookings
              , subq_0.instant_bookings
              , subq_0.booking_value
              , subq_0.max_booking_value
              , subq_0.min_booking_value
              , subq_0.bookers
              , subq_0.average_booking_value
            FROM (
              -- Read Elements From Data Source 'bookings_source'
              SELECT
                1 AS bookings
                , CASE WHEN is_instant THEN 1 ELSE 0 END AS instant_bookings
                , bookings_source_src_10001.booking_value
                , bookings_source_src_10001.booking_value AS max_booking_value
                , bookings_source_src_10001.booking_value AS min_booking_value
                , bookings_source_src_10001.guest_id AS bookers
                , bookings_source_src_10001.booking_value AS average_booking_value
                , bookings_source_src_10001.booking_value AS booking_payments
                , bookings_source_src_10001.is_instant
                , bookings_source_src_10001.ds
                , DATE_TRUNC('week', bookings_source_src_10001.ds) AS ds__week
                , DATE_TRUNC('month', bookings_source_src_10001.ds) AS ds__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.ds) AS ds__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.ds) AS ds__year
                , bookings_source_src_10001.ds_partitioned
                , DATE_TRUNC('week', bookings_source_src_10001.ds_partitioned) AS ds_partitioned__week
                , DATE_TRUNC('month', bookings_source_src_10001.ds_partitioned) AS ds_partitioned__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.ds_partitioned) AS ds_partitioned__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.ds_partitioned) AS ds_partitioned__year
                , bookings_source_src_10001.booking_paid_at
                , DATE_TRUNC('week', bookings_source_src_10001.booking_paid_at) AS booking_paid_at__week
                , DATE_TRUNC('month', bookings_source_src_10001.booking_paid_at) AS booking_paid_at__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.booking_paid_at) AS booking_paid_at__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.booking_paid_at) AS booking_paid_at__year
                , bookings_source_src_10001.is_instant AS create_a_cycle_in_the_join_graph__is_instant
                , bookings_source_src_10001.ds AS create_a_cycle_in_the_join_graph__ds
                , DATE_TRUNC('week', bookings_source_src_10001.ds) AS create_a_cycle_in_the_join_graph__ds__week
                , DATE_TRUNC('month', bookings_source_src_10001.ds) AS create_a_cycle_in_the_join_graph__ds__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.ds) AS create_a_cycle_in_the_join_graph__ds__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.ds) AS create_a_cycle_in_the_join_graph__ds__year
                , bookings_source_src_10001.ds_partitioned AS create_a_cycle_in_the_join_graph__ds_partitioned
                , DATE_TRUNC('week', bookings_source_src_10001.ds_partitioned) AS create_a_cycle_in_the_join_graph__ds_partitioned__week
                , DATE_TRUNC('month', bookings_source_src_10001.ds_partitioned) AS create_a_cycle_in_the_join_graph__ds_partitioned__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.ds_partitioned) AS create_a_cycle_in_the_join_graph__ds_partitioned__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.ds_partitioned) AS create_a_cycle_in_the_join_graph__ds_partitioned__year
                , bookings_source_src_10001.booking_paid_at AS create_a_cycle_in_the_join_graph__booking_paid_at
                , DATE_TRUNC('week', bookings_source_src_10001.booking_paid_at) AS create_a_cycle_in_the_join_graph__booking_paid_at__week
                , DATE_TRUNC('month', bookings_source_src_10001.booking_paid_at) AS create_a_cycle_in_the_join_graph__booking_paid_at__month
                , DATE_TRUNC('quarter', bookings_source_src_10001.booking_paid_at) AS create_a_cycle_in_the_join_graph__booking_paid_at__quarter
                , DATE_TRUNC('year', bookings_source_src_10001.booking_paid_at) AS create_a_cycle_in_the_join_graph__booking_paid_at__year
                , bookings_source_src_10001.listing_id AS listing
                , bookings_source_src_10001.guest_id AS guest
                , bookings_source_src_10001.host_id AS host
                , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph
                , bookings_source_src_10001.listing_id AS create_a_cycle_in_the_join_graph__listing
                , bookings_source_src_10001.guest_id AS create_a_cycle_in_the_join_graph__guest
                , bookings_source_src_10001.host_id AS create_a_cycle_in_the_join_graph__host
              FROM (
                -- User Defined SQL Query
                SELECT * FROM ***************************.fct_bookings
              ) bookings_source_src_10001
            ) subq_0
          ) subq_1
        ) subq_2
      ) subq_3
      WHERE NOT is_instant
    ) subq_4
  ) subq_5
  GROUP BY
    subq_5.metric_time
) subq_6
