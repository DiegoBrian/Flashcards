/*
$("#front").removeClass("d-none");
$("div .back").addClass("d-none");
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
	$("#btn-front").addClass("d-none");
	$("#buttons").removeClass("d-none");
});

var topCard = 1;
var facingUp = true;

function flipCard(n) {
    if (topCard === n) return;

    // Replace the contents of the current back-face with the contents
    // of the element that should rotate into view.
    var curBackFace = $('.' + (facingUp ? 'face2' : 'face1'));
    var nextContent = $('.store' + n).html(); 
    var nextContent = $('.store li:nth-child(' + n + ')').html(); 
    curBackFace.html(nextContent);

    // Rotate the content
    $('.flip').toggleClass('flipped');
    topCard = n;
    facingUp = !facingUp;
}

$('#flipper_ch').on('click', function(){
	esconder("flipper_ch");
	exibir("flipper_pi");
	exibir("flipper_en");

	flipCard(1);
});

$('#flipper_pi').on('click', function(){
	exibir("flipper_ch");
	esconder("flipper_pi");
	exibir("flipper_en");

	flipCard(2);
});

$('#flipper_en').on('click', function(){
	exibir("flipper_ch");
	exibir("flipper_pi");
	esconder("flipper_en");
	
	flipCard(3);
});

$(document).ready(function(){
    // Add the appropriate content to the initial "front side"
    var frontFace = $('.face1');
    var frontContent = $('.store li:first-child').html(); 
	frontFace.html(frontContent);

	esconder("flipper_ch");
});

function strID(id){
	var strID = "'#" + id + "'";
	return strID;
}

function exibir(id){
	var element = document.getElementById(id);

	if(element.hasAttribute("disabled"))
		element.removeAttribute("disabled");
}

function esconder(id){
	var element = document.getElementById(id);

	if(!element.hasAttribute("disabled"))
		element.setAttribute("disabled", "disabled");
}