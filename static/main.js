function deleteRequiredModule(item) {
    $.ajax({type: "GET",
        url: "http://localhost:8080/list/required-modules?remove=" + item.value,
        success: function(result) {
            window.location.reload();
        },
        error: function(result) {
            alert(result);
        }
    });
}

function deleteAllowedInstance(item) {
    $.ajax({type: "GET",
        url: "http://localhost:8080/list/allowed-instances?remove=" + item.value,
        success: function(result) {
            window.location.reload();
        },
        error: function(result) {
            alert(result);
        }
    });
}

function deleteProhibitedResource(item) {
    $.ajax({type: "GET",
        url: "http://localhost:8080/list/prohibited-resources?remove=" + item.value,
        success: function(result) {
            window.location.reload();
        },
        error: function(result) {
            alert(result);
        }
    });
}