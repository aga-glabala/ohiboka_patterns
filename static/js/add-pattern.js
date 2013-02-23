var strings = [];
var nofcols = 5;
var knottype = 1;
var loaded = false;
var limit = 30;
var clickedColorChooser = undefined;
var chosedColor = '';
$(document).ready(function(){
	knottype = braceletType == 1 ? 1 : 5;
	if (bracelet_id != undefined) {
		createPattern();
	} else {
		initDesigner();
	}
	$('#addbracelet').submit(function() { 
		return submit();
	});
	loaded = true;
	$('.dropdown-toggle').dropdown();
	
	$('.dropdown-menu a').click(function(e) {
		e.preventDefault()
		changeBraceletType($(this));
	});
	
	$('#generate-template-button').click(generateTemplate);	
	$('#color-chooser .modal-body a').click(function(e) {
		e.preventDefault();
		setTempColor($(this).data('color'));
	});
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
	
	$('#generate-form-insert-char').click(function(e) {
		e.preventDefault();
		clickedColorChooser = $(this);
		$('#character-chooser').modal();
	});
	$('#character-chooser .modal-body a').click(function(e) {
		e.preventDefault();
		$('#generate-form-text').val($('#generate-form-text').val()+$(e.target).data('character'));
		$('#character-chooser').modal('hide');
	});
	$('#character-chooser').on('hidden', function () {
		$('#character-chooser').modal('hide');
	});
	
	if (braceletType == 2) {
	$('input[name=generate-form-kind]').change(function() {
		var checked = $('input[name=generate-form-kind]:checked').val();
		if (checked == 'text') {
			$('.kind-empty').hide();
			$('.kind-text').show();
		} else {
			$('.kind-empty').show();
			$('.kind-text').hide();
		}
	}).change();
	}

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
		
	$(window).scroll(function(){
		var stickyBox = $("#floating-top");
		stickyBox.css('position', 'relative');
		var stickyBoxPosition = $("#pattern-tool-anchor").offset().top;
		if(stickyBoxPosition < $(window).scrollTop()) {
			stickyBox.stop().animate({
				"top": ($(window).scrollTop() - stickyBoxPosition - 10) + "px"
			}, "fast" );
		} else {
			stickyBox.css('top', 0);
		}
	});
});

function createPattern() {
	$('#colorsInput').empty();
	loaded = false;
	var nofstrTemp = nofstr;
	nofstr = 0;
	for(var i=0; i<nofstrTemp; i++) {
		addInput('colorsInput');
		$('#color'+i+' option:eq(0)').attr("selected", "selected"); //TODO: is this used?
	}
	loaded = true;
	evaluateColors();
	$('#colorsInput .color-chooser-button').each(function(i, el) {
		clickedColorChooser = $(el);
		setTempColor(stringColors[i]);
		setColor(stringColors[i]);
		clickedColorChooser = undefined;
	});
	drawPattern();
}

