# Skill 04: Collect Expert Signals

## Use When

Markets may miss injuries, lineups, rotations, tactics, motivation, or recent news.

## Code To Use

- `audit_expert_signals(...)`
- `apply_expert_signals(...)`

## Required Inputs

- reviewed or reviewable sources
- event ids that match the options table
- signal target, direction, confidence, and source URL

## Method

1. Build a research queue from high-uncertainty matches first.
2. Search targeted queries:
   - `{home} {away} preview injuries predicted lineup`
   - `{home} {away} tactical preview`
   - `{home} {away} expert picks total goals`
3. Extract only actionable claims.
4. Convert each claim into a bounded signal.
5. Review signals manually or mark `needs_review`.
6. Apply signals only with caps. They adjust probabilities; they do not replace the market.

## Signal Targets

Use these targets:

- `home`
- `away`
- `draw`
- `favorite`
- `outsider`
- `low_score`
- `high_score`
- exact `option_id` when known

## Required Columns

- `event_id`
- `source_name`
- `source_url`
- `published_at`
- `signal_target`
- `signal_direction`
- `confidence`
- `note`

## Output

Reviewed signal table plus an audit showing which signals are safe to use.

## Stop If

- source is stale or untrusted
- signal is narrative but not actionable
- target cannot be mapped to an option or outcome bucket
