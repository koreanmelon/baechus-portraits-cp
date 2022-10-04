const path = require("path");

const basePath = "assets/base/";
const svePath = "assets/sve/";

function portraitChange(action, target, update, fromFile) {
    return {
        Action: action,
        Target: `Portraits/${target}`,
        FromFile: `${basePath}/${target}_${config[target]}.png`,
        Update: update,
        When: {
            `HasFile:${fromFile}`: true
        }
    };
}
