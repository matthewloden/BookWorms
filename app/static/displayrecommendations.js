
async function displayrecommendations() {
    //const myvalue = localStorage["key"];
    const myvalue = window.localStorage.getItem('recc');
    const mydata = window.localStorage.getItem('data');
    console.table(myvalue);
    console.log(mydata);
    var res = myvalue.split(",");
    for(var i = 0; i < res.length;i++){
        res[i] = res[i].replace(/[\[\]']+/g,'');
        res[i] = res[i].slice(1,-1);
    }
    console.table(res);

    console.log(res.length);
    const searchResults = document.createElement('div');
    searchResults.setAttribute('class','searchResults');
    searchResults.setAttribute('id','searchResults');       //create search results area
    var newelement = document.getElementById('bodycard');
    newelement.appendChild(searchResults);
    for(var i = 0; i < res.length;i++){
        
        const card = document.createElement('div');         //structure     bodycard > searchfunction = searchResults > card > img card = text card > h2 = p
        card.setAttribute('class','card');

        const imgcard = document.createElement('div');
        imgcard.setAttribute('class','imgcard')

        const textcard = document.createElement('div');
        textcard.setAttribute('class','textcard');

        const h1 = document.createElement('h1');
        h1.setAttribute('class','h1');
        h1.textContent = res[i];

        
        textcard.appendChild(h1);
        card.appendChild(textcard);
        var element = document.getElementById('searchResults');
        element.appendChild(card);
    }
    
}