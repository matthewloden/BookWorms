const api_url = 'https://www.googleapis.com/books/v1/volumes?q=';
const api_key = '&key=AIzaSyBPlm4NB1dn5APzDgnQRse2jX6qXiO1iG4';
var firstSearch = true;
var modifier;
var api_request;

var input = document.getElementById('searchbarfield'); //this function is just chekcing to see if the user pressed the enter key 
input.addEventListener("keyup",function(event) {
    if(event.keyCode === 13) {
        event.preventDefault();
        document.getElementById('mybtn').click();
    }
});


async function getSearch(){

    //parse input
    var userinput = document.getElementById('searchbarfield').value;
    if(userinput == ""){
        alert("Error: Please enter a value into the searchbar");
    }
    userinput = userinput.replace(/\s+/g, "+").trim(); //change to allow + instead of 

    var ele = document.getElementsByName('option'); //get serach option
    for(var i = 0; i < ele.length; i++){
        if(ele[i].checked){
            modifier = ele[i].value;
        }
    }

    //get  language option
    var e = document.getElementById('languagefilter');
    var strUser = e.value;
    var langrest = "&langRestrict=";
    var langmod = langrest+strUser;
    console.log(strUser);

    if(strUser != "na"){
        api_request = api_url+userinput+modifier+langmod+api_key;
    }
    else{
        api_request = api_url+userinput+modifier+api_key;
    }

    //send api request
    console.log(api_request);
    const response = await fetch(api_request);
    const data = await response.json();


    //if the user has already made a search, delete the search results
    if(firstSearch == false) { 
        console.log("deleting searchresults")
        var element = document.getElementById("searchResults");  
        element.parentNode.removeChild(element);
    }

    if(response.status >= 200 && response.status < 400){

        const searchResults = document.createElement('div');
        searchResults.setAttribute('class','searchResults');
        searchResults.setAttribute('id','searchResults');       //create search results area
        var newelement = document.getElementById('bodycard');
        newelement.appendChild(searchResults);

        for(i = 0;i<Math.min(10,data.items.length);i++){     //to display more entries per page, increase the number as the first entry of the min fun
            console.log("starting formatting of api request");
            firstSearch = false;

            const card = document.createElement('div');         //structure     bodycard > searchfunction = searchResults > card > img card = text card > h2 = p
            card.setAttribute('class','card');

            const imgcard = document.createElement('div');
            imgcard.setAttribute('class','imgcard')

            const textcard = document.createElement('div');
            textcard.setAttribute('class','textcard');

            const h2 = document.createElement('h2');
            h2.setAttribute('class','h2');
            h2.textContent = data.items[i].volumeInfo.title;//title
            const a = document.createElement('a');
            a.setAttribute('class','a');
            a.textContent = h2.textContent;
            a.href = data.items[i].volumeInfo.infoLink;

            const p = document.createElement('p');
            p.setAttribute('class','p');
            var temp = ", ";
            var temp1 = "";
            if(data.items[i].volumeInfo.authors != null){ //if there is an author request, get more than one author
                for(var j = 0;j<data.items[i].volumeInfo.authors.length;j++){
                    authornames = data.items[i].volumeInfo.authors[j];
                    temp1 += authornames + temp;
                }
                temp1 = temp1.substring(0, temp1.length - 2);
                var temp2 = "Author: ";
                p.textContent = temp2 + temp1;
            }

            //create description information
            const p1 = document.createElement('p');
            p1.setAttribute('class','p');
            p1.textContent = "Description: ";
            p1.textContent += data.items[i].volumeInfo.description;
            
            const pic = document.createElement('img');
            pic.src = data.items[i].volumeInfo.imageLinks.thumbnail; //smallest image source fails sometimes, craetre if else statement
        
            textcard.appendChild(a);
            textcard.appendChild(p);
            textcard.appendChild(p1);
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