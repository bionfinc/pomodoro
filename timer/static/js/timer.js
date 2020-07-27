document.addEventListener("DOMContentLoaded", pomodoroModeOn);
document.getElementById("startButton").addEventListener("click", startTimer);
document.getElementById("pauseButton").addEventListener("click", pauseTimer);
document.getElementById("resetButton").addEventListener("click", resetTimer);

var pomodoroButton = document.getElementById("pomodoroModeButton");
pomodoroButton.addEventListener("click", pomodoroModeOn);
var shortBreakButton = document.getElementById("shortBreakModeButton");
shortBreakButton.addEventListener("click", shortBreakModeOn);
var longBreakButton = document.getElementById("longBreakModeButton");
longBreakButton.addEventListener("click", longBreakModeOn);

var countdownMins = 0;
var countdownSecs = 0;
var timeRemaining;
var countdownClock;
var currentTimer;
var pomodoroMinutes;
var shortBreakMinutes;
var longBreakMinutes;
var timerState = '';

if (pomodoroButton.value <= 0) {
  pomodoroMinutes = 25
} else {
  pomodoroMinutes = pomodoroButton.value
}

if (shortBreakButton.value <= 0) {
  shortBreakMinutes = 5
} else {
  shortBreakMinutes = shortBreakButton.value;
}

if (longBreakButton.value <= 0) {
  longBreakMinutes = 10
} else {
  longBreakMinutes = longBreakButton.value;
}

function pomodoroModeOn() {

  // Set button color to selected
  if (pomodoroButton.className != "button-selected"){
    pomodoroButton.className = "button-selected";
    shortBreakButton.className = "";
    longBreakButton.className = "";
  }

  // In case the timer was running, stop countdownClock function
  if (currentTimer != 'Pomodoro'){
  clearInterval(countdownClock);

  // Reset time and timer display
  countdownMins = pomodoroMinutes;
  countdownSecs = 0;
  timerState = ''; // clear timer state
  console.log(timerState);
  resetTimer();

  // Set timer to Pomodoro
  currentTimer = "Pomodoro";
  }
}

function shortBreakModeOn() {
  if (currentTimer != 'Short Break'){
    // check if Pomodoro mode is on and timer is running
    if (currentTimer == "Pomodoro" && timeRemaining < (pomodoroMinutes * 60) && timeRemaining != 0) {

      //format prompt message depending if user is logged in or not
      function checkLoggedIn() {
        return new Promise(resolve => {
          $.ajax({
            url: '/isLoggedIn',
            success: function (data) {
              //logged in
              if (data == 'True') {
                resolve("Are you sure you want to end your task early? You'll lose 10 points");
              }
              //not logged in
              else {
                resolve("Are you sure you want to end your task early?");
              }
            }
          });
        })
      }

      //show window prompt message
      async function showMessage() {
        const message = await checkLoggedIn();

        if (window.confirm(message)) {
          // Set button color to selected
          shortBreakButton.className = "button-selected";
          pomodoroButton.className = "";
          longBreakButton.className = "";
          

          //deduct 10 points from score
          $.ajax({
            url: '/deductPoints',
            success: function (data) {
              $("#score_span").html(data)
            }
          });

          // In case the timer was running, stop countdownClock function
          clearInterval(countdownClock);

          // Reset time and timer display
          countdownMins = shortBreakMinutes;
          countdownSecs = 0;
          timerState = ''; // clear timer state
          console.log(timerState);
          resetTimer();

          // Set timer to Short Break
          currentTimer = "Short Break";
        }
      }

      showMessage();

    }
    else {
      //set button color
      shortBreakButton.className = "button-selected";
      pomodoroButton.className = "";
      longBreakButton.className = "";

      // In case the timer was running, stop countdownClock function
      clearInterval(countdownClock);

      // Reset time and timer display
      countdownMins = shortBreakMinutes;
      countdownSecs = 0;
      timerState = ''; // clear timer state
      console.log(timerState);
      resetTimer();

      // Set timer to Short Break
      currentTimer = "Short Break";
    }
  }
}

function longBreakModeOn() {
  if (currentTimer != 'Long Break'){
    // check if Pomodoro mode is on and timer is running
    if (currentTimer == "Pomodoro" && timeRemaining < (pomodoroMinutes * 60) && timeRemaining != 0) {
      

        //format prompt message depending if user is logged in or not
        function checkLoggedIn() {
          return new Promise(resolve => {
            $.ajax({
              url: '/isLoggedIn',
              success: function (data) {
                //logged in
                if (data == 'True') {
                  resolve("Are you sure you want to end your task early? You'll lose 10 points");
                }
                //not logged in
                else {
                  resolve("Are you sure you want to end your task early?");
                }
              }
            });
          })
        }

        //show window prompt message
        async function showMessage() {
          const message = await checkLoggedIn();

          if (window.confirm(message)) {

            //set button color
            longBreakButton.className = "button-selected";
            pomodoroButton.className = "";
            shortBreakButton.className = "";

            //deduct 10 points from score
            $.ajax({
              url: '/deductPoints',
              success: function (data) {
                $("#score_span").html(data)
              }
            });

            // In case the timer was running, stop countdownClock function
            clearInterval(countdownClock);

            // Reset time and timer display
            countdownMins = longBreakMinutes;
            countdownSecs = 0;
            timerState = ''; // clear timer state
            console.log(timerState);
            resetTimer();

            // Set timer to Short Break
            currentTimer = "Long Break";
          }
        }

        showMessage();
      
    }
    else {
      //set button color
      longBreakButton.className = "button-selected";
      pomodoroButton.className = "";
      shortBreakButton.className = "";

      // In case the timer was running, stop countdownClock function
      clearInterval(countdownClock);

      // Reset time and timer display
      countdownMins = longBreakMinutes;
      countdownSecs = 0;
      timerState = ''; // clear timer state
      console.log(timerState);
      resetTimer();

      // Set timer to Short Break
      currentTimer = "Long Break";
    }
  }
}

