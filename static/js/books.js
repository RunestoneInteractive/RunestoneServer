//This is the JavaScript function of the search bar of the library

function search_book() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('book_title');
    let y = document.getElementsByClassName('book_descript');

    for (i = 0; i < x.length; i++) {
        if ((x[i].innerHTML.toLowerCase().includes(input)) || (y[i].innerHTML.toLowerCase().includes(input))) {
            x[i].style.display="list-item";
            y[i].style.display="list-item";
        }
        else {
            x[i].style.display="none";  
            y[i].style.display="none";              
        }
    }
}