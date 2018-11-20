$(".card").flip({
  axis: 'y',
  trigger: 'manual'
});

$(".audio").click(function(){
   //$('.sound')[0].play()
   $(this).parent().siblings('.sound')[0].play();
});

$(".flip-btn").click(function(){
  $(this).closest(".card").flip(true);
});


