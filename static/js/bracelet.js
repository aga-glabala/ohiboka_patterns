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
			},
			select: function(event, ui) {
				var tabID = "#ui-tabs-" + (ui.index + 1);
				$(tabID).html("<b>Fetching Data.... Please wait....</b>");
		        }
		}
	});
	
	// pattern creating
	for (var i=0; i<nofrows-1;i++) {
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
	var directions = [1,0];
	if((nofrows-1)%2==0) {
		cl = "even";
		directions = [0,1];
	}
	$('<div id="row-strings'+(nofrows-1)+'" />').appendTo('#pattern-canvas');
	for(var j=0; j<strings[nofrows-1].length/2;j++) {
		$('<span class="str'+strings[nofrows-1][2*j]+' string'+directions[0]+'"></span>').appendTo('#row-strings'+(nofrows-1));
		if(strings[nofrows-1][2*j+1] != undefined) {
			$('<span class="str'+strings[nofrows-1][2*j+1]+' string'+directions[1]+'"></span>').appendTo('#row-strings'+(nofrows-1));
		}
	}
	
	//step pattern
	$('<div id="step-row-strings'+0+'" />').appendTo('#step-pattern-canvas');
	for(var i=0; i<strings[0].length/2;i++) {
		$('<span class="str'+strings[0][2*i]+' string'+0+'"></span>').appendTo('#step-row-strings'+0);
		if(strings[0][i] != undefined) {
			$('<span class="str'+strings[0][2*i+1]+' string'+1+'"></span>').appendTo('#step-row-strings'+0);
		}
	}
	addKnot();
	
	
	// rates
	$('.icon-star').hover(
	  function () {
	    $('.icon-star').slice(0,$(this).attr('id').substring(4,5)).css('background-position', '0 -15px');
	    $('.icon-star').slice($(this).attr('id').substring(4,5),5).css('background-position', '-15px -15px');
	  }
	);
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
	var cl = "odd";
	var directions = [1,0];
	var move = 0;
	if(lastKnotRow%2==0) {
		cl = "even";
	} else {
		directions = [1,0];
		move=1;
	}
	
	if(lastKnotCol==0) {
			$('<div id="steprow'+lastKnotRow+'" class="'+cl+'" />').appendTo('#step-pattern');
	}
	$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+'"></span>').appendTo('#steprow'+lastKnotRow);
	if($('#step-row-strings'+(lastKnotRow+1)).length==0) {
		$('<div id="step-row-strings'+(lastKnotRow+1)+'" />').appendTo('#step-pattern-canvas');
		if(lastKnotRow%2==1) {
			$('<span class="str'+strings[lastKnotRow+1][0]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
		}
	}
	$('<span class="str'+strings[lastKnotRow+1][2*lastKnotCol+move]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
	if(strings[lastKnotRow+1][2*lastKnotCol+1+move] != undefined) {
		$('<span class="str'+strings[lastKnotRow+1][2*lastKnotCol+1+move]+' string'+directions[1]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
	}
	if(lastKnotCol+1 > strings[lastKnotRow+1].length/2 && lastKnotRow%2==0) {
		$('<span class="str'+strings[lastKnotRow+1][parseInt(strings[lastKnotRow+1].length/2)]+' string'+directions[0]+'"></span>').appendTo('#step-row-strings'+(lastKnotRow+1));
	}
	
	var text = texts[knotsType[lastKnotRow][lastKnotCol]-1];
	text = text.replace('{0}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol]+' knot"></span>');
	text = text.replace('{1}', '<span class="str'+strings[lastKnotRow][2*lastKnotCol+1]+' knot"></span>');
	$('<p>'+text+'</p>').prependTo('#instructions');
		
	if (lastKnotRow == knotsType.length - 1 || lastKnotCol == 0 && lastKnotRow%2==0) {
		
		while (lastKnotRow > 0 && lastKnotCol+lastKnotRow%2 < knotsType[lastKnotRow].length) {
			lastKnotRow -= 1;
			lastKnotCol += lastKnotRow%2 ;
		}
		if (lastKnotRow%2 == 1) {
			lastKnotCol += 1;
		}
		if (lastKnotCol == knotsType[lastKnotRow].length + lastKnotRow%2) {
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
	if (lastKnotRow>0 || lastKnotCol>0) {
			$('.knot:last').remove();
			$('#instructions p:last').remove();
			if(lastKnotCol>0) {
				lastKnotCol--;
			} else if(lastKnotRow>0) {
					lastKnotRow--;	
					lastKnotCol=knotsType[lastKnotRow].length-1;
			}
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
