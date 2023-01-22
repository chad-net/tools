# HTML Rules

goodtags = ['a', 'p', 'strong', 'b', 'em', 'i', 'ul', 'ol', 'li', 'br', 'blockquote', 'q', 's', 'del', 'code', 'pre']


also: img

'hr' can be used, but is not to be overused

Base files in tools/templates/


## images
`<a href="files/image.jpeg" target="_blank"><img class="center" src="files/image.jpeg"></a>`

if there are two successive images you put &lt;br&gt; between them



## captions
`<p class="c">`


## what is removed
we remove everything from a tags that isnt href and target="\_blank"

all other attributes are removed from all tags except src for img which is dealt with separately

we remove any other tags (span, etc)


