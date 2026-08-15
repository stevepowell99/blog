import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { FileTrieNode } from "./quartz/util/fileTrie"

// Sidebar sections in a deliberate order (focus areas first, attic last) rather than
// alphabetically. sortFn is stringified and re-evaluated in the browser, so it must not
// reference anything outside its own body.
const sectionExplorerOptions = {
  title: "Sections",
  sortFn: (a: FileTrieNode, b: FileTrieNode) => {
    const order = [
      "projects",
      "causal-mapping",
      "ai-and-evaluation",
      "theories-of-change",
      "methods",
      "puzzles",
      "attic",
    ]
    const ai = order.indexOf(a.slugSegment)
    const bi = order.indexOf(b.slugSegment)
    const ar = ai === -1 ? order.length : ai
    const br = bi === -1 ? order.length : bi
    if (ar !== br) return ar - br
    return a.displayName.localeCompare(b.displayName, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  },
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "Causal Map": "https://causalmap.app",
      Garden: "https://garden.causalmap.app",
      LinkedIn: "https://www.linkedin.com/in/stevepowell99/",
      "Google Scholar": "http://scholar.google.com/citations?user=RVSHfkAAAAAJ&hl=en",
      GitHub: "https://github.com/stevepowell99",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
    Component.ProjectFilter(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer(sectionExplorerOptions),
  ],
  right: [Component.DesktopOnly(Component.TableOfContents()), Component.Backlinks()],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer(sectionExplorerOptions),
  ],
  right: [],
}
