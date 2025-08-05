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
    """Handles spawning, activation, and timing of power-ups."""

    SPAWN_INTERVAL = 30  # seconds on average

    def __init__(self, powerups: Optional[List[PowerUp]] = None) -> None:
        self.powerups = powerups or POWER_UPS
        self.spawned_powerup: Optional[PowerUp] = None
        self.active_powerup: Optional[PowerUp] = None
        self.active_ends_at: float = 0.0
        now = time.time()
        self.schedule_next_spawn(now)

    def update(self, now: float) -> None:
        """Call regularly to handle spawning and expiration."""
        if self.active_powerup and now >= self.active_ends_at:
            self.active_powerup = None
            self.schedule_next_spawn(now)

        if not self.spawned_powerup and not self.active_powerup and now >= self.next_spawn_time:
            self.spawn()

    def schedule_next_spawn(self, now: float) -> None:
        self.next_spawn_time = now + random.uniform(25, 35)

    def spawn(self) -> None:
        weights = [math.log(p.rank + 1) for p in self.powerups]
        self.spawned_powerup = random.choices(self.powerups, weights=weights, k=1)[0]
        # In the real game, a colored ball sized POWER_UP_RADIUS would appear here.

    def pick_up(self, now: float) -> Optional[PowerUp]:
        """Activate and return the currently spawned power-up if present."""
        if self.spawned_powerup and not self.active_powerup:
            self.active_powerup = self.spawned_powerup
            self.active_ends_at = now + self.spawned_powerup.duration
            self.spawned_powerup = None
            return self.active_powerup
        return None


if __name__ == "__main__":
    mgr = PowerUpManager()
    start = time.time()
    for i in range(5):
        now = start + i * 30
        mgr.update(now)
        if mgr.spawned_powerup:
            print(f"Power-up available: {mgr.spawned_powerup.name} ({mgr.spawned_powerup.tier})")
            mgr.pick_up(now)
            print(f"Activated: {mgr.active_powerup.name} for {mgr.active_powerup.duration}s")
