'''
@author Russell Mezzetta
Documentation for TinyMCE

http://tinymce.moxiecode.com/documentation.php

To use the TinyMCE editor you must call the following two lines in a template (equivalent to an html file)

Normally tinyMCE.init({params-go-here})

General signature:
<script type="text/javascript" src="/media/js/tiny_mce/tiny_mce.js"></script>
<script type="text/javascript">
   tinyMCE.init({})</script>

Every textarea on the page will be replaced with the WYSIWYG editor. It will have the options (bold, center, hyperlink....) you specified inside the tinyMCEinit({}) call.

For an example see implementation/templates/pages/lesson/edit_lesson.html
'''
