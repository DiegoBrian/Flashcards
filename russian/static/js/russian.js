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

$('.btn_flip').on('click', function(){
	$('.btn_flip').each(function(cnt) {
		var id = this.id;
		exibir(id);
	});

	var current_id = this.id;
	esconder(current_id);

	var face_number = current_id.substring(current_id.length - 1);
	face_number = parseInt(face_number) + 1;

	flipCard(face_number);
})

$(document).ready(function(){
    // Add the appropriate content to the initial "front side"
    var frontFace = $('.face1');
    var frontContent = $('.store li:first-child').html(); 
	frontFace.html(frontContent);

	esconder_class(".btn_flip", 0);
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

function esconder_class(class_name, id_number){
	$(class_name).each(function(cnt) {
		if (cnt == id_number){
			var id = this.id;
			esconder(id);
		}
	});

}
