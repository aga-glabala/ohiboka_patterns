$(document).ready(function(){
	// tabs
   $( "#tabs" ).tabs({
			ajaxOptions: {
				error: function( xhr, status, index, anchor ) {
					$( anchor.hash ).html(errorText);
				},
				success: function() {
					$('.photo a').lightBox(
					{
						imageLoading: STATIC_URL+'gfx/lightbox-ico-loading.gif',
						imageBtnClose: STATIC_URL+'gfx/lightbox-btn-close.gif',
						imageBtnPrev: STATIC_URL+'gfx/lightbox-btn-prev.gif',
						imageBtnNext: STATIC_URL+'gfx/lightbox-btn-next.gif',
					}
				);
			}
		}
	});

	$("[rel=tooltip]").tooltip();

	// Mousetrap
	$( "#tabs" ).bind( "tabsshow", function(event, ui) {
		Mousetrap.reset();
		if (ui.index == 1) {
			stepByStepInit();
		}
	});
	if (window.location.hash == '#tabs-2') {
		stepByStepInit();
	}
	
	// pattern creating
	if (braceletType == 1) {
		createDiagonalPattern('#pattern');
	} else if (braceletType == 2) {
		createStraightPattern();
	}
	addKnot();
	
	
	// rates
	$('#ratepattern i').hover(
		function () {
			var els = $('#ratepattern i');
		    els.slice(0,$(this).attr('id').substring(4,5)).removeClass('icon-heart-empty');
		    els.slice(0,$(this).attr('id').substring(4,5)).addClass('icon-heart-full');
		    els.slice($(this).attr('id').substring(4,5),5).removeClass('icon-heart-full');
		    els.slice($(this).attr('id').substring(4,5),5).addClass('icon-heart-empty');
	});
	$('#ratepattern').hover(function () {},
		function () {
	    	setRate();
	});
	$('#ratepattern i').click(
		function () {
			var id = $(this).attr('id').substring(4,5)
			$.ajax({
			  url: "/bracelet/rate/"+bracelet_id+"/"+id
			}).done(function( html ) {
				if(html == "OK") {
					rate = id;
					setRate();
				} else {
			  		alert(html);
			  	}
			});
		}
	);
	setRate();

	$('#delete-link').click(function() {
		$('#delete-confirm').modal();
		return False;
	});

 });
 
function addKnotButton() {
	$('.new').removeClass('new');
	addKnot();
}

function createStraightPattern() {
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
		
		$('<div id="row'+i+'" class="straight" />').appendTo('#pattern');
		$('<div id="column'+i+'" class="column-straight" />').appendTo('#pattern-thumb');
		for(var j=0; j<nofcols; j++) {
			$('<span class="str'+knotsColor[i][j]+' knot knot'+knotsType[i][j]+ifwhite[knotsColor[i][j]]+'"></span>').appendTo('#row'+i);
			$('<span class="str'+knotsColor[i][knotsType[i].length-1-j]+' knot-thumb"></span>').appendTo('#column'+i); 
		}
	}
}

