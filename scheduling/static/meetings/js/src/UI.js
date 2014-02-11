var num = 2.439024;
for (var i=0; i<41; i++) {  
  var k = num * i;
  $( "#col_1" ).before("<div class='lines' style='top:"+k+"%'></div>" );
  }
 // visualize the X grid
  var num_row=14.2857;
  for(var i=0; i<8; i++){  
  var k = num_row * i;
  var exist=$("#lines_container").html();
  $( "#lines_container" ).html(exist+"<div class='lines_row' style='left:"+k+"%'></div>" );
  }

  // visualize the even o'clock Y grid
  var num=2.439024;
  for(var i=0; i<41; i=i+4){  
  var k = num * i;
  $( "#col_1" ).before("<div class='bold_lines' style='top:"+k+"%'></div>" );
  }

//***********************************window-size********************************
  var GLOBAL = {};
  GLOBAL.userHeight=$(window).height();
var containerHeight = parseInt($("#container").height());

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7core&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    var scope = 0;  
    var CalTopY_base = -GLOBAL.userHeight/85;
    var mouseY;
    var initY;
    var WIDTH = 13.6;
    var counter=0;
    var shortest_height = 2;
    // for inelastic time_slot
    var finalY;
    var gridY = new Array(); 
    var test;  
    var initTopPosition; // carry the top position data from 1st funtion to 2nd
    var message; // carry the message
    var messageTime;
    var include = new Array();
    var messageDate;
  var left_mark = 0;
  var initX = new Array();
  var ratio = 17.328125/2.439024;
for(var i = 0; i < 41; i++){
    gridY[i] = 2.439024 * i; // generate the horizontal grid on the div
}
//generate the left attributes of avail_time slots for each one
for(var i=1; i <8;i++){
  left_mark=14.285714*(i-1);
  initX[i] = 0.4+left_mark*0.9999;
};
//set the default scroll value
$('#scrollWindow').scrollTop(167);
//set the new algorithm for scroll------ caltopY = base value(generated by user) + caltop Y updated when scrolling
var CalTopY_scroll = 167;
var CalTopY = CalTopY_base + CalTopY_scroll/8.7;

$('#scrollWindow').scroll(function(){
 CalTopY = CalTopY_base + CalTopY_scroll/8.7;
});

//scope control
var dateModifier = function(a, b, c){ // a is the two digit string, b is the max date of the month
    var temp = parseInt(a) + c*7 - c*b;
    if ( temp < 0){
      return (temp + b).toString();
    }
    else if( temp > b){
      return temp - b;
    }
    else{
      return temp == 0? b: temp;
    }
};

