var pomBtn = document.getElementById("pomodoroModeButton");
var sBreakBtn = document.getElementById("shortBreakModeButton");
var lBreakBtn = document.getElementById("longBreakModeButton");

pomBtn.className = "button-selected"

pomBtn.addEventListener("click", function(event){
    if (pomBtn.className != "button-selected"){
         pomBtn.className = "button-selected";
         sBreakBtn.className = "";
         lBreakBtn.className = "";
    }
});
sBreakBtn.addEventListener("click", function(event){
    if (sBreakBtn.className != "button-selected"){
        sBreakBtn.className = "button-selected";
        pomBtn.className = "";
        lBreakBtn.className = "";
    }
});
lBreakBtn.addEventListener("click", function(event){
    if (lBreakBtn.className != "button-selected"){
        lBreakBtn.className = "button-selected";
        sBreakBtn.className = "";
        pomBtn.className = "";
    }
});