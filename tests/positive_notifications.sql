select * from {{ ref('annual_summary') }}
where notifications <= 0 or reported_weeks < 1 or reported_weeks > 53
