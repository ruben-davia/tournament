from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "model_inputs" / "live_scorekeeper" / "raw"
ASSET_PATH = ROOT / "docs" / "assets" / "readme-ww2026-picks-through-j4.svg"
HTML_PATH = ROOT / "docs" / "ww2026-picks-through-j4.html"
USER_ID = "916"


STRATEGY_BY_DAY = {
    1: "market baseline",
    2: "btts-over controlled",
    3: "risk-capped",
    4: "field leverage + risk cap",
}

FALLBACK_PICKS_BY_DAY = {
    1: [
        ("Mexico", "South Africa", 1, 0, False),
        ("South Korea", "Czechia", 1, 0, False),
        ("Canada", "Bosnia-Herz", 0, 1, False),
        ("USA", "Paraguay", 0, 1, False),
        ("Qatar", "Switzerland", 0, 2, False),
        ("Brazil", "Morocco", 0, 1, False),
        ("Haiti", "Scotland", 1, 0, False),
        ("Australia", "Türkiye", 0, 1, False),
        ("Germany", "Curacao", 3, 0, False),
        ("Netherlands", "Japan", 0, 1, False),
        ("Ivory Coast", "Ecuador", 1, 0, False),
        ("Sweden", "Tunisia", 0, 1, False),
        ("Spain", "Cape Verde", 3, 0, False),
        ("Belgium", "Egypt", 0, 1, False),
        ("Saudi Arabia", "Uruguay", 0, 2, False),
        ("Iran", "New Zealand", 0, 1, False),
        ("France", "Senegal", 2, 0, False),
        ("Iraq", "Norway", 0, 2, False),
        ("Argentina", "Algeria", 2, 0, False),
        ("Austria", "Jordan", 2, 0, False),
        ("Portugal", "Congo DR", 2, 0, False),
        ("England", "Croatia", 0, 1, False),
        ("Ghana", "Panama", 0, 1, False),
        ("Uzbekistan", "Colombia", 0, 2, False),
    ],
    2: [
        ("Czechia", "South Africa", 0, 1, False),
        ("Switzerland", "Bosnia-Herz", 1, 1, False),
        ("Canada", "Qatar", 2, 1, False),
        ("Mexico", "South Korea", 1, 1, False),
        ("USA", "Australia", 1, 1, False),
        ("Scotland", "Morocco", 1, 2, False),
        ("Brazil", "Haiti", 3, 0, False),
        ("Türkiye", "Paraguay", 0, 1, False),
        ("Netherlands", "Sweden", 2, 1, False),
        ("Germany", "Ivory Coast", 2, 1, False),
        ("Ecuador", "Curacao", 2, 0, False),
        ("Tunisia", "Japan", 1, 2, False),
        ("Spain", "Saudi Arabia", 2, 0, False),
        ("Belgium", "Iran", 2, 1, False),
        ("Uruguay", "Cape Verde", 2, 1, False),
        ("New Zealand", "Egypt", 1, 2, False),
        ("Argentina", "Austria", 2, 1, False),
        ("France", "Iraq", 3, 0, False),
        ("Norway", "Senegal", 1, 2, False),
        ("Jordan", "Algeria", 1, 2, False),
        ("Portugal", "Uzbekistan", 2, 0, False),
        ("England", "Ghana", 2, 0, False),
        ("Panama", "Croatia", 1, 2, False),
        ("Colombia", "Congo DR", 2, 1, False),
    ],
    3: [
        ("Bosnia-Herz", "Qatar", 2, 1, False),
        ("Switzerland", "Canada", 2, 1, False),
        ("Morocco", "Haiti", 2, 0, False),
        ("Scotland", "Brazil", 1, 2, False),
        ("Czechia", "Mexico", 1, 2, False),
        ("South Africa", "South Korea", 1, 2, False),
        ("Curacao", "Ivory Coast", 0, 2, False),
        ("Ecuador", "Germany", 1, 2, False),
        ("Japan", "Sweden", 2, 1, False),
        ("Tunisia", "Netherlands", 0, 2, False),
        ("Paraguay", "Australia", 0, 0, False),
        ("Türkiye", "USA", 1, 2, False),
        ("Norway", "France", 1, 2, False),
        ("Senegal", "Iraq", 2, 0, False),
        ("Cape Verde", "Saudi Arabia", 2, 1, False),
        ("Uruguay", "Spain", 1, 2, False),
        ("Egypt", "Iran", 1, 1, False),
        ("New Zealand", "Belgium", 0, 2, False),
        ("Croatia", "Ghana", 2, 1, False),
        ("Panama", "England", 0, 2, False),
        ("Colombia", "Portugal", 1, 2, False),
        ("Congo DR", "Uzbekistan", 2, 1, False),
        ("Algeria", "Austria", 1, 1, False),
        ("Jordan", "Argentina", 0, 2, False),
    ],
    4: [
        ("South Africa", "Canada", 0, 1, False),
        ("Brazil", "Japan", 2, 0, False),
        ("Germany", "Paraguay", 2, 0, False),
        ("Netherlands", "Morocco", 1, 0, False),
        ("Ivory Coast", "Norway", 1, 2, False),
        ("France", "Sweden", 2, 0, True),
        ("Mexico", "Ecuador", 1, 0, False),
        ("England", "Congo DR", 1, 0, False),
        ("Belgium", "Senegal", 1, 0, False),
        ("USA", "Bosnia-Herz", 2, 0, False),
        ("Spain", "Austria", 1, 0, False),
        ("Portugal", "Croatia", 1, 0, False),
        ("Switzerland", "Algeria", 2, 1, False),
        ("Australia", "Egypt", 1, 1, False),
        ("Argentina", "Cape Verde", 2, 0, True),
        ("Colombia", "Ghana", 1, 0, False),
    ],
}