var modifier = function(string, num){ 
    var dateModified = string.slice(3, 5);
    var date = string.slice(0, 2);
    var k = 0;
    var year = string.slice(-4);
    if(date == '02'){
        if(parseInt(string.slice(-4)) % 4 == 0){ 

            if(num == 1 && parseInt(dateModified) > 22){
                k = 1;
                dateModified = dateModifier(dateModified, 29, num);
            }
            else if(num == -1 && parseInt(dateModified) < 8){
              k = -1;
              dateModified = dateModifier(dateModified, 31, num); 
            }
            else{
        dateModified = dateModifier(dateModified, 30, num); 
          }
        } 
        else{
          if(num == 1 && parseInt(dateModified) > 21){
              k = 1;
              dateModified = dateModifier(dateModified, 28, num);
            }
            else if(num == -1 && parseInt(dateModified) < 8){
              k = -1;
                dateModified = dateModifier(dateModified, 31, num); 
            }
            else{
        dateModified = dateModifier(dateModified, 30, num); 
          }           
        }
    }
    else if(date == '04' || date == '06' || date == '09' || date == '11'){
        if(num==1 && parseInt(dateModified) > 23){
          k = 1;
        dateModified = dateModifier(dateModified, 30, num);
        }
        else if(num == -1 && parseInt(dateModified) < 8){
          k = -1;
        dateModified = dateModifier(dateModified, 31, num);
        }
        else{
        dateModified = dateModifier(dateModified, 30, num); 
        }

    }
    else if(date == '12'){
      if(num == 1 && parseInt(dateModified) > 24){
        k = -11;
        year = (parseInt(year) + 1).toString();
      dateModified = dateModifier(dateModified, 31, num);
      }
      else if(num == -1 && parseInt(dateModified) < 8){
            k = -1;
        dateModified = dateModifier(dateModified, 30, num);     
        }
        else{
        dateModified = dateModifier(dateModified, 31, num); 
        }
      
    }
    else if(date == '01'){
      if(num == 1 && parseInt(dateModified) >24){
        k = 1;
          dateModified = dateModifier(dateModified, 31, num);
      }
      else if(num == -1 && parseInt(dateModified) < 8){
        k = 11;
        year = (parseInt(year) - 1).toString();
          dateModified = dateModifier(dateModified, 31, num);
      }
        else{
        dateModified = dateModifier(dateModified, 31, num); 
        }
    }
    else if(date == '08'){
      if(num == 1 && parseInt(dateModified) >24){
        k = 1;
          dateModified = dateModifier(dateModified, 31, num);
      }
      else if(num == -1 && parseInt(dateModified) < 8){
        k = -1;
        dateModified = dateModifier(dateModified, 31, num);
      }
      else{
        dateModified = dateModifier(dateModified, 31, num); 
        }

    }
    else if(date == '03'){
      if(num == 1 && parseInt(dateModified) >24){
        k = 1;
          dateModified = dateModifier(dateModified, 31, num);
      }
      else if(num == -1 && parseInt(dateModified) < 8){
        if(parseInt(string.slice(-4)) % 4 == 0){ 
      k = -1;
          dateModified = dateModifier(dateModified, 29, num);
          } 
        else{
      k = -1;
          dateModified = dateModifier(dateModified, 28, num);        
          }
      }
        else{
        dateModified = dateModifier(dateModified, 31, num); 
        }
    }        
    else{
        if(num == 1 && parseInt(dateModified) > 24){
          k = 1;
        dateModified = dateModifier(dateModified, 31, num);
        }
        else if(num == -1 && parseInt(dateModified) < 8){
          k = -1;
        dateModified = dateModifier(dateModified, 30, num);
        }
        else{
        dateModified = dateModifier(dateModified, 31, num); 
        }

    }
    dateModified = dateModified.toString();
    if(dateModified.length < 2){
      dateModified = '0'.concat(dateModified);
    }
    date = (parseInt(date) + k).toString();
    if(date.length < 2){
      date = '0'.concat(date);
    }
    return date.concat('/', dateModified, '/', year);
};

var changeDatePositive = function(num){
    var string = $('#datesForData_'+num).html();
    $('#datesForData_'+num).html(modifier(string, 1));
}
var changeDateNegative = function(num){
    var string = $('#datesForData_'+num).html();
    $('#datesForData_'+num).html(modifier(string, -1)); 
}
$('#scopeRight').unbind().click(function(){
  changeDatePositive(1);
  changeDatePositive(2);
  changeDatePositive(3);
  changeDatePositive(4);
  changeDatePositive(5);
  changeDatePositive(6);
  changeDatePositive(7);
  $('.scope'+scope).fadeTo('fast', 0);
  $('.scope'+scope).css('display', 'none');
  scope = scope + 1;
  $('.scope'+scope).fadeTo('fast', 0.5);
  $('.scope'+scope).css('display', '');
});
$('#scopeLeft').unbind().click(function(){
  if(scope > 0){
  changeDateNegative(1);
  changeDateNegative(2);
  changeDateNegative(3);
  changeDateNegative(4);
  changeDateNegative(5);
  changeDateNegative(6);
  changeDateNegative(7);
  $('.scope'+scope).fadeTo('fast', 0);
  scope = scope - 1; 
  $('.scope'+scope).fadeTo('fast', 0.5);
  }
});

//Drag&Resize:
var dragResize=function(){
      $(".avail_time").draggable({ 
          cursor: 'move',
          axis: "y",
          snap:'.lines',
          snapTolerance: 30,
          snapMode:'inner',
          containment: '#container',
      });

      $(".avail_time").resizable({
          snap:'.lines',
          snapTolerance: 30,
          handles: 's',
          containment: '#container',        
      });
};