function createDiagonalPattern(patternDivId) {
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
			if(strings[nofrows-1][2*j+1] != undefined) {
				$('<span class="str'+strings[i][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+i);
			}
		}	
		
		$('<div id="row'+i+'" class="'+cl+'" />').appendTo(patternDivId);
		$('<div id="column'+i+'" class="column-'+cl+cl_thumb+'" />').appendTo('#pattern-thumb');
		for(var j=0; j<knotsType[i].length; j++) {
			$('<span class="str'+knotsColor[i][j]+' knot knot'+knotsType[i][j]+ifwhite[knotsColor[i][j]]+'"></span>').appendTo('#row'+i);
			$('<span class="str'+knotsColor[i][knotsType[i].length-1-j]+' knot-thumb"></span>').appendTo('#column'+i); 
		}
	}
	//last row strings
	var cl = "odd";
	var directions = [0,1];
	if((nofrows-1)%2==0) {
		cl = "even";
		directions = [1,0];
	}
	$('<div id="row-strings'+nofrows+'" />').appendTo('#pattern-canvas');
	for(var j=0; j<strings[nofrows].length/2;j++) {
		$('<span class="str'+strings[nofrows][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+nofrows);
		if(strings[nofrows-1][2*j+1] != undefined) {
			$('<span class="str'+strings[nofrows][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+nofrows);
		}
	}
	
	//step pattern
	$('<div id="step-row-strings'+0+'" />').appendTo('#step-pattern-canvas');
	for(var i=0; i<strings[0].length/2;i++) {
		$('<span class="str'+strings[0][2*i]+' string'+0+'"></span>').appendTo('#step-row-strings'+0);
		if(strings[0][2*i+1] != undefined) {
			$('<span class="str'+strings[0][2*i+1]+' string'+1+'"></span>').appendTo('#step-row-strings'+0);
		}
	}	
}

function addKnot() {
	if (lastKnotRow > knotsColor.length - 1 || lastKnotCol > knotsColor[lastKnotRow].length - 1) {
		return;
	}
	
	if (braceletType == 1) {
		addDiagonalKnot();
	} else if (braceletType == 2) {
		addStraightKnot();
	}
		
	$("#instructions").scrollTop($("#instructions")[0].scrollHeight);
	if(sequence>1) {
		$("body").scrollTop($("body")[0].scrollHeight);
	}
}

function addStraightKnot() {
	if(lastKnotCol == 0 && lastKnotRow%2 == 0) {
		$('<div id="steprow'+lastKnotRow+'" class="row-even" />').appendTo('#step-pattern');
	} else if (lastKnotCol == knotsType[0].length - 1 && lastKnotRow%2 == 1) {
		$('<div id="steprow'+lastKnotRow+'" class="row-odd" />').appendTo('#step-pattern');
	}
	
	if (lastKnotRow%2 == 0) {
		$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+ifwhite[knotsColor[lastKnotRow][lastKnotCol]]+' new" title="r'+lastKnotRow+'c'+lastKnotCol+'" id="knot'+sequence+'"></span>').appendTo('#steprow'+lastKnotRow);
	} else {
		$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+ifwhite[knotsColor[lastKnotRow][lastKnotCol]]+' new" title="r'+lastKnotRow+'c'+lastKnotCol+'" id="knot'+sequence+'"></span>').prependTo('#steprow'+lastKnotRow);
	}
	
	var text = "";
	if (lastKnotRow%2 == 0) {
		text = texts[knotsType[lastKnotRow][lastKnotCol]-5]; 
	} else {
		text = texts[knotsType[lastKnotRow][lastKnotCol] == 5 ? 1 : 0];
	}
	text = text.replace('{0}', '<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot"></span>');
	text = text.replace('{1}', '<span class="str'+(lastKnotCol+1)+'">&nbsp;</span>');
	$('<p class="new">'+text+'</p>').appendTo('#instructions');

	if($('#step-row-strings'+(lastKnotRow)).length==0) {
		$('<div id="step-row-strings'+(lastKnotRow)+'" class="'+(lastKnotRow%2 == 0 ? 'row-even' : 'row-odd')+'" />').appendTo('#step-pattern-canvas');
	}
	
	if (lastKnotRow%2 == 0) {
		if (lastKnotCol == 0) {
			$('<span id="string'+sequence+'-first" class="str0 string-ur"></span>').appendTo('#step-row-strings'+(lastKnotRow));
		}
		$('<span id="string'+sequence+'" class="str'+(lastKnotCol+1)+' string-v"></span>').appendTo('#step-row-strings'+(lastKnotRow));
		if (lastKnotCol < knotsType[0].length-1) {
			$('<span id="string'+sequence+'-second" class="str0 string-h"></span>').appendTo('#step-row-strings'+(lastKnotRow));
		} else {
			$('<span id="string'+sequence+'-last" class="str0 string-dl"></span>').appendTo('#step-row-strings'+(lastKnotRow));
		}
	} else {
		if (lastKnotCol < knotsType[0].length-1) {
			$('<span id="string'+sequence+'-first" class="str0 string-h"></span>').prependTo('#step-row-strings'+(lastKnotRow));
		} else {
			$('<span id="string'+sequence+'-second" class="str0 string-ul"></span>').prependTo('#step-row-strings'+(lastKnotRow));
		}
		$('<span id="string'+sequence+'" class="str'+(lastKnotCol+1)+' string-v"></span>').prependTo('#step-row-strings'+(lastKnotRow));
		if (lastKnotCol == 0) {
			$('<span id="string'+sequence+'-last" class="str0 string-dr"></span>').prependTo('#step-row-strings'+(lastKnotRow));
		}
	}
	
	sequence++;
	
	if (lastKnotCol == knotsType[0].length - 1 && lastKnotRow%2 == 0 || lastKnotCol == 0 && lastKnotRow%2 == 1) {
		lastKnotRow++;
	} else if (lastKnotRow%2 == 0) {
		lastKnotCol++;
	} else {
		lastKnotCol--;
	}
}

