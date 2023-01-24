console.log('online');

function getSelectionHtml() {
  var html = "";
  if (typeof window.getSelection != "undefined") {
    var sel = window.getSelection();
    if (sel.rangeCount) {
      var container = document.createElement("p");
      for (var i = 0, len = sel.rangeCount; i < len; ++i) {
        container.appendChild(sel.getRangeAt(i).cloneContents());
      }
      html = container.innerHTML;
    }
  } else if (typeof document.selection != "undefined") {
    if (document.selection.type == "Text") {
      html = document.selection.createRange().htmlText;
    }
  }
  return html;
}

/* copied straight from stackoverflow because firefox clipboard api is autistic */
// return a promise
function copy(textToCopy) {
    // navigator clipboard api needs a secure context (https)
    if (navigator.clipboard && window.isSecureContext) {
        // navigator clipboard api method'
        return navigator.clipboard.writeText(textToCopy);
    } else {
        // text area method
        let textArea = document.createElement("textarea");
        textArea.value = textToCopy;
        // make the textarea out of viewport
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        return new Promise((res, rej) => {
            // here the magic happens
            document.execCommand('copy') ? res() : rej();
            textArea.remove();
        });
    }
}

var selectedHTML = "";

document.addEventListener('mouseup', function(){
  selectedHTML = getSelectionHtml();
});

document.addEventListener("keydown", (event) => {
  if(event.isComposing || event.keyCode === 229) {
    return;
  }
  switch(event.keyCode) {
    case 192: // backtick
      if(selectedHTML != "") {
        console.log(selectedHTML);
        copy(selectedHTML);
        /*
          .then(() => console.log("Text copied"))
          .catch(() => console.log('Error'));
        */
        selectedHTML = ""
      }
      break;
    case 49: //1
      copy('CHADNET_SYSTEM_ALPHA_PARAGRAPH');
      break;
    case 50: //2
      copy('CHADNET_SYSTEM_ALPHA_BLOCKQUOTE_BEGIN');
      break;
    case 51: //3
      copy('CHADNET_SYSTEM_ALPHA_BLOCKQUOTE_END');
      break;
    case 52: //4
      copy('CHADNET_SYSTEM_ALPHA_IMAGE');
      break;
    case 53: //5
      copy('CHADNET_SYSTEM_ALPHA_CAPTION');
      break;
    case 54: //6
      copy('CHADNET_SYSTEM_ALPHA_UNORDERED_LIST_BEGIN');
      break;
    case 55: //7
      copy('CHADNET_SYSTEM_ALPHA_UNORDERED_LIST_END');
      break;
    case 56: //8
      copy('CHADNET_SYSTEM_ALPHA_ORDERED_LIST_BEGIN');
      break;
    case 57: //9
      copy('CHADNET_SYSTEM_ALPHA_ORDERED_LIST_END');
      break;
    case 48: //0
      copy('CHADNET_SYSTEM_ALPHA_STOP');
      break;
    case 173:
      copy('CHADNET_SYSTEM_ALPHA_HELP');
      break;
    default:
      break;
  }
});
