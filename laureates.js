(function(globalObj) {
    'use strict'

    var laureateObj = {};
    var display = null;
    var filterObj = {};
    var xmlhttp = new XMLHttpRequest();

    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else
        init();

    xmlhttp.open("GET", "nobelWinners.json", true);
    if (xmlhttp.readyState != 4)
        xmlhttp.send();

    function init() {
        display = document.getElementById("id04");

        filterObj.start = 0;
        filterObj.end = 0;
        filterObj.category = "";
        filterObj.country = "";
        filterObj.gender = "";

        var start = document.getElementById("start");
        var startRange = document.getElementById("startRange");
        // here using an arrow function
        start.addEventListener("change", () => {
            if (validateYear(start))
                startRange.value = start.value;
        }, false);
        startRange.addEventListener("change", function() {
            start.value = startRange.value;
        }, false);

        var end = document.getElementById("end");
        var endRange = document.getElementById("endRange");
        end.addEventListener("change", function() {
            if (validateYear(end))
                endRange.value = end.value;
        }, false);
        endRange.addEventListener("change", function() {
            end.value = endRange.value;
        }, false);

        var submit = document.getElementById("submitBtn");
        submit.addEventListener("click", function() {
            if (checkUserInput(start, end)) {
                doSubmit(start, end)
            }
        }, false);
    }

    function getLaureate(laureateId) {
        var result = "";
        var laureateArr = laureateObj.laureates;
        for (var i = 0; i < laureateArr.length; i++) {
            if (laureateArr[i].id == laureateId)
                result = laureateArr[i];
        }
        return result;
    }

    function checkUserInput(start, end) {
        var isValid = true;
        if (xmlhttp.readyState != 4 || xmlhttp.status != 200) {
            display.textContent = "JSON File for laureates not loaded";
            isValid = false;
        }
        if (!validateYear(start)) {
            display.textContent = "Invalid Start Year";
            isValid = false;
        }
        if (!validateYear(end)) {
            display.textContent = "Invalid End Year";
            isValid = false;
        }

        if (end.value == "") {
            end.value = 2018;
            end.dispatchEvent(new Event('change'));
        }

        if (start.value == "") {
            start.value = end.value;
            start.dispatchEvent(new Event('change'));
        }

        if (parseInt(start.value) > parseInt(end.value)) {
            display.textContent = "End year must be later than start year"
            isValid = false
        }
        return isValid;
    }

    function doSubmit(start, end) {
        if (!laureateObj.hasOwnProperty('laureates')) {
            console.log("NOT Parsed");
            laureateObj = JSON.parse(xmlhttp.responseText);
        }
        var category = document.getElementById("category").value;
        var country = document.getElementById("country").value;
        var gender = "";
        if (document.getElementById('gendermale').checked)
            gender = "m";
        else {
            if (document.getElementById('genderfemale').checked)
                gender = "f";
        }

        if (isFilterChanged(start.value, end.value, category, country, gender)) {
            filterObj.start = parseInt(start.value);
            filterObj.end = parseInt(end.value);
            filterObj.category = category;
            filterObj.country = country;
            filterObj.gender = gender;
            var laureateArr =
                filterLaureates(laureateObj.laureates, filterObj);
            if (laureateArr.length == 0)
                display.textContent = "No laureates match these criteria";
            else {
                var prizeArr = buildPrizeArray(laureateArr, filterObj);
                while (display.hasChildNodes()) {
                    display.removeChild(display.lastChild);
                }
                display.appendChild(buildPrizeTable(prizeArr));
            }
        }
        toggleGenderCol();
    }

    function isFilterChanged(startYr, endYr, category, country, gender) {
        return startYr != filterObj.start || endYr != filterObj.end ||
            category != filterObj.category || country != filterObj.country ||
            gender != filterObj.gender;
    }

    // Bug in IE requires setting border
    function toggleGenderCol() {
        var e = document.getElementsByClassName("gendercol");
        for (var i = 0; i < e.length; i++) {
            if (e[i].style.visibility != 'visible') {
                e[i].style.visibility = 'visible';
                e[i].style.border = "solid";
            } else {
                e[i].style.visibility = 'hidden';
                e[i].style.border = "none";
            }
        }
    };


    function validateYear(yearEl) {
        var isValid = true;
        if (yearEl.checkValidity() == false) {
            display.textContent = "Invalid Year";
            isValid = false;
        }
        return isValid;
    }

    function moreInformation(prizeId, prizeIndex) {
        var moreElmnt = {};
        var laureate = getLaureate(prizeId);
        if (laureate != "") {
            var prize = laureate.prizes[prizeIndex];
            var infoElmnt = document.createElement("p");
            infoElmnt.setAttribute("class", "moreInfo");
            if (laureate.born != "0000-00-00")
                infoElmnt.appendChild(document.createTextNode("Year of birth: " + laureate.born));
            if (laureate.hasOwnProperty('bornCity')) {
                infoElmnt.appendChild(document.createElement("br"));
                infoElmnt.appendChild(document.createTextNode("City of birth: " + laureate.bornCity));
            }
            if (laureate.died != "0000-00-00") {
                infoElmnt.appendChild(document.createElement("br"));
                infoElmnt.appendChild(document.createTextNode("Died in:  " + laureate.died));
            }
            if (prize.hasOwnProperty('motivation')) {
                infoElmnt.appendChild(document.createElement("br"));
                infoElmnt.appendChild(document.createTextNode("Motivation: " + prize.motivation));
            }

            for (var i = 0; i < prize.affiliations.length; i++) {
                var nm = prize.affiliations[i].name == undefined ? "" : prize.affiliations[i].name;
                var city = prize.affiliations[i].city == undefined ? "" : prize.affiliations[i].city;
                if (nm != "" && city != "") {
                    infoElmnt.appendChild(document.createElement("br"));
                    infoElmnt.appendChild(document.createTextNode("Affiliation: " + nm + ", " + city));
                }
            };
            if (infoElmnt.textContent && infoElmnt.textContent.length > 0)
                moreElmnt = infoElmnt;
        }
        return moreElmnt;
    };

    function buildPrizeArray(laureateArr, filterObj) {
        var prizeArr = [];
        for (var i = 0; i < laureateArr.length; i++) {
            for (var n = 0; n < laureateArr[i].prizes.length; n++) {
                if (laureateArr[i].prizes[n].year >= filterObj.start &&
                    laureateArr[i].prizes[n].year <= filterObj.end &&
                    (filterObj.category == "" ||
                        filterObj.category == laureateArr[i].prizes[n].category)) {
                    var lPrize = {};
                    lPrize.laureate = laureateArr[i];
                    lPrize.prizeIndex = n;
                    lPrize.year = laureateArr[i].prizes[n].year;
                    lPrize.category = laureateArr[i].prizes[n].category;
                    prizeArr.push(lPrize);
                }
            }
        };
        return prizeArr.sort((a, b) => a.year - b.year);
    }

    function createTH(content) {
        var th = document.createElement("th");
        th.textContent = content;
        return th;
    }

    function buildPrizeTable(prizeArr) {
        var table = document.createElement("table");
        table.setAttribute("class", "resultstable");

        var tHead = table.createTHead();
        var tr = tHead.insertRow(0);

        tr.appendChild(createTH("Year"));
        var thName = tr.appendChild(createTH("Name"));
        thName.setAttribute("class", "resultname");
        tr.appendChild(createTH("Category"));
        tr.appendChild(createTH("Gender"));
        tr.appendChild(createTH("Born in"));
        tr.appendChild(createTH("Details"));

        for (var i = 0; i < prizeArr.length; i++) {
            var tr = table.insertRow(i + 1);
            tr.insertCell(0).textContent = prizeArr[i].year;
            var nm = tr.insertCell(1);
            nm.setAttribute("class", "resultname");
            nm.textContent = prizeArr[i].laureate.firstname + " " +
                prizeArr[i].laureate.surname;
            tr.insertCell(2).textContent = prizeArr[i].category;
            tr.insertCell(3).textContent = prizeArr[i].laureate.gender;
            tr.insertCell(4).textContent = prizeArr[i].laureate.bornCountry;

            var tdMore = tr.insertCell(5);
            var detailEl = document.createElement("details");
            tdMore.appendChild(detailEl);
            var summaryEl = document.createElement("summary");
            detailEl.appendChild(summaryEl);
            var moreDetails = moreInformation(prizeArr[i].laureate.id, prizeArr[i].prizeIndex);
            if (moreDetails instanceof HTMLElement) {
                summaryEl.textContent = "More...";
                detailEl.appendChild(moreDetails);
            } else
                summaryEl.textContent = "N/A";
        }
        return table;
    };

    function filterLaureates(laureateArr, filterObj) {
        laureateArr = laureateArr.filter((laureate) => {
            return filterYear(laureate, filterObj);
        });
        if (filterObj.category != "")
            laureateArr = laureateArr.filter((laureate) => {
                return filterCategory(laureate, filterObj);
            });
        if (filterObj.country != "")
            laureateArr = laureateArr.filter((laureate) => {
                var regex = new RegExp(filterObj.country, 'gi');
                return laureate.hasOwnProperty('bornCountry') &&
                    laureate.bornCountry.match(regex) != null;
            });
        if (filterObj.gender != "") {
            laureateArr = laureateArr.filter(function(laureate) {
                return (filterObj.gender == "m" && laureate.gender == "male") ||
                    (filterObj.gender == "f" && laureate.gender == "female")
            });
        }
        return laureateArr;
    };

    function filterYear(laureate, filterObj) {
        var accept = false;
        for (var n = 0; n < laureate.prizes.length; n++) {
            var y = laureate.prizes[n].year;
            if (y >= filterObj.start && y <= filterObj.end)
                accept = true;
        }
        return accept;
    };

    function filterCategory(laureate, filterObj) {
        var accept = false;
        for (var n = 0; n < laureate.prizes.length; n++) {
            if (laureate.prizes[n].category == filterObj.category)
                accept = true;
        }
        return accept;
    };
}(this))