import 'url-search-params-polyfill';

// get query parameters and URL arguments based on the regex pattern provided
export default function parseURL (location, pattern) {

  const search = location.search; // could be '?foo=bar'
  const params = new URLSearchParams(search);
  const href = 
  pattern.
  const foo = params.get('foo'); // bar
}