function addDiagonalKnot() {
	if(lastKnotCol==0) {
		var cl = "odd";
		if(lastKnotRow%2==0) {
			cl = "even";
		}
		$('<div id="steprow'+lastKnotRow+'" class="'+cl+'" />').appendTo('#step-pattern');
	}
	
	var cl = "odd";
	var directions = [1,0];
	if(lastKnotRow%2==1) {
		cl = "even";
		directions = [1,0];
	}
	var even = 0; // strings are even and row is odd
	if(strings[0].length%2==0 && lastKnotRow%2==1) {
		even = 1;
	}
	
	var odd = 0; // strings are odd and row is odd
	if(strings[0].length%2==1 && lastKnotRow%2==1) {
		odd = 1;
	}
	
	$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+ifwhite[knotsColor[lastKnotRow][lastKnotCol]]+' new" title="r'+lastKnotRow+'c'+lastKnotCol+'" id="knot'+sequence+'"></span>').appendTo('#steprow'+lastKnotRow);
	var text = texts[knotsType[lastKnotRow][lastKnotCol]-1];
	if(knotsType[lastKnotRow][lastKnotCol]%2) {
		text = text.replace('{0}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol+even+odd]+' knot"></span>');
		text = text.replace('{1}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol+1+even+odd]+'">&nbsp;</span>');
		 
	} else {
		text = text.replace('{0}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol+1+even+odd]+' knot"></span>');
		text = text.replace('{1}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol+even+odd]+'">&nbsp;</span>');
	}
	$('<p class="new">'+text+'</p>').appendTo('#instructions');
	
	
	if($('#step-row-strings'+(lastKnotRow+1)).length==0) {
		$('<div id="step-row-strings'+(lastKnotRow+1)+'" />').appendTo('#step-pattern-canvas');
		// if row is odd and nofstrings is odd draw last not used string
		if(even && strings.length>lastKnotRow+1 || odd) {
			$('<span id="string'+sequence+'-first" class="str'+strings[lastKnotRow+1][0]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
		}
	}
	if(strings.length>lastKnotRow+1 && strings[lastKnotRow+1].length>2*lastKnotCol+even) {
		$('<span id="string'+sequence+'" class="str'+strings[lastKnotRow+1][2*lastKnotCol+even+odd]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
		if(strings[lastKnotRow+1].length>2*lastKnotCol+1+even) {
			$('<span id="string'+sequence+'-second" class="str'+strings[lastKnotRow+1][2*lastKnotCol+1+even+odd]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
		}
	}
	// if row is odd and nofstrings is odd draw last not used string
	if(even && strings.length > lastKnotRow+1 && 2*lastKnotCol+2+lastKnotRow%2==strings[lastKnotRow+1].length-1) {
		$('<span id="string'+sequence+'-last" class="str'+strings[lastKnotRow+1][2*lastKnotCol+2+even]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
	}
	if(odd && 2*lastKnotCol+2==strings[lastKnotRow].length-1) {
		$('<span id="string'+sequence+'-last" class="str'+strings[lastKnotRow][2*lastKnotCol+2]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow));
	}
	sequence++;
	
	if (lastKnotRow == knotsType.length - 1 || lastKnotCol == 0 && lastKnotRow%2==0) {
		if (lastKnotRow%2 == 1) {
			lastKnotCol += 1;
		}
		while (lastKnotRow > 0 && lastKnotCol < knotsType[lastKnotRow-lastKnotRow%2].length - 1) {
			lastKnotRow -= 1;
			lastKnotCol += lastKnotRow%2 ;
		}
		if (lastKnotCol == knotsType[lastKnotRow].length - 1 + lastKnotRow%2) {
			if (lastKnotRow%2==0 && nofstr%2 == 0) {
				lastKnotRow += 2;
			} else {
				lastKnotRow += 1;
			}
		}  
		if (lastKnotRow == 0) {
			lastKnotCol++;
		}
	} else {
		lastKnotRow++;
		if (lastKnotRow%2 != 0) {
			lastKnotCol--;
		}
	}
}

function delKnot() {
	if (sequence>1) {
			sequence--;
			var element = $('#knot'+sequence);
			$('#string'+sequence).remove()
			$('#string'+sequence+'-second').remove();
			$('#string'+sequence+'-first').remove();
			$('#string'+sequence+'-last').remove();
			
			var title = element.attr('title');
			element.remove();
			$('#instructions p:last').remove();
			lastKnotCol = parseInt(title.slice(title.indexOf('c')+1));
			lastKnotRow = parseInt(title.slice(1, title.indexOf('c')));
			if($('#step-row-strings'+(lastKnotRow+1)).children().length==0) {
				$('#step-row-strings'+(lastKnotRow+1)).remove();
			}
	}
}
function del5Knots() {
	for(var i=0; i<5; i++) {
		delKnot();
	}
}
function add5Knots() {
	$('.new').removeClass('new');
	for(var i=0; i<5; i++) {
		addKnot();
	}
}
function setRate() {
	$('#ratepattern i').slice(0,rate).removeClass('icon-heart-empty');
	$('#ratepattern i').slice(0,rate).addClass('icon-heart-full');
	$('#ratepattern i').slice(rate,5).removeClass('icon-heart-full');
	$('#ratepattern i').slice(rate,5).addClass('icon-heart-empty');
}

function stepByStepInit() {
	Mousetrap.bind('space', addKnotButton);
	Mousetrap.bind('backspace', delKnot);
	Mousetrap.bind('right', add5Knots);
	Mousetrap.bind('left', del5Knots);
}
