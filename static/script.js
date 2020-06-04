document.body.onload  = function() {
  document.getElementById('location-input').value = window.location.pathname
  $.get('https://www.cloudflare.com/cdn-cgi/trace', function(data) {
    $.post('https://ibmath--ryan-jacobjacob.repl.co/setIP', {ip: data.match(/ip=(.+)\n/)[1]})
    document.getElementById('load-screen').remove()
  })
}