<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset = UTF-8">
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>

    <link href="https://stackpath.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>

    <link type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.18.1/styles/github.min.css" rel="stylesheet"/>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.9/highlight.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.9/languages/bash.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.9/languages/json.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.9/languages/xml.min.js"></script>
    <script type="text/javascript">hljs.initHighlightingOnLoad();</script>

    <style>
        pre {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
<div>
    <pre><code class="language-http">${method or "GET"} : "${url or "Unknown"}"</code></pre>
</div>

% if body:
<h4>Body</h4>
<div>
    <pre><code>${body}</code></pre>
</div>
% endif

% if headers:
<h4>Headers</h4>
<div>
    % for name, value in headers.items():
    <div>
        <pre><code class="language-http"><b>${name}</b>: ${value}</code></pre>
    </div>
    % endfor
</div>
% endif

</body>
</html>