$(window).bind("popstate", function(event) {
    numProfs = 0; //RESET
    request_new_checkboxes();
    reloadProfessors();
});
$(document).ready(function() {

    $(document).bind('keyup', function ( e ) {
      if ( e.which == 37 ) {
      modal_slide('prev')();
      }
      else if ( e.which == 39 ) {
      modal_slide('next')();
      }
      });

    $(".prof_modal_next").live("click", modal_slide('next'));
    $(".prof_modal_prev").live("click", modal_slide('prev'));

    $(".prof_box").click(function(){
      $(".prof_modal").hide();
      $('.prof_modal').removeClass("current_modal prev_modal next_modal");
      var modal_id = $(this).attr("id") + "_modal";
      var this_modal = $("#" + modal_id);
      this_modal.addClass('current_modal fade');
      $('<div class="modal-backdrop animate" />').appendTo(document.body)
      this_modal.modal('show');
      });

    $('.prof_modal').bind('hide', function(){
        $('.prof_modal').hide();
        $('.modal-backdrop').remove();
        $('.prof_modal').removeClass("current_modal prev_modal next_modal fade in");
        });

    $('.gray_star').click(function(){
        $(this).hide();
        $(this).prev().show();
        return false;
        });

    $('.gold_star').click(function(){
        $(this).hide();
        $(this).next().show();
        return false;
        });

    $(".close").click(function() {
        $(this.parentElement).slideUp();
        });
    $("li#saved").click(function() {
        $(this).toggleClass('active');
        });
    $("li#starred").click(function() {
        window.history.pushState("some data", "Title", window.location.pathname + '?starred=true');
        numProfs = 0; //RESET
        reloadProfessors();
        request_new_checkboxes();
    });
});

modal_slide = function(move_direction){
  if(move_direction=="next"){
    var move_string='-50%';
    var div_offset = 1;
    var current_modal_becomes = "prev_modal";
  } else if(move_direction=="prev"){
    var move_string='150%';
    var div_offset = -1;
    var current_modal_becomes = "next_modal";
  } else {
    alert("not a valid direction");
  }
  inner = function() {
    var modal = $(".current_modal");
    var this_id = modal.attr("id");
    var next_id = this_id.replace(/(\d+)/g, function(s){
        return (parseInt(s) + div_offset).toString();
        });
    var next_div = $("#" + next_id);
    next_div.addClass(move_direction + "_modal"); 
    next_div.modal('show');
    modal.switchClass("current_modal", current_modal_becomes,350);
    next_div.switchClass(move_direction+"_modal", "current_modal",350);
  }
  return inner;
};

request_new_checkboxes = function() {
  $.ajax({
url:"filter_options.php",
type:"GET",
dataType: "html",
data: window.location.search.replace('?', ''), 
success : loadNewCheckboxes,
error : function(data) {
alert('uhoh');
//TODO: show alert [lost connection to the server]
}
});
}
loadNewCheckboxes = function(data) {
  $(document).ready(function() {
      $('span#filter').html(data); 
      $('[type=checkbox]').change(filterCheckChange);
      });
}
reloadProfessors = function() {
  $.ajax({
url:"get_professors.php",
type:"GET",
dataType: "json",
data: window.location.search.replace('?', '') + '&start=' + numProfs + '&limit=' + rowLimit, 
success : loadNewProfData  
});
}

numProfs = 0;
rowLimit = 50;
blockLoading = false;
loadNewProfData = function(data) {
  $(document).ready(function() {
      blockLoading = true;
      if(numProfs == 0) {
        $('.prof_grid').html(data['html']);
      } else {
        $('.prof_grid').append(data['html']);
      }
      numProfs += data['num_returned'];
      $('span#search_description').html(data['description']);
      $('.gray_star').click(function(){
        $(this).hide();
        $(this).prev().show();
        if($(this).hasClass('search_star')) {
          searchStar(true);
        } else {
          setStar(true, $(this).attr('id'));
        }
          return false;
        });

      $('.gold_star').click(function(){
        $(this).hide();
        $(this).next().show();
        if($(this).hasClass('search_star')) {
          searchStar(false);
        } else {
          setStar(false, $(this).attr('id'));
        }
        return false;
      });
      if(data['num_returned'] == rowLimit) {
        blockLoading = false;
      }
  });
      $(window).scroll(function() {
        if($(window).scrollTop()+$(window).height() + 300 > $('.prof_content').height()) {
          if(!blockLoading) {
            blockLoading = true;
            reloadProfessors();
          }
        }
      });
}

setStar = function(state, id) { 
  $.ajax({
    url:"set_star.php",
    type: "POST",
    dataType: "json",
    data: {
    'state': state,
    'id' : id,
    },
    success : function(data) {
      //TODO: we should probably do something
    },
    error : function(data) {
    }
  });

  var currentCount = parseInt($('span#numstarred').html());
  if(state == true) {
    currentCount += 1;
  } else {
    currentCount -= 1;
  }
  $('span#numstarred').html(currentCount);
}

searchStar = function(state) { 
  $.ajax({
      url:"star_search.php",
      type: "POST",
      dataType: "json",
      data: {
      'state': state,
      'url' : window.location.href,
      'desc' : $('span#search_description').html(), 
      },
  success : function(data) {
      //TODO: we should probably do something
  },
  error : function(data) {
      //somethign here?
  }
});
}
uncheckCategory = function(category) {
  var checkboxes = $('[value=' + category + ']');
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;
  }
  filterCheckChange();
}

filterCheckChange = function() { 
  var new_url = '';
  var checkboxes = $('[type=checkbox]');
  var params = new Array();
  numProfs = 0; //RESET
  for (var i = 0; i < checkboxes.length; i++) {
    var box_cat = checkboxes[i].value;
    if(params[box_cat] == undefined) {
      params[box_cat] = [];
    }
    if (checkboxes[i].checked) {
      params[box_cat].push(checkboxes[i].name);
    }
  }
  for(key in params) {
    if(params[key].length > 0) {
      new_url += '&' + key + '=' + escape(params[key].join(','));
    }
  }
  var query;
  if(getQueryVariable('q')) {
    query = '?q=' + getQueryVariable('q');
  } else {
    query = '?';
    new_url = new_url.substring(1);
  }
  var new_url = window.location.pathname + query + new_url
    window.history.pushState(getState(), "Title", new_url);
  request_new_checkboxes();
  reloadProfessors();
}

function getState() {
  return {url: window.location.search, 
    filter: $('span#filter').html(), 
    grid: {description: $('span#search_description').html(), 
      html: $('.prof_grid').html()}
  };

}

function getQueryVariable(variable) { 
  var query = window.location.search.substring(1); 
  var vars = query.split("&"); 
  for (var i=0;i<vars.length;i++) { 
    var pair = vars[i].split("="); 
    if (pair[0] == variable) { 
      return pair[1]; 
    } 
  } 
  return null;
} 