FLAG_BY_TEAM = {
    "Algeria": "🇩🇿",
    "Argentina": "🇦🇷",
    "Australia": "🇦🇺",
    "Austria": "🇦🇹",
    "Belgium": "🇧🇪",
    "Bosnia-Herz": "🇧🇦",
    "Brazil": "🇧🇷",
    "Canada": "🇨🇦",
    "Cape Verde": "🇨🇻",
    "Colombia": "🇨🇴",
    "Congo DR": "🇨🇩",
    "Croatia": "🇭🇷",
    "Curacao": "🇨🇼",
    "Czechia": "🇨🇿",
    "Ecuador": "🇪🇨",
    "Egypt": "🇪🇬",
    "England": "🏴",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Ghana": "🇬🇭",
    "Haiti": "🇭🇹",
    "Iran": "🇮🇷",
    "Iraq": "🇮🇶",
    "Ivory Coast": "🇨🇮",
    "Japan": "🇯🇵",
    "Jordan": "🇯🇴",
    "Mexico": "🇲🇽",
    "Morocco": "🇲🇦",
    "Netherlands": "🇳🇱",
    "New Zealand": "🇳🇿",
    "Norway": "🇳🇴",
    "Panama": "🇵🇦",
    "Paraguay": "🇵🇾",
    "Portugal": "🇵🇹",
    "Qatar": "🇶🇦",
    "Saudi Arabia": "🇸🇦",
    "Scotland": "🏴",
    "Senegal": "🇸🇳",
    "South Africa": "🇿🇦",
    "South Korea": "🇰🇷",
    "Spain": "🇪🇸",
    "Sweden": "🇸🇪",
    "Switzerland": "🇨🇭",
    "Tunisia": "🇹🇳",
    "Türkiye": "🇹🇷",
    "Uruguay": "🇺🇾",
    "USA": "🇺🇸",
    "Uzbekistan": "🇺🇿",
}


def main() -> int:
    picks_by_day = {day: load_day(day) for day in range(1, 5)}
    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_text(render_svg(picks_by_day), encoding="utf-8")
    HTML_PATH.write_text(render_html(picks_by_day), encoding="utf-8")
    print(f"wrote {ASSET_PATH}")
    print(f"wrote {HTML_PATH}")
    return 0


