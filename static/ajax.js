var refresher;
var json;
var inter = 0;
var update_interval = 500;

//send image into server
function saveImg() {
	var canvas = document.getElementById("sketchpad");
	var dataURL = canvas.toDataURL('image/jpg');
	refresher = window.setInterval(updatePage, update_interval);
	$.ajax({
	  type: "POST",
	  url: "/hook",
	  data:{
		imageBase64: dataURL
		}
	});
}

//dynamic. get image from server before preprocessing
function updatePage() {
    try{
        $.getJSON('/hook', function(data, status) {
            if (status == 'success'){
                place_images(data.images);
                place_predicts(data.predicts);
                window.clearInterval(refresher);
                inter = 0;
            }
        }).fail(function (){
            inter = inter + 1;
            if (inter > 5){
                window.clearInterval(refresher);
                console.log("Time out.");
            }
        });
    }
    catch {}
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









