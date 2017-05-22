// Initialize collapse button
$(".button-collapse").sideNav();
// Initialize collapsible (uncomment the line below if you use the dropdown variation)
//$('.collapsible').collapsible();

// clearForm() from http://stackoverflow.com/questions/6653556/jquery-javascript-function-to-clear-all-the-fields-of-a-form answer by ktamlyn
function clearForm()
{
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $(':checkbox, :radio').prop('checked', false);
    $('#search-text').focus();
}

function getDetailPageColor(courseid) {
    var dept = courseid.slice(0,2);
    var level = parseInt(courseid.slice(3,6));
    var color = {
        "majorColor": "",
        "darkness": "",
        "level": 0
    }
    var colorMap = {
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
    var pageColors = {
        major_color: [color.majorColor, color.darkness.concat("-", color.level)].join(" "),
        text_major: "",
        text_courseid: [color.majorColor.concat("-text"), "text".concat("-", color.darkness, "-4")].join(" "),
        text_title: [color.majorColor.concat("-text"), "text".concat("-", color.darkness, "-3")].join(" "),
        text_instructor: color.majorColor.concat("-text"),
        text_accent: "",
        nav_bar: [color.majorColor, color.darkness.concat("-", Math.abs(color.level-1))].join(" "),
    }
    if (color.darkness == "lighten" && color.level === 3) {
        pageColors.text_major = "grey-text text-darken-2"
    } else {
        pageColors.text_major = "white-text"
    }
    pageColors.text_accent = pageColors.text_major;
    return pageColors
}

function setDetailPageColor(courseid) {
    pageColors = getDetailPageColor(courseid);
    $('.cf-major-color').addClass(pageColors.major_color);
    $('.cf-text-major').addClass(pageColors.text_major);
    $('.cf-text-courseid').addClass(pageColors.text_courseid);
    $('.cf-text-title').addClass(pageColors.text_title);
    $('.cf-text-instructor').addClass(pageColors.text_instructor);
    $('.cf-text-accent').addClass(pageColors.text_accent);
    $('.nav-wrapper').addClass(pageColors.nav_bar);
    $('.cf-nav').addClass(pageColors.nav_bar);
}