def load_day(day: int) -> list[dict[str, object]]:
    rows = []
    path = RAW_DIR / f"journee_{day}.json"
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        for match in payload.get("matchs", []):
            for bet in match.get("paris", []):
                if str(bet.get("user_id")) != USER_ID:
                    continue
                rows.append(
                    {
                        "day": day,
                        "match_id": int(match["match_id"]),
                        "home": match["home"],
                        "away": match["away"],
                        "home_pick": int(bet["home_parie"]),
                        "away_pick": int(bet["away_parie"]),
                        "score_home": match.get("score_home"),
                        "score_away": match.get("score_away"),
                        "doublette": bool(bet.get("doublette")),
                    }
                )
    if not rows and day in FALLBACK_PICKS_BY_DAY:
        rows = [
            {
                "day": day,
                "match_id": 10_000 + index,
                "home": home,
                "away": away,
                "home_pick": home_pick,
                "away_pick": away_pick,
                "score_home": None,
                "score_away": None,
                "doublette": doublette,
            }
            for index, (home, away, home_pick, away_pick, doublette) in enumerate(FALLBACK_PICKS_BY_DAY[day])
        ]
    return sorted(rows, key=lambda row: int(row["match_id"]))


def label(row: dict[str, object]) -> str:
    home = str(row["home"])
    away = str(row["away"])
    return (
        f"{FLAG_BY_TEAM.get(home, '')} {home} "
        f"{row['home_pick']} - {row['away_pick']} "
        f"{away} {FLAG_BY_TEAM.get(away, '')}"
    ).strip()


def render_svg(picks_by_day: dict[int, list[dict[str, object]]]) -> str:
    return render_bracket_svg(picks_by_day[4])


