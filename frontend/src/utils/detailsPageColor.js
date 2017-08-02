const colorMap = {
    "02": "blue",
    "03": "light-blue",
    "04": "indigo",
    "05": "lime",
    "06": "brown",
    "08": "teal",
    "09": "red",
    "10": "light-green",
    "11": "orange",
    "12": "lime",
    "14": "deep-purple",
    "15": "orange",
    "16": "teal",
    "17": "indigo",
    "18": "deep-purple",
    "19": "light-green",
    "20": "yellow",
    "21": "blue",
    "24": "light-blue",
    "27": "brown",
    "32": "purple",
    "33": "indigo",
    "36": "deep-orange",
    "38": "cyan",
    "39": "amber",
    "42": "teal",
    "45": "pink",
    "48": "blue",
    "49": "deep-orange",
    "51": "orange",
    "52": "cyan",
    "53": "cyan",
    "54": "blue",
    "57": "red",
    "60": "purple",
    "62": "red",
    "64": "pink",
    "65": "purple",
    "66": "light-blue",
    "67": "red",
    "69": "amber",
    "70": "deep-purple",
    "73": "orange",
    "76": "green",
    "79": "light-green",
    "80": "lime",
    "82": "green",
    "83": "red",
    "84": "yellow",
    "85": "pink",
    "86": "deep-purple",
    "88": "amber",
    "90": "brown",
    "91": "purple",
    "92": "green",
    "93": "indigo",
    "94": "yellow",
    "95": "red",
    "98": "purple",
    "99": "red"
}

export function getDetailPageColor(courseid) {
    const dept = courseid.slice(0,2);
    const level = parseInt(courseid.slice(3,6), 10);
    let color = {
        "majorColor": "",
        "darkness": "",
        "level": 0
    }
    if (colorMap.hasOwnProperty(dept)) {
        color.majorColor = colorMap[dept];
    } else {
        color.majorColor = "blue-grey";
    }
    if (level < 200) {
        color.darkness = "lighten";
        color.level = 3
    } else if (200 <= level && level < 300) {
        color.darkness = "lighten";
        color.level = 2
    } else if (300 <= level && level < 400) {
        color.darkness = "lighten";
        color.level = 1
    } else if (400 <= level && level < 500) {
        color.darkness = "lighten";
        color.level = 0
    } else if (500 <= level && level < 600) {
        color.darkness = "darken";
        color.level = 1
    } else if (600 <= level && level < 700) {
        color.darkness = "darken";
        color.level = 2
    } else {
        color.darkness = "darken";
        color.level = 3
    }
    let pageColors = {
        majorColor: [color.majorColor, color.darkness.concat("-", color.level)].join(" "),
        textMajorColor: "",
        courseidColor: [color.majorColor.concat("-text"), "text".concat("-", color.darkness, "-4")].join(" "),
        titleColor: [color.majorColor.concat("-text"), "text".concat("-", color.darkness, "-3")].join(" "),
        InstructorColor: color.majorColor.concat("-text"),
        textAccentColor: "",
        NavbarColor: [color.majorColor, color.darkness.concat("-", Math.abs(color.level-1))].join(" "),
    }
    if (color.darkness === "lighten" && color.level === 3) {
        pageColors.textMajorColor = "grey-text text-darken-2"
    } else {
        pageColors.textMajorColor = "white-text"
    }
    pageColors.textAccentColor = pageColors.textMajorColor;
    return pageColors
}
