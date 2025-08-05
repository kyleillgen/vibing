from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass
from typing import List, Optional

# Size constants (placeholder values)
CLAP_HITBOX_RADIUS = 20
POWER_UP_RADIUS = CLAP_HITBOX_RADIUS


@dataclass(frozen=True)
class PowerUp:
    """Definition of a power-up."""

    name: str
    rank: int
    rarity: float
    tier: str
    color: str
    duration: int
    effect: str


# Raw power-up definitions: (name, effect)
_POWER_UP_DEFS = [
    ("Mega Multiplier", "Multiply all points by five."),
    ("Golden Banana", "Each hit grants a massive score bonus."),
    ("Combo Frenzy", "Combo meter builds twice as fast."),
    ("Fever Time", "Triple points for every beat."),
    ("Perfect Shield", "Misses do not break your combo."),
    ("Tempo Boost", "Slightly faster tempo for more scoring chances."),
    ("Time Warp", "Slows beat scroll speed."),
    ("Streak Saver", "Automatically saves the next missed beat."),
    ("Banana Magnet", "Nearby bananas fly toward you."),
    ("Score Burst", "Periodic bursts of bonus points."),
    ("Groove Guard", "Blocks the next obstacle."),
    ("Beat Freeze", "Freezes beats briefly on activation."),
    ("Drum Echo", "Each hit echoes for an extra score tick."),
    ("Banana Bloom", "Spawns extra bananas to catch."),
    ("Rhythm Rush", "More beats spawn for a short time."),
    ("Monkey March", "Auto-hits basic beats."),
    ("Tap Booster", "Temporarily enlarges the hit box."),
    ("Beat Bonus", "Adds a small bonus to every beat."),
    ("Banana Trick", "Random small bonus each hit."),
    ("Happy Hour", "Slight constant score buff."),
]


def _tier_for_rank(rank: int) -> tuple[str, str, int]:
    """Return tier name, color, and duration for a rank."""
    if rank <= 3:
        return "Legendary", "#FF8000", 45
    elif rank <= 7:
        return "Epic", "#A335EE", 35
    elif rank <= 12:
        return "Rare", "#0070FF", 30
    elif rank <= 16:
        return "Uncommon", "#1EFF00", 25
    else:
        return "Common", "#BEBEBE", 20


# Build the ranked power-up list
POWER_UPS: List[PowerUp] = []
for rank, (name, effect) in enumerate(_POWER_UP_DEFS, start=1):
    rarity = round(math.log(rank + 1), 2)  # logarithmic rarity scale
    tier, color, duration = _tier_for_rank(rank)
    POWER_UPS.append(
        PowerUp(
            name=name,
            rank=rank,
            rarity=rarity,
            tier=tier,
            color=color,
            duration=duration,
            effect=effect,
        )
    )


class PowerUpManager:
    """Handles spawning and timing of power-ups."""

    SPAWN_INTERVAL = 30  # seconds on average

    def __init__(self, powerups: Optional[List[PowerUp]] = None) -> None:
        self.powerups = powerups or POWER_UPS
        self.active_powerup: Optional[PowerUp] = None
        self.active_ends_at: float = 0.0
        now = time.time()
        self.next_spawn_time = now + self.SPAWN_INTERVAL

    def update(self, now: float) -> None:
        """Call regularly to handle spawning and expiration."""
        if self.active_powerup and now >= self.active_ends_at:
            self.active_powerup = None
            self.schedule_next_spawn(now)

        if not self.active_powerup and now >= self.next_spawn_time:
            self.spawn(now)

    def schedule_next_spawn(self, now: float) -> None:
        self.next_spawn_time = now + self.SPAWN_INTERVAL

    def spawn(self, now: float) -> None:
        weights = [math.log(p.rank + 1) for p in self.powerups]
        choice = random.choices(self.powerups, weights=weights, k=1)[0]
        self.active_powerup = choice
        self.active_ends_at = now + choice.duration
        # In the real game, a colored ball sized POWER_UP_RADIUS would appear here.


if __name__ == "__main__":
    mgr = PowerUpManager()
    start = time.time()
    for i in range(5):
        now = start + i * 30
        mgr.update(now)
        if mgr.active_powerup:
            print(f"Spawned: {mgr.active_powerup.name} ({mgr.active_powerup.tier})")
