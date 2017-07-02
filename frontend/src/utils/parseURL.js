import 'url-search-params-polyfill';
const XRegExp = require('xregexp');

// get query parameters and URL arguments based on the regex pattern provided
// The pattern needs to be a string
export default function parseURL (href, pattern) {
  const url = new URL(href)
  // Get URL arguments from path
  const path = url.pathname
  const match = XRegExp.exec(path, pattern)
  // Get query parameters from the search part of href
  const search = url.search // could be '?foo=bar'
  const params = new URLSearchParams(search).entries()
  let result = {params: {}, match: {}}
  for (let i in params) {
    let key, value
    [key, value] = params[i]
    result.params[key] = value
  }
  const foo = params.get('foo'); // bar
}
