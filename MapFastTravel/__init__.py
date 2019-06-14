import bl2sdk

class MapFT(bl2sdk.BL2MOD):
    Name = "Map Fast Travel"
    Description = "Every second time placing a custom waypoint (or removing one) will place you to the second placed (or the removed) closest Point of interest."
    Author = "Juso"

    RemovedMarker = False
    MapObjects = []
    ObjectDelta = []

    def GetLocation(self, caller, function, params):
        if self.RemovedMarker == True:
            Pawn = bl2sdk.GetEngine().GamePlayers[0].Actor.Pawn
            for i in caller.MapObjects:
                if i.CustomObjectLoc.X != 0.0: #Get our newest Marker
                    MarkerLoc = (i.CustomObjectLoc.X, i.CustomObjectLoc.Y)
                    
            bl2sdk.Log("MarkerLoc: " + str(MarkerLoc))
            #Get all the objects delta to our Marker
            for MapObjectsLoc in self.MapObjects:
                MapObjLoc = (MapObjectsLoc.Location.X, MapObjectsLoc.Location.Y)
                delta = ( (MapObjLoc[0] - MarkerLoc[0]) ** 2 + (MapObjLoc[1] - MarkerLoc[1]) ** 2)**(0.5) #Calculate the distance between each Point of interest and our maker
                self.ObjectDelta.append( delta )
            
            
            temp = self.ObjectDelta.index(min(self.ObjectDelta))     
            Pawn.Location = (self.MapObjects[temp].Location.X,
                             self.MapObjects[temp].Location.Y,
                             self.MapObjects[temp].Location.Z + 200)

            self.MapObjects.clear()
            self.ObjectDelta.clear()
            self.RemovedMarker = False
            return True
        else:
            for i in caller.MapObjects: #Fill up our List with all interesting objects on map
                if i.ClientInteractiveObject is not None:
                    self.MapObjects.append(i.ClientInteractiveObject)
                if i.Vehicle is not None:
                    self.MapObjects.append(i.Vehicle)
            self.RemovedMarker = True
            return True

    def Enable(self):
        bl2sdk.RegisterHook("WillowGame.StatusMenuMapGFxObject.PlaceCustomObjective", "MarkerHook", Teleport)

    def Disable(self):
        bl2sdk.RemoveHook("WillowGame.StatusMenuMapGFxObject.PlaceCustomObjective", "MarkerHook")


MapFTInstance = MapFT()

def Teleport(caller: bl2sdk.UObject, function: bl2sdk.UFunction, params: bl2sdk.FStruct) -> bool:
    return MapFTInstance.GetLocation(caller, function, params)

bl2sdk.Mods.append(MapFTInstance)