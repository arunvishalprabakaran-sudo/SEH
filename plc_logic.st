(* AUTO-GENERATED PLC LOGIC *)

DECLARATION
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

IMPLEMENTATION
IF Manual_Mode THEN
    pump_on := Manual_Pump;
END_IF;

IF !Manual_Mode && Level < Low_Threshold THEN
    pump_on := True;
END_IF;

IF !Manual_Mode && Level > High_Threshold THEN
    pump_on := False;
END_IF;

Pump := pump_on;
