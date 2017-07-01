// Helper functions

export function daysToString(days) {
    return days.map(day => dayToString(day))
}


let _DAYS = {
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat",
    0: "Sun"
}

export function dayToString(day) {
    return _DAYS[day % 7]
}


let _CMU_BUILDINGS_FROM_ABBR = {
    "BH": "Baker Hall",
    "CYH": "Cyert Hall",
    "DH": "Doherty Hall",
    "EDS": "Elliot Dunlap Smith Hall",
    "GES": "Gesling Stadium",
    "GHC": "Gates and Hillman Centers",
    "HBH": "Hamburg Hall",
    "HH": "Hamerschlag Hall",
    "HL": "Hunt Library",
    "POS": "Posner Hall",
    "IA": "GSIA (Tepper School of Business)",
    "MI": "Mellon Institute",
    "NSH": "Newell-Simon Hall",
    "PCA": "Purnell Center for the Arts",
    "PH": "Porter Hall",
    "REH": "Roberts Engineering Hall",
    "SH": "Scaife Hall",
    "WH": "Warner Hall",
    "WEH": "Wean Hall",
    "SCR": "300 South Craig Street",
    "SEI": "Software Engineering Institute",
    "PTC": "Pittsburgh Technology Center - 2nd Avenue",
    "INI": "4616 Henry Street",
    "MM": "Margaret Morrison Carnegie Hall",
    "CIC": "Collaborative Innovation Center",
    "CFA": "College of Fine Arts"
}

export function getFullBuildingName(name) {
    // TODO check here
    return _CMU_BUILDINGS_FROM_ABBR[name]
    // Return null if not exist
}