//different slot generators for seven lanes
var column_init = function(num){
$("#col_"+num).mousedown( function(e) {


   counter = counter+1;
   initY = - 20 + CalTopY + e.pageY/8.6;  // % conversion 
   var nearestY = gridY[0];
  for(var h = 0; h < 41; h++){
      if(gridY[h+1] > initY){
        nearestY = gridY[h];
        break;
      } 
  }
  messageDate = $("#datesForData_"+num).html();
//$('#col_1').after("<div style='position: absolute; left: 200px; font-size:5em;'>"+initY+"</div>");
  initTopPosition = nearestY;
   $('#col_'+num).after("<div class='avail_time scope"+scope+"' id='slot_"+counter+"' style='top: "+nearestY+"%; left:"+initX[num]+"%; position:absolute; width:"+WIDTH+"%; ' ></div>");

   $("#slot_"+counter+"").html("<div style='display: none;'id='dataCarrier_date_"+counter+"'>"+messageDate+"</div><div style='display:none;'class='dataCarrier' id='dataCarrier_"+counter+"'></div><div class='avail_time_bottom' id='slot_"+counter+"_bottom' style='width:100%; position:absolute; background-color: red; height:5px; bottom: 0;' ></div>");
   
   dragResize();
}); 
};


column_init(7);
column_init(6);
column_init(5);
column_init(4);
column_init(3);
column_init(2);
column_init(1);

//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&xcontinue CORE&&&&&&&&&&&&&&7
$(document).mousemove( function(e) {

   mouseY = -20 + CalTopY + e.pageY/8.6;   //  % conversion
   //calculate the nearest benchmark
   var nearestY_new = gridY[0];
    for(var i = 0; i < 39; i++){
        if(gridY[i] > mouseY){
          nearestY_new = gridY[i];
            break;
        }   
    }
    //subtract the initial benchmark
    nearestY_new = nearestY_new - initTopPosition;
//test
//$('#aaa').remove(); 
//$('#col_1').after("<div id = 'aaa'style='position: absolute; font-size:5em;'>"+nearestY_new+"</div>");
 
if(nearestY_new > 0){
  $('#slot_'+counter+'').css({"height":""+nearestY_new+"%"});
 }
 else{
  var nearestY_top = initTopPosition + nearestY_new;
  $('#slot_'+counter+'').css({"top":""+nearestY_top+"%"});
  $('#slot_'+counter+'').css({"height":""+ (2.4390 - nearestY_new) +"%"});
 }
});  


$(document).mouseup( function(e) {
    $('#slot_'+counter+'').attr("id","slot_"+counter+"_finalize");
//$("#col_2").before("<div>"+processData[1]+"</div>");
    $('#dataCarrier_'+counter+'').css("display","");
//1-3-2013   make sure that the slot exists and it does not exist in the array

    if($("#slot_"+counter+"_finalize").attr('id') == "slot_"+counter+"_finalize"&& jQuery.inArray(counter , include) === -1){
      include.push(counter);
    };
});     

//parse the selected begining time
var processMessageTime = function(messageTime){
if(messageTime <10){
  if(messageTime%2 === 0 ){
    messageTime = (messageTime/2) + 5;
    messageTime = "0" + messageTime + ":00";
  }
  else{
    messageTime = ((messageTime-1)/2) +5
    messageTime = "0" + messageTime + ":30"
  }
}
else {
  if(messageTime%2 === 0 ){
    messageTime = (messageTime/2) + 5;
    messageTime = messageTime + ":00";
  }
  else{
    messageTime = ((messageTime-1)/2) +5
    messageTime = messageTime + ":30"
  }
}

if(messageTime === "24:00"){
  messageTime = "0:00";};
if(messageTime === "24:30"){
  messageTime = "0:30";};
if(messageTime === "25:00"){
  messageTime = "1:00"};
return messageTime;
}
//data processing 
var topForData, bottomForData, topForData2;
$(document).mousemove( function(e) {

  for(var w=0; w < include.length;w++){
    if($("#slot_"+include[w]+"_finalize").css("top").toString().slice(-1) != '%'){
    topForData = parseInt($("#slot_"+include[w]+"_finalize").css("top"));
    }
    bottomForData = $("#slot_"+include[w]+"_finalize").height();
    bottomForData = processMessageTime(Math.round(((bottomForData + topForData)/containerHeight)/0.024378));
    //$('#formDescription').val(topForData2+'----'+bottomForData);
    topForData2 = processMessageTime(Math.round((topForData/containerHeight)/0.024378));

    $("#dataCarrier_"+include[w]+"").html(""+topForData2+"-"+bottomForData+"<a style='margin-left:-1px; margin-top: -3px;' class='trashcan' href='#'>&#215;</a>");
//$('#aaa').remove(); 
//$('#col_1').after("<div id = 'aaa'style='position: absolute; font-size:5em;'>"+topForData2+"|"+bottomForData+"</div>");
  };

$('.trashcan').unbind().click(function(){

      var zzz = $(this).parent().attr('id').replace(/[^\d.]/g,  "");
      zzz = parseInt(zzz);
      var index = jQuery.inArray(zzz, include);
      include.splice(index,1);
      $(this).parent().parent().remove();
  });

var NAME = $("#name").val();
var DESCRIPTION = $("#description").val();
$("#meetingTitle").html(NAME);
$('#meetingDescription').html(DESCRIPTION);
});
var processData = new Array();

