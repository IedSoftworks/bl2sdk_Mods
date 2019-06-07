import bl2sdk

class Sliding(bl2sdk.BL2MOD):

    Name = "Sliding"
    Description = "Extends the movement of Borderlands 2 by allowing you to slide. Depending on the slope you either slide further and faster or slower and shorter. To slide simply stay ducked directly after sprinting, also keep a directional movement key pressed."
    Author = "Juso"
    Types = [3]
    
    SlideSpeed = 2.2
    OldZ = 0


    def GetPlayerController(self):
        return bl2sdk.GetEngine().GamePlayers[0].Actor

    
    def HandleMove(self, caller, function, params):          
        PC = self.GetPlayerController()
        PlayerInput = PC.PlayerInput
        SlopeDelta = PC.Pawn.Location.Z - self.OldZ
        
        if PC.Pawn.Acceleration.X == 0.0 and PC.Pawn.Acceleration.Y == 0.0:
            PC.Pawn.CrouchedPct = self.SlideSpeed = 0.42
        if PC.bDuck == 1 and self.SlideSpeed >= 0.421:#These are the conditions to count as sliding
            if SlopeDelta > 0.5 and PC.Pawn.Physics != 2:#Check for sliding up a slope
                PC.Rotation.Roll = int((self.SlideSpeed-0.4)*275)
                self.SlideSpeed -= ((params.DeltaTime * (1.15 + SlopeDelta * 0.5)) / self.SlideSpeed)
                PC.Pawn.CrouchedPct = self.SlideSpeed
            elif SlopeDelta < -0.75 and PC.Pawn.Physics != 2:#Check for sliding down a slope
                PC.Rotation.Roll = int((self.SlideSpeed-0.4)*275)
                self.SlideSpeed -= ((params.DeltaTime * (1.15 + SlopeDelta * 0.25)) / self.SlideSpeed)
                PC.Pawn.CrouchedPct = self.SlideSpeed
            elif PC.Pawn.Physics != 2:#No slope and not falling
                PC.Rotation.Roll = int((self.SlideSpeed-0.4)*275)
                self.SlideSpeed -= ((params.DeltaTime * 1.15) / self.SlideSpeed)
                PC.Pawn.CrouchedPct = self.SlideSpeed
            else:#While in air dont change the slide speed
                PC.Rotation.Roll = int((self.SlideSpeed-0.4)*275)
                PC.Pawn.CrouchedPct = self.SlideSpeed
        else:#If Player is not sliding set everything back to default
            PC.Rotation.Roll = 0       
            PC.Pawn.CrouchedPct = self.SlideSpeed = 0.42
        self.OldZ = PC.Pawn.Location.Z#We need to refresh our OldZ location after each move tick to make sure we keep sliding the same slope
 
    def HandleDuck(self, caller, function, params):
        PC = self.GetPlayerController()
        self.OldZ = PC.Pawn.Location.Z
        if PC.bInSprintState == True:
            self.SlideSpeed = 2.2
            if PC.bCrouchToggle:
                if caller.bHoldDuck:
                    caller.bHoldDuck = False
                    PC.bDuck = 0            
                    PC.Pawn.CrouchedPct = self.SlideSpeed
                    return False
                else:           
                    caller.bHoldDuck = True
                    PC.bDuck = 1
                    PC.Pawn.CrouchedPct = self.SlideSpeed
                return False
            else:
                PC.bDuck = 1
                PC.Pawn.CrouchedPct = self.SlideSpeed
                return False
        else:
           PC.Pawn.CrouchedPct = self.SlideSpeed
           return True

   

    def Enable(self):
        bl2sdk.RegisterHook("WillowGame.WillowPlayerInput.DuckPressed", "SlideHook", DoSlide)
        bl2sdk.RegisterHook("WillowPlayerController.PlayerWalking.PlayerMove", "MoveHook", AdvancedMove)

    def Disable(self):
        bl2sdk.RemoveHook("WillowGame.WillowPlayerInput.DuckPressed", "SlideHook")
        bl2sdk.RemoveHook("WillowPlayerController.PlayerWalking.PlayerMove", "MoveHook")


SlidingInstance = Sliding()

def DoSlide(caller: bl2sdk.UObject, function: bl2sdk.UFunction, params: bl2sdk.FStruct) -> bool:
    return SlidingInstance.HandleDuck(caller, function, params)

def AdvancedMove(caller: bl2sdk.UObject, function: bl2sdk.UFunction, params: bl2sdk.FStruct) -> bool:
    SlidingInstance.HandleMove(caller, function, params)
    return True

bl2sdk.Mods.append(SlidingInstance)
