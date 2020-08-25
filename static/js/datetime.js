/* for time */
(function() {
    'use strict';
  
    function getDate() {
      var date = new Date();
      var weekday = date.getDay();
      var month = date.getMonth();
      var day = date.getDate();
      var year = date.getFullYear();
      var hour = date.getHours();
      var minutes = date.getMinutes();
      var seconds = date.getSeconds();
  
      if (hour < 10) hour = "0" + hour;
      if (minutes < 10) minutes = "0" + minutes;
      if (seconds < 10) seconds = "0" + seconds;
  
      var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  
      var weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      
      var monthColors = ["#1E90FF", "#FF69B4", "#00FFFF", "#7CFC00", "#00CED1", "#FF1493", "#00008B", "#FF7F50", "#C71585", "#FF4500", "#FFD700", "#800000"]
  
      var ampm = " PM ";
  
      if (hour < 12) ampm = " AM ";
  
      if (hour > 12) hour -= 12;
  
      var showDate = weekdayNames[weekday] + ", " + monthNames[month] + " " + day + ", " + year;
  
      var showTime = hour + ":" + minutes + ":" + seconds + ampm;
      
      var color = monthColors[month];
  
      document.getElementById('date').innerHTML = showDate;
  
      document.getElementById('time').innerHTML = showTime;
      
      document.bgColor = color;
      
  
      requestAnimationFrame(getDate);
    }
  
    getDate();
  
  }());