def render_bracket_svg(rows: list[dict[str, object]]) -> str:
    all_days = {day: load_day(day) for day in range(1, 5)}
    groups = build_group_stage(all_days)
    width = 2600
    card_w = 330
    group_w = 390
    card_h = 82
    group_h = 122
    gap_y = 18
    group_gap = 12
    top = 138
    x_group = 52
    x32 = 520
    x16 = 915
    xqf = 1285
    xsf = 1635
    xfinal = 1955
    xwinner = 2280
    y32 = [top + idx * (card_h + gap_y) for idx in range(len(rows))]
    y16 = [((y32[i * 2] + card_h / 2) + (y32[i * 2 + 1] + card_h / 2)) / 2 - card_h / 2 for i in range(8)]
    yqf = [((y16[i * 2] + card_h / 2) + (y16[i * 2 + 1] + card_h / 2)) / 2 - card_h / 2 for i in range(4)]
    ysf = [((yqf[i * 2] + card_h / 2) + (yqf[i * 2 + 1] + card_h / 2)) / 2 - card_h / 2 for i in range(2)]
    yfinal = [((ysf[0] + card_h / 2) + (ysf[1] + card_h / 2)) / 2 - card_h / 2]
    ywinner = [yfinal[0]]
    group_height = top + len(groups) * (group_h + group_gap)
    bracket_height = y32[-1] + card_h + 72
    height = int(max(group_height, bracket_height))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        ".bg{fill:#202229}.title{fill:#f4f6fb;font:800 32px Inter,Arial,sans-serif}.sub{fill:#a7abb5;font:650 16px Inter,Arial,sans-serif}.round{fill:#f4f6fb;font:800 20px Inter,Arial,sans-serif}.card{fill:#2d2f39;stroke:#555966;stroke-width:1.4}.exact{fill:#213b2a;stroke:#42b883}.good{fill:#213941;stroke:#4aa3bf}.miss{fill:#402527;stroke:#bd4d53}.pending{fill:#2d2f39;stroke:#555966}.group{fill:#2a2d36;stroke:#4d535d;stroke-width:1.25}.meta{fill:#a7abb5;font:800 13px Inter,Arial,sans-serif}.groupName{fill:#f4f6fb;font:800 14px Inter,Arial,sans-serif}.groupPick{fill:#dfe2ea;font:750 11.5px Inter,Arial,sans-serif}.team{fill:#f3f4f8;font:800 17px Inter,Arial,sans-serif}.score{fill:#f3f4f8;font:900 20px Inter,Arial,sans-serif}.line{stroke:#555966;stroke-width:1.5;fill:none}.softLine{stroke:#464b55;stroke-width:1.2;fill:none}.winner{fill:#354038;stroke:#5d755f;stroke-width:1.5}.legend{fill:#a7abb5;font:750 13px Inter,Arial,sans-serif}.dotExact{fill:#42b883}.dotGood{fill:#4aa3bf}.dotMiss{fill:#bd4d53}.dotPending{fill:#777d8a}.pickBgExact{fill:#244a32}.pickBgGood{fill:#234451}.pickBgMiss{fill:#4a292c}.pickBgPending{fill:#343743}",
        "</style>",
        '<rect class="bg" x="0" y="0" width="100%" height="100%"/>',
        '<text class="title" x="52" y="52">WW2026 bracket picks</text>',
        '<text class="sub" x="52" y="82">Updated June 29, 2026 · J1-J3 group picks · J4 bracket strategy: field leverage + risk cap</text>',
        f'<text class="round" x="{x_group}" y="122">Group stage</text>',
        f'<text class="round" x="{x32}" y="122">Round of 32</text>',
        f'<text class="round" x="{x16}" y="122">Round of 16</text>',
        f'<text class="round" x="{xqf}" y="122">Quarter-finals</text>',
        f'<text class="round" x="{xsf}" y="122">Semi-finals</text>',
        f'<text class="round" x="{xfinal}" y="122">Final</text>',
        f'<text class="round" x="{xwinner}" y="122">Winner</text>',
        '<circle class="dotExact" cx="1210" cy="80" r="6"/><text class="legend" x="1222" y="84">exact</text>',
        '<circle class="dotGood" cx="1280" cy="80" r="6"/><text class="legend" x="1292" y="84">result</text>',
        '<circle class="dotMiss" cx="1366" cy="80" r="6"/><text class="legend" x="1378" y="84">miss</text>',
        '<circle class="dotPending" cx="1430" cy="80" r="6"/><text class="legend" x="1442" y="84">pending</text>',
    ]
    for idx, group in enumerate(groups):
        draw_group_card(parts, x_group, top + idx * (group_h + group_gap), group_w, group_h, group)

    for idx, row in enumerate(rows):
        draw_pick_card(parts, x32, y32[idx], card_w, card_h, row, "J4 pick")

    round16 = []
    for idx in range(8):
        first = winner(rows[idx * 2])
        second = winner(rows[idx * 2 + 1])
        round16.append((first, second))
        draw_future_card(parts, x16, y16[idx], card_w, card_h, first, second, "from J4 picks")
        draw_connector(parts, x32 + card_w, y32[idx * 2] + card_h / 2, y32[idx * 2 + 1] + card_h / 2, x16, y16[idx] + card_h / 2)

    for idx in range(4):
        draw_future_card(parts, xqf, yqf[idx], card_w, card_h, "TBD", "TBD", "to fill")
        draw_connector(parts, x16 + card_w, y16[idx * 2] + card_h / 2, y16[idx * 2 + 1] + card_h / 2, xqf, yqf[idx] + card_h / 2)

    for idx in range(2):
        draw_future_card(parts, xsf, ysf[idx], card_w, card_h, "TBD", "TBD", "to fill")
        draw_connector(parts, xqf + card_w, yqf[idx * 2] + card_h / 2, yqf[idx * 2 + 1] + card_h / 2, xsf, ysf[idx] + card_h / 2)

    draw_future_card(parts, xfinal, yfinal[0], card_w, card_h, "TBD", "TBD", "to fill")
    draw_connector(parts, xsf + card_w, ysf[0] + card_h / 2, ysf[1] + card_h / 2, xfinal, yfinal[0] + card_h / 2)

    draw_winner_card(parts, xwinner, ywinner[0], 220, card_h, "TBD")
    draw_connector(parts, xfinal + card_w, yfinal[0] + card_h / 2, yfinal[0] + card_h / 2, xwinner, ywinner[0] + card_h / 2)
    parts.append("</svg>")
    return "\n".join(parts)


