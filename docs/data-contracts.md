# Data Contracts

The framework uses plain tabular data.

## Options Table

Required columns:

| column | type | description |
| --- | --- | --- |
| `event_id` | string | Match or question id. |
| `option_id` | string | Stable pick option id. |

Recommended columns:

| column | type | description |
| --- | --- | --- |
| `label` | string | Human-readable pick label. |
| `decimal_odds` | number | Decimal odds used to infer probabilities. |
| `truth_probability` | number | Direct probability, if not using odds. |
| `popularity_hint` | number | Relative crowd popularity signal. |
| `field_probability` | number | Estimated field pick probability. |
| `points_if_hit` | number | Points earned if the option is correct. |

## Candidate Picks Table

Optional. If omitted, the simulator creates simple default strategies.

| column | type | description |
| --- | --- | --- |
| `strategy` | string | Strategy name. |
| `event_id` | string | Event id. |
| `option_id` | string | Picked option id. |

## Probability Rules

Within each `event_id`:

- truth probabilities should sum to 1
- field probabilities should sum to 1
- if they do not, the helpers normalize them

