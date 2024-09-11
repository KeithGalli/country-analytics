#show: country-report.with(
  $if(title)$
    title: "$title$",
  $endif$
  $if(params.country_code)$
    country_code: "$params.country_code$",
  $endif$
  $if(params.color)$
    color: "$params.color$",
  $endif$
)