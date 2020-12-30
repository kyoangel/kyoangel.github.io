function() {
  var el = {{FindClosest}}({{Click Element}}, '[data-gtm-label]');
  return typeof el !== 'undefined' ? el.dataset.gtmLabel : undefined;
}