$(document).ready(function(e){
	$('#sideBarOrganized').click(function(){
		$('this').css('display','none');	
	});
	$('#sideBarInvited').click(function(){
		$('.organizedMeetingList').css('display','none');
	});
});