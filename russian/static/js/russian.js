$(".card").flip({
  axis: 'y',
  trigger: 'manual'
});

$(".audio").click(function(){
   //$('.sound')[0].play()
   $(this).parent().siblings('.sound')[0].play();
});

$("#btn-front").click(function(){
	$(this).closest(".card").flip(true);
});

$("#btn-back").click(function(){
	$(this).closest(".card").flip(false);
	$('#subtitle1').toggle();
	$('#subtitle2').toggle();
	$("#btn-front").hide();
	$("#buttons").show();
});
