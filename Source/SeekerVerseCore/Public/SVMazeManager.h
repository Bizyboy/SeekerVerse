#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PCGComponent.h" // UE5.4 PCG Framework
#include "SVMazeManager.generated.h"

UCLASS()
class SEEKERVERSECORE_API ASVMazeManager : public AActor
{
    GENERATED_BODY()

public:
    // The Seed that determines the current week's maze layout
    UPROPERTY(Replicated, EditAnywhere, BlueprintReadWrite, Category = "Maze Config")
    int32 WeeklySeed;

    // PCG Graph reference for Generating Ruins
    UPROPERTY(EditAnywhere, Category = "PCG")
    TObjectPtr<UPCGGraph> MazeGenerationGraph;

    // Function to trigger a world shift
    UFUNCTION(BlueprintCallable, Category = "Maze Control")
    void RegenerateSectors();
};
