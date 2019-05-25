import bl2sdk

class Emotes(bl2sdk.BL2MOD):
    Name = "Emotes"
    Description = """Adds emotes to the game that the player can use.
    'Up' = Play Emote
    'Down' = Stop Emote
    'Left'/'Right' = Change Emote
    Written by Juso
    Original idea and method by OurLordAndSaviorGabeNewell"""

    #Loads the Package requierd for the Animations
    def ForceLoad(self):
        Objects = [
                "GD_NPCShared.Perches.Perch_NPC_ArmsCrossedForever:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_BangOnSomething:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_BarrelSitForever:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_ChairSitForever:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_DartsHit:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_KickGround:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_LeanOnCounterForever:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_LeanOnWallNonRandom:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_LookAtGround:SpecialMove_PerchLoop_0",
                "GD_NPCShared.Perches.Perch_NPC_PeerUnder:SpecialMove_PerchLoop_0",
                "GD_Moxxi.Perches.Perch_Moxxi_Dance:SpecialMove_PerchLoop_0",
                "GD_Moxxi.Perches.Perch_Moxxi_WipeBar:SpecialMove_PerchLoop_0",
                "GD_TannisNPC.Perches.Perch_Tannis_LookAround:SpecialMove_PerchLoop_0",
                "GD_TannisNPC.Perches.Perch_Tannis_HandsOnHips:SpecialMove_PerchLoop_0",
                "GD_TannisNPC.Perches.Perch_Tannis_Thinking:SpecialMove_PerchLoop_0"
            ]
        bl2sdk.LoadPackage("SanctuaryAir_Dynamic")
        for Object in Objects:
            x = bl2sdk.FindObject("SpecialMove_PerchLoop", Object)
            bl2sdk.KeepAlive(x)

    #Returns the name of the Animation thats played
    _animation = 0
    def ChooseAnimation(self):
        Animations = [
                "Perch_CoyoteUglyDance_Loop",
                "Perch_WipeBarTop_Loop",
                "Perch_HandsOnHips_Loop",
                "Perch_LookAround_Loop",
                "Perch_ThinkChin_Loop",
                "Perch_Sittingonbarrel_Loop",
                "Perch_ThrowDarts_Loop",
                "Kick_Object_on_Ground",
                "Perch_WallLean_Loop",
                "Perch_InspectGround_Loop",
                "Perch_CounterTopLean_Loop",
                "Kick_Object_on_Ground",
                "Perch_PeerUnder_Loop",
                "Perch_ChairSit_Loop",
                "Perch_BangOnWall_Loop",
                "Perch_ArmsCrossed_Loop"
                ]
        return Animations[self._animation % len(Animations)-1]
    #Returns the current PlayerController
    def GetPlayerController(self):
        return bl2sdk.GetEngine().GamePlayers[0].Actor
    #Gives Feedback on what animation is choosed
    def FeedbackEmote(self):
        if self.GetPlayerController() != None:
            HUD = self.GetPlayerController().GetHUDMovie()
            HUD.ClearTrainingText()
            HUD.AddTrainingText(self.ChooseAnimation(), "Emote", 3.000000, (), "", False, 0, self.GetPlayerController().PlayerReplicationInfo, True)

    def PlayEmote(self):
        #We are going to change the animations that are played on melee to play our emotes instead
        SpecialMoves = [
                    "GD_Assassin_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Lilac_Psycho_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Mercenary_Streaming.Anims.WeaponAnim_Melee",
                    "GD_PlayerShared.Anims.WeaponAnim_Melee_WeaponBlade",
                    "GD_Siren_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Soldier_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Tulip_Mechro_Streaming.Anims.WeaponAnim_Melee"
            ]
        
        PC = self.GetPlayerController()
        for Move in SpecialMoves:
            if bl2sdk.FindObject("SpecialMove_WeaponAction", Move) != None:
                PC.ConsoleCommand("set "+ Move + " AnimName " + self.ChooseAnimation(), 0)
                PC.ConsoleCommand("set "+ Move + " EndingCondition EC_Loop", 0)
                #The first 2 animations are Moxxie only
                if self._animation in (0, 1):
                    PC.ConsoleCommand("set "+ Move + " AnimSet AnimSet'Anim_Moxxi.Anim_Moxxi'", 0)
                #Index 2,3 and 4 are Tannis only
                elif self._animation in (2, 3, 4):
                    PC.ConsoleCommand("set "+ Move + " AnimSet AnimSet'Anim_Tannis.Anim_Tannis'", 0)
                else:
                   PC.ConsoleCommand("set "+ Move + " AnimSet AnimSet'Anim_Generic_NPC.Anim_Generic_NPC'", 0)
        PC.ConsoleCommand("camera 3rd", 0)
        PC.Behavior_Melee()
    #Reverse the changes of PlayEmote()
    def StopEmote(self):
        SpecialMoves = [
                    "GD_Assassin_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Lilac_Psycho_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Mercenary_Streaming.Anims.WeaponAnim_Melee",
                    "GD_PlayerShared.Anims.WeaponAnim_Melee_WeaponBlade",
                    "GD_Siren_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Soldier_Streaming.Anims.WeaponAnim_Melee",
                    "GD_Tulip_Mechro_Streaming.Anims.WeaponAnim_Melee"
            ]
        
        PC = self.GetPlayerController()
        for Move in SpecialMoves:
            if bl2sdk.FindObject("SpecialMove_WeaponAction", Move) != None:
                PC.ConsoleCommand("set "+ Move + " AnimName Melee", 0)
                PC.ConsoleCommand("set "+ Move + " EndingCondition EC_OnBlendOut", 0)
                PC.ConsoleCommand("set "+ Move + " AnimSet None", 0)
        PC.ConsoleCommand("camera 1st", 0)
        PC.Behavior_Melee()


    def GameInputRebound(self, name, key):
        pass

    def GameInputPressed(self, name):
        if name == "Next Emote":
            self._animation += 1
            self.FeedbackEmote()
        elif name == "Previous Emote":
            self._animation -= 1
            self.FeedbackEmote()
        if name == "Play Emote":
            self.PlayEmote()
        if name == "Stop Emote":
            self.StopEmote()


    def HandleEmotes(self, caller, function, params):
        print(params)


    def Enable(self):
        self.ForceLoad()
        self.RegisterGameInput("Play Emote", "Up")
        self.RegisterGameInput("Next Emote", "Right")
        self.RegisterGameInput("Previous Emote", "Left")
        self.RegisterGameInput("Stop Emote", "Down")
    def Disable(self):
        self.UnregisterGameInput("Play Emote")
        self.UnregisterGameInput("Next Emote")
        self.UnregisterGameInput("Previous Emote")
        self.UnregisterGameInput("Stop Emote")


#Create an instance of my class	
EmoteInstance = Emotes()
bl2sdk.Mods.append(EmoteInstance)


