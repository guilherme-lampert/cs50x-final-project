// Selects all checkboxes of a given class
function select_all (class_name) {
    
    let elements = document.getElementsByClassName(class_name);
    
    for (let element of elements) {
        element.checked = true;
    }
}

// Clears all checkboxes of a given class
function clear_all (class_name) {
    
    let elements = document.getElementsByClassName(class_name);
    
    for (let element of elements) {
        element.checked = false;
    }
}

document.addEventListener('DOMContentLoaded', function() {

    // The functions below register the functions select_all() and clear_all() for buttons in the query index page

    let clear_all_country = document.getElementById('query-index-clear-all-country');
    clear_all_country.addEventListener('click', function() {
        clear_all('country-input');
    });

    let select_all_indicator = document.getElementById('query-index-select-all-indicator');
    select_all_indicator.addEventListener('click', function() {
        select_all('indicator-input');
    });

    let clear_all_indicator = document.getElementById('query-index-clear-all-indicator');
    clear_all_indicator.addEventListener('click', function() {
        clear_all('indicator-input');
    });

    // Modify GET parameters before sending the form. Again, i discovered most of the syntax here using chat GPT and Stack Overflow
    let form = document.getElementById('query-index-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        let countries = document.getElementsByClassName('country-input');
        let countries_checked = [];
        
        for (let country of countries) {

            if (country.checked)
            {
                countries_checked.push(country.value)
            }
        }
        countries_checked = countries_checked.toString();

        let indicators = document.getElementsByClassName('indicator-input');
        let indicators_checked = [];

        for (let indicator of indicators) {

            if (indicator.checked)
            {
                indicators_checked.push(indicator.value)
            }
        }
        indicators_checked = indicators_checked.toString();

        let start_year = document.getElementById('start-year-input').value;
        let end_year = document.getElementById('end-year-input').value;

        const url = new URL(form.action);
        url.searchParams.set('country', countries_checked);
        url.searchParams.set('indicator', indicators_checked);
        url.searchParams.set('start_year', start_year);
        url.searchParams.set('end_year', end_year);
        
        window.location.href = url.toString();
    });

    let country_checkboxes = document.getElementsByName('country');

    function getCountriesChecked() {

        let check_count = 0;
        for (let country of country_checkboxes) {
            if (country.checked) {
                check_count++;
            }
        }
        return check_count;
    }

    country_checkboxes.forEach((country) => {
        country.addEventListener('click', function () {

            let countries_checked = getCountriesChecked();

            console.log(countries_checked);

            if (countries_checked > 5) {
                
                // This was copied from bootstrap docs to activate the toast
                const toast = document.getElementById('liveToast');
                const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
                toastBootstrap.show();

                country.click();
            }
        });
    });
});