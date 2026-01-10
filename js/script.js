$(document).ready(function(){
  bindProjectNavArrows();
  fadePageIn();
  addCopyButtonsToCodeBlocks();
});

function bindProjectNavArrows(){
  $(".next-project, .prev-project").click(function(evt){
    evt.preventDefault();
    fadePageOut($(this).attr('href'));
  });
}

function fadePageOut(targetHref){
  $("#main").fadeOut(200, function(){
    $( "#main" ).load( targetHref + " #container #main", function(response, status, xhr){
      bindProjectNavArrows();
      var stateObj = {
        html: $("#main").html()
      };
      document.title = $(response).filter("title").text();
      window.history.pushState(stateObj, document.title, targetHref);
      $("#main").fadeIn(200);
      bindPasswordDetect();
    });
  });
}

function fadePageIn(){
  $("body").fadeIn(200);
}

// Add copy buttons to all code blocks
function addCopyButtonsToCodeBlocks() {
  // Find all pre elements in article content
  $('article.post-content pre, .post-content pre').each(function() {
    var pre = $(this);
    
    // Skip if already wrapped
    if (pre.parent().hasClass('code-block-wrapper')) {
      return;
    }
    
    // Wrap pre in a div for positioning
    pre.wrap('<div class="code-block-wrapper"></div>');
    
    // Create copy button with icon
    var copyButton = $('<button class="copy-code-button" aria-label="Copy code">' +
      '<span class="copy-icon">' +
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' +
          '<path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>' +
        '</svg>' +
      '</span>' +
    '</button>');
    
    // Insert button
    pre.parent().append(copyButton);
    
    // Add click handler
    copyButton.on('click', function(e) {
      e.preventDefault();
      
      // Get the code text, excluding line numbers
      var code = '';
      var codeElement = pre.find('code');
      
      if (codeElement.length) {
        // If there's a code element, get its text
        // Handle line-numbered code (with <a> tags)
        if (pre.find('a').length > 0) {
          pre.find('a').each(function() {
            var lineText = $(this).text().trim();
            if (lineText) {
              code += lineText + '\n';
            }
          });
        } else {
          code = codeElement.text();
        }
      } else {
        // Fallback to pre text
        if (pre.find('a').length > 0) {
          pre.find('a').each(function() {
            var lineText = $(this).text().trim();
            if (lineText) {
              code += lineText + '\n';
            }
          });
        } else {
          code = pre.text();
        }
      }
      
      // Copy to clipboard
      navigator.clipboard.writeText(code.trim()).then(function() {
        // Update button state
        var button = $(e.currentTarget);
        var originalHtml = button.html();
        
        button.addClass('copied');
        button.html('<span class="copy-icon">' +
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' +
            '<path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>' +
          '</svg>' +
        '</span>');
        
        // Reset after 2 seconds
        setTimeout(function() {
          button.removeClass('copied');
          button.html(originalHtml);
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy code: ', err);
      });
    });
  });
}
