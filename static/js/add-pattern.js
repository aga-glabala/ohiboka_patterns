var nofrows = 10;
var nofcols = 5;
var knotColors = [];
var if_white = [];
var knotTypes = [];
var loaded = false;
var nofstrings = 0;
var limit = 30;
var knottype = 1;
var clickedColorChooser = undefined;
var chosedColor = '';
$(document).ready(function(){	
	initDesigner();
	$('#addbracelet').submit(function() { 
		return submit();
	});
	loaded = true;
	$('.dropdown-toggle').dropdown()
	
	var stickyBox = $("#floating-top");
	var stickyBoxPosition = stickyBox.offset().top;
	stickyBox.css('position', 'relative');
	
	$(window).scroll(function(){
		if(stickyBoxPosition < $(window).scrollTop()) {
			stickyBox.stop().animate({
				"top": ($(window).scrollTop() - stickyBoxPosition) + "px"
			}, "fast" );
		} else {
			stickyBox.css('top', 0);
		}
	});
	
	$('.dropdown-menu a').click(function(e) {
		e.preventDefault()
		changeBraceletType($(this));
	});
	
	$('#generate-template-button').click(generateTemplate);	
	$('.modal-body a').click(function(e) {
		e.preventDefault()
		setTempColor($(this).data('color'));
	});
	
	//$('.color-chooser-cancel').click(function(e) {
		
	//});
	
	$('#color-chooser-ok').click(function(e) {
		e.preventDefault();
		setColor();
		$('#color-chooser').modal('hide');
	});
	
	$('#color-chooser').on('hidden', function () {
	  	//e.preventDefault()
		setTempColor(clickedColorChooser.data('color'));
		$('#color-chooser').modal('hide');
	});

	Mousetrap.bind('left', function(e) {
		var sel = $('.current').prev();
		if (sel != undefined && sel.length > 0) {
			$('.current').removeClass('current');
			sel.addClass('current');
		} else {
			var col = $('.current').index();
			var last = $('.current').parent().children().length - 1 == col;
			var row = $('.current').parent().index();
			if (row > 0) {
				$('.current').removeClass('current');
				$('#row'+(row-1)+' > span:last-child').addClass('current');
			}
		}
		return false;
	});
	Mousetrap.bind('right', function(e) { 
		var sel = $('.current').next();
		if (sel != undefined && sel.length > 0) {
			$('.current').removeClass('current');
			sel.addClass('current');
		} else {
			var col = $('.current').index();
			var last = $('.current').parent().children().length - 1 == col;
			var row = $('.current').parent().index();
			if (row + 1 < $('.current').parent().parent().children().length) {
				$('.current').removeClass('current');
				$('#row'+(row+1)+' > span:first-child').addClass('current');
			}
		}
		return false;
	});
	Mousetrap.bind('up', function(e) { 
		var col = $('.current').index();
		var last = $('.current').parent().children().length - 1 == col;
		var row = $('.current').parent().index();
		if (row > 0) {
			$('.current').removeClass('current');
			if (last) {
				$('#row'+(row-1)+' > span:last-child').addClass('current');
			} else {
				$('#row'+(row-1)+' > span:nth-child('+(col+1)+')').addClass('current');
			}
		}
		return false;
	});
	Mousetrap.bind('down', function(e) { 
		var col = $('.current').index();
		var last = $('.current').parent().children().length - 1 == col;
		var row = $('.current').parent().index();
		var rowCount = $('.current').parent().index();
		if (row + 1 < $('.current').parent().parent().children().length) {
			$('.current').removeClass('current');
			if (last) {
				$('#row'+(row+1)+' > span:last-child').addClass('current');
			} else {
				$('#row'+(row+1)+' > span:nth-child('+(col+1)+')').addClass('current');
			}
		}
		return false;
	});
	Mousetrap.bind(['1', '2', '3', '4', 'space'], function(e) {
		changeType($('.current'), $('.current').parent().index(), $('.current').index(), e.keyCode == 32 ? undefined : e.keyCode - 48);
		return false;
	});
	Mousetrap.bind(['.', '>'], function(e) {
		addKnotColumnButton('colorsInput');
		return false;
	});
	Mousetrap.bind([',', '<'], function(e) {
		removeInput();
		return false;
	});
	Mousetrap.bind('del', function(e) {
		removeRow();
		return false;
	});
	Mousetrap.bind('ins', function(e) {
		addRow();
		return false;
	});
	Mousetrap.bind('home', function(e) {
		$('.current').removeClass('current');
		$('#row0 > span:first-child').addClass('current');
		return true;
	});
	Mousetrap.bind('end', function(e) {
		$('.current').removeClass('current');
		$('#pattern-designer > div:last-child > span:last-child').addClass('current');
		return true;
	});
});

function generateTemplate() {
	nofrows = parseInt($('#generate-form-rows').val());
	nofcols = parseInt($('#generate-form-columns').val());
	
	knottype = $('#generate-form-knots').val();
	var els = $('span[class*="icon-knot"]');
	els.removeClass();
	els.addClass('icon-knot'+knottype);
	initDesigner();
}

