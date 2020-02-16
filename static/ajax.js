var refresher;
var json;
var inter = 0;

//send image into server
function saveImg() {
	var canvas = document.getElementById("sketchpad");
	var dataURL = canvas.toDataURL('image/jpg');
	refresher = window.setInterval(updatePage, 3600);
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









