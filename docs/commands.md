# Commands

## dice

```bash
vindicta dice roll 2d6
vindicta dice roll 3d6 --count 10
```

## match

```bash
vindicta match new --player-list my.json
vindicta match score --turn 2 --primary 15
vindicta match end --winner player
vindicta match list --last 10
```

## oracle

```bash
vindicta oracle predict --my-list my.json
vindicta oracle sleepers --faction Tyranids
```

## economy

```bash
vindicta economy balance
vindicta economy history
```

## warscribe

```bash
vindicta warscribe register --unit Captain --id CPT-01
vindicta warscribe action "[MOVE: CPT-01 -> Zone-A]"
```
