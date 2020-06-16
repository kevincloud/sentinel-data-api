function addRequiredModule(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/required-modules?add=" + item,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function deleteRequiredModule(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/required-modules?remove=" + item.value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function addApprovedInstance(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/approved-instances?add=" + item,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function deleteApprovedInstance(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/approved-instances?remove=" + item.value
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function addProhibitedResource(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/prohibited-resources?add=" + item,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function deleteProhibitedResource(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/prohibited-resources?remove=" + item.value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}