import { QuartzComponent, QuartzComponentConstructor } from "./types"
// @ts-ignore
import script from "./scripts/projectfilter.inline"
import style from "./styles/projectFilter.scss"

// Ships only behaviour and styling. The filter bar markup itself is emitted into
// content/projects.md by scripts/build_project_list.py; the script no-ops on
// every other page.
export default (() => {
  const ProjectFilter: QuartzComponent = () => null
  ProjectFilter.afterDOMLoaded = script
  ProjectFilter.css = style
  return ProjectFilter
}) satisfies QuartzComponentConstructor