function changeBraceletType(aElement) {
	knottype = aElement.data('knot-type');
	var els = $('span[class*="icon-knot"]');
	els.removeClass();
	els.addClass('icon-knot'+knottype);
}

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
	
	var kt = knottype;
	if(kt == 5) {
		kt = knotTypes[nofrows-1][0];
		if(kt==3) {
			kt=4;
		} else {
			kt=3;
		}
	}
	
	for(var i=0; i<num; i++) {
		knotTypes[nofrows][i]=kt;
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
		var el = $("<a class='btn color-chooser-button' id='color"+nofstrings+"' name='color"+nofstrings +"' href='#color-chooser'>"); 
		el.click(function(e) {
			e.preventDefault();
			clickedColorChooser = $(this);
			$('#color-chooser').modal();
		});
		$("#"+divColor).append(el);
		$('#color'+nofstrings+' option:eq(0)').attr("selected", "selected");
		//setColor(nofstrings);
		nofstrings++;
		clickedColorChooser = el;
		setTempColor('#ffffff');
		setColor('#ffffff');
		clickedColorChooser = undefined;
	}
}

function addKnotColumn() {
	for(var i=(nofstrings%2); i<nofrows; i+=2) {
		var kt = knottype;
		if(kt == 5) {
			kt = knotTypes[i][knotTypes[i].length-1];
		}
		knotTypes[i][knotTypes[i].length]=kt;
	}
	evaluateColors();
	drawPattern();
}

function setTempColor(color) {
	//var selectbox = $('#color'+i);
	//selectbox.css("background",''+selectbox.val()+'');
	var i = clickedColorChooser.attr('id').slice(5,6);
	var x = color;
	chosedColor = color;
	document.styleSheets[document.styleSheets.length-1].insertRule('.str'+i+' {background-color: '+x+'}', document.styleSheets[document.styleSheets.length-1].rules.length);
	if((parseInt(x.slice(1,3), 16) + parseInt(x.slice(3,5), 16) + parseInt(x.slice(5,7), 16)) / 3.0<128) {
		if_white[i]= '-white';
	} else {
		if_white[i]= '';
	}
	if(loaded) {
		drawPattern();
	}
}

function setColor() {
	prevColor = '';
	clickedColorChooser.css('background', chosedColor);
	clickedColorChooser.data('color', chosedColor);
}

function evaluateColors() {
	knotColors[0] = [];
	for(var i=0; i<nofstrings;i++) {
		knotColors[0][i] = i;
	}
	for(var i=1; i<nofrows+1;i++) {
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
	knotColors = [];
	if_white = [];
	knotTypes = [];
	nofstrings = 0;
	$('#pattern-canvas').empty();
	$('#pattern-thumb').empty();
	$('#pattern-designer').empty();
	$('#colorsInput').empty();
	loaded = false;
	for(var i=0; i<nofcols; i++) {
		addInput('colorsInput');
		$('#color'+i+' option:eq(0)').attr("selected", "selected");
	}
	var kt = knottype;
	for(var i=0; i<nofrows;i++) {
		knotTypes[i] = [];
		if(knottype==5 && knotTypes[i-1]!=undefined) {
			kt=knotTypes[i-1][0];
			if(kt==3) {
				kt=4;
			} else {
				kt=3;
			}
		} else if(knottype==5 && i==0) {
			kt=3;
		}
		for(var j=0; j<parseInt(nofstrings/2)-i%2; j++){
			knotTypes[i][j] = kt;
		}
		if(nofstrings%2==1 && i%2==1) {
			knotTypes[i][knotTypes[i].length] = kt;
		}
	}
	loaded = true;
	evaluateColors();
	drawPattern();
}

function drawPattern() {
	var col = 0;
	var row = 0;
	if ($('.current').length > 0) {
		col = $('.current').index();
		row = $('.current').parent().index();
	}
	$('#pattern-canvas').empty();
	$('#pattern-thumb').empty();
	$('#pattern-designer').empty();
	for (var i=0; i<nofrows;i++) {
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
	var i = nofrows;
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
	$('#row'+(row)+' > span:nth-child('+(col+1)+')').addClass('current');
}

function changeType(obj, i, j, newType) {
	var prevType = knotTypes[i][j];
	$(obj).removeClass('knot'+prevType);
	
	if (newType == undefined) {
		newType = prevType%4+1;
	}
	knotTypes[i][j]=newType;
	$(obj).addClass('knot'+knotTypes[i][j]);

	$('.current').removeClass('current');
	$('#row'+i+' > span:nth-child('+(j+1)+')').addClass('current');
	
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
	
	var colors = $('#colorsInput').children();
	str = '';
	for(var i=0; i<colors.length; i++) {
		str+=$(colors[i]).data('color')+' ';
	}
	$('#pattern-colors').text(str);
	return true;
}
