if !has('python')
  finish
endif

function! CodeDetection(directory)
  pyfile lib/code_detection.py
  echo a:directory
endfunc

command! -nargs=1 CD call CodeDetection(<q-args>)
