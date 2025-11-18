#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "SVCharacter.generated.h"

UENUM(BlueprintType)
enum class ESeekerRank : uint8 {
    Initiate,
    Wanderer,
    Adept,
    MasterSeeker
};

UCLASS()
class SEEKERVERSECORE_API ASVCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    // --- Core Stats ---
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float Coherence; // Replacing HP as the primary survival metric

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float Clarity;   // Mental stamina for casting/crafting

    // --- Economy ---
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Economy")
    int32 LumenBalance;

    // --- AI Integration ---
    /* Sends current context to Python Bridge for LLM processing */
    UFUNCTION(BlueprintCallable, Category = "AI")
    void SendContextToLLM(FString PlayerInput);

    /* Callback when LLM responds */
    UFUNCTION(BlueprintNativeEvent, Category = "AI")
    void OnLLMResponseReceived(const FString& ResponseText, const FString& ActionCommand);
};
