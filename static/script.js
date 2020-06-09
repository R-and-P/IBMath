document.body.onload  = function() {
  document.getElementById('location-input').value = window.location.pathname
  $.get('https://www.cloudflare.com/cdn-cgi/trace', function(data) {
    $.post('https://ibmath--ryan-jacobjacob.repl.co/setIP', {ip: data.match(/ip=(.+)\n/)[1]})
    document.getElementById('load-screen').remove()
  })
}

showingMenu = false;
document.getElementById('menu-button').onclick = function() {
  if (showingMenu) {
    document.getElementById('container').style.transform = 'translateX(-50%)'
    document.getElementById('directory-holder').style.transform = 'translateX(-25%)'
    document.getElementById('directory-holder').style.opacity = '0'
  } else {
    document.getElementById('container').style.transform = 'translateX(-25%)'
    document.getElementById('directory-holder').style.transform = 'translateX(0)'
    document.getElementById('directory-holder').style.opacity = '1'
  }
  showingMenu = !showingMenu
}