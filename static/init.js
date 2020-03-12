var columns = ['DNN', 'CNN', 'GB'];

//clear / init table with predictions
function clear_table(){
    for (var item in columns){
        for (var i = 0; i < 10; i++){
            element = document.getElementById(columns[item] + i.toString()).querySelector(".progress.position-relative");
            element.querySelector(".progress-bar").setAttribute('style', "width: 0%;");
            element.querySelector(".justify-content-center.d-flex.position-absolute.w-100.text-body.mt-1").textContent = "";
        }
    }
}

//clear canvas
function clear_canvas(){
    canvas = document.getElementById("sketchpad");
    ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

//clear field with preprocessed images
function clear_images(){
    document.getElementById("input").setAttribute('src', 'static/images/cap_background.png');
    document.getElementById("bounded").setAttribute('src', 'static/images/cap_background.png');
    document.getElementById("mnist").setAttribute('src', 'static/images/cap_background.png');
}

//clear output field
function clear_output(){
    document.getElementById("number").textContent = "";
    document.getElementById("looklike").textContent = "";
}

//clear all fields(predicts table, canvas, preprocessing images)
function clearFields(){
    clear_canvas();
    clear_images();
    clear_table();
    clear_output();
}