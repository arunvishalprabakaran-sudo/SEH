(* AUTO-GENERATED PLC LOGIC *)

PROGRAM MAIN_PROGRAM
VAR
    Level : INT;
    Manual_Mode : BOOL;
    Manual_Pump : BOOL;
    Low_Threshold : INT;
    High_Threshold : INT;
    Pump : BOOL;
    auto_mode : BOOL;
    pump_on : BOOL;
END_VAR

IF Manual_Mode THEN
    pump_on := Manual_Pump;
END_IF;

IF NOT Manual_Mode  AND  Level < Low_Threshold THEN
    pump_on := TRUE;
END_IF;

IF NOT Manual_Mode  AND  Level > High_Threshold THEN
    pump_on := FALSE;
END_IF;

Pump := pump_on;
