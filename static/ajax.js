function saveImg() {
	var canvas = document.getElementById("sketchpad");
	var dataURL = canvas.toDataURL('image/jpg');
	$.ajax({
	  type: "POST",
	  url: "/hook",
	  data:{
		imageBase64: dataURL,
		test: "abc"
		}
	})

}