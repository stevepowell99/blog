---
name: blog-news
description: Refresh the News page on pogol.net with what Steve has been working on since the last entry, roughly every four months. Use when Steve says /blog-news, "update the blog news", "refresh the news page", "what's new for the blog", or when the xkTODO tracker in this repo comes due.
---

# Refresh the blog News page

`content/news.md` carries one dated section every four months, newest first. This skill writes the next one. Nothing here is automatic: a session runs it, Steve approves the text, and the push publishes it.

## 1. Find the window

Read `content/news.md` and take the date of the top section. Everything after that date is the window. If the page is missing a section for the current period, write one even when the window is thin; a short entry beats a stale page.

## 2. Gather

Only from these sources, and only what is already public or plainly safe to publish:

| Source | What to look for |
|---|---|
| `C:\dev\causal-map-extension` git log | user-facing features in the Causal Map app; ignore refactors, infra, prompts, tests |
| `C:\dev\qualia-edit-multi`, `C:\dev\qualia-client-multi`, `C:\dev\qualia-deliberate` | user-facing Qualia changes, new apps, launches |
| `C:\dev\causalmap-zotero` releases | plugin releases worth a sentence |
| `...\12 Papers and articles and conferences\` | accepted papers, conference dates, published articles |
| `...\19aCMgarden\content\` | new Garden pages and working papers worth linking |
| `C:\dev\IFRC26-dev\CLAUDE.md` and any other live consultancy `CLAUDE.md` | the current engagement, role and dates |
| `content/projects.md` in this repo | new rows since the last entry, which are already public |

Use `git log --since=<date> --no-merges --pretty="%ad %s" --date=short`.

## 3. Judge what goes in

- Public or safe only. Client findings, unannounced client names, revenue, staffing, anything from the CRM or a private client folder stay out. A project already listed on `content/projects.md` is public.
- Say nothing about a product feature Steve has not shipped to users, unless it is described as in testing.
- No invented numbers, dates or titles. Every fact traces to a source above, and anything you cannot trace gets dropped rather than softened.
- Four to seven items. Each one gets a bold lead-in and a short paragraph.

## 4. Write

Add a new `## Month Year` section directly under the intro paragraph, above the previous section. Keep the last six sections and delete anything older, so the page stays about two years long.

House style applies: British English, no em dashes, no boosterism, verbs over nominalisations, no rule-of-three lists, no closing sentence that ties a bow. Run the global `style-review` skill over the new section before showing it to Steve.

## 5. Build, show, push

1. `npx quartz build` and check the page renders and the sidebar entry is there (`news` is first in the `sortFn` order array in `quartz.layout.ts`).
2. Show Steve the new section in chat as bullets and name every claim he should check.
3. Commit. Push only once he has said yes, since this publishes to pogol.net.

## 6. Reset the tracker

Rename the tracker file in this repo root so its `xh-` date is four months after today, for example `xkTODO refresh the blog news page xpCLAUDE xh-2027-04-16.md`. That hide-until date is the whole schedule: the SessionStart hook surfaces the file in this repo once the date passes, and hides it before then. Commit the rename with the news entry.
