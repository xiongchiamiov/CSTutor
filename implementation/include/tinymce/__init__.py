'''
Documentation for TinyMCE

Here is a link to the site's documentation:
http://tinymce.moxiecode.com/documentation.php

To use the TinyMCE editor you must call the following two lines in a template (equivalent to an html file)

General signature:
<script type="text/javascript" src="/media/js/tiny_mce/tiny_mce.js"></script>
<script type="text/javascript">
   tinyMCE.init({})</script>

Every text area on the page will be replaced with the WYSIWYG editor. The editor will contain the options (bold, center, hyperlink....) that are specified inside the tinyMCEinit({}) call.

For an example see implementation/templates/pages/lesson/edit_lesson.html

@author Russell Mezzetta
@author Jon Inloes
'''
