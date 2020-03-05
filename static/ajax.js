//send image into server
function saveImg() {
    document.getElementById("clearButton").disabled = true;
	var canvas = document.getElementById("sketchpad");
	var dataURL = canvas.toDataURL('image/jpg');
	//refresher = window.setInterval(updatePage, update_interval);
	$.ajax({
	  type: "POST",
	  url: "/hook",
	  data:{
		imageBase64: dataURL
		},
	  success: function success(data){
	    if (data.success_compute){
	        document.getElementById("clearButton").disabled = false;
            place_images(data.images);
            place_predicts(data.predicts);
            place_number(data.ensamble);
	    }
	  }
	});
}


//place images
function place_images(data_images){
    //input image
    document.getElementById('input')
        .setAttribute(
            'src', 'data:image/png;base64,' + data_images.input_image
        );
    //bounded digit image
    document.getElementById('bounded')
        .setAttribute(
            'src', 'data:image/png;base64,' + data_images.bounded_digit
        );
    //mnist image
    document.getElementById('mnist')
        .setAttribute(
            'src', 'data:image/png;base64,' + data_images.mnist_image
        );
}

//place predicts
function place_predicts(data_predicts){
    for (var item in data_predicts){
        max_prob = Math.max.apply(Math, data_predicts[item]) * 100;

        for (var i = 0; i < 10; i++){
            proc_prob = data_predicts[item][i] * 100;
            element = document.getElementById(item + i.toString()).querySelector(".progress.position-relative");

            element.querySelector(".justify-content-center.d-flex.position-absolute.w-100.text-body.mt-1").textContent = parseInt(proc_prob*100)/100 + "%";

            if (proc_prob == max_prob){
                element.querySelector(".progress-bar").setAttribute('style', "width: " + Math.round(proc_prob) + "%; background: green;");
            }
            else{
                element.querySelector(".progress-bar").setAttribute('style', "width: " + Math.round(proc_prob) + "%;");
            }
        }
    }
}

function place_number(data_ensamble){
    //number
    document.getElementById("number").textContent = data_ensamble.number;
    //probability
    document.getElementById("probability").textContent = parseInt(data_ensamble.probability*10000)/100 + "%";
}







