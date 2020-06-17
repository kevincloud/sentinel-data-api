function addRequiredModule(item) {
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/required-modules/" + provider + "?add=" + item,
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
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/required-modules/" + provider + "?remove=" + item.value,
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
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/approved-instances/" + provider + "?add=" + item,
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
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/approved-instances/" + provider + "?remove=" + item.value
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
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/prohibited-resources/" + provider + "?add=" + item,
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
    var provider = $("input[name='defprovider']:checked").val();
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/list/prohibited-resources/" + provider + "?remove=" + item.value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function addMandatoryTag(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/tags?add=" + item,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function deleteMandatoryTag(item) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/tags?remove=" + item.value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function resetData() {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/reset",
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function updateDefaultProvider(value) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/set-provider?provider=" + value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function updatePreventDelete(value) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/deletion-policy?value=" + value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function updateMaxCost(value) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/max-cost?cost=" + value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function updateEnforceEncryption(value) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/ddb-encryption?enable=" + value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}

function updateNoStarAccess(value) {
    $.ajax({method: "GET",
        url: "http://" + document.location.hostname + ":8080/no-star-access?enable=" + value,
    }).done(function(result) {
        window.location.reload();
    }).fail(function(xhr, status, error) {
        xhr.textStatus = status;
        xhr.errorThrown = error;
        console.log('Error', xhr);
        alert(xhr);
    });
}
