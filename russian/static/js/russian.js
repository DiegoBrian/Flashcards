$(".audio").on("click",function(){
   $(this).parent().siblings('.sound')[0].play();
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

$('#flipper_chi_ch').on('click', function(){
	esconder("flipper_chi_ch");
	exibir("flipper_chi_pi");
	exibir("flipper_chi_en");

	flipCard(1);
});

$('#flipper_chi_pi').on('click', function(){
	exibir("flipper_chi_ch");
	esconder("flipper_chi_pi");
	exibir("flipper_chi_en");

	flipCard(2);
});

$('#flipper_chi_en').on('click', function(){
	exibir("flipper_chi_ch");
	exibir("flipper_chi_pi");
	esconder("flipper_chi_en");
	
	flipCard(3);
});

$('#flipper_rus_cy').on('click', function(){
	esconder("flipper_rus_cy");
	exibir("flipper_rus_en");
	exibir("flipper_rus_fn");

	flipCard(1);
});

$('#flipper_rus_en').on('click', function(){
	exibir("flipper_rus_cy");
	esconder("flipper_rus_en");
	exibir("flipper_rus_fn");

	flipCard(2);
});

$('#flipper_rus_fn').on('click', function(){
	exibir("flipper_rus_cy");
	exibir("flipper_rus_en");
	esconder("flipper_rus_fn");
	
	flipCard(3);
});

$('#flipper_rus_ex').on('click', function(){
	esconder("flipper_rus_ex");
	exibir("flipper_rus_ex_en");
	exibir("flipper_rus_tr");

	flipCard(1);
});

$('#flipper_rus_ex_en').on('click', function(){
	exibir("flipper_rus_ex");
	esconder("flipper_rus_ex_en");
	exibir("flipper_rus_tr");

	flipCard(2);
});

$('#flipper_rus_tr').on('click', function(){
	exibir("flipper_rus_ex");
	exibir("flipper_rus_ex_en");
	esconder("flipper_rus_tr");
	
	flipCard(3);
});

$(document).ready(function(){
    // Add the appropriate content to the initial "front side"
    var frontFace = $('.face1');
    var frontContent = $('.store li:first-child').html(); 
	frontFace.html(frontContent);

	esconder("flipper_chi_ch");
	esconder("flipper_rus_cy");
	esconder("flipper_rus_ex");
});

function exibir(id){
	var element = document.getElementById(id);

	if(element && element.hasAttribute("disabled"))
		element.removeAttribute("disabled");
}

function esconder(id){
	var element = document.getElementById(id);

	if(element && !element.hasAttribute("disabled"))
		element.setAttribute("disabled", "disabled");
}