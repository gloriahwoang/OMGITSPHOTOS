var apigClient = apigClientFactory.newClient();
window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition

function voiceSearch(){
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }
    
    var inputSearchQuery = document.getElementById("search_query");
    const recognition = new window.SpeechRecognition();
    //recognition.continuous = true;

    micButton = document.getElementById("mic_search");  
    
    if (micButton.innerHTML == "mic") {
        recognition.start();
    } else if (micButton.innerHTML == "mic_off"){
        recognition.stop();
    }

    recognition.addEventListener("start", function() {
        micButton.innerHTML = "mic_off";
        console.log("Recording.....");
    });

    recognition.addEventListener("end", function() {
        console.log("Stopping recording.");
        micButton.innerHTML = "mic";
    });

    recognition.addEventListener("result", resultOfSpeechRecognition);
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        transcript = event.results[current][0].transcript;
        inputSearchQuery.value = transcript;
        console.log("transcript : ", transcript)
    }
}




function textSearch() {
    var searchText = document.getElementById('search_query');
    if (!searchText.value) {
        alert('Please enter a valid text or voice input!');
    } else {
        searchText = searchText.value.trim().toLowerCase();
        console.log('Searching Photos....');
        searchPhotos(searchText);
    }
    
}

function searchPhotos(searchText) {

    console.log(searchText);
    document.getElementById('search_query').value = searchText;
    document.getElementById('photos_search_results').innerHTML = "<h4 style=\"text-align:center\">";

    var params = {
        'q' : searchText
        // "Access-Control-Allow-Origin": "*"
    };

    // var additionalParams = {

    //     headers:

    //     {
    //         "Access-Control-Allow-Origin": "*",
    //         "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    //         "Access-Control-Allow-Credentials": true,
    //         "Access-Control-Allow-Headers": "*"
    //     }
    // };
    apigClient.searchGet(params, {} , {})
        .then(function(result) {
            console.log("Result : ", result);

            image_paths = result["data"];
            console.log("image_paths:",image_paths)

            if (image_paths != null) {
                console.log("image_paths : ", image_paths);

                var photosDiv = document.getElementById("photos_search_results");
                photosDiv.innerHTML = "";

                var n;
                for (n = 0; n < image_paths.length; n++) {
                  images_list = image_paths[n].split('/');
                   imageName = images_list[images_list.length - 1];

                    photosDiv.innerHTML += '<figure><img src="' + image_paths[n] + '" style="width:25%"><figcaption>' + imageName + '</figcaption></figure>';
            }
            } else {
                var photosDiv = document.getElementById("photos_search_results");
                photosDiv.innerHTML = "shauyshuadauyd";

            }
            

        }).catch(function(result) {
            var photosDiv = document.getElementById("photos_search_results");
            photosDiv.innerHTML = "No Photo Found";
            console.log(result);
        });
}
var fileExt = null;
function uploadPhoto() {
    var filePath = (document.getElementById('uploaded_file').value).split("\\");
    var fileName = filePath[filePath.length - 1];
    
    if (!document.getElementById('custom_labels').innerText == "") {
        var customLabels = document.getElementById('custom_labels');
    }
    console.log(fileName);
    console.log(custom_labels.value);

    // var reader = new FileReader();
    var file = document.getElementById('uploaded_file').files[0];
    file.constructor = () => file;

    // fileExt = file.name.split(".").pop();
    console.log('File : ', file);
    // document.getElementById('uploaded_file').value = "";

    if ((filePath == "") || (!['png', 'jpg', 'jpeg'].includes(filePath.toString().split(".")[1]))) {
        alert("Please upload a png, jpg, or jpeg file!!!");
    } else {

        var params = {
            "item": file.name,
            "photo": 'asm2',
            "Content-Type": file.type,
            "x-amz-meta-customLabels": custom_labels.value
        };
        var additionalParams = {
            
        };
        apigClient.uploadPhotoItemPut(params, file, additionalParams)
        
    }
}