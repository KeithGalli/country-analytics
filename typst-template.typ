#let country-report(
  title: "title",
  country_code: "GBR",
  color: "#036531",
  body,
) = {
  
 set text(
    font: "Open Sans",
    size: 12pt,
  )

 set page(
    "us-letter",
    margin: (left: 0.5in, right: 0.5in, top: 0.55in, bottom: 0.0in),
    background: place(top, rect(fill: rgb(color), width: 100%, height: 0.5in)),
    header: align(
      horizon,
      grid(
        columns: (80%, 20%),
        align(left, text(size: 20pt, fill: white, weight: "bold", title)),
        align(right, text(size: 12pt, fill: white, weight: "bold", country_code)),
      ),
    ),
    // footer: align(
    //   grid(
    //     columns: (40%, 60%),
    //     align(horizon, text(fill: rgb("15397F"), size: 12pt, counter(page).display("1"))),
    //     align(right, image("path/to/logo.svg", height: 300%)),
    //   )
    // )
  )
  body
}