from dataclasses import dataclass


@dataclass
class SongBracket:
    level: int
    count: int


song_brackets = [
    SongBracket(level=17, count=20),
    SongBracket(level=18, count=45),
    SongBracket(level=19, count=30),
    SongBracket(level=20, count=5),
]


@dataclass
class SongGoal:
    name: str
    volforce: int


song_goals = [
    SongGoal("A Rank", 1),
    SongGoal("AA Rank", 5),
    SongGoal("AAA Rank", 10),
    SongGoal("S Rank", 20),
]
