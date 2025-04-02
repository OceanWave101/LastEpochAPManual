# Last Epoch Archipelago Manual
Archipelago manual world for the game Last Epoch by Eleventh Hour Games
The current goal for this AP world is to run through the campaign on a new character, with a victory condition of completing Chapter 9 (beating Majasa). Your gear slots, additional passive points, and idol slot expansions are locked behind completing random main quests, side quests, or opening the One-Shot Caches located in the campaign zones. 

## Requirements
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) 
- <ins>AP Manual Client</ins> from the [AP Manual discord](https://discord.gg/T5bcsVHByx)
- [Last Epoch](https://lastepoch.com/)
- (Recommended) [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases)

## Options & Settings
> [!NOTE]
> Options marked as (WIP) are works in progress, and are not yet implemented in the current AP world.
The [.yaml file](/../Manual_LastEpoch_Ocean.yaml) contains user options for personalizing your experience, including the following:
- Including or excluding the three dungeons (Lightless Arbor, Soulfire Bastion, and Temporal Sanctum) as campaign skips
- Enabling or disabling traps, with relative weighting
  - Traps currently include restarting the current area over from the beginning, and temporarily removing any movement speed items being worn for the current area. (Additional trap idea are welcome!)
- (WIP) Difficulty scaling (by modifying starting items/planned item locations)
- (WIP) Optional inclusion of endgame monolith completion, or exclusively monolith completion worlds
- (WIP) "Areasanity", Merchant's Guild / Circle of Fortune Factions' favor ranks, and more (or less!) location checks

## How to Play
*Assumes playing and generating your own world*

1. [Install Archipelago](https://archipelago.gg/tutorial/Archipelago/setup/en). 
2. Download the `manual_lastepoch_ocean.apworld` file and move it into your `Archipelago/custom_worlds` folder where you installed Archipelago.
3. (Optional) Download the latest version of Universal Tracker, and move its `.apworld` file also into your `Archipelago/custom_worlds` folder.
4. Download the `Manual_LastEpoch_Ocean.yaml` file, adjust any options as desired (with a text editor of your choice), save any changes, and then place the file in your `Archipelago/Players` folder.
   - Alternatively, use Archipelago's `Generate Template Options` on the left side of the Archipelago Launcher to create a default `yaml` template in your `Archipelago/Players/Templates` folder, and then copy and paste this template into your `Archipelago/Players` folder.
5. Run `ArchipelagoGenerate.exe` (or click `Generate` in the Archipelago Launcher) to generate your AP world. This may take a second. It should create a `.zip` folder in `Archipelago/output` once finished.
6. To use the Archipelago website to host your game, use [this link](https://archipelago.gg/uploads) and upload the previous `.zip` file to the website. This will present a new page with your world's seed, spoiler log, and the option to **Create New Room**.
7. Press **Create New Room**, and on this webpage (your room), make note of the server address (looks like `archipelago.gg:00000`, where the zeroes are your server's port number). Leave this page open, and remember to refresh it if the server pauses while you're playing (or continuing a previous session).
8. If not already open, launch the Archipelago Launcher (`ArchipelagoLauncher.exe`). On the right side, look for and press the button labeled **Manual Client**.
9. In the Manual Client window, enter the server address (using your room's port number) at the top, and below that next to "Manual Game ID", type in `Manual_LastEpoch_Ocean` if it's not already filled in. Then press the Connect button at the top right.
10. If you correctly connected to your room, you should receive a prompt to enter the slot name, which will be whatever name you submitted in your `yaml`; note this name also shows up in your room webpage (by default, this will be `Player1`). Type in the slot name, and press Enter.
11. Now you are connected to the server and ready to play the game! Navigate to the **Manual** tab in the Manual Client, and open the categories on the left to view your current (allowed) inventory of items, and on the right to view the buttons to press when you complete the specific checks/locations. Items you receive will show up on the left in bold as you complete your checks, and when you've achieved the goal, press the GOAL: button to release your game.
    - If you installed Universal Tracker, you will have an additional tab on the right labeled **Tracker Page**, which will list out all of the current locations and/or quests you can reach or complete in logic.

