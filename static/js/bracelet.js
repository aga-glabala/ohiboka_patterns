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
	$('<br />').appendTo('#pattern');
	for (var i=0; i<nofrows-1;i++) {
		var cl = "odd";
		var cl_thumb = "";
		var directions = [1,0];
		if(i%2==0) {
			cl = "even";
			cl_thumb = " column-margin";
			directions = [0,1];
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
	$('<div id="steprow0" class="even" />').appendTo('#steppattern');
	$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+'"></span>').appendTo('#steprow0');
	$('<p>'+texts[knotsType[lastKnotRow][lastKnotCol]-1]+'</p>').appendTo('#instructions');
	
	
	// rates
	$('.icon-star').hover(
	  function () {
	    $('.icon-star').slice(0,$(this).attr('id').substring(4,5)).css('background-position', '0 -15px');
	    $('.icon-star').slice($(this).attr('id').substring(4,5),5).css('background-position', '-15px -15px');
	  }, 
	  function () {
	    setRate();
	  }
	);
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
		if(lastKnotCol+1<knotsType[lastKnotRow].length) {
			lastKnotCol++;
			$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+'"></span>').appendTo('#steprow'+lastKnotRow);
			$('<p>'+texts[knotsType[lastKnotRow][lastKnotCol]-1]+'</p>').appendTo('#instructions');
		} else {
			if(lastKnotRow+1<knotsType.length) {
				lastKnotRow++;
				lastKnotCol = 0;
				var cl = "odd";
				if(lastKnotRow%2==0) {
					cl = "even";
				}
				$('<div id="steprow'+lastKnotRow+'" class="'+cl+'" />').appendTo('#steppattern');
				$('<span class="str'+knotsColor[lastKnotRow][lastKnotCol]+' knot knot'+knotsType[lastKnotRow][lastKnotCol]+'"></span>').appendTo('#steprow'+lastKnotRow);	
				$('<p>'+texts[knotsType[lastKnotRow][lastKnotCol]-1]+'</p>').appendTo('#instructions');
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
