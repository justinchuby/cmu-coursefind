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

export function getFullBuildingName(name) {
  // TODO check here
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


// let _CMU_NUMBER_DEPARTMENTS = {
//     "48": "Architecture",
//     "60": "Art",
//     "52": "BXA Intercollege Degree Programs",
//     "83": "Biological Sciences",
//     "42": "Biomedical Engineering",
//     "70": "Business Administration",
//     "62": "CFA Interdisciplinary",
//     "39": "CIT Interdisciplinary",
//     "99": "Carnegie Mellon University-Wide Studies",
//     "64": "Center for the Arts in Society",
//     "86": "Center for the Neural Basis of Cognition",
//     "06": "Chemical Engineering",
//     "09": "Chemistry",
//     "12": "Civil & Environmental Engineering",
//     "02": "Computational Biology",
//     "15": "Computer Science",
//     "62": "Computer Science and Arts",
//     "93": "Creative Enterprise:Sch of Pub Pol & Mgt",
//     "51": "Design",
//     "67": "Dietrich College Information Systems",
//     "66": "Dietrich College Interdisciplinary",
//     "54": "Drama",
//     "73": "Economics",
//     "18": "Electrical & Computer Engineering",
//     "20": "Electronic Commerce",
//     "19": "Engineering & Public Policy",
//     "76": "English",
//     "53": "Entertainment Technology Pittsburgh",
//     "65": "General Dietrich College",
//     "94": "Heinz College Wide Courses",
//     "79": "History",
//     "05": "Human-Computer Interaction",
//     "62": "Humanities and Arts",
//     "04": "Information & Communication Technology",
//     "14": "Information Networking Institute",
//     "95": "Information Systems:Sch of IS & Mgt",
//     "84": "Institute for Politics and Strategy",
//     "08": "Institute for Software Research",
//     "49": "Integrated Innovation Institute",
//     "11": "Language Technologies Institute",
//     "38": "MCS Interdisciplinary",
//     "10": "Machine Learning",
//     "27": "Materials Science & Engineering",
//     "21": "Mathematical Sciences",
//     "24": "Mechanical Engineering",
//     "92": "Medical Management:Sch of Pub Pol & Mgt",
//     "82": "Modern Languages",
//     "57": "Music",
//     "32": "Naval Science - ROTC",
//     "80": "Philosophy",
//     "69": "Physical Education",
//     "33": "Physics",
//     "85": "Psychology",
//     "91": "Public Management:Sch of Pub Pol & Mgt",
//     "90": "Public Policy & Mgt: Sch of Pub Pol & Mgt",
//     "16": "Robotics",
//     "62": "Science and Arts",
//     "88": "Social & Decision Sciences",
//     "17": "Software Engineering",
//     "36": "Statistics",
//     "98": "StuCo (Student Led Courses)",
//     "45": "Tepper School of Business",
//     "03": " Biological Sciences"
// }

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