$("#submit").click(function(e){
//transfer the data:

$("#id_name").val($("#name").val());
$("#id_description").val($("#description").val());
$("#id_location").val($("#location").val());
$("#id_visibility").val($("#visibility").val());

});

$("#nextStep").click(function(){
if($("#name").val() == ""){
  $("#div_id_name_jia").addClass("has-error");
  $("#name").after('<p id="error_1_id_email" class="help-block"><strong>请填写会议名称！</strong></p>');
}
  else{
  $("#createPageFirst").fadeOut("fast");
  $("#progressAnimation").css("width","34%");
  $("#createPageSecond").fadeIn("fast");
}
});
$("#nextStep2").click(function(){
    for(var cc=0; cc < include.length; cc++){
// replace : and '' and get rid of the trashcan image symbol 12.31.2013
    processData[cc] = $("#dataCarrier_"+include[cc]+"").html().replace(/[^\d.]/g, "").slice(0, 8) + $("#dataCarrier_date_"+include[cc]+"").html().replace(/[^\d.]/g, "");
  };
  var proposed = "";
  for(var ccc=0; ccc < include.length; ccc++){
    proposed = proposed + processData[ccc];
  }; 
  $("#dataStorage").val(proposed);
if($("#name").val() == ""){ 
}
  else{
  $("#createPageSecond").fadeOut("fast");
  $("#progressAnimation").css("width", "66%");
  $("#createPageThird").fadeIn("fast");
  $("#div_id_name").hide();
  $("#div_id_description").hide();
  $("#div_id_location").hide();
  $("#submit").fadeIn("fast");
}
});

$("#lastStep").click(function(){
  $("#createPageSecond").fadeOut("fast");
  $("#progressAnimation").css("width", "1%");
  $("#createPageFirst").fadeIn("fast");
  $("#div_id_name").show();
  $("#div_id_description").show();
  $("#div_id_location").show();
});
$("#lastStep2").click(function(){
  $("#createPageThird").fadeOut("fast");
  $("#progressAnimation").css("width", "33%");
  $("#createPageSecond").fadeIn("fast");
  $("#submit").fadeOut("fast");
});

//merge the messages
$(document).ready(function(){
if(typeof($("#error_1_id_share").html()) == "string"){ 
var validationMessage = $("#error_1_id_share").html();

if( validationMessage.slice(3,5) != "" ){
  $("#progressAnimation").css("width","100%")
  $("#createPageFirst").hide();
  $("#createPageSecond").hide();
  $("#div_id_name").hide();
  $("#div_id_description").hide();
  $("#div_id_location").hide();
  $("#submit").fadeIn("fast");
  $("#createPageThird").fadeIn("fast");
}
}
else{
    $("#createPageFirst").hide();
    $("#createPageFirst").fadeIn("fast");
    $("#createPageSecond").hide();
}
});

// client-side Validation||||||||||||||||||||||||||||||||||||||||
function validateEmail(field) {
    var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,5}$/;
    return (regex.test(field)) ? true : false;
}
function validateMultipleEmailsCommaSeparated(emailcntl) {

    var seperator = ",";
    var value = emailcntl;
    value.replace(";", ",");
    if (value != '') {
        var result = value.split(seperator);
        for (var i = 0; i < result.length; i++) {
            if (result[i] != '') {
              result[i] = result[i].trim();
                if (!validateEmail(result[i])) {
                    $("#id_share").after('<p id="error_1_id_share" class="help-block"><strong>' + result[i] + ' 不是一个有效的邮箱地址，请重新输入！</strong></p>');
                    $("#div_id_share").addClass("has-error");
                    return false; 
                }
            }
        }
    }
    return true;
}