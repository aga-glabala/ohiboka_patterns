$(document).ready(function(){
	// tabs
   $( "#tabs" ).tabs({
			ajaxOptions: {
				error: function( xhr, status, index, anchor ) {
					$( anchor.hash ).html(errorText);
				},
				success: function() {
					$('.photoTd a').lightBox(
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
	
	// pattern creating
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
		
		$('<div id="row'+i+'" class="'+cl+'" />').appendTo('#pattern');
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
	addKnot();
	
	
	// rates
	$('.icon-star').hover(
		function () {
		    $('.icon-star').slice(0,$(this).attr('id').substring(4,5)).css('background-position', '0 -15px');
		    $('.icon-star').slice($(this).attr('id').substring(4,5),5).css('background-position', '-15px -15px');
	});
	$('.icon-star').parent().hover(function () {},
		function () {
	    	setRate();
	});
	$('.icon-star').click(
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
 });

function addKnot() {
		
		if (lastKnotRow > knotsColor.length - 1 || lastKnotCol > knotsColor[lastKnotRow].length - 1) {
			return;
		}
		
		if(lastKnotCol==0) {
//			if(lastKnotRow<knotsType.length) {
				var cl = "odd";
				if(lastKnotRow%2==0) {
					cl = "even";
				}
				$('<div id="steprow'+lastKnotRow+'" class="'+cl+'" />').appendTo('#step-pattern');
				
				
//			}
		}
		$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+ifwhite[knotsColor[lastKnotRow][lastKnotCol]]+'" title="r'+lastKnotRow+'c'+lastKnotCol+'" id="knot'+sequence+'"></span>').appendTo('#steprow'+lastKnotRow);
		var text = texts[knotsType[lastKnotRow][lastKnotCol]-1];
		text = text.replace('{0}', '<span class="str'+knotsColor[lastKnotRow][2*lastKnotCol]+' knot"></span>');
		text = text.replace('{1}', '<span class="str'+knotsColor[lastKnotRow][2*lastKnotCol+1]+' knot"></span>');
		$('<p>'+text+'</p>').prependTo('#instructions');
		
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
		
		// TODO something goes wrong here..
		var odd = 0; // strings are odd and row is odd
		if(strings[0].length%2==1 && lastKnotRow%2==1) {
			odd = 1;
		}
		
		if($('#step-row-strings'+(lastKnotRow+1)).length==0) {
			$('<div id="step-row-strings'+(lastKnotRow+1)+'" />').appendTo('#step-pattern-canvas');
			// if row is odd and nofstrings is odd draw last not used string
			if(even && strings.length>lastKnotRow+1 || odd) {
				$('<span id="string'+sequence+'sec" class="str'+strings[lastKnotRow+1][0]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
			}
		}
		if(strings.length>lastKnotRow+1 && strings[lastKnotRow+1].length>2*lastKnotCol+even) {
			$('<span id="string'+sequence+'" class="str'+strings[lastKnotRow+1][2*lastKnotCol+even+odd]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
			if(strings[lastKnotRow+1].length>2*lastKnotCol+1+even) {
				$('<span id="string'+sequence+'sec" class="str'+strings[lastKnotRow+1][2*lastKnotCol+1+even+odd]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
			}
		}
		// if row is odd and nofstrings is odd draw last not used string
		if(even && strings.length > lastKnotRow+1 && 2*lastKnotCol+2+lastKnotRow%2==strings[lastKnotRow+1].length-1) {
			$('<span id="string'+sequence+'sec" class="str'+strings[lastKnotRow+1][2*lastKnotCol+2+even]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
		}
		if(odd && 2*lastKnotCol+2==strings[lastKnotRow].length-1) {
			$('<span id="string'+sequence+'sec" class="str'+strings[lastKnotRow+1][2*lastKnotCol+2]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
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
	if (sequence>0) {
			sequence--;
			var element = $('#knot'+sequence);
			$('#string'+sequence).remove()
			$('#string'+sequence+'sec').remove();
			var title = element.attr('title');
			element.remove();
			$('#instructions p:last').remove();
			lastKnotCol = title.slice(title.indexOf('c')+1);
			lastKnotRow = title.slice(1, title.indexOf('c'));
	}
}
function del5Knots() {
	for(var i=0; i<5; i++) {
		delKnot();
	}
}
function add5Knots() {
	for(var i=0; i<5; i++) {
		addKnot();
	}
}
function setRate() {
	$('.icon-star').slice(0,rate).css('background-position', '0 -15px');
	$('.icon-star').slice(rate,5).css('background-position', '-15px -15px');
}
