#show: country-report.with(
  $if(title)$
    title: "$title$",
  $endif$
  $if(country_code)$
    country_code: "$country_code$",
  $endif$
  $if(color)$
    color: "$color$",
  $endif$
)