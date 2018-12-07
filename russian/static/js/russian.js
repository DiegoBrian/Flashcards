/*
$("#front").show();
$("div .back").hide();
//*/
var sumir = false;

$(".card").flip({
  axis: 'y',
  trigger: 'manual'
});

$(".audio").on("click",function(){
   //$('.sound')[0].play()
   $(this).parent().siblings('.sound')[0].play();
});

$("#btn-front").on("click", function(){
	$(this).closest(".card").flip(true);
	//alert("front");
});

$("#btn-back").on("click",function(){
	$(this).closest(".card").flip(false);
	$('#subtitle1').toggle();
	$('#subtitle2').toggle();
	$("#btn-front").hide();
	$("#buttons").show();
	/*
	$("div .back").hide();
	$("#front").show();
	//*/
	//alert("back");
});


$("#flipper").on("click", function flip() {
	$('#flip-ex').toggleClass('flipped');
	//$('#bEasy').hide();
	if (!$('#flip-ex').hasClass('flipped')){
		if(!sumir){
			$('#sumir-fst').show();
			$('#sumir-snd').hide();
			//$('#bGood').hide();
			$('#flipper').hide();
		}else{
			$('#sumir-fst').hide();
			$('#sumir-snd').show();
			
		}
	}
});