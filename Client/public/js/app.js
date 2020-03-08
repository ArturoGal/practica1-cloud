$(document).ready(function() {
  $("#version").html("v0.14");

  var page = 1;
  var prev;
  var dataLen = 0;
  
  $("#searchbutton").click( function (e) {
    displayModal();
  });
  
  $("#searchfield").keydown( function (e) {
    if(e.keyCode == 13) {
      displayModal();
    }	
  });
  
  function displayModal() {
    $("#myModal").modal('show');

    $("#status").html("Searching...");
    $("#dialogtitle").html("Search for: "+$("#searchfield").val());
    $("#previous").hide();
    $("#next").hide();
    $.getJSON('/search/' + $("#searchfield").val() , function(data) {
      renderQueryResults(data);
    });
  }
  
  $("#next").click( function(e) {
    ++page;
    afterPreviousNextClickCheck();
    renderQueryResults(prev);
  });
  
  $("#previous").click( function(e) {
    --page;
    afterPreviousNextClickCheck();
    renderQueryResults(prev);
  });

  function afterPreviousNextClickCheck() {
    if(dataLen-4*page > 0) {
      $("#next").show();
    } else {
      $("#next").hide();
    }

    if(page > 1) {
      $("#previous").show();
    } else {
      $("#previous").hide();
    }
  }

  function renderQueryResults(data) {
    if (data.error != undefined) {
      $("#status").html("Error: "+data.error);
    } else {
      dataLen = data.num_results;
      prev = data;
      $("#status").html(""+data.num_results+" result(s)");
      for(var i=(page-1)*4, j=0; i<data.num_results && j<4; ++i, ++j) {
          $("#photo"+j).html("<img src='"+data.results[i]+"' height='250' width='250'>");
      }
      afterPreviousNextClickCheck();
     }
   }
});
