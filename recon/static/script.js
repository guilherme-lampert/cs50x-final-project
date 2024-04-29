// inspired by cs50 class


document.addEventListener('DOMContentLoaded', function() {
    
    let input = document.getElementById('index-input-country');
    
    input.addEventListener('input', async function() {
        let response = await fetch('/search-country?q=' + input.value);
        let countries = await response.json();
        let countries_list_items = '';

        for (country of countries) {
            let name = country.name;
            countries_list_items += '<li><a class="dropdown-item country-item" href="#">' + name + '</a></li>';
        }
        document.getElementById('autocomplete-field').innerHTML = countries_list_items;

        if (countries_list_items == '') {
            document.getElementById('autocomplete-field').classList.remove('show');
        }
        else {
            let country_items = document.getElementsByClassName('country-item');

            for (let country_item of country_items) {
                country_item.addEventListener('click', function() {
                    console.log("clicado");
                    input.value = country_item.innerHTML;
                    document.getElementById('autocomplete-field').classList.remove('show');
                });
            }
            document.getElementById('autocomplete-field').classList.add('show');
        }
    });
});