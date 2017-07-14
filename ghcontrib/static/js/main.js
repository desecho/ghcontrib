function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function displayMessage(message) {
  return $.jGrowl(message);
};

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  crossDomain: false,  // obviate need for sameOrigin test
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type)) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$.jGrowl.defaults.closerTemplate = '<div>' + gettext('Close all notifications') + '</div>';