# Saturday 21 November 2026 — the world in one image

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261121-ff6a00)](https://make.fun/r/68mq8j14)
![Built with Claude Code + Grok Build](https://img.shields.io/badge/built%20with-Claude%20Code%20%2B%20Grok%20Build-555)

Entry for the make.fun bounty `news-image-20261121`: sum up one day's world news in a single 1024x1024 image.

![entry](entry.png)

## What the image shows

- 40 stories from Saturday 21 November 2026: 12 with pictures (4 lead stories and 8 smaller ones) and 28 one-line briefs.
- 7 regions: Europe (9 stories), Asia (8), Americas (6), Africa (6), Middle East (6), Oceania (4) and World/Space (1). Each region has its own colour, and a bar shows how many stories each region has.
- A map with numbered pins for the pictured stories, six key numbers, and a UTC timeline of the day.
- Every story is date-checked. A date-check band near the bottom lists 5 stories left out because they were first reported earlier (19 or 20 November) and 2 that are scheduled for later (22 and 29 November).
- Each picture card is tagged CONFIRMED or CLAIM, and each brief names its source. Claims made by governments, armed groups or officials are attributed to them.

## How it is made

1. **Research** sessions in Grok Build (r1 to r4) collected candidate stories with source links (`research/r*.json`, notes in `research/*-notes.md`). Two later gap-filling sessions (rx1, rx2) added stories for regions and beats that had too few (`research/rx1.json`, `research/rx2.json`).
2. **Re-check** sessions in Grok Build (va, vb) checked each shortlisted story's date, figures and wording on their own (`research/verify-a.json`, `research/verify-b.json`). Stories first reported before 21 November were dropped. Figures were corrected where the sources disagreed.
3. The final content is in `data/stories.json`.
4. Code sessions in Claude Code wrote `build.py` (Python), which turns that file into an HTML/SVG page. The pictures and map are drawn in code. Headless Chrome renders the page, and Pillow reduces the screenshot to a 256-colour palette PNG. The build renders twice and checks that both renders match. It also checks the file size, that no text is smaller than 11 px, and that no text overflows its box.

## How to rebuild

```sh
python3 build.py      # data/stories.json -> entry.png
python3 main.py
```

You need Python 3 with Pillow, and Google Chrome.

## Sources

AP, Reuters, AFP, BBC, Al Jazeera, EFE, Kyodo, Yonhap, ABC News, USGS, UKMTO. The briefs also cite Ukrinform, TVP, Guardian, Met Office, IRNA, Xinhua, CAF, Daily Trust, Actualite.cd, Daily Star, NDTV, PTI, Senapred and CAAP. Each story's own source is printed on the image.

Join make.fun: https://make.fun/r/68mq8j14
