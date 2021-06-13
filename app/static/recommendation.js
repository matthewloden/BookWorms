const apiUrl = "https://openlibrary.org/";
const returnjson = ".json";
const returndetails = "?&details=true";
const returnSubjects = "subjects/";
const returnSearch = "search";
const returnByTitle = "?title=";
const returnByAuthor = "?author=";
const numresponses = "?&limit=12"; //testing, the api only returns 12 responses per api request, potentially add offset to get all values needed

const datareturned = [];

async function getRecommendations() {
    //parse the input from the user
    var j = 0;
    var favGenres = [];
    var ele = document.getElementsByClassName('favGenres'); //get serach option
    for(var i = 0; i < ele.length; i++){
        if(ele[i].checked){
            favGenres[j] = ele[i].value;
            j++;
        }
    }
    if(favGenres.length == 0){
        alert("Please select a favorite Genre"); //error handling
        return  0;
    }
    
    const userAge = document.getElementById("userAge").value;
    if(userAge == ""){
        alert("Please enter an age. If you are above 18 this value will not influence your recommendations.");
        return 0;
    }

    var userinput = document.getElementById("lastBookRead").value;
        var bkDataReturned;
        if(userinput == ""){
            alert("Please Enter the last book you read");
            return 0;
        }

        //get data from the page
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //format the rest of the data and send the requests

    //send multiple api requests in a loop. if there is a problem it will probably be in this function
    for(var i = 0; i < favGenres.length;i++){
        //format the api request, hardcoded for the first vlaue for now
    var api_request = apiUrl + returnSubjects + favGenres[i] + returnjson + returndetails + numresponses;

    //console.log(api_request);
    const response = await fetch(api_request , {
        headers : {
        //    'Content-Type' : 'application/json', dont ever uncomment this. this is left as a reminder. fuck stack overflow
            'Accept' : 'application/json'
        }
    });
    const data = await response.json();
    //console.log(data);
    datareturned[i] = data;
    //end api request loop
    }
    for(var i = 0; i  < datareturned.length;i++){
        console.log(datareturned[i]); //output the  data within datareturned
    }

    //should now have data about the genre selection
    //now get data about the book they selected

    
    userinput = userinput.replace(/\s+/g, '+');
    var bkApi_request = apiUrl + returnSearch + returnjson + returnByTitle + userinput;
    console.log(bkApi_request);
    const bkResponse = await fetch(bkApi_request);
    data = await bkResponse.json();
    bkDataReturned = data.docs[0]; //just getting the first value returned, could be an issue later
    console.log(bkDataReturned);
    var bkSubjects = [];

    
    for(var i = 0; i < bkDataReturned.subject.length; i++){
        //get array of subjects from the book
        bkSubjects[i] = bkDataReturned.subject[i];
        //console.log(bkSubjects[i]);       //for bug checking. values now stored inside this variagble kbSubjects. 
                                            //each value in the array is a genre we want to match with the other serach
    }
    

    var genresSubject = {}; //object with values stored in it
    //completed getting data from the book and the genre. stored data in datareturned[].json and bkDataReturned.json
    for(var i = 0; i < datareturned.length;i++){
        for(var j = 0; j < datareturned[i].works.length;j++){
            genresSubject[datareturned[i].works[j].title] = datareturned[i].works[j].subject; //gets the values for each book seen and then places them in a special array called genreSubject[booktitle][genres]
        }
    }   
    //console.table(genresSubject); //display the information gathered
    var recommendedBooks = [];
    var k = 0;
   //genresSubject object , [bookname][genres list]
   var matchingpair = 0;
   //console.table(genresSubject);
   for(const book in genresSubject){
       //console.log(genresSubject[book].length);
       for(var i = 0; i < genresSubject[book].length;i++){
           //console.log(genresSubject[book][i]);
           if(matchingpair == 4){
               break;
           }
           for(var j = 0; j < bkSubjects.length;j++){
            //console.log("comparision: ",bkSubjects[j]," :: ",genresSubject[book][i]);
            if(matchingpair == 4){ //find five matching pairs
                recommendedBooks[k] = book; 
                k++;
                console.log("found a recommendation book");
                break;
            } 
            if(bkSubjects[j] === genresSubject[book][i]){
                matchingpair++;
                console.log("matched Genres: ",bkSubjects[j], " " , genresSubject[book][i]," matchingpair =",matchingpair);
            }
           } 
           
       }
       matchingpair = 0;
       console.log("finished ",genresSubject[book]);
   }
   console.log("All Done")
   //console.table(recommendedBooks);

   shuffle(recommendedBooks);
   console.table(recommendedBooks);

   if(userAge < 18){
       var youngReader = ["Children's fiction","young adult fiction"];
       var readingLevelHigh = ["Reading Level-Grade 12","Reading Level-Grade 11"];
       var readingLevelMedium = ["Reading Level-Grade 10","Reading Level-Grade 9"];
       var readingLevelLow = ["Reading Level-Grade 8","Reading Level-Grade 7"];         //very wip
   }

   window.localStorage.setItem('data',JSON.stringify(datareturned));
   window.localStorage.setItem('recc',JSON.stringify(recommendedBooks));
   //window.location.href = "/recommendations.html"; should work on the server
   //window.location.assign("{{url_for(reccomendations)}}");
}


function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
  }