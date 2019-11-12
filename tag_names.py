# dictionary of Tag Names, for individual languages

tagNames = {} #dictionary of Tag Names

def LoadTagNames(lang):
    global tagNames

    tagNames.clear() # vymaze povodne tagy

    if lang == 'PL': # Polish
        tagNames['BAT_DB_SOC_BOX'] = 'BATERIA (%)'
        tagNames['BMZ_DB_Actual_current_for_battery_set_Value'] = 'POBÓR PRĄDU (A)'
        tagNames['CONTROL_DATA_Rychlost_MS'] = 'PRĘDKOŚĆ (m/s)'
        tagNames['CONTROL_DATA_SPEED_SETPOINT_MS'] = 'PRĘDKOŚĆ NADANA(m/s)'
        tagNames['GF1_DB_HP_READ_VALUE_Vykon'] = 'MOC SILNIKA 1 (kW)'
        tagNames['GF2_DB_HP_READ_VALUE_Vykon'] = 'MOC SILNIKA 2 (kW)'
        tagNames['Nap_24V'] = 'NAPIĘCIE AKUMULATORA (V)'
        tagNames['BMZ_DB_Actual_voltage_for_battery_set_Value'] = 'NAPIĘCIE BATERII (V)'

        tagNames['DrahaDB_DrahaLog'] = 'DYSTANS (m)'
        tagNames['BAT_DB_MaxTemp'] = 'TEMPERATURA BATERII (C)'
        tagNames['KONTAKT_RUČNÁ_BRZDA_AKTÍVNA'] = 'HAMULEC AKTYWNY ()'
        tagNames['GF1_DB_HP_READ_VALUE_Teplota_elektroniky'] = 'TEMPERATURA ELEKTRONIKY (C)'
        tagNames['GF2_DB_HP_READ_VALUE_Teplota_elektroniky'] = 'TEMPERATURA ELEKTRONIKY GF2 (C)'   
    
    else: # English is default
        tagNames['BAT_DB_SOC_BOX'] = 'BATTERY SOC [%]'
        tagNames['BMZ_DB_Actual_current_for_battery_set_Value'] = 'Batt. current [A]'
        tagNames['CONTROL_DATA_Rychlost_MS'] = 'Speed [m/s]'
        tagNames['CONTROL_DATA_SPEED_SETPOINT_MS'] = 'Speed setpoint [m/s]'
        tagNames['GF1_DB_HP_READ_VALUE_Vykon'] = 'Motor power GF1 [kW]'
        tagNames['GF2_DB_HP_READ_VALUE_Vykon'] = 'Motor power GF2 [kW]'
        tagNames['Nap_24V'] = '24V voltage [V]'
        tagNames['BMZ_DB_Actual_voltage_for_battery_set_Value'] = 'Batt. voltage [V]'

        tagNames['DrahaDB_DrahaLog'] = 'Distance [m]'
        tagNames['BAT_DB_MaxTemp'] = 'Batt. temperature [C]'
        tagNames['KONTAKT_RUČNÁ_BRZDA_AKTÍVNA'] = 'Hand brake active []'
        tagNames['GF1_DB_HP_READ_VALUE_Teplota_elektroniky'] = 'CB temperature GF1 [C]'
        tagNames['GF2_DB_HP_READ_VALUE_Teplota_elektroniky'] = 'CB temperature GF2 [C]'   

