var nofrows = 10;
var knotColors = [];
var if_white = [];
var knotTypes = [];
	var loaded = false;
$(document).ready(function(){
	addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');addInput('colorsInput');
	$('#color0 option:eq(0)').attr("selected", "selected");setColor(0);
	$('#color1 option:eq(0)').attr("selected", "selected");setColor(1);
	$('#color2 option:eq(0)').attr("selected", "selected");setColor(2);
	$('#color3 option:eq(0)').attr("selected", "selected");setColor(3);
	$('#color4 option:eq(0)').attr("selected", "selected");setColor(4);
	initDesigner();
	drawPattern();
	$('#addbracelet').submit(function() { 
		return submit();
	});
	loaded = true;
});
function addKnotColumnButton(divColor) {
	addInput(divColor);
	addKnotColumn();
}

function removeInput() {
	if(nofstrings>3) {		
		for(var i=(nofstrings%2); i<knotTypes.length;i+=2) {
			knotTypes[i] = knotTypes[i].slice(0, knotTypes[i].length-1);
		}
		element = document.getElementById("color"+(nofstrings-1));
		element.parentNode.removeChild(element);
		nofstrings--;			
		evaluateColors();
		drawPattern();
	}
}

function addRow() {
	knotTypes[nofrows] = [];
	var num = parseInt(nofstrings/2);
	if(nofstrings%2==0 && knotTypes[nofrows-1].length==num) {
		num--;
	}
	for(var i=0; i<num; i++) {
		knotTypes[nofrows][i]=1;
	}
	nofrows++;
	evaluateColors();
	drawPattern();	
}

function removeRow() {
	knotTypes.slice(0, nofrows-1);
	nofrows--;
	evaluateColors();
	drawPattern();	
}
function addInput(divColor){
	if (nofstrings == limit)  {
		alert("You have reached the limit of adding " + nofstrings + " inputs");
	} else {
		var el = $("<select id='color"+nofstrings+"' name='color"+nofstrings +"' onchange='setColor("+nofstrings+")'>");
		for (i=0;i<=colors.length-1;i++)
		{
			$("<option value='"+colors[i]+"' style='background-color:"+colors[i]+"'>                  </option>").appendTo(el);
		}
		$("#"+divColor).append(el);
		$('#color'+nofstrings+' option:eq(0)').attr("selected", "selected");
		setColor(nofstrings);
		nofstrings++;
	}
}

function addKnotColumn() {
	for(var i=(nofstrings%2); i<nofrows; i+=2) {
		knotTypes[i][knotTypes[i].length]=1;
	}
	evaluateColors();
	drawPattern();
}

function setColor(i) {
	var selectbox = $('#color'+i);
	selectbox.css("background",''+selectbox.val()+'');
	document.styleSheets[document.styleSheets.length-1].insertRule('.str'+i+' {background-color: '+selectbox.val()+'}', document.styleSheets[document.styleSheets.length-1].rules.length);
	if(if_white[i]==undefined) {
		if_white[i]= '';
	}
	var x = selectbox.val();
	if((parseInt(x.slice(1,3), 16) + parseInt(x.slice(3,5), 16) + parseInt(x.slice(5,7), 16)) / 3.0<128) {
		if_white[i]= '-white';
	}
	if(loaded) {
		drawPattern();
	}
}

function evaluateColors() {
	knotColors[0] = [];
	for(var i=0; i<nofstrings;i++) {
		knotColors[0][i] = i;
	}
	for(var i=1; i<nofrows;i++) {
		knotColors[i] = [];
		var even = 0;
		var evenstr_evenrow = 0;
		if(i%2==0) {
			even = 1;
			knotColors[i][0] = knotColors[i-1][0];
			if(nofstrings%2==0) {
				evenstr_evenrow = 1;
			}
		}
		for(var j=0; j<parseInt(nofstrings/2)-evenstr_evenrow; j++){
			if(knotTypes[i-1][j]<3) {
				knotColors[i][2*j+even] = knotColors[i-1][2*j+1+even];
				if(2*j+1+even<nofstrings) {
					knotColors[i][2*j+1+even] = knotColors[i-1][2*j+even];
				}
			} else {
				knotColors[i][2*j+even] = knotColors[i-1][2*j+even];
				if(2*j+1+even<nofstrings) {
					knotColors[i][2*j+1+even] = knotColors[i-1][2*j+1+even];
				}
			}
		}
		if(even && nofstrings%2==0) {
			knotColors[i][nofstrings-1] = knotColors[i-1][nofstrings-1];
		} else if(nofstrings%2==1 && !even){
			knotColors[i][nofstrings-1] = knotColors[i-1][nofstrings-1];
		}
	}
}

