#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "SVGameMode.generated.h"

USTRUCT(BlueprintType)
struct FMarketData {
    GENERATED_BODY()
    
    UPROPERTY(BlueprintReadOnly)
    float BioMassPrice;
    
    UPROPERTY(BlueprintReadOnly)
    float DataPrice;
    
    UPROPERTY(BlueprintReadOnly)
    float InflationRate;
};

UCLASS()
class SEEKERVERSECORE_API ASVGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    // Updates market prices based on player transactions
    UFUNCTION(BlueprintCallable, Category = "Economy")
    void SimulateMarketTick();

    UPROPERTY(BlueprintReadOnly, Category = "Economy")
    FMarketData CurrentMarketState;
};