def build_group_stage(picks_by_day: dict[int, list[dict[str, object]]]) -> list[dict[str, object]]:
    parent: dict[str, str] = {}

    def find(team: str) -> str:
        parent.setdefault(team, team)
        if parent[team] != team:
            parent[team] = find(parent[team])
        return parent[team]

    def union(a: str, b: str) -> None:
        parent[find(b)] = find(a)

    match_order: dict[str, int] = {}
    index = 0
    for day in (1, 2, 3):
        for row in picks_by_day[day]:
            home = str(row["home"])
            away = str(row["away"])
            union(home, away)
            match_order.setdefault(home, index)
            match_order.setdefault(away, index)
            index += 1

    groups_by_root: dict[str, list[str]] = {}
    for team in parent:
        groups_by_root.setdefault(find(team), []).append(team)
    groups = sorted(groups_by_root.values(), key=lambda teams: min(match_order[t] for t in teams))
    result = []
    for idx, teams in enumerate(groups):
        team_set = set(teams)
        picks = [
            row
            for day in (1, 2, 3)
            for row in picks_by_day[day]
            if str(row["home"]) in team_set and str(row["away"]) in team_set
        ]
        result.append({"name": f"Group {chr(ord('A') + idx)}", "teams": teams, "picks": picks})
    return result


