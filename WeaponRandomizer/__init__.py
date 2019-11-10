import bl2sdk
from bl2sdk import *

from .bl2tools import *

from random import choice


class Rando(bl2sdk.BL2MOD):
    Name = "Weapon Randomizer"
    Description = "Changes your Weapon every 10 seconds."
    Author = "Juso"

    def __init__(self):
        self.old_gun = None
        self.clock = 0.0
        self.WeaponTypeDefinition = []
        self.BalanceDefinition = []
        self.ManufacturerDefinition = []
        self.BodyPartDefinition = []
        self.GripPartDefinition = []
        self.BarrelPartDefinition = []
        self.SightPartDefinition = []
        self.StockPartDefinition = []
        self.ElementalPartDefinition = []
        self.Accessory1PartDefinition = []
        self.Accessory2PartDefinition = []
        self.MaterialPartDefinition = []
        self.PrefixPartDefinition = []
        self.TitlePartDefinition = []
        self.types = ("pistol", "sniper", "launcher", "shotgun", "smg", "assault")

    def Enable(self):
        bl2sdk.RegisterHook("WillowGame.WillowGameViewportClient.Tick", "Tick", on_tick)
        self.populate_lists()

    def Disable(self):
        bl2sdk.RemoveHook("WillowGame.WillowGameViewportClient.Tick", "Tick")

    def populate_lists(self):
        temp_wpd = FindAll("WeaponPartDefinition")

        self.WeaponTypeDefinition = FindAll("WeaponTypeDefinition")
        self.BalanceDefinition = FindAll("WeaponBalanceDefinition")
        self.ManufacturerDefinition = FindAll("ManufacturerDefinition")
        self.BodyPartDefinition = [x for x in temp_wpd if ".body." in get_obj_path_name(x).lower()]
        self.GripPartDefinition = [x for x in temp_wpd if ".grip." in get_obj_path_name(x).lower()]
        self.BarrelPartDefinition = [x for x in temp_wpd if ".barrel." in get_obj_path_name(x).lower()]
        self.SightPartDefinition = [x for x in temp_wpd if ".sight." in get_obj_path_name(x).lower()]
        self.StockPartDefinition = [x for x in temp_wpd if ".stock." in get_obj_path_name(x).lower()]
        self.ElementalPartDefinition = [x for x in temp_wpd if ".elemental." in get_obj_path_name(x).lower()]
        self.Accessory1PartDefinition = [x for x in temp_wpd if ".accessory." in get_obj_path_name(x).lower()]
        self.Accessory2PartDefinition = [x for x in temp_wpd if ".accessory." in get_obj_path_name(x).lower()]
        self.MaterialPartDefinition = [x for x in temp_wpd if ".manufacturermaterials." in get_obj_path_name(x).lower()]
        self.PrefixPartDefinition = [x for x in FindAll("WeaponNamePartDefinition")
                                     if ".prefix" in get_obj_path_name(x).lower()]
        self.TitlePartDefinition = [x for x in FindAll("WeaponNamePartDefinition")
                                    if ".title" in get_obj_path_name(x).lower()]

    def get_random_def_data(self):
        criteria = choice(self.types)

        def choice_c(iter, criteria):
            temp = [x for x in iter if criteria in get_obj_path_name(x).lower()]
            if temp:
                return choice(temp)
            return None

        exp_level = get_player_controller().Pawn.GetExpLevel()
        return (choice_c(self.WeaponTypeDefinition, criteria), choice_c(self.BalanceDefinition, criteria),
                choice(self.ManufacturerDefinition), exp_level, choice_c(self.BodyPartDefinition, criteria),
                choice_c(self.GripPartDefinition, criteria), choice_c(self.BarrelPartDefinition, criteria),
                choice_c(self.SightPartDefinition, criteria), choice_c(self.StockPartDefinition, criteria),
                choice(self.ElementalPartDefinition), choice(self.Accessory1PartDefinition),
                choice(self.Accessory2PartDefinition), choice_c(self.MaterialPartDefinition, criteria),
                choice(self.PrefixPartDefinition), choice(self.TitlePartDefinition),
                exp_level, exp_level)

    def change_weapon(self):
        pawn_inv_manager = get_player_controller().GetPawnInventoryManager()
        if not self.old_gun:
            pass
        else:
            pawn_inv_manager.InventoryUnreadied(pawn_inv_manager.GetWeaponInSlot(1), False)

        willow_weapon = get_current_worldinfo().Spawn(bl2sdk.FindClass('WillowWeapon'))
        pawn_inv_manager.ChangedWeapon()
        definition_data = self.get_random_def_data()

        willow_weapon.InitializeFromDefinitionData(definition_data, pawn_inv_manager.Instigator, True)
        willow_weapon.AdjustWeaponForBeingInBackpack()
        pawn_inv_manager.GiveStoredAmmoBeforeGoingToBackpack(definition_data[0].AmmoResource,
                                                             definition_data[0].StartingAmmoCount)
        pawn_inv_manager.AddInventoryToBackpack(willow_weapon)
        pawn_inv_manager.ReadyBackpackInventory(willow_weapon, 1)
        self.old_gun = willow_weapon


RandoInstance = Rando()


def on_tick(caller: UObject, function: UFunction, params: FStruct) -> bool:
    RandoInstance.clock += params.DeltaTime
    if RandoInstance.clock > 10.:
        RandoInstance.clock = 0.
        RandoInstance.change_weapon()
    return True


bl2sdk.Mods.append(RandoInstance)
