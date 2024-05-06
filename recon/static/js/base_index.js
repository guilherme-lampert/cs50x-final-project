// Autocomplete search query - Function inspired by the example showed during the 9th CS50 Class - Flask
async function get_countries(input, mode) {

    if (!(mode === true)) {
        mode = false;
    }

    let countries = await fetch('/query/index-search-query-country?s=' + mode + '&c=' + input);
    countries = await countries.json();
    
    return countries;
}

// Includes li tags inside the ul tag
function list_countries (countries) {

    let ul = document.getElementById('index-autocomplete-list');
    ul.innerHTML = '';

    if (!countries.length) {
        return;
    }

    for (let country of countries) {
        
        let li = document.createElement('li');
        li.classList.add('dropdown-item', 'country-item');
        li.setAttribute('id', country.acronym);
        li.innerHTML = country.name;
        
        ul.appendChild(li);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    
    let input = document.getElementById('index-input-country');
    
    // Updates the ul when new input is provided
    input.addEventListener('input', async function() {
        
        let countries = await get_countries(input.value, false);

        list_countries(countries);
        
        let ul = document.getElementById('index-autocomplete-list');
        
        console.log(ul.querySelectorAll('li').length)
        
        if (ul.querySelectorAll('li').length == 0) {
            ul.classList.remove('show');
        }
        else {
            let li_list = document.getElementsByClassName('country-item');

            for (let li of li_list) {
                li.addEventListener('click', async function() {
                    input.value = li.innerHTML;
                    
                    let countries = await get_countries(input);
                    list_countries(countries);
                    
                    ul.classList.remove('show');
                });
            }
            ul.classList.add('show');
        }
    });

    // Modify clicking behaviors. Chat GPT gave me the main insight for this one
    document.addEventListener('click', function(event) {
        var target = event.target;

        var ul = document.getElementById('index-autocomplete-list');
    
        if (!target.closest('#index-input-country') && !target.closest('#index-autocomplete-list')) {
            ul.classList.remove('show');
        }
        else if (target.closest('#index-input-country') && ul.querySelectorAll('li').length > 0) {
            ul.classList.add('show');
        }
    });

    // Modify GET parameters before sending the form. Again, i discovered most of the syntax here using chat GPT and Stack Overflow
    let form = document.getElementById('index-country-form');
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const country = input.value;
        let country_id = await get_countries(country, true);

        console.log(country_id)

        if (Object.keys(country_id).length === 0) {
            country_id = 'none';
        }
        else {
            country_id = country_id.acronym;
        }

        const url = new URL(form.action);
        url.searchParams.set('country', country_id);
        window.location.href = url.toString();
    });
});
