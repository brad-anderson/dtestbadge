Code for https://dtestbadge.appspot.com

Outputs an image with the current test results for a pull request using HTTP
referrer.  Just paste the Markdown
`\!\[Test Results\]\(https://dtestbadge.appspot.com\)` anywhere on the pull
request's page (in the description or a comment, for instance) and this will
return an image with the pull request's current test results. It uses HTTP
referrer to figure out which pull request's test results to look up.

Ideally this could be moved onto the actual autotester but using App Engine
means we get SSL for free (which is necessary for HTTP referrer based
redirection because GitHub is SSL only and the browser won't set the referrer
when transitioning from SSL to non-SSL).
