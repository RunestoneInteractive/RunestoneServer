function validateForm2(form) {
    for(let num of Object.keys(form)){
        if (["newBookIdentifier","baseBook","newGithubRepo","githubUser"].includes(form[num].name)){

            if (form[num].value == "" || form[num].value.indexOf(" ") !== -1 || form[num].value.indexOf("/") > -1) {
                alert(`Error:  Your ${form[num].name} may not contain spaces or /`)
                return false;
            }

            if (!/^([\x30-\x39]|[\x41-\x5A]|[\x61-\x7A]|[_-])*$/.test(form[num].value)) {
                alert(`Error: Your ${form[num].name} can only contain ASCII letters digits and - or _`);
                return false;
            }

        }
    }
    form.action="/runestone/designer/book_edit"
    form.submit()
    return true
}