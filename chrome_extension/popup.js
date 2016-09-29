chrome.tabs.getSelected(null, function(tab) {
  d = document;
  d.getElementById("url").value = tab.url;
});
