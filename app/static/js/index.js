let countrySearch = document.getElementById('search_button');
let countryAdd = document.getElementById('submit_form_button');
let tableCard = document.getElementsByClassName('table_card');

countrySearch.addEventListener('click', searchCountry);
// tableCard.addEventListener('click', function(){tableCard.classList.toggle('is-visible');
// tableCard.classList.toggle('is-invisible')} );

countryAdd.addEventListener('click', addCountry);

function addCountry(e){
    submitButton = document.getElementById('submit_form_button_id')
    submitButton.addEventListener('click', e => {
    form = document.getElementById('country_form')
    form.submit()
    })
}

function searchCountry(e){
    e.preventDefault();
    const country = document.getElementsByName('name')[0].value;
    const url = `https://restcountries.com/v3.1/name/${country}`;

    fetch(url)
        .then(response => response.json())
        .then(data => displayCountry(data))
        .catch(err => console.error(err))
}

function displayCountry(data){
    let table = document.getElementById('search_country');
    table.classList.add('table-primary', 'p-5')

    table.innerHTML = '';

    if (data.length){
        const thead = document.createElement('thead');
        table.append(thead);
        let tr = document.createElement('tr');
        thead.append(tr);
        const tableHeadings = ['Name', 'Capital', 'Currency', 'Languages', 'Flag', 'Coat of Arms'];
        for (let heading of tableHeadings){
            let th = document.createElement('th');
            th.scope = 'col';
            th.innerText = heading;
            tr.append(th);
        }
    
        for (let field of data){
            let tr = document.createElement('tr');
            table.append(tr);

            const td = document.createElement('td');
            td.innerText = field.name.official
            tr.append(td);
    
            newDataCell(tr, field.capital);
            newDataCell(tr, field.currencies[Object.keys(field.currencies)]['name']);
            newDataCell(tr, field.languages[Object.keys(field.languages)[0]]); 
            newDataCell(tr, `<img src="${field.flags.png}" class="table_img" width="100%">`);
            newDataCell(tr, `<img src="${field.coatOfArms.png}" class="table_img" height="200px">`);
        }
}}

function newDataCell(tr, value){
    let td = document.createElement('td');
    td.innerHTML = value ?? '-';
    tr.append(td);
}