function generateTemplate() {
	function setLoader(isLoading) {
		if (isLoading) {
			$("#generate-template-button").attr("disabled", "disabled");
		} else {
			$("#generate-template-button").removeAttr("disabled");
		}
	}
	
	setLoader(true);
	var checked = $('input[name=generate-form-kind]:checked').val();
	if (braceletType == 1 || checked != 'text') {
		nofrows = parseInt($('#generate-form-rows').val());
		nofcols = parseInt($('#generate-form-columns').val());
		if(parseInt(nofcols) > 2 && parseInt(nofcols)<30 && parseInt(nofrows) > 2 && parseInt(nofrows)<95) {
			knottype = braceletType == 2 ? 5 : $('#generate-form-knots').val();
			var els = $('span[class*="icon-knot"]');
			els.removeClass();
			els.addClass('icon-knot'+knottype);
			initDesigner();
		} else {
			alert(patternGeneratorError);
		}
		setLoader(false);
	} else if (braceletType == 2) {
		nofcols = parseInt($('input[name=generate-form-letter-height]:checked').val());
		var text = encodeURIComponent($('#generate-form-text').val().split('').join('\f'));
		if (text == undefined || text.length == 0) {
			setLoader(false);
			return;
		}
		$.getJSON("/bracelet/generate/"+text+"/"+nofcols, function(data) {
			if (data == undefined || data.pattern == undefined || data.pattern[0].length == 0) {
				alert(patternTextGeneratorError);
			}
			knotsType = data.pattern;
			nofrows = knotsType.length;
			nofstr = knotsType[0].length+1;
			stringColors = ['#000000'];
			for (var i=0; i<nofcols; i++) {
				stringColors[stringColors.length] = '#ffffff';
			}
			createPattern();
			if (data.error) {
				alert(data.error);
			}
			setLoader(false);
		}).error(function(jqXHR, textStatus, errorThrown) { 
			alert(jqXHR.responseText);
			setLoader(false);
		});
	}
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
	if(nofstr>3) {
		if (braceletType == 1) {
			for(var i=(nofstr%2); i<knotsType.length;i+=2) {
				knotsType[i] = knotsType[i].slice(0, knotsType[i].length-1);
			}
		} else if (braceletType == 2) {
			for(var i=0; i<nofrows; i++) {
				knotsType[i] = knotsType[i].slice(0, knotsType[i].length-1);
			}
		}
		element = document.getElementById("color"+(nofstr-1));
		element.parentNode.removeChild(element);
		nofstr--;			
		evaluateColors();
		drawPattern();
	}
}

function addRow() {
	if(nofrows<95) {
		knotsType[nofrows] = [];
		var num = 0;
		if(braceletType == 1) {
			num = parseInt(nofstr/2);
			if (nofstr%2==0 && knotsType[nofrows-1].length==num) {
				num--;
			}
		} else if (braceletType == 2) {
			num = knotsType[0].length;
		}
		
		var kt = knottype;
		if(braceletType == 1 && kt == 5) {
			kt = knotsType[nofrows-1][0];
			if(kt==3) {
				kt=4;
			} else {
				kt=3;
			}
		}
		
		for(var i=0; i<num; i++) {
			knotsType[nofrows][i]=kt;
		}
		nofrows++;
		evaluateColors();
		drawPattern();	
	}
}

function removeRow() {
	if(nofrows>3) {
		knotsType.slice(0, nofrows-1);
		nofrows--;
		evaluateColors();
		drawPattern();
	}	
}

function addInput(divColor){
	if (nofstr == limit)  {
		alert("You have reached the limit of adding " + nofstr + " inputs");
	} else {
		var el = $("<a class='btn color-chooser-button' id='color"+nofstr+"' name='color"+nofstr +"' href='#color-chooser'>"); 
		el.click(function(e) {
			e.preventDefault();
			clickedColorChooser = $(this);
			$('#color-chooser').modal();
		});
		$("#"+divColor).append(el);
		$('#color'+nofstr+' option:eq(0)').attr("selected", "selected");
		//setColor(nofstr);
		nofstr++;
		clickedColorChooser = el;
		setTempColor('#ffffff');
		setColor('#ffffff');
		clickedColorChooser = undefined;
	}
}

function addKnotColumn() {
	if (braceletType == 1) {
		for(var i=(nofstr%2); i<nofrows; i+=2) {
			var kt = knottype;
			if(kt == 5) {
				kt = knotsType[i][knotsType[i].length-1];
			}
			knotsType[i][knotsType[i].length]=kt;
		}
	} else if (braceletType == 2) {
		for(var i=0; i<nofrows; i++) {
			knotsType[i][knotsType[i].length]=knottype;
		}
	}
	evaluateColors();
	drawPattern();
}

