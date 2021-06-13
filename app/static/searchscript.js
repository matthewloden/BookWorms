const api_url = 'https://www.googleapis.com/books/v1/volumes?q=';
const api_key = '&key=AIzaSyBPlm4NB1dn5APzDgnQRse2jX6qXiO1iG4';
var firstSearch = true;

//console.log(userinput);

async function getSearch(){
    var userinput = document.getElementById('searchbarfield').value;
    userinput = userinput.replace(/\s+/g, "").trim();
    //document.getElementById('testing').textContent = api_url + userinput + api_key;
    const response = await fetch(api_url+userinput+api_key);
    const data = await response.json();
    var i;
    
    
    if(firstSearch == false) { //if the user has already made a search, delete the search results
        console.log("deleting searchresults")
        var element = document.getElementById("searchResults");  
        element.parentNode.removeChild(element);

    }

    if(response.status >= 200 && response.status < 400){

        const searchResults = document.createElement('div');
        searchResults.setAttribute('class','searchResults');
        searchResults.setAttribute('id','searchResults');       //create search results area
        var newelement = document.getElementById('searchBox');
        newelement.appendChild(searchResults);

        for(i = 0;i<Math.min(3,data.items.length);i++){     //to display more entries per page, increase the number as the first entry of the min fun
            console.log("within for loop");
            firstSearch = false;

            const card = document.createElement('div');         //structure     searchBox > searchfunction = searchResults > card > img card = text card > h1 = p
            card.setAttribute('class','card');

            const imgcard = document.createElement('div');
            imgcard.setAttribute('class','imgcard')

            const textcard = document.createElement('div');
            textcard.setAttribute('class','textcard');

            const h1 = document.createElement('h1');
            h1.setAttribute('class','h1');
            h1.textContent = data.items[i].volumeInfo.title;//title

            const p = document.createElement('p');
            p.setAttribute('class','p');
            if(data.items[i].volumeInfo.authors != null){ //if there is an author request
                for(var j = 0;j<data.items[i].volumeInfo.authors.length;j++){
                    p.textContent = data.items[i].volumeInfo.authors[j]; //author
                }
                
            }
            
            const pic = document.createElement('img');
            pic.src = data.items[i].volumeInfo.imageLinks.smallThumbnail; //smallest image source
        
            textcard.appendChild(h1);
            textcard.appendChild(p);
            imgcard.appendChild(pic);
            card.appendChild(imgcard);
            card.appendChild(textcard);
            var element = document.getElementById('searchResults');
            element.appendChild(card);
        }
            
    }
    else{
        alert("Error with API request \n Please Contact a Dev");
    }
    
}