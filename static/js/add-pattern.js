var nofrows = 10;
var knotColors = [];
var knotTypes = [];
$(document).ready(function(){
addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');
$('#color0 option:eq(6)').attr("selected", "selected");setColor(0);
$('#color1 option:eq(22)').attr("selected", "selected");setColor(1);
$('#color2 option:eq(30)').attr("selected", "selected");setColor(2);
$('#color3 option:eq(34)').attr("selected", "selected");setColor(3);
initDesigner();
drawPattern();
});

function addInput(divColor){
	if (nofstrings == limit)  {
		alert("You have reached the limit of adding " + nofstrings + " inputs");
	}
	else {
		var el = $("<select id='color"+nofstrings+"' name='color"+nofstrings +"' onchange='setColor("+nofstrings+")'>");
		for (i=0;i<=colors.length-1;i++)
		{
			$("<option value='"+colors[i]+"' style='background-color:"+colors[i]+"'>                  </option>").appendTo(el);
		}
		$("#"+divColor).append(el);
		nofstrings++;
	}
}

function removeInput() {
	if(nofstrings>1) {
		element = document.getElementById("color"+(nofstrings-1));
		element.parentNode.removeChild(element);
		nofstrings--;
	}
}

function setColor(i) {
	var selectbox = $('#color'+i);
	selectbox.css("background",''+selectbox.val()+'');
	document.styleSheets[2].insertRule('.str'+i+' {background-color: '+selectbox.val()+'}', 0);
}

function initDesigner() {
	knotColors[0] = [];
	for(var i=0; i<nofstrings;i++) {
		knotColors[0][i] = i;
	}
	for(var i=1; i<nofrows;i++) {
		knotColors[i] = [];
		var even = 0;
		if(i%2==0) {
			even = 1;
			knotColors[i][0] = knotColors[i-1][0];
		} else if(nofstrings%2==1){
			
		}
		for(var j=0; j<parseInt(nofstrings/2); j++){
			knotColors[i][2*j+even] = knotColors[i-1][2*j+1+even];
			if(2*j+1+even<nofstrings) {
				knotColors[i][2*j+1+even] = knotColors[i-1][2*j+even];
			}
		}
		if(even && nofstrings%2==0) {
			knotColors[i][nofstrings-1] = knotColors[i-1][nofstrings-1];
		} else if(nofstrings%2==1 && !even){
			knotColors[i][nofstrings-1] = knotColors[i-1][nofstrings-1];
		}
	}
	for(var i=0; i<nofrows;i++) {
		knotTypes[i] = [];
		for(var j=0; j<parseInt(nofstrings/2)-i%2; j++){
			knotTypes[i][j] = 1;
		}
		if(nofstrings%2==1 && i%2==1) {
			knotTypes[i][knotTypes[i].length] = 1;
		}
	}
}

function drawPattern() {
	for (var i=0; i<nofrows-1;i++) {
		var cl = "odd";
		if(i%2==0) {
			cl = "even";
		}
		$('<div id="row'+i+'" class="'+cl+'" />').appendTo('#pattern-designer');
		$('<div id="column'+i+'" class="column-'+cl+'" />').appendTo('#pattern-thumb');
		for(var j=0; j<knotTypes[i].length; j++) {
			if(knotTypes[i][j]<3) {
				$('<span class="str'+knotColors[i][2*j+i%2]+' knot knot'+knotTypes[i][j]+'"></span>').appendTo('#row'+i);
				$('<span class="str'+knotColors[i][knotTypes[i].length-1-(2*j+i%2)]+' knot-thumb"></span>').appendTo('#column'+i);
			}
		}
	}
}






