// Helper functions

var moment = require('moment');

export function daysToString(days) {
  return days.map(day => dayToString(day)).join(", ")
}


const _DAYS = {
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


const _CMU_BUILDINGS_FROM_ABBR = {
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

const _CMU_BUILDINGS = {
    "baker": "BH",
    "cyert": "CYH",
    "doherty": "DH",
    "stadium": "GES",
    "gates": "GHC",
    "weigand": "GYM",
    "gymnasium": "GYM",
    "gym": "GYM",
    "hamburg": "HBH",
    "hamerschlag": "HH",
    "hunt": "HL",
    "library": "HL",
    "tepper": "POS",
    "posner": "POS",
    "gsia": "IA",
    "mellon": "MI",
    "newell": "NSH",
    "simon": "NSH",
    "purnell": "PCA",
    "porter": "PH",
    "roberts": "REH",
    "scaife": "SH",
    "warner": "WH",
    "wean": "WEH"
}

export function getFullBuildingName(name) {
  return _CMU_BUILDINGS_FROM_ABBR[name]
  // Return null if not exist
}

export function titleCase(str) {
  return str.toLowerCase().replace(/\b(\w)/g, s => s.toUpperCase());
}

export function convertName(str) {
  const name = str.split(", ")
  if (name.length !== 1) {
    return `${name[1]} ${name[0]}`
  }
  return name[0]
}

export function randomPick(myArray) {
  return myArray[Math.floor(Math.random() * myArray.length)];
}

export function getMini(date) {
  let mMonth = (month) => { return month - 1 }
  if (!date) {
    date = moment()
  } else {
    date.year(moment().year())
  }
  if (date.isBetween(moment({ month: mMonth(8), day: 20 }), moment({ month: mMonth(10), day: 15 }))) {
    return 1
  } else if (date.isBetween(moment({ month: mMonth(10), day: 15 }), moment({ month: mMonth(12), day: 31 }))) {
    return 2
  } else if (date.isBetween(moment({ month: mMonth(1), day: 1 }), moment({ month: mMonth(3), day: 15 }))) {
    return 3
  } else if (date.isBetween(moment({ month: mMonth(3), day: 15 }), moment({ month: mMonth(5), day: 15 }))) {
    return 4
  } else if (date.isBetween(moment({ month: mMonth(5), day: 15 }), moment({ month: mMonth(7), day: 1 }))) {
    return 5
  } else if (date.isBetween(moment({ month: mMonth(7), day: 1 }), moment({ month: mMonth(8), day: 20 }))) {
    return 6
  }
  return 0
}

export function getCurrentSemester() {
  return getSemesterFromDate(moment())
}

export function getSemesterFromDate(date) {
  if (date === null) {
    date = moment()
  }
  const mini = getMini(date)
  let semester
  if (1 <= mini && mini <= 2) {
    semester = "Fall"
  } else if (3 <= mini && mini <= 4) {
    semester = "Spring"
  } else if (mini === 5) {
    semester = "Summer One"
  } else {
    semester = "Summer Two"
  }
  return `${semester} ${date.year()}`
}

export var searchTips = [
  "a course number '15-112'",
  "name of an instructor",
  "name of a course",
  "a room 'DH2210'",
  "a building 'Doherty'",
  "a time '8:00am'",
  "a day 'Monday'"
]

var queryRe = {
  courseid: /\b(\d{2}-\d{3}|\d{5})\b/,
  building: /\b(bh|cfa|cic|cyh|dh|eds|ges|ghc|gym|hbh|hh|hl|ia|ini|mi|mm|nsh|pca|pos|ph|ptc|reh|scr|sei|sh|uc|wh|weh)\b/,
  buidlingFull: /\b(baker|cyert|doherty|stadium|gates|weigand|gymnasium|gym|hamburg|hamerschlag|hunt|library|tepper|posner|gsia|mellon|newell|simon|purnell|porter|roberts|scaife|warner|wean)\b/,
  room: /\b\w?\d+\w?\b/,
  buildingRoom: /\b(bh|cfa|cic|cyh|dh|eds|ges|ghc|gym|hbh|hh|hl|ia|ini|mi|mm|nsh|pca|pos|ph|ptc|reh|scr|sei|sh|uc|wh|weh)(\w?\d+\w?)\b/
}

export function parseSearchQuery(query) {
  let parsedQuery = {}
  // Only keep the first 100 letters in the query
  query = query.slice(0, 100).toLowerCase()
  if (queryRe.courseid.test(query)) {
    parsedQuery.courseid = query.match(queryRe.courseid)[0]
    parsedQuery.courseid = parsedQuery.courseid.replace(/(\d{2})(\d{3})/, "$1-$2")
    query = query.replace(queryRe.courseid, '')
  }
  if (queryRe.buildingRoom.test(query)) {
    parsedQuery.building = query.match(queryRe.buildingRoom)[1]
    parsedQuery.room = query.match(queryRe.buildingRoom)[2]
    query = query.replace(queryRe.buildingRoom, '')
  } else {
    if (queryRe.building.test(query)) {
      parsedQuery.building = query.match(queryRe.building)[0]
      query = query.replace(queryRe.building, '')
    } else if (queryRe.buidlingFull.test(query)) {
      parsedQuery.building = query.match(queryRe.buidlingFull)[0]
      query = query.replace(queryRe.buidlingFull, '')
    }
    if (queryRe.room.test(query)) {
      parsedQuery.room = query.match(queryRe.room)[0]
      query = query.replace(queryRe.room, '')
    }
  }
  if (query && query.trim() !== "") {
    parsedQuery.text = query
  }
  console.log(parsedQuery)
  return parsedQuery
}

export function encodeURIParams(params) {
  return Object.keys(params)
      .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
      .join('&')
}
