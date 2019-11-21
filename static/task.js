testForm.onsubmit = function (e) {
    submitBtn.disabled = true;
    e.preventDefault();

    let form = document.getElementById('testForm');
    const formData = new FormData(form);
    setTimeout(function() {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.response)
                submitBtn.disabled = false
            }
        }

        xhr.open(testForm.method, testForm.action, true);
        xhr.send(formData);
    }, (1000));
};
