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