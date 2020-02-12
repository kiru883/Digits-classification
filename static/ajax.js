function saveImg() {
	var canvas = document.getElementById("the_stage");
	var dataURL = canvas.toDataURL('image/jpg');
	$.ajax({
	  type: "POST",
	  url: "/hook",
	  data:{
		imageBase64: dataURL,
		}
	}).done(function(response) {
	  console.log(response)
	});
	
}