function setTempColor(color) {
	//var selectbox = $('#color'+i);
	//selectbox.css("background",''+selectbox.val()+'');
	var i = clickedColorChooser.attr('id').slice(5);
	var x = color;
	chosedColor = color;
	var styleSheet = document.styleSheets[document.styleSheets.length-1];
	var crossrule = styleSheet.rules;
	if (styleSheet.cssRules)
		crossrule=styleSheet.cssRules;
	styleSheet.crossInsertRule = styleSheet.insertRule ? styleSheet.insertRule : styleSheet.addRule;
	styleSheet.crossInsertRule('.str'+i+' {background-color: '+x+'}', crossrule.length);
	if((parseInt(x.slice(1,3), 16) + parseInt(x.slice(3,5), 16) + parseInt(x.slice(5,7), 16)) / 3.0<128) {
		ifwhite[i]= '-white';
	} else {
		ifwhite[i]= '';
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
	if (braceletType == 2) {
		strings = [];
		return;
	}
	strings[0] = [];
	for(var i=0; i<nofstr;i++) {
		strings[0][i] = i;
	}
	for(var i=1; i<nofrows+1;i++) {
		strings[i] = [];
		var even = 0;
		var evenstr_evenrow = 0;
		if(i%2==0) {
			even = 1;
			strings[i][0] = strings[i-1][0];
			if(nofstr%2==0) {
				evenstr_evenrow = 1;
			}
		}
		for(var j=0; j<parseInt(nofstr/2)-evenstr_evenrow; j++){
			if(knotsType[i-1][j]<3) {
				strings[i][2*j+even] = strings[i-1][2*j+1+even];
				if(2*j+1+even<nofstr) {
					strings[i][2*j+1+even] = strings[i-1][2*j+even];
				}
			} else {
				strings[i][2*j+even] = strings[i-1][2*j+even];
				if(2*j+1+even<nofstr) {
					strings[i][2*j+1+even] = strings[i-1][2*j+1+even];
				}
			}
		}
		if(even && nofstr%2==0) {
			strings[i][nofstr-1] = strings[i-1][nofstr-1];
		} else if(nofstr%2==1 && !even){
			strings[i][nofstr-1] = strings[i-1][nofstr-1];
		}
	}
}

function initDesigner() {
	strings = [];
	ifwhite = [];
	knotsType = [];
	nofstr = 0;
	$('#pattern-canvas').empty();
	$('#pattern-thumb').empty();
	$('#pattern-designer').empty();
	$('#colorsInput').empty();
	loaded = false;
	var nofinputs = nofcols;
	if (braceletType == 2) {
		nofinputs++;
	}
	for(var i=0; i<nofinputs; i++) {
		addInput('colorsInput');
		$('#color'+i+' option:eq(0)').attr("selected", "selected");
	}
	var kt = knottype;
	for(var i=0; i<nofrows;i++) {
		knotsType[i] = [];
		if (braceletType == 1) {
			if(knottype==5 && knotsType[i-1]!=undefined) {
				kt=knotsType[i-1][0];
				if(kt==3) {
					kt=4;
				} else {
					kt=3;
				}
			} else if(knottype==5 && i==0) {
				kt=3;
			}
			for(var j=0; j<parseInt(nofstr/2)-i%2; j++){
				knotsType[i][j] = kt;
			}
			if(nofstr%2==1 && i%2==1) {
				knotsType[i][knotsType[i].length] = kt;
			}
		} else if (braceletType == 2) {
			for(var j=0; j<nofstr-1; j++){
				knotsType[i][j] = kt;
			}
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
	if (braceletType == 2) {
		var nofcols = knotsType[0].length;
		for (var i=0; i<nofrows;i++) {
			$('<div id="row-strings'+i+'" />').appendTo('#pattern-canvas');
			$('<span class="str0 string-'+( i%2 == 0 ? 'ur' : 'dr' )+'"></span>').appendTo('#row-strings'+i);
			for(var j=0; j<nofcols; j++) {
				$('<span class="str'+(j+1)+' string-v"></span>').appendTo('#row-strings'+i);
				if (j<nofcols-1) 
					$('<span class="str0 string-h"></span>').appendTo('#row-strings'+i);
			}
			$('<span class="str0 string-'+( i%2 == 0 ? 'dl' : 'ul' )+'"></span>').appendTo('#row-strings'+i);
			
			$('<div id="row'+i+'" class="straight" />').appendTo('#pattern-designer');
			$('<div id="column'+i+'" class="column-straight" />').appendTo('#pattern-thumb');
			for(var j=0; j<nofcols; j++) {
				var color = knotsType[i][j] == 5 ? 0 : j+1;
				$('<span class="str'+color+' knot knot'+knotsType[i][j]+ifwhite[color]+'" onclick="changeType(this, '+i+','+j+')"></span>').appendTo('#row'+i);
				$('<span class="str'+(knotsType[i][knotsType[i].length-1-j] == 5 ? 0 : nofcols-j)+' knot-thumb"></span>').appendTo('#column'+i); 
			}
		}
		$('#row'+(row)+' > span:nth-child('+(col+1)+')').addClass('current');
		return;
	}
	for (var i=0; i<nofrows;i++) {
		var cl = "odd";
		var cl_thumb = "";
		var directions = [1,0];
		if(i%2==0) {
			cl = "even";
			var directions = [0,1];
			if(nofstr%2==1) {
				cl_thumb = " column-margin";
			}
		} else if(nofstr%2==0) {
			cl_thumb = " column-margin";
		}
		
		$('<div id="row-strings'+i+'" />').appendTo('#pattern-canvas');
		for(var j=0; j<strings[i].length/2;j++) {
			$('<span class="str'+strings[i][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+i);
			if(strings[i][2*j+1] != undefined) {
				$('<span class="str'+strings[i][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+i);
			}
		}
		
		$('<div id="row'+i+'" class="'+cl+'" />').appendTo('#pattern-designer');
		$('<div id="column'+i+'" class="column-'+cl+cl_thumb+'" />').appendTo('#pattern-thumb');
		var minus = 0;
		if(nofstr%2==0 && (i)%2==1) {
			minus=1; //if number of strings is even and row is odd draw one knot less
		}
		for(var j=0; j<parseInt(strings[i].length/2)-minus; j++) {
			var move = 0;
			if(knotsType[i][j]%2==0) {
				move = 1;
			}
			$('<span class="str'+strings[i][2*j+i%2+move]+' knot knot'+knotsType[i][j]+ifwhite[strings[i][2*j+i%2+move]]+'" onclick="changeType(this, '+i+','+j+')"></span>').appendTo('#row'+i);
		}
		for(var j=parseInt(strings[i].length/2)-minus-1; j>=0; j--) {
			var move = 0;
			if(knotsType[i][j]%2==0) {
				move = 1;
			}
			$('<span class="str'+strings[i][2*j+i%2+move]+' knot-thumb"></span>').appendTo('#column'+i);
		}
	}
	var i = nofrows;
	var directions = [1,0];
	if(i%2==0) {
		var directions = [0,1];
	}
	$('<div id="row-strings'+i+'" />').appendTo('#pattern-canvas');
	for(var j=0; j<strings[i].length/2;j++) {
		$('<span class="str'+strings[i][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+i);
		if(strings[i][2*j+1] != undefined) {
			$('<span class="str'+strings[i][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+i);
		}
	}
	$('#row'+(row)+' > span:nth-child('+(col+1)+')').addClass('current');
}

function changeType(obj, i, j, newType) {
	var prevType = knotsType[i][j];
	$(obj).removeClass('knot'+prevType);
	
	if (newType == undefined) {
		newType = braceletType == 1 ? prevType%4+1 : (prevType == 5 ? 6 : 5);
	}
	knotsType[i][j]=newType;
	$(obj).addClass('knot'+knotsType[i][j]);

	$('.current').removeClass('current');
	$('#row'+i+' > span:nth-child('+(j+1)+')').addClass('current');
	
	evaluateColors();
	drawPattern();
}

function getCode() {
	var rows = $('#pattern-designer').children();
	var str = '[';
	for(var i=0; i<rows.length; i++) {
		var knots = $(rows[i]).children();
		if (i>0)
			str += ",";
		str += '[';
		for(var j=0; j<knots.length; j++) {
			var cls = $(knots[j]).attr('class').split(/\s+/)[2].slice(4,5);
			if (j>0)
				str += ",";
			str += cls;
		}
		str += ']';
	}
	str += ']';
	window.alert(str);
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
	
	if($('#generate-form-name').val().length == 0) {
		alert(noNameError);
		return false;
	} 
	
	return true;
}
