import os
from datetime import date, timedelta
from github import Github

MESSAGE = [
    "X   X  XXXXX   XX XX   XXXXX  X    XXXXX  XXXXX  X   ",
    "X   X  X      X  X  X  X   X  X      X    X      X   ",
    "X   X  X      X     X  X   X  X      X    X      X   ",
    "X X X  XXXXX  X     X  XXXXX  X      X    XXXXX  X   ",
    "X X X  X       X   X   X      X      X    X      X   ",
    "XX XX  X        X X    X      X      X    X          ",
    "X   X  XXXXX     X     X      XXXXX  X    X      X   "
]

STARTING_YEAR = 2024
STARTING_WEEK = 44

def create_commit(repo, date):
    # Create an empty commit
    contents = repo.get_contents("README.md")
    repo.update_file(
        contents.path,
        f"Contribution on {date.isoformat()}",
        f"Contribution on {date.isoformat()}",
        contents.sha,
        branch="main",
        committer=Github.InputGitAuthor(
            name="GitHub Action",
            email="action@github.com",
            date=date.isoformat()
        )
    )

def get_start_date(year, week):
    start_date = date(year, 1, 1)
    start_date += timedelta(days=7 * (week - 1) - get_weekday(start_date))
    return start_date

def get_weekday(date):
    return (date.weekday() + 1) % 7

def main():
    # Authenticate with GitHub
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

    current_date = date.today()
    start_date = get_start_date(STARTING_YEAR, STARTING_WEEK)

    days_since_start = (current_date - start_date).days
    current_week = (days_since_start // 7) % 53
    current_day = get_weekday(current_date)

    if MESSAGE[current_day][current_week] == 'X':
        create_commit(repo, current_date)

if __name__ == "__main__":
    main()