function startTimer() {
  // change button colors
  document.getElementById("startButton").classList.add("control-button-selected");
  document.getElementById("pauseButton").classList.remove("control-button-selected");
  
  console.log(timerState);
  // Check to see if the timer has already been completed and reset if it has
  if (timeRemaining == 0) {
    resetTimer();
  }
  if (timerState == 'STOPPED' || timerState == 'PAUSED'){
    timerState = 'STARTED';
    console.log(timerState)
    // Call countdownTimer function every second (1000ms)
    countdownClock = setInterval(function () { countdownTimer(); }, 1000);
  } 

  // save task data to db if task is started fresh only
  if(timeRemaining == pomodoroMinutes * 60){
    let currentCategory = document.getElementById('taskCategory').value;
    $.ajax({
      url: '/saveTaskData/',
      method: 'post',
      dataType: 'json',
      data: JSON.stringify({
          'task_name': $('#taskName').text(),
          'task_time' : pomodoroMinutes,
          'category' : currentCategory,
        }),
      success: function(data) {
        console.log(data);
      }
    });

  }

}

function pauseTimer() {
  
  

  if (timerState == 'STARTED') {
    document.getElementById("pauseButton").classList.add("control-button-selected");
    document.getElementById("startButton").classList.remove("control-button-selected");
    console.log(timerState);
  // Stop countdownClock function
  clearInterval(countdownClock);
  timerState = 'PAUSED';
  console.log(timerState);
  } 
}

function resetTimer() {
  console.log(timerState);
  if (timerState != 'STOPPED'){
  // Stop the countdownClockfunction
  pauseTimer();

  // Reset the values
  document.getElementById('minsValue').textContent = countdownMins;
  document.getElementById('secsValue').textContent = '00';
  timeRemaining = (countdownMins * 60) + countdownSecs;

  // Display the reset time and title
  displayTimer();
  document.title = "Pomodoro Posse Timer";
  timerState = 'STOPPED';
  console.log(timerState);

  document.getElementById("pauseButton").classList.remove("control-button-selected");
  document.getElementById("startButton").classList.remove("control-button-selected");

  }
}

function displayTimer() {

  var temp = timeRemaining;

  // Calculate the minute and second values
  var minutesValue = Math.floor(temp / 60);
  var secondsValue = temp % 60;

  // Pad the number if needed (ex. 9 is padded to 09) to display properly
  var minutesString = padValue(minutesValue);
  var secondsString = padValue(secondsValue);

  // Update the countdown values on the screen and title
  document.getElementById('minsValue').textContent = minutesString;
  document.getElementById('secsValue').textContent = secondsString;
  document.title = "(" + minutesString + ":" + secondsString + ") - " + currentTimer;
}

function padValue(integerValue) {
  if (integerValue > 9) {
    return integerValue.toString();
  }
  else {
    return '0' + integerValue.toString();
  }
}

function countdownTimer() {
  timeRemaining--;
  displayTimer();
  //console.log(timerState)
  // If time is up, stop the timer and display notification
  if (timeRemaining == 0 && currentTimer == "Pomodoro") {

    document.title = "Time is up!";
    pauseTimer();

    //format prompt message depending if user is logged in
    function checkLoggedIn() {
      return new Promise(resolve => {
        $.ajax({
          url: '/isLoggedIn',
          success: function (data) {
            console.log(data);
            //logged in
            if (data == 'True') {
              resolve("Congrats! You won 10 points for completing your task!");
            }
            //not logged in
            else {
              resolve("Congrats on finishing your task! Log in to track rewards for completed tasks.");
            }
          }
        });
      })
    }

    //display alert message
    async function showMessage() {
      const message = await checkLoggedIn();
      // add points to score
      $.ajax({
        url: '/addPoints',
        success: function (data) {
          $("#score_span").html(data)
        }
      });

      setTimeout(function () {
        alert(message);
      }, 0)
    }

    showMessage();
    timerState == 'STOPPED'
    console.log(timerState)
  }
  else if (timeRemaining == 0) {
    pauseTimer();
    timerState == 'STOPPED'
    console.log(timerState)
  }
}