type Section = {
  heading: HTMLElement
  table: HTMLTableElement
  rows: HTMLTableRowElement[]
  rowText: string[]
  rowSource: string[]
  countable: boolean
}

// The projects page is a generated table of ~200 rows grouped under h2 themes.
// Rows carry no data attributes, so match on cell text: last cell is the source
// bucket (talks tables have no source column, so they only show under "All").
function collectSections(root: HTMLElement): Section[] {
  const sections: Section[] = []
  for (const heading of Array.from(root.querySelectorAll("h2")) as HTMLElement[]) {
    let el = heading.nextElementSibling
    while (el && el.tagName !== "H2" && el.tagName !== "TABLE") {
      el = el.nextElementSibling
    }
    if (!el || el.tagName !== "TABLE") continue
    const table = el as HTMLTableElement
    const rows = Array.from(table.tBodies[0]?.rows ?? [])
    const headers = Array.from(table.tHead?.rows[0]?.cells ?? []).map((c) =>
      (c.textContent ?? "").trim().toLowerCase(),
    )
    const sourceCol = headers.indexOf("source")
    sections.push({
      heading,
      table,
      rows,
      rowText: rows.map((r) => (r.textContent ?? "").toLowerCase()),
      rowSource: rows.map((r) =>
        sourceCol >= 0 ? (r.cells[sourceCol]?.textContent ?? "").trim() : "",
      ),
      countable: sourceCol >= 0,
    })
  }
  return sections
}

document.addEventListener("nav", () => {
  const filter = document.getElementById("project-filter")
  if (!filter) return
  const article = filter.closest("article")
  if (!article) return

  const search = document.getElementById("project-search") as HTMLInputElement | null
  const theme = document.getElementById("project-theme") as HTMLSelectElement | null
  const source = document.getElementById("project-source") as HTMLSelectElement | null
  const count = document.getElementById("project-count")
  const reset = document.getElementById("project-reset")
  if (!search || !theme || !source || !count) return

  const sections = collectSections(article)
  // the talks table has no source column and is not counted as a project
  const total = sections.reduce((n, s) => n + (s.countable ? s.rows.length : 0), 0)

  // populate the theme select from the headings actually present
  for (const s of sections) {
    const opt = document.createElement("option")
    opt.value = opt.textContent = (s.heading.textContent ?? "").trim()
    theme.appendChild(opt)
  }

  const apply = () => {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean)
    const wantTheme = theme.value
    const wantSource = source.value
    let shown = 0

    for (const s of sections) {
      const label = (s.heading.textContent ?? "").trim()
      const themeOk = wantTheme === "" || wantTheme === label
      let visibleHere = 0

      s.rows.forEach((row, i) => {
        const sourceOk = wantSource === "" || s.rowSource[i] === wantSource
        const textOk = terms.every((t) => s.rowText[i].includes(t))
        const show = themeOk && sourceOk && textOk
        row.hidden = !show
        if (show) visibleHere++
      })

      s.heading.hidden = visibleHere === 0
      s.table.hidden = visibleHere === 0
      if (s.countable) shown += visibleHere
    }

    const filtering = terms.length > 0 || wantTheme !== "" || wantSource !== ""
    count.textContent = filtering
      ? `Showing ${shown} of ${total} projects`
      : `${total} projects`
    if (reset) reset.hidden = !filtering
  }

  const onReset = () => {
    search.value = ""
    theme.value = ""
    source.value = ""
    apply()
  }

  search.addEventListener("input", apply)
  theme.addEventListener("change", apply)
  source.addEventListener("change", apply)
  reset?.addEventListener("click", onReset)
  window.addCleanup(() => {
    search.removeEventListener("input", apply)
    theme.removeEventListener("change", apply)
    source.removeEventListener("change", apply)
    reset?.removeEventListener("click", onReset)
  })

  apply()
})
