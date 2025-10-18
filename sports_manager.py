import time

class Player:
    def __init__(self, name, age, position, stats=None):
        self.name = name.title()
        self.age = age
        self.position = position.title()
        self.stats = stats or {}
        self.team = None

    def update_stats(self, stat_name, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Stat value must be a positive number.")
        self.stats[stat_name] = self.stats.get(stat_name, 0) + value
        print(f"✅ {stat_name} updated successfully for {self.name}!")

    def __str__(self):
        stats_str = ', '.join([f"{k}: {v}" for k, v in self.stats.items()]) or "No stats yet"
        return f"Name: {self.name}, Age: {self.age}, Position: {self.position}, Team: {self.team or 'None'}, Stats: [{stats_str}]"


class Team:
    def __init__(self, team_name):
        if not team_name.strip():
            raise ValueError("Team name cannot be empty.")
        self.team_name = team_name.strip().title()
        self.players = []
        self.matches = []

    def add_player(self, player):
        if any(p.name == player.name for p in self.players):
            print(f"⚠️ Player {player.name} is already in the team.")
        else:
            player.team = self.team_name
            self.players.append(player)
            print(f"✅ Player {player.name} added to {self.team_name}!")

    def remove_player(self, player_name):
        for player in self.players:
            if player.name == player_name.title():
                self.players.remove(player)
                player.team = None
                print(f"🗑️ Player {player_name} removed successfully.")
                return
        print(f"❌ Player {player_name} not found in the team.")

    def display_team(self):
        print(f"\n🏏 Team {self.team_name} Players:")
        if not self.players:
            print("No players added yet.")
        else:
            for player in self.players:
                print(" -", player)

    def schedule_match(self, opponent_team, date):
        if any(m["opponent"] == opponent_team.title() and m["date"] == date for m in self.matches):
            print(f"⚠️ Match already scheduled against {opponent_team} on {date}.")
            return
        match = {"opponent": opponent_team.title(), "date": date, "result": None}
        self.matches.append(match)
        print(f"📅 Match scheduled vs {opponent_team} on {date}!")

    def record_match_result(self, opponent_team, result):
        for match in self.matches:
            if match["opponent"] == opponent_team.title() and match["result"] is None:
                match["result"] = result.title()
                print(f"🏆 Result recorded: {self.team_name} {result} vs {opponent_team}")
                return
        print(f"❌ No scheduled match found against {opponent_team} or result already recorded.")

    def display_matches(self):
        print(f"\n📋 Match Schedule for {self.team_name}:")
        if not self.matches:
            print("No matches scheduled yet.")
        else:
            for m in self.matches:
                result = m["result"] or "Pending"
                print(f" - Opponent: {m['opponent']}, Date: {m['date']}, Result: {result}")

    def calculate_win_loss_ratio(self):
        wins = sum(1 for m in self.matches if m["result"] == "Win")
        losses = sum(1 for m in self.matches if m["result"] == "Loss")
        total = wins + losses
        if total == 0:
            print("⚠️ No completed matches yet.")
            return
        ratio = wins / total
        print(f"🏅 Win/Loss Ratio for {self.team_name}: {wins}/{losses} ({ratio:.2f})")

    def reset_team(self):
        confirm = input("Are you sure you want to reset all team data? (yes/no): ").lower()
        if confirm == "yes":
            self.players.clear()
            self.matches.clear()
            print("⚠️ Team data cleared successfully!")
        else:
            print("Action cancelled.")

    def view_player_stats(self, player_name):
        for player in self.players:
            if player.name == player_name.title():
                print(player)
                return
        print(f"❌ Player {player_name} not found.")

    def update_player_stat(self, player_name):
        for player in self.players:
            if player.name == player_name.title():
                stat = input("Enter stat name to update: ")
                try:
                    value = float(input("Enter value to add: "))
                    if value < 0:
                        print("❌ Stat value cannot be negative.")
                        return
                    player.update_stats(stat, value)
                except ValueError:
                    print("❌ Invalid input! Please enter a numeric value.")
                return
        print(f"❌ Player {player_name} not found.")


# -------- INTERACTIVE MENU ----------
if __name__ == "__main__":
    team = None
    while True:
        print("\n=== ⚡ Sports Team Management System ⚡ ===")
        print("1. Create a Team")
        print("2. Add Player")
        print("3. Remove Player")
        print("4. Display Team")
        print("5. View Player Stats")
        print("6. Update Player Stats")
        print("7. Schedule Match")
        print("8. Record Match Result")
        print("9. Display Matches")
        print("10. Calculate Win/Loss Ratio")
        print("11. Reset Team")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            team_name = input("Enter team name: ")
            try:
                team = Team(team_name)
                print(f"✅ Team '{team_name}' created successfully!")
            except ValueError as e:
                print(e)

        elif choice == "2":
            if team:
                # Validate player name
                while True:
                    name = input("Enter player name: ").strip()
                    if not name:
                        print("❌ Name cannot be empty.")
                    elif name.isnumeric():
                        print("❌ Name cannot be numeric. Please enter a valid name.")
                    else:
                        break

                # Immediately validate age
                while True:
                    try:
                        age = int(input("Enter player age: "))
                        if age <= 0:
                            print("❌ Invalid age! Age must be a positive number.")
                            continue
                        break
                    except ValueError:
                        print("❌ Invalid input! Please enter a numeric age.")

                position = input("Enter player position: ")
                player = Player(name, age, position)
                team.add_player(player)
            else:
                print("❌ Please create a team first.")

        elif choice == "3":
            if team:
                pname = input("Enter player name to remove: ")
                team.remove_player(pname)
            else:
                print("❌ Please create a team first.")

        elif choice == "4":
            if team:
                team.display_team()
            else:
                print("❌ Please create a team first.")

        elif choice == "5":
            if team:
                pname = input("Enter player name to view stats: ")
                team.view_player_stats(pname)
            else:
                print("❌ Please create a team first.")

        elif choice == "6":
            if team:
                pname = input("Enter player name to update stats: ")
                team.update_player_stat(pname)
            else:
                print("❌ Please create a team first.")

        elif choice == "7":
            if team:
                opp = input("Enter opponent team name: ")
                date = input("Enter match date (YYYY-MM-DD): ")
                team.schedule_match(opp, date)
            else:
                print("❌ Please create a team first.")

        elif choice == "8":
            if team:
                opp = input("Enter opponent team name: ")
                res = input("Enter result (Win/Loss): ")
                team.record_match_result(opp, res)
            else:
                print("❌ Please create a team first.")

        elif choice == "9":
            if team:
                team.display_matches()
            else:
                print("❌ Please create a team first.")

        elif choice == "10":
            if team:
                team.calculate_win_loss_ratio()
            else:
                print("❌ Please create a team first.")

        elif choice == "11":
            if team:
                team.reset_team()
            else:
                print("❌ Please create a team first.")

        elif choice == "12":
            print("\n👋 Exiting the system... Goodbye!\n")
            time.sleep(1)
            break

        else:
            print("❌ Invalid choice, please try again.")
