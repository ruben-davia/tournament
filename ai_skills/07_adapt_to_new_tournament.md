# Skill: Adapt To New Tournament

## Use When

Use this when porting the framework to a different football prediction contest.

## Inputs Needed

- tournament brief
- scoring spec
- raw options
- probability sources
- participant behavior assumptions

## Questions To Ask

- Which parts match the existing framework?
- Which parts need custom scoring or constraints?
- What is the smallest public fixture that proves it works?

## Steps

1. Create a new folder under `examples/`.
2. Add config files and a small sample dataset.
3. Map raw data into the standard options contract.
4. Run probabilities, field model, and strategy simulation.
5. Add a README explaining the example.
6. Add or update tests for any new generic behavior.

## Output

A runnable example with no private data and a documented adaptation path.

## Common Mistakes

- Copying private data into the repo.
- Hardcoding local paths in generic modules.
- Adding tournament-specific logic to the framework core.

