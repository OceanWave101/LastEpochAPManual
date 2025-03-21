# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, ItemClassification

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

# using math.floor for weighting
import math

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    if is_option_enabled(multiworld, player, "exclude_dungeon_skips"):
        dungeons = ["Lightless Arbor Access", "Soulfire Bastion Access", "Temporal Sanctum Access"]
        itemNamesToRemove.extend(dungeons)

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # We don't need to check if filler_traps is 0 since item pool has already been created
    # Instead, we count all instances of traps in the item pool, calculate the number of traps of each type based on the ratios, then remove/add to approximately the correct ratio
    # e.g., if count_traps(item_pool) = 15, option_area_restart = 3, option_discard_movement = 4, then 15/(3+4) ~= 2.14 -> Area Restart Traps = round(3 * 2.14) = 6, Discard Movement traps = round(4 * 2.14) = 9, 15 - (6 + 9) = 0, all traps replaced  
    new_item_pool = [ i for i in item_pool if i.classification != ItemClassification.trap ] # creates item pool with all traps removed
    item_pool_traps = [ i for i in item_pool if i.classification == ItemClassification.trap ] # creates list of all traps originally in item pool
    """ the following code can be re-enabled once OptionsDict is resolved for trap weights; note that this still fails to account for low amounts of traps generated, resulting in no traps added
    if len(item_pool_traps) == 0: # if there are no traps in the item pool
        return item_pool # return the original item pool
    else: # if there are any traps in the item pool
        # grab the values of the trap weights from the YAML
        area_restart_weight = multiworld.worlds[player].options.TrapWeights.option_area_restart.value
        discard_movement_weight = multiworld.worlds[player].options.TrapWeights.option_discard_movement.value
        
        # calculate the multiplier for each trap by dividing the total number of traps in the pool by the sum of the trap weights
        trap_count_mult = len(item_pool_traps) / (area_restart_weight + discard_movement_weight)
        
        # calculate the number of each trap, rounding to the nearest integer
        area_restart_traps = math.floor(area_restart_weight * trap_count_mult)
        discard_movement_traps = math.floor(discard_movement_weight * trap_count_mult)
        
        # calculate difference between traps removed and traps to add (should always be 0 or positive)
        filler_offset = len(item_pool_traps) - (area_restart_traps + discard_movement_traps)
        if filler_offset > 0: # if number of traps to fill is less than number of traps originally
            for _ in range(filler_offset):
                # add a filler item to the pool for each missing trap filler
                new_item_pool.append(world.create_item("0 XP"))        
                
        # loop over each trap's count and add the traps to the new item pool
        for _ in range(area_restart_traps): # append an area restart trap for each count of area_restart_traps
            new_item_pool.append(world.create_item("Reset current area / Return to last waypoint"))
        for _ in range(discard_movement_traps): # append a discard movement trap for each count of discard_movement_traps
            new_item_pool.append(world.create_item("Remove all Movement Speed items until next area"))
    """ 
    # following code is substitute until OptionDict for trap weights can be figured out; this instead works as if the trap types are exclusive from one another
    # vvv this list constructor would perform basically the same thing as the first conditional once appended to new_item_pool
    #traps_list = ["Reset current area / Return to last waypoint" for _ in range(len(item_pool_traps)) if get_option_value(multiworld, player, "trap_choice") == 0]
    for _ in range(len(item_pool_traps)): # if no traps in item pool, this is skipped
        if multiworld.worlds[player].options.trap_choice.value == 0: # if TrapChoice is option_area_restart
            new_item_pool.append(world.create_item("Reset current area / Return to last waypoint"))
        elif multiworld.worlds[player].options.trap_choice.value == 1: # if TrapChoice is option_discard_movement
            new_item_pool.append(world.create_item("Remove all Movement Speed items until next area"))
    return new_item_pool # will return equivalent of item_pool if no traps at all, otherwise returns modified item pool with replaced traps

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True
    
    #if Exclude Dungeon Skips is enabled in YAML
    if is_option_enabled(multiworld, player, "exclude_dungeon_skips"):
        # define lists of each chapter with an associated entrance or exit to a dungeon
        #dungeon_exit = ['Chapter 4', 'Chapter 7', 'Chapter 9']
        dungeon_entrance = ['Chapter 2', 'Chapter 4', 'Chapter 5']
        # also define list of each chapter's exit to be removed
        exits_to_remove = ['Chapter 2ToChapter 4', 'Chapter 4ToChapter 7', 'Chapter 5ToChapter 9']
        
        # remove exits from each chapter leading into a dungeon 
        for chapter in dungeon_entrance:
            region_to_change = multiworld.get_region(chapter, player)
            #logging.info(f"Our current region is {region_to_change}.")
            #logging.info("The list of exits in this region include: ")
            for region_exit in region_to_change.exits:
                #logging.info(region_exit)
                #logging.info(str(region_exit))
                if str(region_exit) in exits_to_remove:
                    #logging.info(f"This region exit {region_exit} is being blocked.")
                    multiworld.get_entrance(region_exit.name, player).access_rule = lambda state: False
                #else:
                    #logging.info(f"This region exit {region_exit} is safe.")
        
        # remove entrances from each chapter that leads from a dungeon -- multiworld.get_exit doesn't exist, so maybe only need to remove entrances?
        """
        for chapter in dungeon_entrance:
            region_to_change = multiworld.get_region(chapter, player)
            for region_entrance in region_to_change.entrances:
                multiworld.get_exit(region_entrance.name, player).access_rule = lambda state: False
        """

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
