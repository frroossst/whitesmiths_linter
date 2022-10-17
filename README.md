![tests](https://github.com/frroossst/whitesmiths_linter/actions/workflows/ci.yml/badge.svg)

After picking up the whitemsiths indentation style from my first internship, I simply can't go back to any other style, the whitesmiths style makes blocks of code clear visually, This style of indent fits in perfectly with the Gestalt Principles of vision.  


<br>
<br>

## What is the whitesmiths-style?
```
if (data != NULL && res > 0)
    {
    if (!JS_DefineProperty(cx, o, "data", STRING_TO_JSVAL(JS_NewStringCopyN(cx, data, res)), NULL, NULL, JSPROP_ENUMERATE))
        {
        QUEUE_EXCEPTION("Internal error!");
        goto err;
        }
    PQfreemem(data);
    }
else if (!JS_DefineProperty(cx, o, "data", OBJECT_TO_JSVAL(NULL), NULL, NULL, JSPROP_ENUMERATE))
    {
    QUEUE_EXCEPTION("Internal error!");
    goto err;
    }
```


<br>
<br>

## Why is it the best?
"this alignment uses the visual cortex better (basically fewer “visuospatial objects” by creating a gestalt (joining together a shape) between the braces and the associated command block)" - [Gustav Tresselt](https://community.notepad-plus-plus.org/topic/10868/new-auto-indentation-vs-whitesmith-indent-style)  

<br>
<br>


"The clean line between the controlling statement and the block that it owns is broken by the braces in the BSD style.  The blocking of the code should not change just because the "if" statement has more then one line in it.  In WS the look of the code is similar to the above example with only one line.  This consistency is very important in maintaining readability in code." - [ActiveWebClick](http://www.activeclickweb.com/whitesmiths/index.html)


<br>
<br>






And that is the life of a programmer, come across something, pick that has a hill to die on, write tools to automate said task, and of course convert everyone else to your way of programming.

NOTE : Not the best, quick and dirty, gets the job done decently well, I still have to go through the codebase to fix things here and there but saves me time and that's that  

