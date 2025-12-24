var jpdbBaseURL = "http://api.login2explore.com:5577";
var jpdbIRL = "/api/irl";
var jpdbIML = "/api/iml";
var stuDBName = "SCHOOL-DB";
var stuRelName = "STUDENT-TABLE";
var connToken = "90934834|-31949265161826839|90957882";

$("#rollNo").focus();
function executeCommand(reqString, dbBaseUrl, apiEndPointUrl) {
    var url = dbBaseUrl + apiEndPointUrl;
    var jsonObj;
    $.post(url, reqString, function (result) {
        jsonObj = JSON.parse(result);
    }).fail(function (result) {
        var dataJsonObj = result.responseText;
        jsonObj = JSON.parse(dataJsonObj);
    });
    return jsonObj;
}

function createGET_BY_KEYRequest(token, dbn, rel, jsonStr) {
    var getRequest = "{\n"
            + "\"token\" : \"" + token + "\",\n"
            + "\"dbName\" : \"" + dbn + "\",\n"
            + "\"rel\" : \"" + rel + "\",\n"
            + "\"jsonStr\" : " + jsonStr + "\n"
            + "}";
    return getRequest;
}
function saveRecNo2LS(jsonObj) {
    var lvData = JSON.parse(jsonObj.data);
    localStorage.setItem("recno", lvData.rec_no);
}

function getStudentIdAsJsonObj() {
    var rollNo = $("#rollNo").val();
    var jsonStr = { Roll_No: rollNo };
    return JSON.stringify(jsonStr);
}

function fillData(jsonObj) {
    saveRecNo2LS(jsonObj);
    var record = JSON.parse(jsonObj.data).record;
    $("#fullName").val(record.Full_Name);
    $("#stuClass").val(record.Class);
    $("#birthDate").val(record.Birth_Date);
    $("#address").val(record.Address);
    $("#enrollDate").val(record.Enrollment_Date);
}

function resetForm() {
    $("#rollNo").val("");
    $("#fullName").val("");
    $("#stuClass").val("");
    $("#birthDate").val("");
    $("#address").val("");
    $("#enrollDate").val("");
    $("#rollNo").prop("disabled", false);
    $("#save").prop("disabled", true);
    $("#update").prop("disabled", true);
    $("#reset").prop("disabled", true);
    $("#rollNo").focus();
}

function validateData() {
    var rollNo, fullName, stuClass, birthDate, address, enrollDate;
    rollNo = $("#rollNo").val();
    fullName = $("#fullName").val();
    stuClass = $("#stuClass").val();
    birthDate = $("#birthDate").val();
    address = $("#address").val();
    enrollDate = $("#enrollDate").val();

    if (rollNo === "" || fullName === "" || stuClass === "" || 
        birthDate === "" || address === "" || enrollDate === "") {
        alert("All fields are required");
        return "";
    }
    
    var jsonStrObj = {
        Roll_No: rollNo,
        Full_Name: fullName,
        Class: stuClass,
        Birth_Date: birthDate,
        Address: address,
        Enrollment_Date: enrollDate
    };
    return JSON.stringify(jsonStrObj);
}

function getStudent() {
    var rollNoVar = $("#rollNo").val();
    if (rollNoVar === "") {
        alert("Roll No is required");
        $("#rollNo").focus();
        return "";
    }
    var getRequest = createGET_BY_KEYRequest(connToken, stuDBName, stuRelName, JSON.stringify({Roll_No: rollNoVar}));
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommand(getRequest, jpdbBaseURL, jpdbIRL);
    jQuery.ajaxSetup({async: true});

    if (resJsonObj.status === 400) { // Record not found
        $("#save").prop("disabled", false);
        $("#reset").prop("disabled", false);
        enableFields();
        $("#fullName").focus();
    } else if (resJsonObj.status === 200) { // Record found
        $("#rollNo").prop("disabled", true);
        fillData(resJsonObj);
        $("#update").prop("disabled", false);
        $("#reset").prop("disabled", false);
        enableFields();
        $("#fullName").focus();
    }
}

function enableFields() {
    $("#fullName").prop("disabled", false);
    $("#class").prop("disabled", false);
    $("#birthDate").prop("disabled", false);
    $("#address").prop("disabled", false);
    $("#enrollDate").prop("disabled", false);
}

function createPUTRequest(token, jsonStr, dbName, rel) {
    var putRequest = "{\n"
            + "\"token\" : \"" + token + "\",\n"
            + "\"dbName\" : \"" + dbName + "\",\n"
            + "\"cmd\" : \"PUT\",\n"
            + "\"rel\" : \"" + rel + "\",\n"
            + "\"jsonStr\" : " + jsonStr + "\n"
            + "}";
    return putRequest;
}

function executeCommandAtNoForm(reqString, dbBaseUrl, apiEndPointUrl) {
    var url = dbBaseUrl + apiEndPointUrl;
    var jsonObj;
    $.post(url, reqString, function (result) {
        jsonObj = JSON.parse(result);
    }).fail(function (result) {
        var dataJsonObj = result.responseText;
        jsonObj = JSON.parse(dataJsonObj);
    });
    return jsonObj;
}

function createUPDATERequest(token, jsonStr, dbName, rel, rec_no) {
    var updateRequest = "{\n"
            + "\"token\" : \"" + token + "\",\n"
            + "\"dbName\" : \"" + dbName + "\",\n"
            + "\"cmd\" : \"UPDATE\",\n"
            + "\"rel\" : \"" + rel + "\",\n"
            + "\"jsonStr\" : " + jsonStr + ",\n"
            + "\"record\" : { \"rec_no\" : " + rec_no + " }\n"
            + "}";
    return updateRequest;
}

function saveData() {
    var jsonStrObj = validateData();
    if (jsonStrObj === "") return;
    var putRequest = createPUTRequest(connToken, jsonStrObj, stuDBName, stuRelName);
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtNoForm(putRequest, jpdbBaseURL, jpdbIML);
    jQuery.ajaxSetup({async: true});
    resetForm();
}

function updateData() {
    $("#update").prop("disabled", true);
    var jsonChg = validateData();
    var updateRequest = createUPDATERequest(connToken, jsonChg, stuDBName, stuRelName, localStorage.getItem("recno"));
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtNoForm(updateRequest, jpdbBaseURL, jpdbIML);
    jQuery.ajaxSetup({async: true});
    console.log(resJsonObj);
    resetForm();
}