async function postData(url = '', data = {}) {
    let body = JSON.stringify(data);
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrer: 'no-referrer', // no-referrer, *client
        body: body // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}

async function loadOptions(mainId, subDivId, parentLoopCounter) {
    let link = "/classify/load-subs/";

    try {
        const data = await postData(link, {id: mainId});
        setOptions(data, subDivId, parentLoopCounter)
    } catch (error) {
        console.error(error);
    }
}

function setOptions(optionObject, subDivId, parentLoopCounter) {
    let subDiv = $(`#${subDivId}`);
    subDiv.empty();
    for (let key in optionObject) {
        let lbl = document.createElement("label");
        let btnId = `sub-${parentLoopCounter}`;
        lbl.setAttribute("class", "btn btn-sm btn-secondary");
        lbl.setAttribute("id", btnId);
        lbl.setAttribute("data-value", key);
        lbl.innerHTML = optionObject[key];

        let inpt = document.createElement("input");
        inpt.setAttribute("type", "radio");
        lbl.prepend(inpt);

        subDiv.append(lbl)
    }
}

function getDataValue(elemId) {
    try {
        return $(elemId).attr("data-value")
    } catch (e) {
        console.log(e);
        return ""
    }
}

function collectFormData(numColumns) {
    let formData = {};
    for (let i = 0; i < numColumns; i++) {
        formData[i] = {
            main: getDataValue(`#main-${i}.active`),
            sub: getDataValue(`#sub-${i}.active`)
        }
    }
    formData["sourceId"] = sourceId;
    return formData
}

async function sendFormData(numColumns) {
    let data = collectFormData(numColumns);
    let link = "/classify/";

    try {
        const reply = await postData(link, data);
        window.location.replace(reply["location"])
    } catch (error) {
        console.error(error);
    }
}