def draw_group_card(parts: list[str], x: float, y: float, w: float, h: float, group: dict[str, object]) -> None:
    parts.append(f'<rect class="group" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
    parts.append(f'<text class="groupName" x="{x + 14}" y="{y + 21}">{html.escape(str(group["name"]))}</text>')
    for idx, row in enumerate(group["picks"][:6]):
        row_y = y + 31 + idx * 14
        parts.append(f'<rect class="{pick_bg_class(row)}" x="{x + 10}" y="{row_y}" width="{w - 20}" height="13" rx="4"/>')
        parts.append(f'<text class="groupPick" x="{x + 14}" y="{row_y + 10}">{html.escape(compact_label(row))}</text>')


def draw_connector(parts: list[str], start_x: float, top_y: float, bottom_y: float, end_x: float, end_y: float) -> None:
    mid_x = start_x + 18
    parts.append(f'<path class="line" d="M{start_x} {top_y} H{mid_x} V{bottom_y} H{start_x}"/>')
    parts.append(f'<path class="line" d="M{mid_x} {end_y} H{end_x}"/>')


def draw_pick_card(parts: list[str], x: float, y: float, w: float, h: float, row: dict[str, object], meta: str) -> None:
    home = str(row["home"])
    away = str(row["away"])
    parts.append(f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
    parts.append(f'<text class="meta" x="{x + 16}" y="{y + 20}">{html.escape(meta)}</text>')
    parts.append(f'<text class="team" x="{x + 16}" y="{y + 47}">{html.escape(team_label(home))}</text>')
    parts.append(f'<text class="score" x="{x + w - 34}" y="{y + 47}" text-anchor="middle">{row["home_pick"]}</text>')
    parts.append(f'<text class="team" x="{x + 16}" y="{y + 72}">{html.escape(team_label(away))}</text>')
    parts.append(f'<text class="score" x="{x + w - 34}" y="{y + 72}" text-anchor="middle">{row["away_pick"]}</text>')


def draw_future_card(parts: list[str], x: float, y: float, w: float, h: float, first: str, second: str, meta: str) -> None:
    parts.append(f'<rect class="card" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
    parts.append(f'<text class="meta" x="{x + 16}" y="{y + 20}">{html.escape(meta)}</text>')
    parts.append(f'<text class="team" x="{x + 16}" y="{y + 49}">{html.escape(team_label(first))}</text>')
    parts.append(f'<text class="team" x="{x + 16}" y="{y + 74}">{html.escape(team_label(second))}</text>')


def draw_winner_card(parts: list[str], x: float, y: float, w: float, h: float, team: str) -> None:
    parts.append(f'<rect class="winner" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
    parts.append(f'<text class="meta" x="{x + 16}" y="{y + 20}">to fill</text>')
    parts.append(f'<text class="team" x="{x + 16}" y="{y + 54}">{html.escape(team_label(team))}</text>')


def winner(row: dict[str, object]) -> str:
    home_pick = int(row["home_pick"])
    away_pick = int(row["away_pick"])
    if home_pick > away_pick:
        return str(row["home"])
    if away_pick > home_pick:
        return str(row["away"])
    return "TBD"


def team_label(team: str) -> str:
    if team == "TBD":
        return "◼ TBD"
    return f"{FLAG_BY_TEAM.get(team, '')} {team}".strip()


def compact_label(row: dict[str, object]) -> str:
    home = str(row["home"])
    away = str(row["away"])
    return (
        f"J{row['day']} · {FLAG_BY_TEAM.get(home, '')} {short_team(home)} "
        f"{row['home_pick']}-{row['away_pick']} "
        f"{short_team(away)} {FLAG_BY_TEAM.get(away, '')}"
    ).strip()


def short_team(team: str) -> str:
    replacements = {
        "Bosnia-Herz": "Bosnia",
        "Saudi Arabia": "Saudi",
        "South Africa": "S. Africa",
        "South Korea": "S. Korea",
        "New Zealand": "N. Zealand",
        "Ivory Coast": "C. d'Ivoire",
    }
    return replacements.get(team, team)


def render_html(picks_by_day: dict[int, list[dict[str, object]]]) -> str:
    columns = []
    for day, rows in picks_by_day.items():
        table_rows = []
        for row in rows:
            table_rows.append(
                f"<tr><td>{len(table_rows) + 1}</td><td>{html.escape(label(row))}</td></tr>"
            )
        columns.append(
            "<section class='day-column'>"
            f"<header><h2>J{day}</h2><p>{html.escape(STRATEGY_BY_DAY[day])}</p></header>"
            + "<table><tbody>"
            + "\n".join(table_rows)
            + "</tbody></table>"
            + "</section>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>WW2026 picks through J4</title>
  <style>
    body {{ margin: 0; background: #202229; color: #f4f6fb; font-family: Inter, Arial, sans-serif; }}
    main {{ padding: 42px 52px 60px; }}
    h1 {{ margin: 0 0 8px; font-size: 42px; }}
    .lead {{ margin: 0 0 34px; color: #a7abb5; font-weight: 650; }}
    .board {{ display: grid; grid-template-columns: repeat(4, minmax(340px, 1fr)); gap: 28px; align-items: start; }}
    .day-column header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }}
    .day-column h2 {{ margin: 0; font-size: 30px; }}
    .day-column p {{ margin: 0; padding: 8px 14px; border-radius: 999px; background: #343743; color: #d9dce4; font-weight: 750; font-size: 14px; }}
    table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 8px; border: 1px solid #555966; background: #282b35; }}
    tr:nth-child(even) {{ background: #2d303a; }}
    td {{ border-top: 1px solid #50545f; padding: 10px 12px; font-size: 16px; font-weight: 750; }}
    td:first-child {{ width: 30px; color: #8f95a3; text-align: right; border-right: 1px solid #50545f; }}
    @media (max-width: 1200px) {{ .board {{ grid-template-columns: repeat(2, minmax(320px, 1fr)); }} }}
    @media (max-width: 760px) {{ main {{ padding: 28px 18px; }} .board {{ grid-template-columns: 1fr; }} td {{ font-size: 15px; }} }}
  </style>
</head>
<body>
  <main>
    <h1>WW2026 picks through J4</h1>
    <p class="lead">Updated June 29, 2026 · submitted pick table by matchday.</p>
    <div class="board">
      {"".join(columns)}
    </div>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
