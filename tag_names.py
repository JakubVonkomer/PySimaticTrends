# dictionary of Tag Names, for individual languages

import config

tagNames = {} #dictionary of Tag Names

if config.LANG_DEFAULT == 'PL':
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
    
elif config.LANG_DEFAULT == 'EN':
    tagNames['test'] = 'test'

