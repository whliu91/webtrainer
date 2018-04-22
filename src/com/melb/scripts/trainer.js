/**
* Author: lucy
* Target: trainer.html
* Purpose: This file is for the java script of a html file
* Created: 22/04/2018
* Last updated: 
* Credits: 
*/

"use strict";

function add(){
	var total_text=document.getElementsByClassName("number");
	var number=document.getElementById("number").value;
	total_text=total_text.length+1;
	var str = "";
	for (var i=0; i<number; i++){
		str += "<p><input type='text' class='input_text' id='input_text"+"' placeholder='Enter Text'></p>";
	} 
	document.getElementById("textarea").innerHTML=str;
}

/*function init(){
	var click = document.getElementById("click");
	click.onclick = add;
}

window.onload = init;*/