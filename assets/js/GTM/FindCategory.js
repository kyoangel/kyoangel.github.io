function() {
  var el = {{FindClosest}}({{Click Element}}, '[data-gtm-category]');
  return typeof el !== 'undefined' ? el.dataset.gtmCategory : undefined;
}