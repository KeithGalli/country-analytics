#show: psc-report.with(
  $if(title)$
    title: "$title$",
  $endif$
  $if(country_code)$
    country_code: "$country_code$",
  $endif$
)