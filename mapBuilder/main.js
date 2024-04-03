const heightMax = 49;
const widthMax = 49;

let dateBtn = new Array(heightMax);

let chosenValue = 2;

function makeGrid(){
    for(let i= 0; i< heightMax;i++){
        dateBtn[i] = new Array(widthMax);
    }

    for(let y = 0; y<heightMax; y++){
        makeRow(y);
        for(let x = 0; x<widthMax; x++){
            dateBtn[y][x] = 1;
            appendRow(y,x);
        }
    }
    return;
}

function makeRow(count){
    let list_new  = document.createElement("ul");
    list_new.classList.add(`list-${count}`)
    let main_list = document.getElementById("main_list");
    main_list.appendChild(document.createElement("br"));
    main_list.appendChild(list_new);
}

function appendRow(row_,colum_){
    let main_list = document.getElementsByClassName(`list-${row_}`)[0];
    let list_btn = document.createElement("li");
    let btn_new = document.createElement("button");
    btn_new.classList.add("std_button");
    btn_new.setAttribute("id",`${row_};${colum_}`)
    btn_new.setAttribute("onclick","change(this.id)")
    list_btn.appendChild(btn_new);
    main_list.appendChild(list_btn);
}

function change(id_new){
    let row_now = id_new.split(";")[0];
    let colum_now = id_new.split(";")[1];
    if(dateBtn[row_now][colum_now] != chosenValue){
        document.getElementById(id_new).style["background-color"] = colorSwitch(chosenValue,true);
        dateBtn[row_now][colum_now] = chosenValue;
    }
    console.log(dateBtn);
}

function changeState(id_in){
    chosenValue = parseInt(id_in[3]);
    document.getElementById("color_chosen_show").style["background-color"] = colorSwitch(chosenValue,false);
}

function colorSwitch(color_value, change_){
    switch(color_value){
        case 1:
            return "#000";
            break;
        case 2:
            return "#fff";
            break;
        case 3:
            return "#00f";
            break;
        case 4:
            return "#0f0";
            break;
        case 5:
            return "#f00";
            break;
        case 6:
            return "#0ff";
            break;
        case 7:
            if(change_ == true){
                setPlayerPos()
            }
            return "#f0f";
            break;
        case 8:
            return "#dad";
            break;
    }
}

function setPlayerPos(){
    for(let y = 0; y<heightMax; y++){
        for(let x = 0; x<widthMax; x++){
            if(dateBtn[x][y] == 7){
                dateBtn[x][y] = 1;
                document.getElementById(`${x};${y}`).style["background-color"] = "#000";
            }
        }
    }
}

function reset(){
    for(let y = 0; y<heightMax; y++){
        for(let x = 0; x<widthMax; x++){
            document.getElementById(`${x};${y}`).style["background-color"] = "#000";
            dateBtn[y][x] = 1;
        }
    }
}

function exporting(){
    let output = "";
    output += String(widthMax) + String("\n");
    output += String(heightMax) + String("\n");
    for(let x = widthMax-1; x >= 0; x--){
        for(let y = 0; y < heightMax; y++){
            output  += `${dateBtn[x][y]},`;
        }
        output += "\n";
        //output = output.substring(0, output.length - 1);
    }
    output = output.substring(0, output.length - 1);
    output = output.substring(0, output.length - 1);
    copyStringToClipboard(output);
    alert("added to clipboard");
}

function copyStringToClipboard (str) {
    var el = document.createElement('textarea');
    el.value = str;
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}