function initDesigner() {
	for(var i=0; i<nofrows;i++) {
		knotTypes[i] = [];
		for(var j=0; j<parseInt(nofstrings/2)-i%2; j++){
			knotTypes[i][j] = 1;//parseInt(Math.random()*3)+1;
		}
		if(nofstrings%2==1 && i%2==1) {
			knotTypes[i][knotTypes[i].length] = 1;//parseInt(Math.random()*3)+1;
		}
	}
	evaluateColors();
}

function drawPattern() {
	$('#pattern-canvas').empty();
	$('#pattern-thumb').empty();
	$('#pattern-designer').empty();
	for (var i=0; i<nofrows-1;i++) {
		var cl = "odd";
		var cl_thumb = "";
		var directions = [1,0];
		if(i%2==0) {
			cl = "even";
			var directions = [0,1];
			if(nofstrings%2==1) {
				cl_thumb = " column-margin";
			}
		} else if(nofstrings%2==0) {
			cl_thumb = " column-margin";
		}
		
		$('<div id="row-strings'+i+'" />').appendTo('#pattern-canvas');
		for(var j=0; j<knotColors[i].length/2;j++) {
			$('<span class="str'+knotColors[i][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+i);
			if(knotColors[i][2*j+1] != undefined) {
				$('<span class="str'+knotColors[i][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+i);
			}
		}
		
		$('<div id="row'+i+'" class="'+cl+'" />').appendTo('#pattern-designer');
		$('<div id="column'+i+'" class="column-'+cl+cl_thumb+'" />').appendTo('#pattern-thumb');
		var minus = 0;
		if(nofstrings%2==0 && (i)%2==1) {
			minus=1; //if number of strings is even and row is odd draw one knot less
		}
		for(var j=0; j<parseInt(knotColors[i].length/2)-minus; j++) {
			var move = 0;
			if(knotTypes[i][j]%2==0) {
				move = 1;
			}
			$('<span class="str'+knotColors[i][2*j+i%2+move]+' knot knot'+knotTypes[i][j]+if_white[knotColors[i][2*j+i%2+move]]+'" onclick="changeType(this, '+i+','+j+')"></span>').appendTo('#row'+i);
		}
		for(var j=parseInt(knotColors[i].length/2)-minus-1; j>=0; j--) {
			var move = 0;
			if(knotTypes[i][j]%2==0) {
				move = 1;
			}
			$('<span class="str'+knotColors[i][2*j+i%2+move]+' knot-thumb"></span>').appendTo('#column'+i);
		}
	}
	var i = nofrows-1;
	var directions = [1,0];
	if(i%2==0) {
		var directions = [0,1];
	}
	$('<div id="row-strings'+i+'" />').appendTo('#pattern-canvas');
	for(var j=0; j<knotColors[i].length/2;j++) {
		$('<span class="str'+knotColors[i][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+i);
		if(knotColors[i][2*j+1] != undefined) {
			$('<span class="str'+knotColors[i][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+i);
		}
	}
}

function changeType(obj, i, j) {
	var prevType = knotTypes[i][j];
	$(obj).removeClass('knot'+prevType);
	
	knotTypes[i][j]=(prevType%4+1);
	$(obj).addClass('knot'+knotTypes[i][j]);
	
	evaluateColors();
	drawPattern();
}

function submit() {
	var rows = $('#pattern-designer').children();
	var str = '';
	for(var i=0; i<rows.length; i++) {
		var knots = $(rows[i]).children();
		for(var j=0; j<knots.length; j++) {
			var cls = $(knots[j]).attr('class').split(/\s+/)[2].slice(4,5);
			str += cls+" ";
		}
	}
	$('#pattern-string').text(str);
	return true;
}
