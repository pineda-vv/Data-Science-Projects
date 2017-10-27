## re.sub('[^A-Za-z0-9]+', ' ', input_string)
#### '[^A-Za-z0-9]+' this little tidbit covers all the letters and numbers
* re.sub(pattern, repl, string, count=0, flags=0)
* Return the string obtained by replacing the leftmost non-overlapping occurrences of the pattern in string by the replacement repl. repl can be either a string or a callable; if a string, backslash escapes in it are processed. If it is a callable, it's passed the match object and must return a replacement string to be used.
* can also use .isalnum()
* ex "".join([char if char.isalnum() else " " for char in a ])
