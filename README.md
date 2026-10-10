# VU23560 class web

The student homepage for VU23560 Access the internet and email.
It lists every `vu23560...` activity repo as cards inside lesson tabs.

Student link: https://teacherfrances.github.io/vu23560/

## How new activities appear

1. Make a new repo whose name starts with `vu23560` (capital letters are fine).
2. Turn on GitHub Pages for it.
3. That's it. It shows on the homepage within an hour.

Two things keep the list up to date:

- **The hourly update** (`.github/workflows/update-activities.yml`) checks your repos every hour
  and saves the list in `activities.json`. To run it now: Actions tab > Update activity list > Run workflow.
- **The live check** in `index.html` also asks GitHub for new repos when a student opens the page
  (once an hour per device), so a new activity can show up before the hourly update runs.

## How the homepage sorts things

| Repo name contains | Shown as |
|---|---|
| `lesson1`, `lesson2` ... (also `lesson_4`, `lesson-4`) | That lesson's tab |
| no lesson number | The Bonus tab |
| `deck` or `slides` | Lesson slides |
| `revision` | Revision |
| `jeopardy` or `board` | Double Jeopardy |
| `escape` | Escape room |
| `seek` or `hunt` | Seek and find |
| `phone` | Phone game |
| `email` or `inbox` | Email game |
| `quiz` | Quiz |
| `record`, `sayit`, `pronun`, `speak` | Speaking practice |
| anything else | Activity |

- The card name comes from the `<title>` of the activity page.
- The lesson name on each tab comes from the revision or jeopardy title (the part before the colon),
  or from the slide deck title if there is no revision or jeopardy yet.
- Activities made in the last 14 days show as new emails in the Inbox and get a NEW tag.

## Changing things (settings.json)

```json
{
  "prefix": "vu23560",
  "hide": ["VU23560_week1_lesson1"],
  "titles": { "vu23560seekandfind1": "Find it on the screen" },
  "lessonNames": { "4": "Emails at work" },
  "types": { "vu23560lesson4game": "email" }
}
```

- `hide`: repos to leave off the homepage. `VU23560_week1_lesson1` is hidden because it is the same
  page as `vu23560lesson1revision`. Delete it from this list to show it again.
- `titles`: a different name to show for a repo.
- `lessonNames`: a different name for a lesson tab.
- `types`: a different card type for a repo (deck, revision, jeopardy, escape, seek, phone, email, quiz, speak, other).

Saving this file runs the update straight away.

## If the Actions tab is empty

The `.github` folder is hidden on most computers, so it often does not upload.
Make it by hand:

1. In the repo, click **Add file > Create new file**.
2. Type the name `.github/workflows/update-activities.yml`
3. Paste in everything from `setup/update-activities.yml` (it is the same file).
4. Click **Commit changes**.
