# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, Visibility

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
#class TotalCharactersToWinWith(Range):
#    """Instead of having to beat the game with all characters, you can limit locations to a subset of character victory locations."""
#    display_name = "Number of characters to beat the game with before victory"
#    range_start = 10
#    range_end = 50
#    default = 50

class ExcludeDungeonSkips(Toggle):
    """Removes Lightless Arbor, Soulfire Bastion, and Temporal Sanctum pathways from logic.
    Note that this will lead to a more linear playthrough with less backtracking, at the expense of being stuck more frequently.
    """
    display_name = "Remove Dungeon Skips from logic" # shows up in Spoiler log
    
#class ExcludeTraps(Toggle):
#    """"""
#    display_name = "Disable traps"
#    # Unnecessary, can use filler_traps set to 0 for same result
    
#class TrapChoice(Choice):
#    """This setting determines which type of trap will appear, if traps are enabled.
#    This does not define the number of traps that will appear, only the kind of trap.
#    Note that trap types are exclusive, so only one trap type will appear, if any.
#    """
#    display_name = "Choice of Trap Type"
#    option_area_restart = 0
#    option_discard_movement = 1
#    default = 0

# this allows us to skip needing to use OptionDict by just assigning weights for each trap type; these values are ignored if filler_traps is zero
# can do something like for every trap option not 0, sum all trap option weights, then divide individual weight by summed weight, and reassign traps as close to that value as possible; can result in 0 traps if weight is too small 
class AreaRestartTrap(Range):
    """ If traps are enabled, this determines how often the \"Reset current area \/ Return to last waypoint\" Trap appears.
    This weight is relative to any other traps that will appear.
    If you don't want this specific type of trap to appear, set this value to 0.
    """
    display_name = "Area Restart trap weight"
    range_start = 0
    range_end = 100
    default = 0

class DiscardMovementTrap(Range):
    """ If traps are enabled, this determines how often the \"Remove all Movement Speed items until next area\" Trap appears.
    This weight is relative to any other traps that will appear.
    If you don't want this specific type of trap to appear, set this value to 0.
    """
    display_name = "Remove Movement Speed Items trap weight"
    range_start = 0
    range_end = 100
    default = 0


# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    # options['attribute_name_here'] = ClassName
    #options['trap_choice'] = TrapChoice
    #options['trap_weights'] = TrapWeights
    options['area_restart_trap'] = AreaRestartTrap
    options['discard_movement_trap'] = DiscardMovementTrap
    options['exclude_dungeon_skips'] = ExcludeDungeonSkips
    
    return options